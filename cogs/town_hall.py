"""
Town Hall command module for Avatar Realms Collide Discord Bot.
Provides town hall information and requirements viewing functionality.
"""

import discord
from discord import app_commands
from discord.ext import commands
from utils.ui_components import TownHallModal

class TownHall(commands.Cog):
    """Town Hall command cog."""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
    
    @app_commands.command(name="townhall", description="View town hall information and requirements")
    async def townhall(self, interaction: discord.Interaction):
        """Interactive command to view town hall information."""
        embed = discord.Embed(
            title="🏛️ Town Hall Information",
            description="Enter the town hall level you want to see requirements for (3-30).",
            color=discord.Color.gold()
        )
        
        embed.add_field(
            name="📊 Overview",
            value="• **Max Level:** 30\n• **Resource Growth:** Exponential\n• **Time Growth:** Exponential\n• **Note:** Times shown do not include research and town hall buffs for time reduction",
            inline=False
        )
        
        embed.add_field(
            name="🎯 How to Use",
            value="Click the button below to enter the town hall level you want to check.",
            inline=False
        )
        
        embed.set_footer(text="Provided by Deng (@2rk) • Click the button below")
        
        # Create view with modal button
        view = discord.ui.View(timeout=60)
        
        async def show_modal(interaction: discord.Interaction):
            modal = TownHallModal()
            await interaction.response.send_modal(modal)
        
        button = discord.ui.Button(
            label="Enter Town Hall Level",
            style=discord.ButtonStyle.primary,
            emoji="🏛️"
        )
        button.callback = show_modal
        view.add_item(button)
        
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(TownHall(bot)) 