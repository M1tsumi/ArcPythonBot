"""
Skill Priorities command module for Avatar Realms Collide Discord Bot.
Provides skill priority viewing functionality for heroes.
"""

import discord
from discord import app_commands
from discord.ext import commands
from utils.data_parser import DataParser
from utils.ui_components import SkillPriorityElementDropdown
from utils.embed_generator import EmbedGenerator

class SkillPriorities(commands.Cog):
    """Skill Priorities command cog."""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        self.data_parser = DataParser()
    
    @app_commands.command(name="skill_priorities", description="View skill priorities for heroes")
    async def skill_priorities(self, interaction: discord.Interaction):
        """Interactive command to view skill priorities for all heroes."""
        skill_priorities = self.data_parser.get_skill_priorities()
        all_characters = self.data_parser.get_character_list()
        
        # Find characters with and without skill priorities
        characters_with_skills = set(skill_priorities.keys())
        all_character_names = {char['name'] for char in all_characters}
        characters_without_skills = all_character_names - characters_with_skills
        
        # Create main embed
        embed = EmbedGenerator.create_embed(
            title="Hero Skill Priorities",
            description="Choose an element to view skill priorities for heroes.",
            color=discord.Color.purple()
        )
        
        # Add statistics
        total_characters = len(all_character_names)
        characters_with_skills_count = len(characters_with_skills)
        
        embed.add_field(
            name="📊 Statistics",
            value=f"**{characters_with_skills_count}/{total_characters}** heroes with skill priorities",
            inline=False
        )
        
        embed.add_field(
            name="🎯 Available Elements",
            value="**🔥 Fire** • **💧 Water** • **🌍 Earth** • **💨 Air**",
            inline=False
        )
        
        embed = EmbedGenerator.finalize_embed(embed, default_footer="Information provided by Kuvira (@archfiends)")
        
        # Create view with element selection dropdown
        view = discord.ui.View(timeout=60)
        view.add_item(SkillPriorityElementDropdown(self.data_parser))
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(SkillPriorities(bot)) 