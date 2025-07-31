"""
View components for Avatar Realms Collide Discord Bot.
Contains interactive view components with buttons and layouts.
"""

import discord
from typing import List, Dict
from pathlib import Path
from utils.data_parser import DataParser

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
        from .dropdowns import ElementSelectDropdown
        view.add_item(ElementSelectDropdown(self.data_parser))
        await interaction.response.edit_message(embed=embed, view=view)

class SkillPriorityHeroView(discord.ui.View):
    """View for selecting heroes with skill priorities."""
    
    def __init__(self, data_parser: DataParser, heroes: List[str]):
        super().__init__(timeout=60)
        self.data_parser = data_parser
        self.heroes = heroes
        
        # Add hero buttons (max 25 buttons per Discord limit)
        for hero_name in heroes[:25]:  # Limit to 25 buttons
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
            file_path = Path("assets/images/leaderboards/top-leaders.webp")
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
            file_path = Path("assets/images/leaderboards/top-alliances.webp")
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
        
        from .dropdowns import TownHallDropdown
        self.add_item(TownHallDropdown(self.town_hall_data, options))

class HeroRankupView(discord.ui.View):
    """View for interactive hero rankup guide."""
    
    def __init__(self):
        super().__init__(timeout=300)  # 5 minute timeout
        
    @discord.ui.button(label="🔓 Unlock", style=discord.ButtonStyle.secondary)
    async def unlock_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show unlock information."""
        embed = discord.Embed(
            title="🔓 Hero Unlock",
            description="Information for unlocking a hero",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="Cost",
            value="**10 shards** - Unlock hero",
            inline=False
        )
        
        embed.add_field(
            name="Total Shards Used",
            value="**10 shards**",
            inline=False
        )
        
        embed.set_footer(text="Information Provided and Processed by Kuvira (@archfiends)")
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="⭐ 1 Star", style=discord.ButtonStyle.primary)
    async def one_star_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show 1 star information."""
        embed = discord.Embed(
            title="⭐ 1 Star (Level 1-10)",
            description="Information for 1 star rankup",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Cost Breakdown",
            value="**1-5 shards** - Partial stars (1,1,1,2,3)\n**3 shards** - Complete 1 star\n**3-5 shards** - Partial stars (3,3,3,5)",
            inline=False
        )
        
        embed.add_field(
            name="Total Shards Used",
            value="**28 shards** (10 unlock + 18 for 1 star)",
            inline=False
        )
        
        embed.set_footer(text="Information Provided and Processed by Kuvira (@archfiends)")
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="⭐⭐ 2 Stars", style=discord.ButtonStyle.primary)
    async def two_star_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show 2 star information."""
        embed = discord.Embed(
            title="⭐⭐ 2 Stars (Level 20)",
            description="Information for 2 star rankup",
            color=discord.Color.purple()
        )
        
        embed.add_field(
            name="Cost Breakdown",
            value="**8 shards** - Complete 2 stars\n**8-12 shards** - Partial stars (8,8,8,12)",
            inline=False
        )
        
        embed.add_field(
            name="Total Shards Used",
            value="**64 shards** (10 unlock + 18 for 1 star + 36 for 2 stars)",
            inline=False
        )
        
        embed.set_footer(text="Information Provided and Processed by Kuvira (@archfiends)")
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="⭐⭐⭐ 3 Stars", style=discord.ButtonStyle.primary)
    async def three_star_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show 3 star information."""
        embed = discord.Embed(
            title="⭐⭐⭐ 3 Stars (Level 30)",
            description="Information for 3 star rankup",
            color=discord.Color.orange()
        )
        
        embed.add_field(
            name="Cost Breakdown",
            value="**20 shards** - Complete 3 stars\n**20-30 shards** - Partial stars (20,20,20,30)",
            inline=False
        )
        
        embed.add_field(
            name="Total Shards Used",
            value="**154 shards** (10 unlock + 18 for 1 star + 36 for 2 stars + 90 for 3 stars)",
            inline=False
        )
        
        embed.set_footer(text="Information Provided and Processed by Kuvira (@archfiends)")
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="⭐⭐⭐⭐ 4 Stars", style=discord.ButtonStyle.primary)
    async def four_star_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show 4 star information."""
        embed = discord.Embed(
            title="⭐⭐⭐⭐ 4 Stars (Level 40)",
            description="Information for 4 star rankup",
            color=discord.Color.red()
        )
        
        embed.add_field(
            name="Cost Breakdown",
            value="**50 shards** - Complete 4 stars\n**50-60 shards** - Partial stars (50,50,50,60)",
            inline=False
        )
        
        embed.add_field(
            name="Total Shards Used",
            value="**364 shards** (10 unlock + 18 for 1 star + 36 for 2 stars + 90 for 3 stars + 210 for 4 stars)",
            inline=False
        )
        
        embed.set_footer(text="Information Provided and Processed by Kuvira (@archfiends)")
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="⭐⭐⭐⭐⭐ 5 Stars", style=discord.ButtonStyle.primary)
    async def five_star_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show 5 star information."""
        embed = discord.Embed(
            title="⭐⭐⭐⭐⭐ 5 Stars (Level 50)",
            description="Information for 5 star rankup",
            color=discord.Color.gold()
        )
        
        embed.add_field(
            name="Cost Breakdown",
            value="**80 shards** - Complete 5 stars\n**80 shards** - All partial stars (80,80,80,80)",
            inline=False
        )
        
        embed.add_field(
            name="Total Shards Used",
            value="**764 shards** (10 unlock + 18 for 1 star + 36 for 2 stars + 90 for 3 stars + 210 for 4 stars + 400 for 5 stars)",
            inline=False
        )
        
        embed.set_footer(text="Information Provided and Processed by Kuvira (@archfiends)")
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="⭐⭐⭐⭐⭐⭐ 6 Stars", style=discord.ButtonStyle.primary)
    async def six_star_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show 6 star information."""
        embed = discord.Embed(
            title="⭐⭐⭐⭐⭐⭐ 6 Stars (Level 60)",
            description="Information for 6 star rankup",
            color=discord.Color.dark_purple()
        )
        
        embed.add_field(
            name="Cost Breakdown",
            value="**120 shards** - Complete 6 stars",
            inline=False
        )
        
        embed.add_field(
            name="Total Shards Used",
            value="**884 shards** (10 unlock + 18 for 1 star + 36 for 2 stars + 90 for 3 stars + 210 for 4 stars + 400 for 5 stars + 120 for 6 stars)",
            inline=False
        )
        
        embed.set_footer(text="Information Provided and Processed by Kuvira (@archfiends)")
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="💰 Total Cost", style=discord.ButtonStyle.success)
    async def total_cost_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show total cost information."""
        embed = discord.Embed(
            title="💰 Total Hero Rankup Cost",
            description="Complete cost breakdown from unlock to 6 stars",
            color=discord.Color.dark_green()
        )
        
        embed.add_field(
            name="Cost Breakdown",
            value="🔓 **Unlock**: 10 shards\n⭐ **1 Star**: 18 shards\n⭐⭐ **2 Stars**: 36 shards\n⭐⭐⭐ **3 Stars**: 90 shards\n⭐⭐⭐⭐ **4 Stars**: 210 shards\n⭐⭐⭐⭐⭐ **5 Stars**: 400 shards\n⭐⭐⭐⭐⭐⭐ **6 Stars**: 120 shards",
            inline=False
        )
        
        embed.add_field(
            name="💰 Total Cost",
            value="**884 Spirit Shards** - Total cost from unlock to 6 stars",
            inline=False
        )
        
        embed.set_footer(text="Information Provided and Processed by Kuvira (@archfiends)")
        
        await interaction.response.edit_message(embed=embed, view=self) 