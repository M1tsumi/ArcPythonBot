"""
Talent Trees command module for Avatar Realms Collide Discord Bot.
Provides interactive talent tree browsing functionality.
"""

import discord
from discord import app_commands
from discord.ext import commands
from utils.data_parser import DataParser
from utils.ui_components import ElementSelectDropdown
from utils.embed_generator import EmbedGenerator

class TalentTrees(commands.Cog):
    """Talent Trees command cog."""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        self.data_parser = DataParser()
    
    @app_commands.command(name="talent_trees", description="Interactive talent tree browser")
    async def talent_trees(self, interaction: discord.Interaction):
        """Interactive command to browse talent trees by element."""
        embed = EmbedGenerator.create_embed(
            title="Talent Tree Browser",
            description="Choose your element to discover characters and their talent trees.",
            color=discord.Color.from_rgb(52, 152, 219)
        )
        
        embed.add_field(
            name="🎯 Available Elements",
            value="**🔥 Fire** • **💧 Water** • **🌍 Earth** • **💨 Air**",
            inline=False
        )
        
        embed.add_field(
            name="📊 Character Rarities",
            value="**🔵 Rare** • **🟣 Epic** • **🟡 Legendary**",
            inline=False
        )
        
        embed = EmbedGenerator.finalize_embed(embed, default_footer="Provided by Deng (@2rk)")
        
        view = discord.ui.View(timeout=60)
        view.add_item(ElementSelectDropdown(self.data_parser))
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(TalentTrees(bot)) 