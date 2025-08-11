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
            if self.logger:
                self.logger.error(f"Error getting translated text for user {user_id}, key {key}: {e}")
            return f"[Translation error: {key}]"
    
    @app_commands.command(name="talent_trees", description="Interactive talent tree browser")
    async def talent_trees(self, interaction: discord.Interaction):
        """Interactive command to browse talent trees by element."""
        embed = EmbedGenerator.create_embed(
            title=self.get_text(interaction.user.id, "talent_tree_browser_title"),
            description=self.get_text(interaction.user.id, "talent_tree_browser_desc"),
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
        
        embed = EmbedGenerator.finalize_embed(embed, default_footer="Information provided by Kuvira (@archfiends)")
        
        view = discord.ui.View(timeout=60)
        view.add_item(ElementSelectDropdown(self.data_parser))
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(TalentTrees(bot)) 