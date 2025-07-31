"""
Slash commands cog for the Avatar Realms Collide Discord Bot.
Provides modern slash command interface for better user experience.
"""

import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional, Dict, List
from utils.embed_generator import EmbedGenerator
from utils.data_parser import DataParser
from config.settings import ERROR_MESSAGES
from pathlib import Path

class ElementSelectDropdown(discord.ui.Select):
    """Dropdown for element selection."""
    
    def __init__(self, data_parser: DataParser):
        options = [
            discord.SelectOption(label="Fire", description="Firebenders and Fire Nation", value="Fire", emoji="🔥"),
            discord.SelectOption(label="Water", description="Waterbenders and Water Tribe", value="Water", emoji="💧"),
            discord.SelectOption(label="Earth", description="Earthbenders and Earth Kingdom", value="Earth", emoji="🌍"),
            discord.SelectOption(label="Air", description="Airbenders and Air Nomads", value="Air", emoji="💨")
        ]
        
        super().__init__(
            placeholder="Select an element...",
            min_values=1,
            max_values=1,
            options=options
        )
        self.data_parser = data_parser
        
    async def callback(self, interaction: discord.Interaction):
        """Handle element selection and show character buttons."""
        element = self.values[0]
        
        # Get characters by element
        characters = self.data_parser.get_character_list()
        element_characters = [char for char in characters if char.get('element', '').lower() == element.lower()]
        
        if not element_characters:
            embed = discord.Embed(
                title="No Characters Found",
                description=f"Looks like we don't have any {element} characters in our collection yet. Check back soon!",
                color=discord.Color.dark_red()
            )
            await interaction.response.edit_message(embed=embed, view=None)
            return
        
        # Create character selection embed
        embed = discord.Embed(
            title=f"Meet the {element} Masters",
            description=f"Discover {len(element_characters)} incredible characters from the {element} element",
            color=self.get_element_color(element)
        )
        
        # Add character list with clean formatting
        char_list = ""
        for char in element_characters:
            rarity_emoji = self.get_rarity_emoji(char.get('rarity', 'Unknown'))
            char_list += f"{rarity_emoji} **{char['name']}**\n"
        
        embed.add_field(
            name="Available Characters",
            value=char_list,
            inline=False
        )
        
        embed.set_footer(text="Choose your champion below")
        
        # Create character selection view
        view = CharacterSelectView(self.data_parser, element_characters)
        await interaction.response.edit_message(embed=embed, view=view)
    
    def get_element_color(self, element: str) -> discord.Color:
        """Get the appropriate color for each element."""
        colors = {
            "Fire": discord.Color.red(),
            "Water": discord.Color.blue(),
            "Earth": discord.Color.dark_green(),
            "Air": discord.Color.light_grey()
        }
        return colors.get(element, discord.Color.blue())
    
    def get_rarity_emoji(self, rarity: str) -> str:
        """Get emoji for character rarity."""
        rarity_emojis = {
            "Common": "⚪",
            "Rare": "🔵",
            "Epic": "🟣",
            "Legendary": "🟡",
            "Mythic": "🟠"
        }
        return rarity_emojis.get(rarity, "⚪")

