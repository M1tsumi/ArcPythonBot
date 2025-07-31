"""
Leaderboards command module for Avatar Realms Collide Discord Bot.
Provides leaderboard viewing functionality.
"""

import discord
from discord import app_commands
from discord.ext import commands
from utils.ui_components import LeaderboardView

class Leaderboards(commands.Cog):
    """Leaderboards command cog."""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
    
    @app_commands.command(name="leaderboard", description="View top leaders and alliances")
    async def leaderboard(self, interaction: discord.Interaction):
        """Interactive command to view leaderboards."""
        embed = discord.Embed(
            title="🏆 Leaderboard Rankings",
            description="Track top performers in Avatar Realms Collide",
            color=discord.Color.gold()
        )
        
        embed.add_field(
            name="👑 Individual Rankings",
            value="**Top 10 Leaders**",
            inline=True
        )
        
        embed.add_field(
            name="🤝 Alliance Rankings",
            value="**Top 10 Alliances**",
            inline=True
        )
        
        embed.set_footer(text="Information Provided and Processed by Kuvira (@archfiends) • Choose a leaderboard to view")
        
        view = LeaderboardView()
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(Leaderboards(bot)) 