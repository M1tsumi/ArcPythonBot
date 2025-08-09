"""
Player System Cog - Hero upgrade and management commands.
"""

import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional, List

from utils.embed_generator import EmbedGenerator
from utils.global_profile_manager import global_profile_manager
from utils.player_manager import player_manager
from utils.skill_manager import skill_manager


class HeroUpgradeView(discord.ui.View):
    """Interactive view for hero upgrades."""
    
    def __init__(self, user_id: int, element: str):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.element = element
    
    @discord.ui.button(label="Upgrade Hero", style=discord.ButtonStyle.success, emoji="⬆️")
    async def upgrade_hero(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your upgrade panel!", ephemeral=True)
            return
        
        # Sync resources from minigame first
        if interaction.guild:
            global_profile_manager.sync_resources_from_minigame(self.user_id, interaction.guild.id)
        
        success, message = global_profile_manager.upgrade_hero(self.user_id, self.element)
        
        if success:
            # Show updated hero info
            embed = await self._create_hero_embed()
            await interaction.response.edit_message(embed=embed, view=self)
            await interaction.followup.send(f"🎉 {message}", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ {message}", ephemeral=True)
    
    @discord.ui.button(label="Refresh", style=discord.ButtonStyle.secondary, emoji="🔄")
    async def refresh(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your upgrade panel!", ephemeral=True)
            return
        
        # Sync resources from minigame first
        if interaction.guild:
            global_profile_manager.sync_resources_from_minigame(self.user_id, interaction.guild.id)
        
        embed = await self._create_hero_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def _create_hero_embed(self) -> discord.Embed:
        """Create hero information embed."""
        hero_data = global_profile_manager.ensure_hero_exists(self.user_id, self.element)
        resources = global_profile_manager.get_resources(self.user_id)
        skill_bonuses = global_profile_manager.get_skill_bonuses(self.user_id)
        
        # Calculate current stats with skill bonuses
        stats = player_manager.calculate_stats(hero_data, skill_bonuses)
        
        # Get upgrade info
        upgrade_cost = player_manager.get_upgrade_cost(hero_data)
        next_tier = player_manager.get_next_tier_info(hero_data)
        can_upgrade, upgrade_status = player_manager.can_upgrade(hero_data, resources)
        
        # Format display
        rarity = hero_data["rarity"].title()
        stars = player_manager.format_star_display(hero_data["stars"])
        element_emoji = player_manager.get_element_emoji(self.element)
        
        title = f"{element_emoji} {self.element.title()} Hero - {rarity} {stars}"
        
        fields = [
            {
                "name": "📊 Current Stats",
                "value": (
                    f"**ATK:** {stats.current_atk} (Base: {stats.base_atk})\n"
                    f"**DEF:** {stats.current_def} (Base: {stats.base_def})\n"
                    f"**HP:** {stats.current_hp} (Base: {stats.base_hp})"
                ),
                "inline": True
            },
            {
                "name": "💎 Resources",
                "value": (
                    f"**Basic Hero Shards:** {resources.get('basic_hero_shards', 0)}\n"
                    f"**Epic Hero Shards:** {resources.get('epic_hero_shards', 0)}\n"
                    f"**Skill Points:** {resources.get('skill_points', 0)}"
                ),
                "inline": True
            }
        ]
        
        if upgrade_cost and next_tier:
            next_rarity, next_stars = next_tier
            next_display = f"{next_rarity.title()} {player_manager.format_star_display(next_stars)}"
            
            fields.append({
                "name": "⬆️ Next Upgrade",
                "value": (
                    f"**To:** {next_display}\n"
                    f"**Cost:** {upgrade_cost.basic_hero_shards} Basic + {upgrade_cost.epic_hero_shards} Epic Shards\n"
                    f"**Status:** {upgrade_status}"
                ),
                "inline": False
            })
        else:
            fields.append({
                "name": "⬆️ Upgrade Status",
                "value": "🎉 **MAX LEVEL REACHED!** 🎉\nYour hero is at Legendary 6★",
                "inline": False
            })
        
        color = player_manager.get_rarity_color(hero_data["rarity"])
        
        embed = EmbedGenerator.create_embed(
            title=title,
            description=f"Manage your {self.element} hero upgrades and view stats.",
            color=discord.Color(color),
            fields=fields
        )
        
        return EmbedGenerator.finalize_embed(embed)


class ElementSelectView(discord.ui.View):
    """View for selecting elements."""
    
    def __init__(self, user_id: int, command_type: str = "hero"):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.command_type = command_type
        
        # Add element selection buttons
        elements = player_manager.get_all_elements()
        for element in elements:
            emoji = player_manager.get_element_emoji(element)
            button = discord.ui.Button(
                label=element.title(),
                emoji=emoji,
                style=discord.ButtonStyle.primary,
                custom_id=f"element_{element}"
            )
            button.callback = self._element_callback
            self.add_item(button)
    
    async def _element_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your selection panel!", ephemeral=True)
            return
        
        element = interaction.data["custom_id"].split("_")[1]
        
        if self.command_type == "hero":
            view = HeroUpgradeView(self.user_id, element)
            embed = await view._create_hero_embed()
            await interaction.response.edit_message(embed=embed, view=view)
        else:
            await interaction.response.send_message(f"Selected {element}", ephemeral=True)


class PlayerSystem(commands.Cog):
    """Player progression and hero management system."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    hero_group = app_commands.Group(name="hero", description="Hero management commands")
    
    @hero_group.command(name="upgrade", description="Upgrade your hero for a specific element")
    @app_commands.describe(element="The element of the hero to upgrade")
    @app_commands.choices(element=[
        app_commands.Choice(name="🔥 Fire", value="fire"),
        app_commands.Choice(name="💧 Water", value="water"),
        app_commands.Choice(name="🌍 Earth", value="earth"),
        app_commands.Choice(name="💨 Air", value="air")
    ])
    async def hero_upgrade(self, interaction: discord.Interaction, element: Optional[str] = None):
        user_id = interaction.user.id
        
        # Sync resources from minigame first
        if interaction.guild:
            global_profile_manager.sync_resources_from_minigame(user_id, interaction.guild.id)
        
        if element:
            # Direct element specified
            view = HeroUpgradeView(user_id, element)
            embed = await view._create_hero_embed()
            await interaction.response.send_message(embed=embed, view=view)
        else:
            # Show element selection
            embed = EmbedGenerator.create_embed(
                title="🦸 Select Hero Element",
                description="Choose which elemental hero you want to upgrade:",
                color=discord.Color.blue()
            )
            embed = EmbedGenerator.finalize_embed(embed)
            
            view = ElementSelectView(user_id, "hero")
            await interaction.response.send_message(embed=embed, view=view)
    
    @hero_group.command(name="info", description="View detailed information about your hero")
    @app_commands.describe(element="The element of the hero to view")
    @app_commands.choices(element=[
        app_commands.Choice(name="🔥 Fire", value="fire"),
        app_commands.Choice(name="💧 Water", value="water"),
        app_commands.Choice(name="🌍 Earth", value="earth"),
        app_commands.Choice(name="💨 Air", value="air")
    ])
    async def hero_info(self, interaction: discord.Interaction, element: Optional[str] = None):
        user_id = interaction.user.id
        
        if element:
            hero_data = global_profile_manager.get_hero(user_id, element)
            if not hero_data:
                global_profile_manager.ensure_hero_exists(user_id, element)
                hero_data = global_profile_manager.get_hero(user_id, element)
            
            skill_bonuses = global_profile_manager.get_skill_bonuses(user_id)
            stats = player_manager.calculate_stats(hero_data, skill_bonuses)
            
            # Create detailed info embed
            rarity = hero_data["rarity"].title()
            stars = player_manager.format_star_display(hero_data["stars"])
            element_emoji = player_manager.get_element_emoji(element)
            
            title = f"{element_emoji} {element.title()} Hero - {rarity} {stars}"
            
            # Calculate total star level for progression display
            total_star_level = player_manager._get_total_star_level(hero_data["rarity"], hero_data["stars"])
            max_star_level = 11  # Legendary 6★ = star level 11
            progress_bar = "▰" * total_star_level + "▱" * (max_star_level - total_star_level)
            
            fields = [
                {
                    "name": "📊 Detailed Stats",
                    "value": (
                        f"**Attack:** {stats.current_atk} (Base: {stats.base_atk})\n"
                        f"**Defense:** {stats.current_def} (Base: {stats.base_def})\n"
                        f"**Health:** {stats.current_hp} (Base: {stats.base_hp})\n"
                        f"**Level:** {hero_data.get('level', 1)}"
                    ),
                    "inline": True
                },
                {
                    "name": "⭐ Progression",
                    "value": (
                        f"**Rarity:** {rarity}\n"
                        f"**Stars:** {stars}\n"
                        f"**Total Level:** {total_star_level}/11\n"
                        f"**Progress:** {progress_bar}"
                    ),
                    "inline": True
                },
                {
                    "name": "🔮 Skill Bonuses Active",
                    "value": self._format_skill_bonuses(skill_bonuses),
                    "inline": False
                }
            ]
            
            color = player_manager.get_rarity_color(hero_data["rarity"])
            
            embed = EmbedGenerator.create_embed(
                title=title,
                description=f"Detailed information for your {element} hero.",
                color=discord.Color(color),
                fields=fields
            )
            
            await interaction.response.send_message(embed=EmbedGenerator.finalize_embed(embed))
        else:
            # Show element selection for info
            embed = EmbedGenerator.create_embed(
                title="🦸 Select Hero Element",
                description="Choose which elemental hero you want to view:",
                color=discord.Color.blue()
            )
            embed = EmbedGenerator.finalize_embed(embed)
            
            view = ElementSelectView(user_id, "info")
            await interaction.response.send_message(embed=embed, view=view)
    
    @hero_group.command(name="list", description="View all your heroes and their levels")
    async def hero_list(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        profile = global_profile_manager.load_global_profile(user_id)
        heroes = profile.get("heroes", {}).get("owned_heroes", {})
        primary_element = profile.get("heroes", {}).get("primary_element")
        
        if not heroes:
            # Create default heroes for all elements
            for element in player_manager.get_all_elements():
                global_profile_manager.ensure_hero_exists(user_id, element)
            
            # Reload profile
            profile = global_profile_manager.load_global_profile(user_id)
            heroes = profile.get("heroes", {}).get("owned_heroes", {})
            primary_element = profile.get("heroes", {}).get("primary_element")
        
        hero_list = []
        for element, hero_data in heroes.items():
            emoji = player_manager.get_element_emoji(element)
            rarity = hero_data["rarity"].title()
            stars = player_manager.format_star_display(hero_data["stars"])
            
            # Calculate current stats
            skill_bonuses = global_profile_manager.get_skill_bonuses(user_id)
            stats = player_manager.calculate_stats(hero_data, skill_bonuses)
            
            primary_marker = " 👑" if element == primary_element else ""
            
            hero_list.append(
                f"{emoji} **{element.title()}** {rarity} {stars}{primary_marker}\n"
                f"   ATK: {stats.current_atk} | DEF: {stats.current_def} | HP: {stats.current_hp}"
            )
        
        # Get resources
        resources = global_profile_manager.get_resources(user_id)
        
        embed = EmbedGenerator.create_embed(
            title="🦸 Your Hero Collection",
            description="\n\n".join(hero_list),
            color=discord.Color.gold(),
            fields=[
                {
                    "name": "💎 Resources",
                    "value": (
                        f"**Basic Hero Shards:** {resources.get('basic_hero_shards', 0)}\n"
                        f"**Epic Hero Shards:** {resources.get('epic_hero_shards', 0)}\n"
                        f"**Skill Points:** {resources.get('skill_points', 0)}"
                    ),
                    "inline": False
                },
                {
                    "name": "ℹ️ Legend",
                    "value": "👑 = Primary Hero\nUse `/hero upgrade [element]` to upgrade specific heroes",
                    "inline": False
                }
            ]
        )
        
        await interaction.response.send_message(embed=EmbedGenerator.finalize_embed(embed))
    
    @app_commands.command(name="inventory", description="View your resources and inventory")
    async def inventory(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        
        # Sync resources from minigame first
        if interaction.guild:
            global_profile_manager.sync_resources_from_minigame(user_id, interaction.guild.id)
        
        resources = global_profile_manager.get_resources(user_id)
        skills = global_profile_manager.get_skills(user_id)
        skill_progress = skill_manager.get_skill_tree_progress(skills)
        
        # Calculate total hero power
        profile = global_profile_manager.load_global_profile(user_id)
        heroes = profile.get("heroes", {}).get("owned_heroes", {})
        total_power = 0
        
        skill_bonuses = global_profile_manager.get_skill_bonuses(user_id)
        for hero_data in heroes.values():
            stats = player_manager.calculate_stats(hero_data, skill_bonuses)
            total_power += stats.current_atk + stats.current_def + stats.current_hp
        
        fields = [
            {
                "name": "💎 Resources",
                "value": (
                    f"**Basic Hero Shards:** {resources.get('basic_hero_shards', 0)}\n"
                    f"**Epic Hero Shards:** {resources.get('epic_hero_shards', 0)}\n"
                    f"**Skill Points:** {resources.get('skill_points', 0)}"
                ),
                "inline": True
            },
            {
                "name": "🔮 Skill Progress",
                "value": (
                    f"**Skills Unlocked:** {skill_progress['total_unlocked']}/{skill_progress['total_available']}\n"
                    f"**Skill Points Spent:** {skill_progress['skill_points_spent']}\n"
                    f"**Available to Spend:** {resources.get('skill_points', 0)}"
                ),
                "inline": True
            },
            {
                "name": "⚡ Total Power",
                "value": f"**Combined Hero Power:** {total_power:,}",
                "inline": False
            },
            {
                "name": "🔮 Active Skill Bonuses",
                "value": self._format_skill_bonuses(skill_bonuses),
                "inline": False
            }
        ]
        
        embed = EmbedGenerator.create_embed(
            title="🎒 Your Inventory",
            description="Current resources, skills, and progression summary.",
            color=discord.Color.purple(),
            fields=fields
        )
        
        await interaction.response.send_message(embed=EmbedGenerator.finalize_embed(embed))
    
    def _format_skill_bonuses(self, bonuses: dict) -> str:
        """Format skill bonuses for display."""
        if not bonuses or all(v == 0 for v in bonuses.values()):
            return "No skill bonuses active"
        
        bonus_lines = []
        for bonus_type, value in bonuses.items():
            if value > 0:
                stat_name = bonus_type.replace("_bonus", "").replace("_", " ").title()
                bonus_lines.append(f"**{stat_name}:** +{value*100:.0f}%")
        
        return "\n".join(bonus_lines) if bonus_lines else "No skill bonuses active"


async def setup(bot: commands.Bot):
    await bot.add_cog(PlayerSystem(bot))