class CharacterSelectView(discord.ui.View):
    """View for selecting characters with buttons."""
    
    def __init__(self, data_parser: DataParser, characters: List[Dict]):
        super().__init__(timeout=60)
        self.data_parser = data_parser
        self.characters = characters
        
        # Add character buttons (max 25 buttons per Discord limit)
        for i, char in enumerate(characters[:25]):  # Limit to 25 buttons
            button = discord.ui.Button(
                label=char['name'],
                style=discord.ButtonStyle.primary,
                custom_id=f"char_{char['name'].lower().replace(' ', '_')}"
            )
            button.callback = self.create_character_callback(char['name'])
            self.add_item(button)
        
    def create_character_callback(self, character_name: str):
        """Create a callback function for a character button."""
        async def callback(interaction: discord.Interaction):
            await self.show_character_talents(interaction, character_name)
        return callback
        
    async def show_character_talents(self, interaction: discord.Interaction, character_name: str):
        """Show talent trees for the selected character."""
        # Get character information
        character = self.data_parser.get_character(character_name)
        
        # Get talent type information
        talent_type_info = self.data_parser.get_talent_type_info(character_name)
        
        # Get talent tree images
        talent_images = self.data_parser.get_talent_tree_images(character_name)
        
        if not talent_images:
            embed = discord.Embed(
                title="No Talent Trees Found",
                description=f"Sorry! We don't have talent trees available for {character_name} yet. They're still in development!",
                color=discord.Color.dark_red()
            )
            await interaction.response.edit_message(embed=embed, view=None)
            return
        
        # Create comprehensive embed with character information
        embed = discord.Embed(
            title=f"🌟 {character_name}",
            description=character.get('description', ''),
            color=self.get_element_color(character.get('element', 'Unknown'))
        )
        
        # Add character information if available
        if character:
            # Create stats section
            stats_text = ""
            if 'rarity' in character:
                rarity_emoji = self.get_rarity_emoji(character['rarity'])
                stats_text += f"{rarity_emoji} **{character['rarity']}**\n"
            
            if 'element' in character:
                element_emoji = self.get_element_emoji(character['element'])
                stats_text += f"{element_emoji} **{character['element']}**\n"
            
            if 'category' in character:
                stats_text += f"**{character['category']}**\n"
            
            if stats_text:
                embed.add_field(
                    name="Character Stats",
                    value=stats_text,
                    inline=True
                )
        
        # Add talent type information
        if talent_type_info and talent_type_info.get('talent_type'):
            embed.add_field(
                name="Talent Specialization",
                value=talent_type_info['talent_type'],
                inline=True
            )
        
        embed.set_footer(text="Your talent trees are ready below")
        
        # Send the embed first
        await interaction.response.edit_message(embed=embed, view=None)
        
        # Send talent tree images in separate embeds
        if talent_images.get('talent_tree_1'):
            embed1 = discord.Embed(
                title=f"🌳 {character_name}'s First Talent Tree",
                color=self.get_element_color(character.get('element', 'Unknown'))
            )
            file1 = discord.File(talent_images['talent_tree_1'], filename=Path(talent_images['talent_tree_1']).name)
            embed1.set_image(url=f"attachment://{Path(talent_images['talent_tree_1']).name}")
            await interaction.followup.send(embed=embed1, file=file1)
        
        if talent_images.get('talent_tree_2'):
            embed2 = discord.Embed(
                title=f"🌿 {character_name}'s Second Talent Tree",
                color=self.get_element_color(character.get('element', 'Unknown'))
            )
            file2 = discord.File(talent_images['talent_tree_2'], filename=Path(talent_images['talent_tree_2']).name)
            embed2.set_image(url=f"attachment://{Path(talent_images['talent_tree_2']).name}")
            await interaction.followup.send(embed=embed2, file=file2)
    
    def get_element_color(self, element: str) -> discord.Color:
        """Get the appropriate color for each element."""
        colors = {
            "Fire": discord.Color.red(),
            "Water": discord.Color.blue(),
            "Earth": discord.Color.dark_green(),
            "Air": discord.Color.light_grey()
        }
        return colors.get(element, discord.Color.blue())
    
    def get_element_emoji(self, element: str) -> str:
        """Get emoji for element."""
        element_emojis = {
            "Fire": "🔥",
            "Water": "💧",
            "Earth": "🌍",
            "Air": "💨"
        }
        return element_emojis.get(element, "❓")
    
    def get_rarity_emoji(self, rarity: str) -> str:
        """Get emoji for character rarity."""
        rarity_emojis = {
            "Common": "⚪",
            "Rare": "🔵",
            "Epic": "🟣",
            "Legendary": "🟡",
            "Mythic": "🟠"
        }
        return rarity_emojis.get(rarity, "⚪")
    
    @discord.ui.button(label="⬅️ Back to Elements", style=discord.ButtonStyle.secondary, emoji="⬅️")
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Go back to element selection."""
        embed = discord.Embed(
            title="Welcome to the Talent Tree Browser",
            description="Ready to explore the bending arts? Choose your element to discover amazing characters!",
            color=discord.Color.from_rgb(52, 152, 219)
        )
        
        embed.add_field(
            name="Available Elements",
            value="🔥 Fire • 💧 Water • 🌍 Earth • 💨 Air",
            inline=False
        )
        
        embed.set_footer(text="Pick your element to begin your journey")
        
        view = discord.ui.View(timeout=60)
        view.add_item(ElementSelectDropdown(self.data_parser))
        await interaction.response.edit_message(embed=embed, view=view)

class LeaderboardView(discord.ui.View):
    """View for leaderboard selection."""
    
    def __init__(self):
        super().__init__(timeout=60)
    
    @discord.ui.button(label="👑 Top 10 Leaders", style=discord.ButtonStyle.primary, emoji="👑")
    async def top_leaders_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show top 10 leaders leaderboard."""
        try:
            file_path = Path("HeroTalentImages/top-leaders.webp")
            if not file_path.exists():
                embed = discord.Embed(
                    title="❌ Leaderboard Not Found",
                    description="The top leaders leaderboard is currently unavailable.",
                    color=discord.Color.dark_red()
                )
                await interaction.response.edit_message(embed=embed, view=None)
                return
            
            embed = discord.Embed(
                title="👑 Top 10 Leaders",
                description="The most powerful players in Avatar Realms Collide!",
                color=discord.Color.gold()
            )
            
            file = discord.File(file_path, filename="top-leaders.webp")
            embed.set_image(url="attachment://top-leaders.webp")
            embed.set_footer(text="Updated regularly")
            
            await interaction.response.edit_message(embed=embed, view=None)
            await interaction.followup.send(file=file)
            
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error Loading Leaderboard",
                description="Sorry! There was an issue loading the leaderboard. Please try again later.",
                color=discord.Color.dark_red()
            )
            await interaction.response.edit_message(embed=embed, view=None)
    
    @discord.ui.button(label="🤝 Top 10 Alliances", style=discord.ButtonStyle.primary, emoji="🤝")
    async def top_alliances_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show top 10 alliances leaderboard."""
        try:
            file_path = Path("HeroTalentImages/top-alliances.webp")
            if not file_path.exists():
                embed = discord.Embed(
                    title="❌ Leaderboard Not Found",
                    description="The top alliances leaderboard is currently unavailable.",
                    color=discord.Color.dark_red()
                )
                await interaction.response.edit_message(embed=embed, view=None)
                return
            
            embed = discord.Embed(
                title="🤝 Top 10 Alliances",
                description="The strongest alliances in Avatar Realms Collide!",
                color=discord.Color.blue()
            )
            
            file = discord.File(file_path, filename="top-alliances.webp")
            embed.set_image(url="attachment://top-alliances.webp")
            embed.set_footer(text="Updated regularly")
            
            await interaction.response.edit_message(embed=embed, view=None)
            await interaction.followup.send(file=file)
            
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error Loading Leaderboard",
                description="Sorry! There was an issue loading the leaderboard. Please try again later.",
                color=discord.Color.dark_red()
            )
            await interaction.response.edit_message(embed=embed, view=None)

class SlashCommands(commands.Cog):
    """Slash commands for modern Discord interface."""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        self.data_parser = DataParser()
    
    @app_commands.command(name="talent_trees", description="Interactive talent tree browser")
    async def talent_trees(self, interaction: discord.Interaction):
        """Interactive command to browse talent trees by element."""
        embed = discord.Embed(
            title="Welcome to the Talent Tree Browser",
            description="Ready to explore the bending arts? Choose your element to discover amazing characters!",
            color=discord.Color.from_rgb(52, 152, 219)
        )
        
        embed.add_field(
            name="Available Elements",
            value="🔥 Fire • 💧 Water • 🌍 Earth • 💨 Air",
            inline=False
        )
        
        embed.set_footer(text="Pick your element to begin your journey")
        
        view = discord.ui.View(timeout=60)
        view.add_item(ElementSelectDropdown(self.data_parser))
        await interaction.response.send_message(embed=embed, view=view)
    
    @app_commands.command(name="leaderboard", description="View top leaders and alliances")
    async def leaderboard(self, interaction: discord.Interaction):
        """Interactive command to view leaderboards."""
        embed = discord.Embed(
            title="🏆 Leaderboard Rankings",
            description="Check out the top performers in Avatar Realms Collide!",
            color=discord.Color.gold()
        )
        
        embed.add_field(
            name="Available Rankings",
            value="👑 Top 10 Leaders • 🤝 Top 10 Alliances",
            inline=False
        )
        
        embed.set_footer(text="Choose a leaderboard to view")
        
        view = LeaderboardView()
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(SlashCommands(bot)) 