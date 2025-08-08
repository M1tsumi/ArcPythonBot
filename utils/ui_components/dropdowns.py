"""
Dropdown components for Avatar Realms Collide Discord Bot.
Contains interactive dropdown menus for user selection.
"""

import discord
from typing import List, Dict
from utils.data_parser import DataParser

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
            title=f"🌟 {element} Element Masters",
            description=f"{len(element_characters)} characters available",
            color=self.get_element_color(element)
        )
        
        # Sort characters by rarity (Legendary first, then Epic, then Rare)
        rarity_order = {"Legendary": 1, "Epic": 2, "Rare": 3}
        sorted_characters = sorted(element_characters, key=lambda x: rarity_order.get(x.get('rarity', 'Rare'), 3))
        
        # Add character list with clean formatting
        char_list = ""
        for char in sorted_characters:
            rarity_emoji = self.get_rarity_emoji(char.get('rarity', 'Unknown'))
            char_list += f"{rarity_emoji} **{char['name']}**\n"
        
        embed.add_field(
            name=f"🎯 {element} Characters",
            value=char_list,
            inline=False
        )
        
        embed.set_footer(text="Information Provided and Processed by Kuvira (@archfiends) • Choose your champion below")
        
        # Create character selection view
        from .views import CharacterSelectView
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
            "Rare": "🔵",
            "Epic": "🟣",
            "Legendary": "🟡"
        }
        return rarity_emojis.get(rarity, "🔵")

class SkillPriorityElementDropdown(discord.ui.Select):
    """Dropdown for element selection in skill priorities."""
    
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
        """Handle element selection and show hero buttons."""
        element = self.values[0]
        
        # Get heroes by element that have skill priorities
        skill_priorities = self.data_parser.get_skill_priorities()
        all_characters = self.data_parser.get_character_list()
        
        # Find characters of this element that have skill priorities
        element_heroes = []
        for char in all_characters:
            if (char.get('element', '').lower() == element.lower() and 
                char['name'] in skill_priorities):
                element_heroes.append(char)
        
        if not element_heroes:
            embed = discord.Embed(
                title="No Heroes Found",
                description=f"Looks like we don't have skill priorities for any {element} heroes yet. Check back soon!",
                color=discord.Color.dark_red()
            )
            await interaction.response.edit_message(embed=embed, view=None)
            return
        
        # Create hero selection embed
        embed = discord.Embed(
            title=f"🎯 {element} Hero Skill Priorities",
            description=f"{len(element_heroes)} heroes available with skill priorities",
            color=self.get_element_color(element)
        )
        
        # Sort heroes by rarity (Legendary first, then Epic, then Rare)
        rarity_order = {"Legendary": 1, "Epic": 2, "Rare": 3}
        sorted_heroes = sorted(element_heroes, key=lambda x: rarity_order.get(x.get('rarity', 'Rare'), 3))
        
        # Add hero list with clean formatting and rarity emojis
        hero_list = ""
        for hero in sorted_heroes:
            rarity_emoji = self.get_rarity_emoji(hero.get('rarity', 'Unknown'))
            hero_list += f"{rarity_emoji} **{hero['name']}**\n"
        
        embed.add_field(
            name=f"⚔️ {element} Heroes",
            value=hero_list,
            inline=False
        )
        
        embed.set_footer(text="Information Provided and Processed by Kuvira (@archfiends) • Choose your hero below")
        
        # Create hero selection view with just the hero names
        hero_names = [hero['name'] for hero in sorted_heroes]
        from .views import SkillPriorityHeroView
        view = SkillPriorityHeroView(self.data_parser, hero_names)
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
            "Rare": "🔵",
            "Epic": "🟣",
            "Legendary": "🟡"
        }
        return rarity_emojis.get(rarity, "🔵")

class TownHallDropdown(discord.ui.Select):
    """Dropdown for town hall level selection."""
    
    def __init__(self, town_hall_data: dict, options: list):
        super().__init__(
            placeholder="Select a town hall level...",
            min_values=1,
            max_values=1,
            options=options
        )
        self.town_hall_data = town_hall_data
        
    async def callback(self, interaction: discord.Interaction):
        """Handle town hall level selection."""
        level = int(self.values[0])
        data = self.town_hall_data.get(level)
        
        if not data:
            embed = discord.Embed(
                title="❌ Level Not Found",
                description=f"Town Hall level {level} information is not available.",
                color=discord.Color.dark_red()
            )
            await interaction.response.edit_message(embed=embed, view=None)
            return
        
        embed = discord.Embed(
            title=f"🏛️ Town Hall {level}",
            description=f"Requirements for upgrading to Town Hall level {level}",
            color=discord.Color.gold()
        )
        
        embed.add_field(
            name="🌾 Food",
            value=f"**{data['food']}**",
            inline=True
        )
        
        embed.add_field(
            name="🪵 Wood",
            value=f"**{data['wood']}**",
            inline=True
        )
        
        embed.add_field(
            name="🪨 Stone",
            value=f"**{data['stone']}**",
            inline=True
        )
        
        embed.add_field(
            name="⏰ Base Time",
            value=f"**{data['time']}**",
            inline=False
        )
        
        embed.add_field(
            name="📝 Note",
            value="*Times shown do not include research and town hall buffs for time reduction*",
            inline=False
        )
        
        embed.set_footer(text="Information Provided and Processed by Kuvira (@archfiends) • Town Hall requirements")
        
        await interaction.response.edit_message(embed=embed, view=None) 