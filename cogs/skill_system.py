"""
Skill System Cog - Skill tree and upgrade commands.
"""

import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional, List

from utils.embed_generator import EmbedGenerator
from utils.global_profile_manager import global_profile_manager
from utils.skill_manager import skill_manager


class SkillTreeView(discord.ui.View):
    """Interactive view for skill tree management."""
    
    def __init__(self, user_id: int, element: str):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.element = element
        self._build_buttons()
    
    def _build_buttons(self):
        """Build skill tree buttons."""
        # Clear existing buttons
        self.clear_items()
        
        # Get current skills and skill points
        skills = global_profile_manager.get_skills(self.user_id)
        resources = global_profile_manager.get_resources(self.user_id)
        skill_points = resources.get("skill_points", 0)
        
        # Create buttons for each tier
        for tier in range(1, 5):
            skill = skill_manager.get_skill(self.element, tier)
            if not skill:
                continue
            
            is_unlocked = skills.get(self.element, {}).get(f"tier_{tier}", False)
            can_unlock, _ = skill_manager.can_unlock_skill(self.element, tier, skills, skill_points)
            
            # Determine button style and emoji
            if is_unlocked:
                style = discord.ButtonStyle.success
                emoji = "✅"
                label = f"Tier {tier}: {skill.name}"
            elif can_unlock:
                style = discord.ButtonStyle.primary
                emoji = "🟢"
                label = f"Tier {tier}: {skill.name} ({skill.cost} SP)"
            else:
                style = discord.ButtonStyle.secondary
                emoji = "🔒"
                label = f"Tier {tier}: {skill.name} (Locked)"
            
            button = discord.ui.Button(
                label=label,
                emoji=emoji,
                style=style,
                custom_id=f"skill_{tier}",
                disabled=is_unlocked or not can_unlock
            )
            button.callback = self._skill_callback
            self.add_item(button)
        
        # Add refresh button
        refresh_btn = discord.ui.Button(
            label="Refresh",
            emoji="🔄",
            style=discord.ButtonStyle.secondary,
            custom_id="refresh"
        )
        refresh_btn.callback = self._refresh_callback
        self.add_item(refresh_btn)
    
    async def _skill_callback(self, interaction: discord.Interaction):
        """Handle skill button clicks."""
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your skill tree!", ephemeral=True)
            return
        
        tier = int(interaction.data["custom_id"].split("_")[1])
        
        # Sync resources from minigame first
        if interaction.guild:
            global_profile_manager.sync_resources_from_minigame(self.user_id, interaction.guild.id)
        
        success, message = global_profile_manager.unlock_skill(self.user_id, self.element, tier)
        
        if success:
            # Rebuild buttons and update embed
            self._build_buttons()
            embed = await self._create_skill_tree_embed()
            await interaction.response.edit_message(embed=embed, view=self)
            await interaction.followup.send(f"🎉 {message}", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ {message}", ephemeral=True)
    
    async def _refresh_callback(self, interaction: discord.Interaction):
        """Handle refresh button clicks."""
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your skill tree!", ephemeral=True)
            return
        
        # Sync resources from minigame first
        if interaction.guild:
            global_profile_manager.sync_resources_from_minigame(self.user_id, interaction.guild.id)
        
        self._build_buttons()
        embed = await self._create_skill_tree_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def _create_skill_tree_embed(self) -> discord.Embed:
        """Create skill tree embed."""
        skills = global_profile_manager.get_skills(self.user_id)
        resources = global_profile_manager.get_resources(self.user_id)
        skill_points = resources.get("skill_points", 0)
        
        element_skills = skill_manager.get_element_skills(self.element)
        element_emoji = skill_manager.get_element_emoji(self.element)
        
        title = f"{element_emoji} {self.element.title()} Skill Tree"
        
        # Build skill list
        skill_lines = []
        total_cost = 0
        unlocked_count = 0
        
        for tier in range(1, 5):
            skill = element_skills.get(tier)
            if not skill:
                continue
            
            is_unlocked = skills.get(self.element, {}).get(f"tier_{tier}", False)
            status_emoji = "✅" if is_unlocked else skill_manager.get_tier_emoji(tier, is_unlocked)
            
            if is_unlocked:
                unlocked_count += 1
                total_cost += skill.cost
            
            skill_lines.append(
                f"{status_emoji} **Tier {tier}: {skill.name}** ({skill.cost} SP)\n"
                f"   {skill.description}"
            )
        
        description = "\n\n".join(skill_lines)
        
        # Calculate bonuses for this element
        element_bonuses = {}
        for tier_key, is_unlocked in skills.get(self.element, {}).items():
            if is_unlocked:
                tier = int(tier_key.split("_")[1])
                skill = skill_manager.get_skill(self.element, tier)
                if skill:
                    for bonus_type, bonus_value in skill.bonuses.items():
                        element_bonuses[bonus_type] = element_bonuses.get(bonus_type, 0) + bonus_value
        
        fields = [
            {
                "name": "📊 Progress",
                "value": (
                    f"**Unlocked:** {unlocked_count}/4 skills\n"
                    f"**Cost Spent:** {total_cost} SP\n"
                    f"**Available:** {skill_points} SP"
                ),
                "inline": True
            },
            {
                "name": "🔮 Element Bonuses",
                "value": self._format_bonuses(element_bonuses),
                "inline": True
            }
        ]
        
        embed = EmbedGenerator.create_embed(
            title=title,
            description=description,
            color=discord.Color.purple(),
            fields=fields
        )
        
        return EmbedGenerator.finalize_embed(embed)
    
    def _format_bonuses(self, bonuses: dict) -> str:
        """Format bonuses for display."""
        if not bonuses or all(v == 0 for v in bonuses.values()):
            return "No bonuses from this tree"
        
        bonus_lines = []
        for bonus_type, value in bonuses.items():
            if value > 0:
                stat_name = bonus_type.replace("_bonus", "").replace("_", " ").title()
                bonus_lines.append(f"**{stat_name}:** +{value*100:.0f}%")
        
        return "\n".join(bonus_lines) if bonus_lines else "No bonuses from this tree"


class SkillElementSelectView(discord.ui.View):
    """View for selecting skill tree elements."""
    
    def __init__(self, user_id: int, command_type: str = "tree"):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.command_type = command_type
        
        # Add element selection buttons
        elements = ["fire", "water", "earth", "air"]
        for element in elements:
            emoji = skill_manager.get_element_emoji(element)
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
        
        if self.command_type == "tree":
            view = SkillTreeView(self.user_id, element)
            embed = await view._create_skill_tree_embed()
            await interaction.response.edit_message(embed=embed, view=view)
        else:
            await interaction.response.send_message(f"Selected {element}", ephemeral=True)


class SkillSystem(commands.Cog):
    """Skill tree and upgrade system."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    skills_group = app_commands.Group(name="skills", description="Skill tree management commands")
    
    @skills_group.command(name="tree", description="View and upgrade skills for a specific element")
    @app_commands.describe(element="The element skill tree to view")
    @app_commands.choices(element=[
        app_commands.Choice(name="🔥 Fire", value="fire"),
        app_commands.Choice(name="💧 Water", value="water"),
        app_commands.Choice(name="🌍 Earth", value="earth"),
        app_commands.Choice(name="💨 Air", value="air")
    ])
    async def skills_tree(self, interaction: discord.Interaction, element: Optional[str] = None):
        user_id = interaction.user.id
        
        # Sync resources from minigame first
        if interaction.guild:
            global_profile_manager.sync_resources_from_minigame(user_id, interaction.guild.id)
        
        if element:
            # Direct element specified
            view = SkillTreeView(user_id, element)
            embed = await view._create_skill_tree_embed()
            await interaction.response.send_message(embed=embed, view=view)
        else:
            # Show element selection
            embed = EmbedGenerator.create_embed(
                title="🔮 Select Skill Tree",
                description="Choose which elemental skill tree you want to view:",
                color=discord.Color.purple()
            )
            embed = EmbedGenerator.finalize_embed(embed)
            
            view = SkillElementSelectView(user_id, "tree")
            await interaction.response.send_message(embed=embed, view=view)
    
    @skills_group.command(name="overview", description="View all your skill progress across elements")
    async def skills_overview(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        
        # Sync resources from minigame first
        if interaction.guild:
            global_profile_manager.sync_resources_from_minigame(user_id, interaction.guild.id)
        
        skills = global_profile_manager.get_skills(user_id)
        resources = global_profile_manager.get_resources(user_id)
        skill_points = resources.get("skill_points", 0)
        
        # Get progress for each element
        element_progress = []
        total_unlocked = 0
        total_spent = 0
        
        for element in ["fire", "water", "earth", "air"]:
            emoji = skill_manager.get_element_emoji(element)
            element_skills = skills.get(element, {})
            unlocked = sum(1 for unlocked in element_skills.values() if unlocked)
            
            # Calculate spent skill points for this element
            spent = 0
            for tier_key, is_unlocked in element_skills.items():
                if is_unlocked:
                    tier = int(tier_key.split("_")[1])
                    skill = skill_manager.get_skill(element, tier)
                    if skill:
                        spent += skill.cost
            
            total_unlocked += unlocked
            total_spent += spent
            
            progress_bar = "▰" * unlocked + "▱" * (4 - unlocked)
            element_progress.append(
                f"{emoji} **{element.title()}:** {unlocked}/4 skills [{progress_bar}] ({spent} SP spent)"
            )
        
        # Get total bonuses
        total_bonuses = skill_manager.calculate_total_bonuses(skills)
        
        # Get available upgrades
        available_upgrades = skill_manager.get_available_upgrades(skills, skill_points)
        
        fields = [
            {
                "name": "📊 Overall Progress",
                "value": (
                    f"**Total Skills Unlocked:** {total_unlocked}/16\n"
                    f"**Total Skill Points Spent:** {total_spent}\n"
                    f"**Available Skill Points:** {skill_points}"
                ),
                "inline": False
            },
            {
                "name": "🌟 Element Progress",
                "value": "\n".join(element_progress),
                "inline": False
            },
            {
                "name": "🔮 Total Active Bonuses",
                "value": self._format_bonuses(total_bonuses),
                "inline": False
            }
        ]
        
        if available_upgrades:
            upgrade_list = []
            for upgrade in available_upgrades[:5]:  # Show top 5
                emoji = skill_manager.get_element_emoji(upgrade["element"])
                upgrade_list.append(
                    f"{emoji} {upgrade['element'].title()} Tier {upgrade['tier']}: "
                    f"{upgrade['skill'].name} ({upgrade['cost']} SP)"
                )
            
            if len(available_upgrades) > 5:
                upgrade_list.append(f"...and {len(available_upgrades) - 5} more")
            
            fields.append({
                "name": "⬆️ Available Upgrades",
                "value": "\n".join(upgrade_list),
                "inline": False
            })
        
        embed = EmbedGenerator.create_embed(
            title="🔮 Skill Tree Overview",
            description="Your complete skill progression across all elements.",
            color=discord.Color.purple(),
            fields=fields
        )
        
        await interaction.response.send_message(embed=EmbedGenerator.finalize_embed(embed))
    
    @skills_group.command(name="upgrade", description="Quickly upgrade a specific skill")
    @app_commands.describe(
        element="The element of the skill",
        tier="The tier of the skill to upgrade"
    )
    @app_commands.choices(
        element=[
            app_commands.Choice(name="🔥 Fire", value="fire"),
            app_commands.Choice(name="💧 Water", value="water"),
            app_commands.Choice(name="🌍 Earth", value="earth"),
            app_commands.Choice(name="💨 Air", value="air")
        ],
        tier=[
            app_commands.Choice(name="Tier 1", value=1),
            app_commands.Choice(name="Tier 2", value=2),
            app_commands.Choice(name="Tier 3", value=3),
            app_commands.Choice(name="Tier 4", value=4)
        ]
    )
    async def skills_upgrade(self, interaction: discord.Interaction, element: str, tier: int):
        user_id = interaction.user.id
        
        # Sync resources from minigame first
        if interaction.guild:
            global_profile_manager.sync_resources_from_minigame(user_id, interaction.guild.id)
        
        skill = skill_manager.get_skill(element, tier)
        if not skill:
            await interaction.response.send_message("❌ Invalid skill specified.", ephemeral=True)
            return
        
        # Check if can upgrade
        skills = global_profile_manager.get_skills(user_id)
        resources = global_profile_manager.get_resources(user_id)
        skill_points = resources.get("skill_points", 0)
        
        can_unlock, message = skill_manager.can_unlock_skill(element, tier, skills, skill_points)
        
        if not can_unlock:
            await interaction.response.send_message(f"❌ {message}", ephemeral=True)
            return
        
        # Create confirmation embed
        emoji = skill_manager.get_element_emoji(element)
        
        embed = EmbedGenerator.create_embed(
            title=f"🔮 Confirm Skill Upgrade",
            description=(
                f"**Skill:** {emoji} {element.title()} - {skill.name}\n"
                f"**Cost:** {skill.cost} Skill Points\n"
                f"**Effect:** {skill.description}\n\n"
                f"**Current Skill Points:** {skill_points}\n"
                f"**After Upgrade:** {skill_points - skill.cost}"
            ),
            color=discord.Color.purple()
        )
        embed = EmbedGenerator.finalize_embed(embed)
        
        # Confirmation view
        class ConfirmView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=60)
            
            @discord.ui.button(label="Confirm Upgrade", style=discord.ButtonStyle.success, emoji="✅")
            async def confirm(self, button_interaction: discord.Interaction, button: discord.ui.Button):
                if button_interaction.user.id != user_id:
                    await button_interaction.response.send_message("This is not your upgrade!", ephemeral=True)
                    return
                
                success, upgrade_message = global_profile_manager.unlock_skill(user_id, element, tier)
                
                if success:
                    await button_interaction.response.edit_message(
                        content=f"🎉 {upgrade_message}",
                        embed=None,
                        view=None
                    )
                else:
                    await button_interaction.response.edit_message(
                        content=f"❌ {upgrade_message}",
                        embed=None,
                        view=None
                    )
            
            @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary, emoji="❌")
            async def cancel(self, button_interaction: discord.Interaction, button: discord.ui.Button):
                if button_interaction.user.id != user_id:
                    await button_interaction.response.send_message("This is not your upgrade!", ephemeral=True)
                    return
                
                await button_interaction.response.edit_message(
                    content="❌ Upgrade cancelled.",
                    embed=None,
                    view=None
                )
        
        await interaction.response.send_message(embed=embed, view=ConfirmView())
    
    def _format_bonuses(self, bonuses: dict) -> str:
        """Format bonuses for display."""
        if not bonuses or all(v == 0 for v in bonuses.values()):
            return "No active skill bonuses"
        
        bonus_lines = []
        for bonus_type, value in bonuses.items():
            if value > 0:
                stat_name = bonus_type.replace("_bonus", "").replace("_", " ").title()
                bonus_lines.append(f"**{stat_name}:** +{value*100:.0f}%")
        
        return "\n".join(bonus_lines) if bonus_lines else "No active skill bonuses"


async def setup(bot: commands.Bot):
    await bot.add_cog(SkillSystem(bot))
