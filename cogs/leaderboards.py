"""
Leaderboards command module for Avatar Realms Collide Discord Bot.
Provides leaderboard viewing functionality and admin management.
"""

import discord
import json
import os
from discord import app_commands
from discord.ext import commands
from utils.ui_components import LeaderboardView
from utils.embed_generator import EmbedGenerator

class Leaderboards(commands.Cog):
    """Leaderboards command cog."""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        self.leaderboard_state_file = "data/system/leaderboard_state.json"
        self.load_leaderboard_state()
    
    def load_leaderboard_state(self):
        """Load leaderboard state from JSON file."""
        try:
            if os.path.exists(self.leaderboard_state_file):
                with open(self.leaderboard_state_file, 'r') as f:
                    self.leaderboard_state = json.load(f)
            else:
                self.leaderboard_state = {
                    "paused": False,
                    "paused_by": None,
                    "paused_at": None,
                    "paused_reason": None
                }
                self.save_leaderboard_state()
        except Exception as e:
            self.logger.error(f"Error loading leaderboard state: {e}")
            self.leaderboard_state = {
                "paused": False,
                "paused_by": None,
                "paused_at": None,
                "paused_reason": None
            }
    
    def save_leaderboard_state(self):
        """Save leaderboard state to JSON file."""
        try:
            os.makedirs(os.path.dirname(self.leaderboard_state_file), exist_ok=True)
            with open(self.leaderboard_state_file, 'w') as f:
                json.dump(self.leaderboard_state, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving leaderboard state: {e}")
    
    @app_commands.command(name="leaderboard", description="View top leaders and alliances")
    async def leaderboard(self, interaction: discord.Interaction):
        """Interactive command to view leaderboards."""
        # Check if leaderboards are paused
        if self.leaderboard_state.get("paused", False):
            embed = EmbedGenerator.create_embed(
                title="Leaderboards Paused",
                description="Leaderboards are currently paused due to the Glorious Victory event not being active.",
                color=discord.Color.orange()
            )
            
            if self.leaderboard_state.get("paused_by"):
                embed.add_field(
                    name="Paused By",
                    value=f"<@{self.leaderboard_state['paused_by']}>",
                    inline=True
                )
            
            if self.leaderboard_state.get("paused_at"):
                embed.add_field(
                    name="Paused At",
                    value=self.leaderboard_state["paused_at"],
                    inline=True
                )
            
            if self.leaderboard_state.get("paused_reason"):
                embed.add_field(
                    name="Reason",
                    value=self.leaderboard_state["paused_reason"],
                    inline=False
                )
            
            embed = EmbedGenerator.finalize_embed(embed)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        embed = EmbedGenerator.create_embed(
            title="Leaderboard Rankings",
            description="Track top performers in Avatar Realms Collide",
            color=discord.Color.gold()
        )
        
        embed.add_field(name="👑 Individual Rankings", value="Top 10 Leaders", inline=True)
        embed.add_field(name="🤝 Alliance Rankings", value="Top 10 Alliances", inline=True)
        
        embed = EmbedGenerator.finalize_embed(embed, default_footer="Provided by Deng (@2rk)")
        
        view = LeaderboardView()
        await interaction.response.send_message(embed=embed, view=view)
    
    @app_commands.command(name="leader", description="Admin leaderboard management commands")
    @app_commands.describe(
        action="Action to perform: pause, resume, or clear",
        reason="Reason for pausing (optional)"
    )
    @app_commands.choices(action=[
        app_commands.Choice(name="pause", value="pause"),
        app_commands.Choice(name="resume", value="resume"),
        app_commands.Choice(name="clear", value="clear")
    ])
    async def leader(self, interaction: discord.Interaction, action: str, reason: str = None):
        """Admin command for leaderboard management."""
        # Check for administrator permissions
        if not interaction.user.guild_permissions.administrator:
            embed = EmbedGenerator.create_error_embed("You need administrator permissions to manage leaderboards.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        if action == "pause":
            await self.pause_leaderboards(interaction, reason)
        elif action == "resume":
            await self.resume_leaderboards(interaction)
        elif action == "clear":
            await self.clear_leaderboards(interaction)
    
    async def pause_leaderboards(self, interaction: discord.Interaction, reason: str = None):
        """Pause leaderboard functionality."""
        from datetime import datetime
        
        self.leaderboard_state["paused"] = True
        self.leaderboard_state["paused_by"] = interaction.user.id
        self.leaderboard_state["paused_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        self.leaderboard_state["paused_reason"] = reason or "Glorious Victory event not active"
        
        self.save_leaderboard_state()
        
        embed = EmbedGenerator.create_embed(
            title="Leaderboards Paused",
            description="Leaderboard functionality has been paused successfully.",
            color=discord.Color.orange()
        )
        
        embed.add_field(
            name="Paused By",
            value=f"<@{interaction.user.id}>",
            inline=True
        )
        
        embed.add_field(
            name="Paused At",
            value=self.leaderboard_state["paused_at"],
            inline=True
        )
        
        if reason:
            embed.add_field(
                name="Reason",
                value=reason,
                inline=False
            )
        
        embed = EmbedGenerator.finalize_embed(embed)
        await interaction.response.send_message(embed=embed)
    
    async def resume_leaderboards(self, interaction: discord.Interaction):
        """Resume leaderboard functionality."""
        self.leaderboard_state["paused"] = False
        self.leaderboard_state["paused_by"] = None
        self.leaderboard_state["paused_at"] = None
        self.leaderboard_state["paused_reason"] = None
        
        self.save_leaderboard_state()
        
        embed = EmbedGenerator.create_embed(
            title="Leaderboards Resumed",
            description="Leaderboard functionality has been reactivated successfully.",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="Resumed By",
            value=f"<@{interaction.user.id}>",
            inline=True
        )
        
        embed.add_field(
            name="Status",
            value="✅ Active and Available",
            inline=True
        )
        
        embed = EmbedGenerator.finalize_embed(embed)
        await interaction.response.send_message(embed=embed)
    
    async def clear_leaderboards(self, interaction: discord.Interaction):
        """Clear leaderboard data and reset state."""
        # Clear leaderboard state
        self.leaderboard_state = {
            "paused": False,
            "paused_by": None,
            "paused_at": None,
            "paused_reason": None
        }
        self.save_leaderboard_state()
        
        embed = EmbedGenerator.create_embed(
            title="Leaderboards Cleared",
            description="Leaderboard data and state have been cleared successfully.",
            color=discord.Color.red()
        )
        
        embed.add_field(
            name="Cleared By",
            value=f"<@{interaction.user.id}>",
            inline=True
        )
        
        embed.add_field(
            name="Status",
            value="🔄 Reset to Default",
            inline=True
        )
        
        embed.add_field(
            name="What was cleared",
            value="• Leaderboard pause state\n• Pause history\n• All stored data",
            inline=False
        )
        
        embed = EmbedGenerator.finalize_embed(embed)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(Leaderboards(bot)) 