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
            # Create clean stats section
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
                    name="📊 Character Stats",
                    value=stats_text,
                    inline=True
                )
        
        # Add talent type information
        if talent_type_info and talent_type_info.get('talent_type'):
            embed.add_field(
                name="🌳 Talent Type",
                value=talent_type_info['talent_type'],
                inline=True
            )
        
        embed.set_footer(text="Information Provided and Processed by Kuvira (@archfiends) • Your talent trees are ready below")
        
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
            "Rare": "🔵",
            "Epic": "🟣",
            "Legendary": "🟡"
        }
        return rarity_emojis.get(rarity, "🔵")
    
    @discord.ui.button(label="⬅️ Back to Elements", style=discord.ButtonStyle.secondary, emoji="⬅️")
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Go back to element selection."""
        embed = discord.Embed(
            title="🌟 Welcome to the Talent Tree Browser",
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
        
        embed.set_footer(text="Information Provided and Processed by Kuvira (@archfiends) • Pick your element to begin your journey")
        
        view = discord.ui.View(timeout=60)
        view.add_item(ElementSelectDropdown(self.data_parser))
        await interaction.response.edit_message(embed=embed, view=view)

class SkillPriorityView(discord.ui.View):
    """View for skill priority selection."""
    
    def __init__(self, data_parser: DataParser):
        super().__init__(timeout=60)
        self.data_parser = data_parser
        
        # Add hero selection buttons (max 25 buttons per Discord limit)
        skill_priorities = self.data_parser.get_skill_priorities()
        heroes_with_skills = sorted(skill_priorities.keys())
        
        for hero_name in heroes_with_skills[:25]:  # Limit to 25 buttons
            button = discord.ui.Button(
                label=hero_name,
                style=discord.ButtonStyle.primary,
                custom_id=f"skill_{hero_name.lower().replace(' ', '_')}"
            )
            button.callback = self.create_hero_callback(hero_name)
            self.add_item(button)
    
    def create_hero_callback(self, hero_name: str):
        """Create a callback function for a hero button."""
        async def callback(interaction: discord.Interaction):
            await self.show_skill_priorities(interaction, hero_name)
        return callback
    
    async def show_skill_priorities(self, interaction: discord.Interaction, hero_name: str):
        """Show skill priorities for the selected hero."""
        skill_priorities = self.data_parser.get_skill_priorities()
        hero_data = skill_priorities.get(hero_name)
        
        if not hero_data:
            embed = discord.Embed(
                title="❌ Skill Priorities Not Found",
                description=f"Sorry! Skill priorities for {hero_name} are not available yet.",
                color=discord.Color.dark_red()
            )
            await interaction.response.edit_message(embed=embed, view=None)
            return
        
        # Get character info for additional details
        character = self.data_parser.get_character(hero_name)
        
        # Create comprehensive embed
        embed = discord.Embed(
            title=f"🎯 {hero_name}",
            description="Skill priority order",
            color=self.get_element_color(character.get('element', 'Unknown') if character else 'Unknown')
        )
        
        # Add skill priorities
        skills = hero_data['skills']
        skills_text = ""
        for i, skill in enumerate(skills, 1):
            skills_text += f"**{i}.** {skill}\n"
        
        embed.add_field(
            name="⚔️ Skill Order",
            value=skills_text,
            inline=False
        )
        
        # Add notes if available
        if hero_data.get('notes'):
            embed.add_field(
                name="💡 Notes",
                value=hero_data['notes'],
                inline=False
            )
        
        embed.set_footer(text="Information Provided and Processed by Kuvira (@archfiends) • Skill priorities for optimal progression")
        
        await interaction.response.edit_message(embed=embed, view=None)
    
    def get_element_color(self, element: str) -> discord.Color:
        """Get the appropriate color for each element."""
        colors = {
            "Fire": discord.Color.red(),
            "Water": discord.Color.blue(),
            "Earth": discord.Color.dark_green(),
            "Air": discord.Color.light_grey()
        }
        return colors.get(element, discord.Color.purple())

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
                description="Most powerful players in Avatar Realms Collide",
                color=discord.Color.gold()
            )
            
            file = discord.File(file_path, filename="top-leaders.webp")
            embed.set_image(url="attachment://top-leaders.webp")
            embed.set_footer(text="Information Provided and Processed by Kuvira (@archfiends) • Updated regularly")
            
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
                description="Strongest alliances in Avatar Realms Collide",
                color=discord.Color.blue()
            )
            
            file = discord.File(file_path, filename="top-alliances.webp")
            embed.set_image(url="attachment://top-alliances.webp")
            embed.set_footer(text="Information Provided and Processed by Kuvira (@archfiends) • Updated regularly")
            
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
            title="🌟 Welcome to the Talent Tree Browser",
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
        
        embed.set_footer(text="Information Provided and Processed by Kuvira (@archfiends) • Pick your element to begin your journey")
        
        view = discord.ui.View(timeout=60)
        view.add_item(ElementSelectDropdown(self.data_parser))
        await interaction.response.send_message(embed=embed, view=view)
    
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
        embed = discord.Embed(
            title="🎯 Hero Skill Priorities",
            description="View optimal skill upgrade order for each hero",
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
        
        embed.set_footer(text="Information Provided and Processed by Kuvira (@archfiends) • Select a hero to view their skill priorities")
        
        # Create view with hero selection buttons
        view = SkillPriorityView(self.data_parser)
        await interaction.response.send_message(embed=embed, view=view)
    
    @app_commands.command(name="links", description="Get bot links and information")
    async def links(self, interaction: discord.Interaction):
        """Command to provide bot links and information."""
        embed = discord.Embed(
            title="🔗 Bot Links & Information",
            description="Connect with the Avatar Realms Collide community!",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="📱 Join Our Discord Server",
            value="[Join Server](https://discord.gg/a3tGyAwVRc)",
            inline=True
        )
        
        embed.add_field(
            name="🤖 Add Bot to Your Server",
            value="[Add to Server](https://discord.com/oauth2/authorize?client_id=1242988284347420673)",
            inline=True
        )
        
        embed.add_field(
            name="👨‍💻 Developer",
            value="**Developed by Quefep**",
            inline=False
        )
        
        embed.set_footer(text="Join our Discord for more information and updates!")
        
                await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="townhall", description="View town hall information and requirements")
    async def townhall(self, interaction: discord.Interaction):
        """Interactive command to view town hall information."""
        embed = discord.Embed(
            title="🏛️ Town Hall Information",
            description="Maximum town hall level is **30**. Resources and time increase exponentially with each level.",
            color=discord.Color.gold()
        )
        
        embed.add_field(
            name="📊 Overview",
            value="• **Max Level:** 30\n• **Resource Growth:** Exponential\n• **Time Growth:** Exponential\n• **Note:** Times shown do not include research and town hall buffs for time reduction",
            inline=False
        )
        
        embed.add_field(
            name="🎯 Select Level",
            value="Choose a town hall level (3-30) to view detailed requirements:",
            inline=False
        )
        
        embed.set_footer(text="Information Provided and Processed by Kuvira (@archfiends) • Select a level below")
        
        # Create view with town hall level selection
        view = TownHallView()
        await interaction.response.send_message(embed=embed, view=view)

class TownHallView(discord.ui.View):
    """View for town hall level selection."""
    
    def __init__(self):
        super().__init__(timeout=60)
        
        # Town hall data
        self.town_hall_data = {
            3: {"food": "2.3K", "wood": "2.3K", "stone": "700", "time": "15s"},
            4: {"food": "3.7K", "wood": "3.7K", "stone": "1.0K", "time": "40s"},
            5: {"food": "6.7K", "wood": "6.7K", "stone": "3.0K", "time": "2m"},
            6: {"food": "12.0K", "wood": "12.0K", "stone": "7.2K", "time": "5m"},
            7: {"food": "16.8K", "wood": "16.8K", "stone": "10.1K", "time": "50m"},
            8: {"food": "23.5K", "wood": "23.5K", "stone": "14.1K", "time": "2h 30m"},
            9: {"food": "32.9K", "wood": "32.9K", "stone": "19.7K", "time": "5h"},
            10: {"food": "47.4K", "wood": "47.4K", "stone": "28.4K", "time": "7h 20m"},
            11: {"food": "68.3K", "wood": "68.3K", "stone": "41.0K", "time": "12h"},
            12: {"food": "98.4K", "wood": "98.4K", "stone": "59.0K", "time": "13h 12m"},
            13: {"food": "142.0K", "wood": "142.0K", "stone": "85.2K", "time": "14h 31m 10s"},
            14: {"food": "204.0K", "wood": "204.0K", "stone": "122.0K", "time": "1d 3h 35m 10s"},
            15: {"food": "298.0K", "wood": "298.0K", "stone": "179.0K", "time": "1d 9h 6m 10s"},
            16: {"food": "435.0K", "wood": "435.0K", "stone": "261.0K", "time": "1d 15h 43m 20s"},
            17: {"food": "635.0K", "wood": "635.0K", "stone": "381.0K", "time": "1d 19h 41m 40s"},
            18: {"food": "927.0K", "wood": "927.0K", "stone": "556.0K", "time": "2d 3m 50s"},
            19: {"food": "1.4M", "wood": "1.4M", "stone": "840.0K", "time": "2d 4h 52m 10s"},
            20: {"food": "2.0M", "wood": "2.0M", "stone": "1.2M", "time": "3d 2h 1m"},
            21: {"food": "2.9M", "wood": "2.9M", "stone": "1.7M", "time": "3d 16h 49m 10s"},
            22: {"food": "4.3M", "wood": "4.3M", "stone": "2.6M", "time": "4d 10h 35m"},
            23: {"food": "6.3M", "wood": "6.3M", "stone": "3.8M", "time": "5d 7h 54m"},
            24: {"food": "9.3M", "wood": "9.3M", "stone": "5.6M", "time": "6d 9h 28m 50s"},
            25: {"food": "13.7M", "wood": "13.7M", "stone": "8.2M", "time": "8d 22h 52m 20s"},
            26: {"food": "20.3M", "wood": "20.3M", "stone": "12.2M", "time": "16d 2h 46m 10s"},
            27: {"food": "30.0M", "wood": "30.0M", "stone": "18.0M", "time": "20d 22h 48m"},
            28: {"food": "44.4M", "wood": "44.4M", "stone": "26.6M", "time": "27d 5h 38m 20s"},
            29: {"food": "65.7M", "wood": "65.7M", "stone": "39.4M", "time": "46d 7h 11m 10s"},
            30: {"food": "98.6M", "wood": "98.6M", "stone": "59.2M", "time": "148d 3h 47m 40s"}
        }
        
        # Add level selection dropdown
        options = []
        for level in range(3, 31):
            options.append(discord.SelectOption(
                label=f"Town Hall {level}",
                description=f"Level {level} requirements",
                value=str(level)
            ))
        
        self.add_item(TownHallDropdown(self.town_hall_data, options))

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

async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(SlashCommands(bot)) 