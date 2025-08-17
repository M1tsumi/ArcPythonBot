"""
Hero Rankup command module for Avatar Realms Collide Discord Bot.
Provides hero rankup guide and cost viewing functionality.
"""

import discord
from discord import app_commands
from discord.ext import commands
from utils.ui_components import HeroRankupView

class HeroRankup(commands.Cog):
    """Hero Rankup command cog."""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
    
    @app_commands.command(name="hero_rankup", description="View hero rankup guide and costs")
    async def hero_rankup(self, interaction: discord.Interaction):
        """Command to show interactive hero rankup guide with costs."""
        embed = discord.Embed(
            title="⭐ Hero Rankup Guide",
            description="Select a star level to view detailed rankup information and costs",
            color=discord.Color.purple()
        )
        
        embed.add_field(
            name="📋 Available Options",
            value="Click the buttons below to view information for each star level:\n\n🔓 **Unlock** - Hero unlock cost\n⭐ **1 Star** - Level 1-10 requirements\n⭐ **2 Stars** - Level 20 requirements\n⭐ **3 Stars** - Level 30 requirements\n⭐ **4 Stars** - Level 40 requirements\n⭐ **5 Stars** - Level 50 requirements\n⭐ **6 Stars** - Level 60 requirements\n💰 **Total Cost** - Complete cost breakdown",
            inline=False
        )
        
        embed.set_footer(text="Information Provided and Processed by Kuvira (@archfiends) • Select a button to view details")
        
        view = HeroRankupView()
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(HeroRankup(bot)) 