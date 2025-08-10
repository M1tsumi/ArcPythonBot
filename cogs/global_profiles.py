"""
Global Profiles command module for Avatar Realms Collide Discord Bot.
Provides global profile management and cross-server leaderboards.
"""

import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional, Literal
import asyncio

from utils.global_profile_manager import global_profile_manager
from utils.data_migration import data_migration_manager
from utils.embed_generator import EmbedGenerator

class GlobalProfiles(commands.Cog):
    """Global Profiles and cross-server leaderboard system."""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
    
    # Profile command moved to profile_images.py to include custom profile images
    
    async def _show_global_profile(self, interaction: discord.Interaction, user: discord.Member):
        """Show global profile for a user."""
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
        
        # Add user avatar
        embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
        
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
        await interaction.followup.send(embed=embed)
    
    async def _show_server_profile(self, interaction: discord.Interaction, user: discord.Member):
        """Show server-specific profile for a user."""
        # This would integrate with the existing avatar play system
        # For now, redirect to global profile
        embed = EmbedGenerator.create_embed(
            title="🏠 Server Profile",
            description="Server-specific profiles are coming soon! Use `/profile global` to see cross-server stats.",
            color=discord.Color.blue()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="leaderboard", description="View global or server leaderboards")
    @app_commands.describe(
        scope="Leaderboard scope",
        category="Statistic to rank by",
        page="Page number (10 entries per page)"
    )
    async def leaderboard(
        self,
        interaction: discord.Interaction,
        scope: Literal["global", "server"] = "global",
        category: Literal["total_xp", "accuracy", "best_streak", "total_games", "perfect_games"] = "total_xp",
        page: int = 1
    ):
        """View global or server-specific leaderboards."""
        await interaction.response.defer()
        
        if scope == "global":
            await self._show_global_leaderboard(interaction, category, page)
        else:
            await self._show_server_leaderboard(interaction, category, page)
    
    async def _show_global_leaderboard(self, interaction: discord.Interaction, category: str, page: int):
        """Show global leaderboard."""
        entries_per_page = 10
        start_index = (page - 1) * entries_per_page
        
        # Get leaderboard data
        all_entries = global_profile_manager.get_global_leaderboard(limit=1000, category=category)
        
        if not all_entries:
            embed = EmbedGenerator.create_embed(
                title="🏆 Global Leaderboard",
                description="No global leaderboard data available yet!",
                color=discord.Color.gold()
            )
            await interaction.followup.send(embed=embed)
            return
        
        # Calculate pagination
        total_pages = (len(all_entries) + entries_per_page - 1) // entries_per_page
        page = max(1, min(page, total_pages))
        start_index = (page - 1) * entries_per_page
        end_index = start_index + entries_per_page
        
        page_entries = all_entries[start_index:end_index]
        
        # Create embed
        category_names = {
            "total_xp": "Total XP",
            "accuracy": "Accuracy",
            "best_streak": "Best Streak",
            "total_games": "Games Played",
            "perfect_games": "Perfect Games"
        }
        
        embed = EmbedGenerator.create_embed(
            title=f"🏆 Global Leaderboard - {category_names.get(category, category)}",
            description=f"Cross-server rankings • Page {page}/{total_pages}",
            color=discord.Color.gold()
        )
        
        # Add leaderboard entries
        leaderboard_text = ""
        for i, entry in enumerate(page_entries):
            rank = start_index + i + 1
            user_id = entry["user_id"]
            
            # Get rank emoji
            if rank == 1:
                rank_emoji = "🥇"
            elif rank == 2:
                rank_emoji = "🥈"
            elif rank == 3:
                rank_emoji = "🥉"
            else:
                rank_emoji = f"{rank}."
            
            # Get display name
            display_name = entry.get("display_name")
            if not display_name:
                try:
                    user = await self.bot.fetch_user(user_id)
                    display_name = user.display_name
                except:
                    display_name = f"User#{user_id}"
            
            # Format value based on category
            if category == "total_xp":
                value = f"{entry['total_xp']:,} XP (Lv.{entry['global_level']})"
            elif category == "accuracy":
                value = f"{entry['accuracy']:.1f}%"
            elif category == "best_streak":
                value = f"{entry['best_streak']} correct"
            elif category == "total_games":
                value = f"{entry['total_games']:,} games"
            elif category == "perfect_games":
                value = f"{entry['perfect_games']} perfect"
            else:
                value = f"{entry.get(category, 0)}"
            
            leaderboard_text += f"{rank_emoji} **{display_name}** - {value}\n"
        
        embed.add_field(
            name="Rankings",
            value=leaderboard_text or "No entries found",
            inline=False
        )
        
        # Find user's rank if they're in the leaderboard
        user_rank = None
        for i, entry in enumerate(all_entries):
            if entry["user_id"] == interaction.user.id:
                user_rank = i + 1
                break
        
        if user_rank:
            embed.add_field(
                name="Your Rank",
                value=f"You are ranked **#{user_rank}** globally in {category_names.get(category, category)}",
                inline=False
            )
        
        embed = EmbedGenerator.finalize_embed(embed)
        await interaction.followup.send(embed=embed)
    
    async def _show_server_leaderboard(self, interaction: discord.Interaction, category: str, page: int):
        """Show server-specific leaderboard."""
        embed = EmbedGenerator.create_embed(
            title="🏠 Server Leaderboard",
            description="Server-specific leaderboards are coming soon! Use `/leaderboard global` for cross-server rankings.",
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
    
    @app_commands.command(name="migrate_data", description="[Admin] Migrate existing data to global profiles")
    async def migrate_data(self, interaction: discord.Interaction, dry_run: bool = True):
        """Admin command to migrate existing data to global profiles."""
        # Check if user is authorized (you may want to add proper permission checks)
        if interaction.user.id != 1051142172130422884:  # Replace with your user ID
            embed = EmbedGenerator.create_error_embed("You don't have permission to use this command.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            # Run migration
            report = data_migration_manager.migrate_all_data(dry_run=dry_run)
            
            # Create report embed
            embed = EmbedGenerator.create_embed(
                title="📊 Data Migration Report",
                description="Migration completed!" if not dry_run else "Dry run completed - no data was changed",
                color=discord.Color.green() if not report["avatar_play"]["errors"] and not report["minigame"]["errors"] else discord.Color.orange()
            )
            
            embed.add_field(
                name="Avatar Play Migration",
                value=f"**Servers:** {report['avatar_play']['servers_processed']}\n"
                      f"**Users:** {report['avatar_play']['users_migrated']}\n"
                      f"**Errors:** {len(report['avatar_play']['errors'])}",
                inline=True
            )
            
            embed.add_field(
                name="Minigame Migration",
                value=f"**Servers:** {report['minigame']['servers_processed']}\n"
                      f"**Users:** {report['minigame']['users_migrated']}\n"
                      f"**Errors:** {len(report['minigame']['errors'])}",
                inline=True
            )
            
            embed.add_field(
                name="Summary",
                value=f"**Total Unique Users:** {report['total_unique_users']}\n"
                      f"**Mode:** {'Dry Run' if dry_run else 'Live Migration'}",
                inline=True
            )
            
            if report["avatar_play"]["errors"] or report["minigame"]["errors"]:
                all_errors = report["avatar_play"]["errors"] + report["minigame"]["errors"]
                error_text = "\n".join(all_errors[:5])
                if len(all_errors) > 5:
                    error_text += f"\n... and {len(all_errors) - 5} more errors"
                
                embed.add_field(
                    name="⚠️ Errors",
                    value=f"```{error_text}```",
                    inline=False
                )
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            
        except Exception as e:
            self.logger.error(f"Error during data migration: {e}")
            embed = EmbedGenerator.create_error_embed(f"Migration failed: {str(e)}")
            await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(GlobalProfiles(bot))
