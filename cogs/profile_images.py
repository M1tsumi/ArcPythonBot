"""
Profile Images command module for Avatar Realms Collide Discord Bot.
Handles profile image submission, approval, and display.
"""

import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
import asyncio
import aiohttp
import io
from pathlib import Path
import json
from datetime import datetime, timezone

from utils.global_profile_manager import global_profile_manager
from utils.embed_generator import EmbedGenerator

class ProfileImages(commands.Cog):
    """Profile image management system with approval workflow."""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        self.owner_id = 1051142172130422884  # Bot owner ID for approvals
        self.pending_approvals = {}  # Store pending approvals: {user_id: approval_data}
        self.images_dir = Path("data/users/profile_images")
        self.images_dir.mkdir(parents=True, exist_ok=True)
    
    @app_commands.command(name="setprofile", description="Submit your Avatar Realms profile image for approval")
    @app_commands.describe(
        image="Screenshot of your Avatar Realms account (must be a valid image)"
    )
    async def set_profile(
        self, 
        interaction: discord.Interaction, 
        image: discord.Attachment
    ):
        """Submit profile image for approval."""
        await interaction.response.defer(ephemeral=True)
        
        # Validate image
        if not image.content_type or not image.content_type.startswith('image/'):
            embed = EmbedGenerator.create_error_embed(
                "❌ Invalid file type! Please upload an image file (PNG, JPG, etc.)."
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        # Check file size (max 10MB)
        if image.size > 10 * 1024 * 1024:
            embed = EmbedGenerator.create_error_embed(
                "❌ Image file too large! Please upload an image smaller than 10MB."
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        try:
            # Download and save the image
            async with aiohttp.ClientSession() as session:
                async with session.get(image.url) as resp:
                    if resp.status != 200:
                        embed = EmbedGenerator.create_error_embed(
                            "❌ Failed to download image. Please try again."
                        )
                        await interaction.followup.send(embed=embed, ephemeral=True)
                        return
                    
                    image_data = await resp.read()
            
            # Save image temporarily
            temp_image_path = self.images_dir / f"temp_{interaction.user.id}.png"
            with open(temp_image_path, 'wb') as f:
                f.write(image_data)
            
            # Store approval request
            approval_data = {
                "user_id": interaction.user.id,
                "user_name": interaction.user.display_name,
                "guild_id": interaction.guild_id,
                "guild_name": interaction.guild.name,
                "image_path": str(temp_image_path),
                "submitted_at": datetime.now(timezone.utc).isoformat(),
                "image_url": image.url
            }
            
            self.pending_approvals[interaction.user.id] = approval_data
            
            # Send approval request to owner
            await self._send_approval_request(interaction.user, approval_data)
            
            # Confirm submission to user
            embed = EmbedGenerator.create_embed(
                title="📸 Profile Image Submitted",
                description="Your profile image has been submitted for approval!",
                color=discord.Color.blue()
            )
            embed.add_field(
                name="What happens next?",
                value="• The bot owner will review your image\n"
                      "• You'll receive a DM when it's approved or rejected\n"
                      "• Once approved, your image will appear on your profile",
                inline=False
            )
            embed.add_field(
                name="Note",
                value="Please ensure your image shows a valid Avatar Realms account screenshot.",
                inline=False
            )
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            
        except Exception as e:
            self.logger.error(f"Error processing profile image for user {interaction.user.id}: {e}")
            embed = EmbedGenerator.create_error_embed(
                "❌ An error occurred while processing your image. Please try again."
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    async def _send_approval_request(self, user: discord.Member, approval_data: dict):
        """Send approval request to the bot owner."""
        try:
            owner = await self.bot.fetch_user(self.owner_id)
            
            embed = EmbedGenerator.create_embed(
                title="🔍 Profile Image Approval Request",
                description=f"**User:** {user.mention} (`{user.id}`)\n"
                           f"**Server:** {approval_data['guild_name']}\n"
                           f"**Submitted:** <t:{int(datetime.fromisoformat(approval_data['submitted_at']).timestamp())}:R>",
                color=discord.Color.orange()
            )
            
            # Add the image
            embed.set_image(url=approval_data['image_url'])
            
            # Create approval buttons
            view = ProfileApprovalView(self, approval_data)
            
            await owner.send(embed=embed, view=view)
            
        except Exception as e:
            self.logger.error(f"Error sending approval request to owner: {e}")
    
    async def approve_profile_image(self, user_id: int, approval_data: dict):
        """Approve a profile image."""
        try:
            # Move image to permanent location
            permanent_path = self.images_dir / f"{user_id}.png"
            temp_path = Path(approval_data['image_path'])
            
            if temp_path.exists():
                temp_path.rename(permanent_path)
            
            # Update global profile
            profile = global_profile_manager.load_global_profile(user_id)
            profile["preferences"]["profile_image_path"] = str(permanent_path)
            profile["preferences"]["profile_image_approved_at"] = datetime.now(timezone.utc).isoformat()
            global_profile_manager.save_global_profile(user_id, profile)
            
            # Remove from pending approvals
            self.pending_approvals.pop(user_id, None)
            
            # Notify user
            await self._notify_user_approval(user_id, True, approval_data)
            
            self.logger.info(f"Profile image approved for user {user_id}")
            
        except Exception as e:
            self.logger.error(f"Error approving profile image for user {user_id}: {e}")
    
    async def reject_profile_image(self, user_id: int, approval_data: dict, reason: str = "Image rejected"):
        """Reject a profile image."""
        try:
            # Delete temporary image
            temp_path = Path(approval_data['image_path'])
            if temp_path.exists():
                temp_path.unlink()
            
            # Remove from pending approvals
            self.pending_approvals.pop(user_id, None)
            
            # Notify user
            await self._notify_user_approval(user_id, False, approval_data, reason)
            
            self.logger.info(f"Profile image rejected for user {user_id}: {reason}")
            
        except Exception as e:
            self.logger.error(f"Error rejecting profile image for user {user_id}: {e}")
    
    async def _notify_user_approval(self, user_id: int, approved: bool, approval_data: dict, reason: str = ""):
        """Notify user of approval/rejection."""
        try:
            user = await self.bot.fetch_user(user_id)
            
            if approved:
                embed = EmbedGenerator.create_embed(
                    title="✅ Profile Image Approved!",
                    description="Your profile image has been approved and is now active!",
                    color=discord.Color.green()
                )
                embed.add_field(
                    name="Next Steps",
                    value="Use `/profile` to view your profile with the new image.",
                    inline=False
                )
            else:
                embed = EmbedGenerator.create_embed(
                    title="❌ Profile Image Rejected",
                    description=f"Your profile image was not approved.\n\n**Reason:** {reason}",
                    color=discord.Color.red()
                )
                embed.add_field(
                    name="What to do",
                    value="Please submit a new image using `/setprofile` with a valid Avatar Realms account screenshot.",
                    inline=False
                )
            
            await user.send(embed=embed)
            
        except Exception as e:
            self.logger.error(f"Error notifying user {user_id} of approval result: {e}")
    
    def get_profile_image_path(self, user_id: int) -> Optional[str]:
        """Get the approved profile image path for a user."""
        profile = global_profile_manager.load_global_profile(user_id)
        return profile.get("preferences", {}).get("profile_image_path")
    
    @app_commands.command(name="profile", description="View your or another user's profile")
    @app_commands.describe(
        user="User to view profile for (default: yourself)",
        scope="Profile scope to display"
    )
    async def profile(
        self, 
        interaction: discord.Interaction, 
        user: Optional[discord.Member] = None,
        scope: str = "global"
    ):
        """View user profile with image."""
        target_user = user or interaction.user
        user_id = target_user.id
        
        await interaction.response.defer()
        
        if scope == "global":
            await self._show_global_profile_with_image(interaction, target_user)
        else:
            await self._show_server_profile(interaction, target_user)
    
    async def _show_global_profile_with_image(self, interaction: discord.Interaction, user: discord.Member):
        """Show global profile with custom image if available."""
        profile = global_profile_manager.load_global_profile(user.id)
        global_stats = profile["global_stats"]
        preferences = profile.get("preferences", {})
        
        # Check privacy settings
        if user.id != interaction.user.id:
            privacy_settings = preferences.get("privacy_settings", {})
            if not privacy_settings.get("show_on_global_leaderboard", True):
                embed = EmbedGenerator.create_error_embed(
                    "This user has chosen to keep their global profile private."
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                return
        
        # Create profile embed
        display_name = preferences.get("display_name") or user.display_name
        custom_title = preferences.get("custom_title")
        
        embed = EmbedGenerator.create_embed(
            title=f"🌟 Global Profile - {display_name}",
            description=f"**{custom_title}**" if custom_title else "Cross-server Avatar Trivia statistics",
            color=discord.Color.gold()
        )
        
        # Set profile image if available
        profile_image_path = preferences.get("profile_image_path")
        if profile_image_path and Path(profile_image_path).exists():
            # Use the custom profile image
            embed.set_image(url=f"attachment://profile_image.png")
            file = discord.File(profile_image_path, filename="profile_image.png")
            has_custom_image = True
        else:
            # Use Discord avatar as fallback
            embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
            file = None
            has_custom_image = False
        
        # Basic stats
        total_questions = global_stats.get("total_questions_answered", 0)
        correct_answers = global_stats.get("total_correct_answers", 0)
        accuracy = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        
        embed.add_field(
            name="📊 Global Statistics",
            value=f"**Level:** {global_stats.get('global_level', 1)}\n"
                  f"**Total XP:** {global_stats.get('total_xp', 0):,}\n"
                  f"**Games Played:** {global_stats.get('total_games_played', 0):,}\n"
                  f"**Accuracy:** {accuracy:.1f}%",
            inline=True
        )
        
        embed.add_field(
            name="🎯 Performance",
            value=f"**Correct Answers:** {correct_answers:,}\n"
                  f"**Best Streak:** {global_stats.get('best_streak_ever', 0)}\n"
                  f"**Perfect Games:** {global_stats.get('perfect_games_total', 0)}\n"
                  f"**Servers Played:** {len(global_stats.get('servers_played', []))}",
            inline=True
        )
        
        # Global rank
        global_rank = global_profile_manager.get_user_global_rank(user.id, "total_xp")
        rank_text = f"#{global_rank}" if global_rank else "Unranked"
        
        embed.add_field(
            name="🏆 Global Ranking",
            value=f"**Rank:** {rank_text}\n"
                  f"**Category:** Total XP",
            inline=True
        )
        
        # Achievements
        global_achievements = profile.get("achievements", {}).get("global", [])
        if global_achievements:
            achievement_text = ", ".join([self._format_achievement(ach) for ach in global_achievements[:5]])
            if len(global_achievements) > 5:
                achievement_text += f" and {len(global_achievements) - 5} more..."
            embed.add_field(
                name="🏅 Global Achievements",
                value=achievement_text,
                inline=False
            )
        
        # Account info
        embed.add_field(
            name="📅 Account Info",
            value=f"**Created:** <t:{int(discord.utils.parse_time(profile['created_at']).timestamp())}:R>\n"
                  f"**Last Active:** <t:{int(discord.utils.parse_time(global_stats.get('last_global_activity', profile['created_at'])).timestamp())}:R>",
            inline=False
        )
        
        embed = EmbedGenerator.finalize_embed(embed)
        
        if has_custom_image and file:
            await interaction.followup.send(embed=embed, file=file)
        else:
            await interaction.followup.send(embed=embed)
    
    async def _show_server_profile(self, interaction: discord.Interaction, user: discord.Member):
        """Show server-specific profile for a user."""
        embed = EmbedGenerator.create_embed(
            title="🏠 Server Profile",
            description="Server-specific profiles are coming soon! Use `/profile global` to see cross-server stats.",
            color=discord.Color.blue()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    def _format_achievement(self, achievement_id: str) -> str:
        """Format achievement for display."""
        achievement_names = {
            "global_novice": "🎓 Global Novice",
            "global_apprentice": "📚 Global Apprentice", 
            "global_expert": "🔥 Global Expert",
            "global_master": "⭐ Global Master",
            "global_grandmaster": "👑 Global Grandmaster",
            "streak_champion": "🏆 Streak Champion",
            "streak_legend": "🌟 Streak Legend",
            "perfect_master": "💎 Perfect Master",
            "perfect_legend": "✨ Perfect Legend",
            "server_explorer": "🗺️ Server Explorer",
            "server_nomad": "🚀 Server Nomad",
            "dedicated_player": "❤️ Dedicated Player",
            "addicted_player": "🎮 Addicted Player",
            "trivia_god": "🔱 Trivia God"
        }
        return achievement_names.get(achievement_id, achievement_id.replace("_", " ").title())
    
    @app_commands.command(name="pendingapprovals", description="[Owner] View pending profile image approvals")
    async def pending_approvals(self, interaction: discord.Interaction):
        """View pending profile image approvals (owner only)."""
        if interaction.user.id != self.owner_id:
            embed = EmbedGenerator.create_error_embed("You don't have permission to use this command.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        if not self.pending_approvals:
            embed = EmbedGenerator.create_embed(
                title="📋 Pending Approvals",
                description="No pending profile image approvals.",
                color=discord.Color.green()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        embed = EmbedGenerator.create_embed(
            title="📋 Pending Profile Image Approvals",
            description=f"**Total Pending:** {len(self.pending_approvals)}",
            color=discord.Color.orange()
        )
        
        for user_id, approval_data in self.pending_approvals.items():
            embed.add_field(
                name=f"User: {approval_data['user_name']}",
                value=f"**ID:** {user_id}\n"
                      f"**Server:** {approval_data['guild_name']}\n"
                      f"**Submitted:** <t:{int(datetime.fromisoformat(approval_data['submitted_at']).timestamp())}:R>",
                inline=True
            )
        
        await interaction.followup.send(embed=embed, ephemeral=True)

class ProfileApprovalView(discord.ui.View):
    """View for profile image approval buttons."""
    
    def __init__(self, cog: ProfileImages, approval_data: dict):
        super().__init__(timeout=None)
        self.cog = cog
        self.approval_data = approval_data
    
    @discord.ui.button(label="✅ Approve", style=discord.ButtonStyle.green, custom_id="approve_profile")
    async def approve_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Approve the profile image."""
        if interaction.user.id != self.cog.owner_id:
            embed = EmbedGenerator.create_error_embed("You don't have permission to approve profile images.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        await interaction.response.defer()
        
        await self.cog.approve_profile_image(self.approval_data["user_id"], self.approval_data)
        
        embed = EmbedGenerator.create_embed(
            title="✅ Profile Image Approved",
            description=f"Profile image for {self.approval_data['user_name']} has been approved.",
            color=discord.Color.green()
        )
        
        # Disable buttons
        for child in self.children:
            child.disabled = True
        
        await interaction.followup.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="❌ Reject", style=discord.ButtonStyle.red, custom_id="reject_profile")
    async def reject_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Reject the profile image."""
        if interaction.user.id != self.cog.owner_id:
            embed = EmbedGenerator.create_error_embed("You don't have permission to reject profile images.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Create modal for rejection reason
        modal = RejectionReasonModal(self.cog, self.approval_data)
        await interaction.response.send_modal(modal)

class RejectionReasonModal(discord.ui.Modal, title="Profile Image Rejection"):
    """Modal for entering rejection reason."""
    
    def __init__(self, cog: ProfileImages, approval_data: dict):
        super().__init__()
        self.cog = cog
        self.approval_data = approval_data
    
    reason = discord.ui.TextInput(
        label="Rejection Reason",
        placeholder="Enter the reason for rejecting this profile image...",
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=500
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        await interaction.response.defer()
        
        await self.cog.reject_profile_image(
            self.approval_data["user_id"], 
            self.approval_data, 
            self.reason.value
        )
        
        embed = EmbedGenerator.create_embed(
            title="❌ Profile Image Rejected",
            description=f"Profile image for {self.approval_data['user_name']} has been rejected.\n\n**Reason:** {self.reason.value}",
            color=discord.Color.red()
        )
        
        await interaction.followup.send(embed=embed)

async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(ProfileImages(bot))
