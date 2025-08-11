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
        
        # Ensure all necessary directories exist
        self.images_dir = Path("data/users/profile_images")
        try:
            self.images_dir.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Profile images directory ready: {self.images_dir}")
        except Exception as e:
            self.logger.error(f"Error creating profile images directory: {e}")
        
        # Ensure global profiles directory exists
        global_profiles_dir = Path("data/users/global_profiles")
        try:
            global_profiles_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            self.logger.error(f"Error creating global profiles directory: {e}")
    
    def get_text(self, user_id: int, key: str, **kwargs) -> str:
        """Get translated text for a user using the language system."""
        try:
            # Get the language system cog
            language_cog = self.bot.get_cog('LanguageSystem')
            if language_cog:
                return language_cog.get_text(user_id, key, **kwargs)
            else:
                # Fallback to English if language system not available
                return f"[{key}]"
        except Exception as e:
            self.logger.error(f"Error getting translated text for user {user_id}, key {key}: {e}")
            return f"[Translation error: {key}]"
    
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
                self.get_text(interaction.user.id, "invalid_file_type")
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        # Check file size (max 10MB)
        if image.size > 10 * 1024 * 1024:
            embed = EmbedGenerator.create_error_embed(
                self.get_text(interaction.user.id, "file_too_large")
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        try:
            # Ensure directories exist
            self.images_dir.mkdir(parents=True, exist_ok=True)
            
            # Download and save the image
            async with aiohttp.ClientSession() as session:
                async with session.get(image.url) as resp:
                    if resp.status != 200:
                        embed = EmbedGenerator.create_error_embed(
                            self.get_text(interaction.user.id, "download_failed")
                        )
                        await interaction.followup.send(embed=embed, ephemeral=True)
                        return
                    
                    image_data = await resp.read()
            
            # Save image temporarily
            temp_image_path = self.images_dir / f"temp_{interaction.user.id}.png"
            try:
                with open(temp_image_path, 'wb') as f:
                    f.write(image_data)
                self.logger.info(f"Temporary image saved for user {interaction.user.id}: {temp_image_path}")
            except Exception as e:
                self.logger.error(f"Error saving temporary image for user {interaction.user.id}: {e}")
                embed = EmbedGenerator.create_error_embed(
                    self.get_text(interaction.user.id, "save_failed")
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                return
            
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
            try:
                await self._send_approval_request(interaction.user, approval_data)
            except Exception as e:
                self.logger.error(f"Error sending approval request for user {interaction.user.id}: {e}")
                # Still show success to user, but log the error
            
            # Confirm submission to user
            embed = EmbedGenerator.create_embed(
                title=self.get_text(interaction.user.id, "profile_image_submitted"),
                description=self.get_text(interaction.user.id, "profile_image_submitted_desc"),
                color=discord.Color.blue()
            )
            embed.add_field(
                name=self.get_text(interaction.user.id, "what_happens_next"),
                value=self.get_text(interaction.user.id, "what_happens_next_desc"),
                inline=False
            )
            embed.add_field(
                name=self.get_text(interaction.user.id, "note"),
                value=self.get_text(interaction.user.id, "note_desc"),
                inline=False
            )
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            
        except Exception as e:
            self.logger.error(f"Error processing profile image for user {interaction.user.id}: {e}")
            embed = EmbedGenerator.create_error_embed(
                self.get_text(interaction.user.id, "processing_error")
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    async def _send_approval_request(self, user: discord.Member, approval_data: dict):
        """Send approval request to the bot owner."""
        try:
            owner = await self.bot.fetch_user(self.owner_id)
            
            embed = EmbedGenerator.create_embed(
                title=self.get_text(self.owner_id, "approval_request_title"),
                description=self.get_text(self.owner_id, "approval_request_desc",
                    user_mention=user.mention,
                    user_id=user.id,
                    guild_name=approval_data['guild_name'],
                    submitted_time=f"<t:{int(datetime.fromisoformat(approval_data['submitted_at']).timestamp())}:R>"
                ),
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
                # Ensure the target directory exists
                permanent_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Move the file
                temp_path.rename(permanent_path)
                
                # Verify the file was moved successfully
                if not permanent_path.exists():
                    raise Exception("Failed to move file to permanent location")
                
                self.logger.info(f"Profile image moved to permanent location: {permanent_path}")
            else:
                raise Exception("Temporary image file not found")
            
            # Update global profile
            profile = global_profile_manager.load_global_profile(user_id)
            if "preferences" not in profile:
                profile["preferences"] = {}
            
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
            # Try to clean up if something went wrong
            try:
                temp_path = Path(approval_data['image_path'])
                if temp_path.exists():
                    temp_path.unlink()
            except:
                pass
            raise e
    
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
                    title=self.get_text(user_id, "profile_approved_title"),
                    description=self.get_text(user_id, "profile_approved_desc"),
                    color=discord.Color.green()
                )
                embed.add_field(
                    name=self.get_text(user_id, "next_steps"),
                    value=self.get_text(user_id, "next_steps_desc"),
                    inline=False
                )
            else:
                embed = EmbedGenerator.create_embed(
                    title=self.get_text(user_id, "profile_rejected_title"),
                    description=self.get_text(user_id, "profile_rejected_desc", reason=reason),
                    color=discord.Color.red()
                )
                embed.add_field(
                    name=self.get_text(user_id, "what_to_do"),
                    value=self.get_text(user_id, "what_to_do_desc"),
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
        try:
            target_user = user or interaction.user
            user_id = target_user.id
            
            await interaction.response.defer()
            
            if scope == "global":
                await self._show_global_profile_with_image(interaction, target_user)
            else:
                await self._show_server_profile(interaction, target_user)
                
        except Exception as e:
            self.logger.error(f"Error in profile command for user {interaction.user.id}: {e}")
            embed = EmbedGenerator.create_error_embed(
                self.get_text(interaction.user.id, "profile_error")
            )
            try:
                await interaction.followup.send(embed=embed, ephemeral=True)
            except:
                # If followup fails, try to send a new response
                await interaction.response.send_message(embed=embed, ephemeral=True)
    
    async def _show_global_profile_with_image(self, interaction: discord.Interaction, user: discord.Member):
        """Show global profile with custom image if available."""
        try:
            profile = global_profile_manager.load_global_profile(user.id)
            global_stats = profile["global_stats"]
            preferences = profile.get("preferences", {})
            
            # Check privacy settings
            if user.id != interaction.user.id:
                privacy_settings = preferences.get("privacy_settings", {})
                if not privacy_settings.get("show_on_global_leaderboard", True):
                    embed = EmbedGenerator.create_error_embed(
                        self.get_text(interaction.user.id, "profile_private")
                    )
                    await interaction.followup.send(embed=embed, ephemeral=True)
                    return
            
            # Create profile embed
            display_name = preferences.get("display_name") or user.display_name
            custom_title = preferences.get("custom_title")
            
            embed = EmbedGenerator.create_embed(
                title=self.get_text(interaction.user.id, "global_profile_title", display_name=display_name),
                description=f"**{custom_title}**" if custom_title else self.get_text(interaction.user.id, "global_profile_desc"),
                color=discord.Color.gold()
            )
            
            # Set profile image if available
            profile_image_path = preferences.get("profile_image_path")
            file = None
            has_custom_image = False
            
            if profile_image_path:
                image_path = Path(profile_image_path)
                if image_path.exists() and image_path.is_file():
                    try:
                        # Verify file is readable and not corrupted
                        file_size = image_path.stat().st_size
                        if file_size > 0 and file_size < 10 * 1024 * 1024:  # Max 10MB
                            embed.set_image(url=f"attachment://profile_image.png")
                            file = discord.File(str(image_path), filename="profile_image.png")
                            has_custom_image = True
                        else:
                            self.logger.warning(f"Profile image file size issue for user {user.id}: {file_size} bytes")
                    except Exception as e:
                        self.logger.error(f"Error loading profile image for user {user.id}: {e}")
            
            # Fallback to Discord avatar if no custom image
            if not has_custom_image:
                try:
                    avatar_url = user.avatar.url if user.avatar else user.default_avatar.url
                    embed.set_thumbnail(url=avatar_url)
                except Exception as e:
                    self.logger.error(f"Error setting avatar thumbnail for user {user.id}: {e}")
        
        except Exception as e:
            self.logger.error(f"Error in _show_global_profile_with_image for user {user.id}: {e}")
            embed = EmbedGenerator.create_error_embed(
                self.get_text(interaction.user.id, "profile_error")
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        # Basic stats
        total_questions = global_stats.get("total_questions_answered", 0)
        correct_answers = global_stats.get("total_correct_answers", 0)
        accuracy = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        
        embed.add_field(
            name=self.get_text(interaction.user.id, "global_statistics"),
            value=f"**{self.get_text(interaction.user.id, 'level')}:** {global_stats.get('global_level', 1)}\n"
                  f"**{self.get_text(interaction.user.id, 'total_xp')}:** {global_stats.get('total_xp', 0):,}\n"
                  f"**{self.get_text(interaction.user.id, 'games_played')}:** {global_stats.get('total_games_played', 0):,}\n"
                  f"**{self.get_text(interaction.user.id, 'accuracy')}:** {accuracy:.1f}%",
            inline=True
        )
        
        embed.add_field(
            name=self.get_text(interaction.user.id, "performance"),
            value=f"**{self.get_text(interaction.user.id, 'correct_answers')}:** {correct_answers:,}\n"
                  f"**{self.get_text(interaction.user.id, 'best_streak')}:** {global_stats.get('best_streak_ever', 0)}\n"
                  f"**{self.get_text(interaction.user.id, 'perfect_games')}:** {global_stats.get('perfect_games_total', 0)}\n"
                  f"**{self.get_text(interaction.user.id, 'servers_played')}:** {len(global_stats.get('servers_played', []))}",
            inline=True
        )
        
        # Global rank
        global_rank = global_profile_manager.get_user_global_rank(user.id, "total_xp")
        rank_text = f"#{global_rank}" if global_rank else "Unranked"
        
        embed.add_field(
            name=self.get_text(interaction.user.id, "global_ranking"),
            value=f"**{self.get_text(interaction.user.id, 'rank')}:** {rank_text}\n"
                  f"**{self.get_text(interaction.user.id, 'category')}:** {self.get_text(interaction.user.id, 'total_xp')}",
            inline=True
        )
        
        # Achievements
        global_achievements = profile.get("achievements", {}).get("global", [])
        if global_achievements:
            achievement_text = ", ".join([self._format_achievement(ach, interaction.user.id) for ach in global_achievements[:5]])
            if len(global_achievements) > 5:
                achievement_text += f" and {len(global_achievements) - 5} more..."
            embed.add_field(
                name=self.get_text(interaction.user.id, "global_achievements"),
                value=achievement_text,
                inline=False
            )
        
        # Account info
        try:
            created_timestamp = discord.utils.parse_time(profile['created_at'])
            last_active = global_stats.get('last_global_activity', profile['created_at'])
            last_active_timestamp = discord.utils.parse_time(last_active) if last_active else created_timestamp
            
            embed.add_field(
                name=self.get_text(interaction.user.id, "account_info"),
                value=f"**{self.get_text(interaction.user.id, 'created')}:** <t:{int(created_timestamp.timestamp())}:R>\n"
                      f"**{self.get_text(interaction.user.id, 'last_active')}:** <t:{int(last_active_timestamp.timestamp())}:R>",
                inline=False
            )
        except Exception as e:
            self.logger.error(f"Error parsing timestamps for user {user.id}: {e}")
            embed.add_field(
                name=self.get_text(interaction.user.id, "account_info"),
                value=f"**{self.get_text(interaction.user.id, 'created')}:** {self.get_text(interaction.user.id, 'unknown')}\n**{self.get_text(interaction.user.id, 'last_active')}:** {self.get_text(interaction.user.id, 'unknown')}",
                inline=False
            )
        
        embed = EmbedGenerator.finalize_embed(embed)
        
        try:
            if has_custom_image and file:
                await interaction.followup.send(embed=embed, file=file)
            else:
                await interaction.followup.send(embed=embed)
        except Exception as e:
            self.logger.error(f"Error sending profile embed for user {user.id}: {e}")
            # Fallback: try to send without file
            try:
                embed.set_image(url=None)  # Remove image if it was causing issues
                await interaction.followup.send(embed=embed)
            except Exception as e2:
                self.logger.error(f"Fallback profile send also failed for user {user.id}: {e2}")
                error_embed = EmbedGenerator.create_error_embed(
                    self.get_text(interaction.user.id, "profile_display_error")
                )
                await interaction.followup.send(embed=error_embed, ephemeral=True)
    
    async def _show_server_profile(self, interaction: discord.Interaction, user: discord.Member):
        """Show server-specific profile for a user."""
        embed = EmbedGenerator.create_embed(
            title=self.get_text(interaction.user.id, "server_profile_title"),
            description=self.get_text(interaction.user.id, "server_profile_desc"),
            color=discord.Color.blue()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    def _format_achievement(self, achievement_id: str, user_id: int) -> str:
        """Format achievement for display."""
        return self.get_text(user_id, achievement_id)
    
    @app_commands.command(name="pendingapprovals", description="[Owner] View pending profile image approvals")
    async def pending_approvals(self, interaction: discord.Interaction):
        """View pending profile image approvals (owner only)."""
        if interaction.user.id != self.owner_id:
            embed = EmbedGenerator.create_error_embed(
                self.get_text(interaction.user.id, "no_permission")
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        if not self.pending_approvals:
            embed = EmbedGenerator.create_embed(
                title=self.get_text(interaction.user.id, "pending_approvals_title"),
                description=self.get_text(interaction.user.id, "no_pending_approvals"),
                color=discord.Color.green()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        embed = EmbedGenerator.create_embed(
            title=self.get_text(interaction.user.id, "pending_approvals_title"),
            description=self.get_text(interaction.user.id, "pending_approvals_desc", count=len(self.pending_approvals)),
            color=discord.Color.orange()
        )
        
        for user_id, approval_data in self.pending_approvals.items():
            # Check if temp file still exists
            temp_path = Path(approval_data['image_path'])
            file_status = self.get_text(interaction.user.id, "file_exists") if temp_path.exists() else self.get_text(interaction.user.id, "file_missing_status")
            file_size = self.get_text(interaction.user.id, "file_size_mb", size=temp_path.stat().st_size / (1024*1024)) if temp_path.exists() else "N/A"
            
            embed.add_field(
                name=f"User: {approval_data['user_name']}",
                value=f"**ID:** {user_id}\n"
                      f"**Server:** {approval_data['guild_name']}\n"
                      f"**File:** {file_status} ({file_size})\n"
                      f"**Submitted:** <t:{int(datetime.fromisoformat(approval_data['submitted_at']).timestamp())}:R>",
                inline=True
            )
        
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="profileimageinfo", description="[Owner] Get information about a user's profile image")
    @app_commands.describe(user="User to check profile image for")
    async def profile_image_info(self, interaction: discord.Interaction, user: discord.Member):
        """Get detailed information about a user's profile image (owner only)."""
        if interaction.user.id != self.owner_id:
            embed = EmbedGenerator.create_error_embed(
                self.get_text(interaction.user.id, "no_permission")
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            # Load user profile
            profile = global_profile_manager.load_global_profile(user.id)
            preferences = profile.get("preferences", {})
            profile_image_path = preferences.get("profile_image_path")
            
            embed = EmbedGenerator.create_embed(
                title=self.get_text(interaction.user.id, "profile_image_info_title", display_name=user.display_name),
                description=f"User ID: {user.id}",
                color=discord.Color.blue()
            )
            
            if profile_image_path:
                image_path = Path(profile_image_path)
                if image_path.exists():
                    file_size = image_path.stat().st_size
                    file_size_mb = file_size / (1024 * 1024)
                    approved_at = preferences.get("profile_image_approved_at", "Unknown")
                    
                    embed.add_field(
                        name=self.get_text(interaction.user.id, "profile_image_found"),
                        value=f"**Path:** `{image_path}`\n"
                              f"**Size:** {self.get_text(interaction.user.id, 'file_size_mb', size=file_size_mb)} ({self.get_text(interaction.user.id, 'file_size_bytes', size=file_size)})\n"
                              f"**Approved:** {approved_at}\n"
                              f"**Status:** {self.get_text(interaction.user.id, 'status_active')}",
                        inline=False
                    )
                else:
                    embed.add_field(
                        name=self.get_text(interaction.user.id, "file_missing"),
                        value=f"**Path:** `{image_path}`\n"
                              f"**Status:** {self.get_text(interaction.user.id, 'status_file_not_found')}",
                        inline=False
                    )
            else:
                embed.add_field(
                    name=self.get_text(interaction.user.id, "no_profile_image"),
                    value=self.get_text(interaction.user.id, "status_no_image"),
                    inline=False
                )
            
            # Check if user has pending approval
            if user.id in self.pending_approvals:
                approval_data = self.pending_approvals[user.id]
                temp_path = Path(approval_data['image_path'])
                temp_status = self.get_text(interaction.user.id, "file_exists") if temp_path.exists() else self.get_text(interaction.user.id, "file_missing_status")
                
                embed.add_field(
                    name=self.get_text(interaction.user.id, "pending_approval_status"),
                    value=f"**Temp File:** {temp_status}\n"
                          f"**Submitted:** <t:{int(datetime.fromisoformat(approval_data['submitted_at']).timestamp())}:R>",
                    inline=False
                )
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            
        except Exception as e:
            self.logger.error(f"Error getting profile image info for user {user.id}: {e}")
            embed = EmbedGenerator.create_error_embed(
                self.get_text(interaction.user.id, "error_getting_info", error=str(e))
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="fixprofileimage", description="[Owner] Fix a user's profile image if it's broken")
    @app_commands.describe(user="User to fix profile image for")
    async def fix_profile_image(self, interaction: discord.Interaction, user: discord.Member):
        """Fix a user's profile image if it's broken (owner only)."""
        if interaction.user.id != self.owner_id:
            embed = EmbedGenerator.create_error_embed(
                self.get_text(interaction.user.id, "no_permission")
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            # Load user profile
            profile = global_profile_manager.load_global_profile(user.id)
            preferences = profile.get("preferences", {})
            profile_image_path = preferences.get("profile_image_path")
            
            if not profile_image_path:
                embed = EmbedGenerator.create_error_embed(
                    self.get_text(interaction.user.id, "status_no_image")
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                return
            
            image_path = Path(profile_image_path)
            
            if image_path.exists():
                embed = EmbedGenerator.create_embed(
                    title=self.get_text(interaction.user.id, "profile_image_ok"),
                    description=self.get_text(interaction.user.id, "status_working", user=user.display_name),
                    color=discord.Color.green()
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                return
            
            # Image file is missing, remove the reference
            if "profile_image_path" in preferences:
                del preferences["profile_image_path"]
            if "profile_image_approved_at" in preferences:
                del preferences["profile_image_approved_at"]
            
            profile["preferences"] = preferences
            global_profile_manager.save_global_profile(user.id, profile)
            
            embed = EmbedGenerator.create_embed(
                title=self.get_text(interaction.user.id, "profile_image_fixed"),
                description=self.get_text(interaction.user.id, "status_broken", user=user.display_name),
                color=discord.Color.orange()
            )
            embed.add_field(
                name=self.get_text(interaction.user.id, "what_was_fixed"),
                value=self.get_text(interaction.user.id, "status_fixed_desc"),
                inline=False
            )
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            
        except Exception as e:
            self.logger.error(f"Error fixing profile image for user {user.id}: {e}")
            embed = EmbedGenerator.create_error_embed(
                self.get_text(interaction.user.id, "error_fixing", error=str(e))
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="clearpendingapprovals", description="[Owner] Clear all pending profile image approvals")
    async def clear_pending_approvals(self, interaction: discord.Interaction):
        """Clear all pending profile image approvals (owner only)."""
        if interaction.user.id != self.owner_id:
            embed = EmbedGenerator.create_error_embed(
                self.get_text(interaction.user.id, "no_permission")
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            if not self.pending_approvals:
                embed = EmbedGenerator.create_embed(
                    title=self.get_text(interaction.user.id, "no_pending_to_clear"),
                    description=self.get_text(interaction.user.id, "no_pending_desc"),
                    color=discord.Color.green()
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                return
            
            # Count how many files we'll clean up
            files_cleaned = 0
            for approval_data in self.pending_approvals.values():
                temp_path = Path(approval_data['image_path'])
                if temp_path.exists():
                    try:
                        temp_path.unlink()
                        files_cleaned += 1
                    except Exception as e:
                        self.logger.error(f"Error deleting temp file {temp_path}: {e}")
            
            # Clear the pending approvals
            total_pending = len(self.pending_approvals)
            self.pending_approvals.clear()
            
            embed = EmbedGenerator.create_embed(
                title=self.get_text(interaction.user.id, "pending_cleared"),
                description=self.get_text(interaction.user.id, "pending_cleared_desc", total=total_pending, files=files_cleaned),
                color=discord.Color.orange()
            )
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            
        except Exception as e:
            self.logger.error(f"Error clearing pending approvals: {e}")
            embed = EmbedGenerator.create_error_embed(
                self.get_text(interaction.user.id, "error_clearing", error=str(e))
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

class ProfileApprovalView(discord.ui.View):
    """View for profile image approval buttons."""
    
    def __init__(self, cog: ProfileImages, approval_data: dict):
        super().__init__(timeout=86400)  # 24 hour timeout
        self.cog = cog
        self.approval_data = approval_data
    
    async def on_timeout(self):
        """Handle timeout by cleaning up the approval request."""
        try:
            # Remove from pending approvals
            self.cog.pending_approvals.pop(self.approval_data["user_id"], None)
            
            # Clean up temp file
            temp_path = Path(self.approval_data['image_path'])
            if temp_path.exists():
                temp_path.unlink()
            
            # Notify user that their approval request timed out
            try:
                user = await self.cog.bot.fetch_user(self.approval_data["user_id"])
                embed = EmbedGenerator.create_embed(
                    title=self.cog.get_text(self.approval_data["user_id"], "approval_expired_title"),
                    description=self.cog.get_text(self.approval_data["user_id"], "approval_expired_desc"),
                    color=discord.Color.orange()
                )
                embed.add_field(
                    name=self.cog.get_text(self.approval_data["user_id"], "what_happened"),
                    value=self.cog.get_text(self.approval_data["user_id"], "what_happened_desc"),
                    inline=False
                )
                await user.send(embed=embed)
            except Exception as e:
                self.cog.logger.error(f"Error notifying user of approval timeout: {e}")
            
            self.cog.logger.info(f"Profile approval request timed out for user {self.approval_data['user_id']}")
        except Exception as e:
            self.cog.logger.error(f"Error handling approval timeout: {e}")
    
    @discord.ui.button(label="✅ Approve", style=discord.ButtonStyle.green, custom_id="approve_profile")
    async def approve_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Approve the profile image."""
        if interaction.user.id != self.cog.owner_id:
            embed = EmbedGenerator.create_error_embed(
                self.cog.get_text(interaction.user.id, "no_permission")
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Check if this approval has already been processed
        if self.approval_data["user_id"] not in self.cog.pending_approvals:
            embed = EmbedGenerator.create_error_embed(
                self.cog.get_text(interaction.user.id, "already_processed")
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        await interaction.response.defer()
        
        try:
            # Get file information before approval
            temp_path = Path(self.approval_data['image_path'])
            file_size = temp_path.stat().st_size if temp_path.exists() else 0
            file_size_mb = file_size / (1024 * 1024)
            
            await self.cog.approve_profile_image(self.approval_data["user_id"], self.approval_data)
            
            # Get permanent file path after approval
            permanent_path = self.cog.images_dir / f"{self.approval_data['user_id']}.png"
            
            embed = EmbedGenerator.create_embed(
                title="✅ Profile Image Approved",
                description=f"Profile image for **{self.approval_data['user_name']}** has been approved and is now active!",
                color=discord.Color.green()
            )
            
            embed.add_field(
                name="📁 File Information",
                value=f"**Location:** `{permanent_path}`\n"
                      f"**Size:** {file_size_mb:.2f} MB\n"
                      f"**User ID:** {self.approval_data['user_id']}\n"
                      f"**Server:** {self.approval_data['guild_name']}",
                inline=False
            )
            
            embed.add_field(
                name="✅ Status",
                value="• Image moved to permanent storage\n"
                      "• User profile updated\n"
                      "• User notified via DM\n"
                      "• Image will now appear on their profile",
                inline=False
            )
            
            # Disable buttons
            for child in self.children:
                child.disabled = True
            
            # Send a new message instead of trying to edit the original
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            self.cog.logger.error(f"Error in approve button: {e}")
            error_embed = EmbedGenerator.create_error_embed(
                self.cog.get_text(interaction.user.id, "error_approving", error=str(e))
            )
            await interaction.followup.send(embed=error_embed, ephemeral=True)
    
    @discord.ui.button(label="❌ Reject", style=discord.ButtonStyle.red, custom_id="reject_profile")
    async def reject_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Reject the profile image."""
        if interaction.user.id != self.cog.owner_id:
            embed = EmbedGenerator.create_error_embed(
                self.cog.get_text(interaction.user.id, "no_permission")
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Check if this approval has already been processed
        if self.approval_data["user_id"] not in self.cog.pending_approvals:
            embed = EmbedGenerator.create_error_embed(
                self.cog.get_text(interaction.user.id, "already_processed")
            )
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
        
        # Check if this approval is still pending
        if self.approval_data["user_id"] not in self.cog.pending_approvals:
            embed = EmbedGenerator.create_error_embed(
                self.cog.get_text(interaction.user.id, "already_processed")
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        await self.cog.reject_profile_image(
            self.approval_data["user_id"], 
            self.approval_data, 
            self.reason.value
        )
        
        embed = EmbedGenerator.create_embed(
            title=self.cog.get_text(interaction.user.id, "profile_rejected_title"),
            description=self.cog.get_text(interaction.user.id, "profile_rejected_desc", reason=self.reason.value),
            color=discord.Color.red()
        )
        
        await interaction.followup.send(embed=embed)

async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(ProfileImages(bot))
