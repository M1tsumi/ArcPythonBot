"""
Duel System Cog - PvP combat commands and battle UI.
"""

import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from datetime import datetime, timezone
from typing import Optional, Dict, Any

from utils.embed_generator import EmbedGenerator
from utils.global_profile_manager import global_profile_manager
from utils.duel_manager import duel_manager, DuelPhase
from utils.rating_system import rating_system
from utils.player_manager import player_manager


class DuelChallengeView(discord.ui.View):
    """View for duel challenge acceptance/decline."""
    
    def __init__(self, challenger_id: int, challenged_id: int, duel_state):
        super().__init__(timeout=300)
        self.challenger_id = challenger_id
        self.challenged_id = challenged_id
        self.duel_state = duel_state
        self.responded = False
    
    @discord.ui.button(label="Accept Challenge", style=discord.ButtonStyle.success, emoji="⚔️")
    async def accept_challenge(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.challenged_id:
            await interaction.response.send_message("This challenge is not for you!", ephemeral=True)
            return
        
        if self.responded:
            await interaction.response.send_message("You already responded to this challenge!", ephemeral=True)
            return
        
        self.responded = True
        
        # Show element selection for challenged player
        embed = EmbedGenerator.create_embed(
            title="🔮 Select Your Hero",
            description="Choose which elemental hero you want to use for this duel:",
            color=discord.Color.blue()
        )
        embed = EmbedGenerator.finalize_embed(embed)
        
        view = ElementSelectionView(self.challenged_id, self.duel_state, is_challenger=False)
        await interaction.response.edit_message(embed=embed, view=view)
    
    @discord.ui.button(label="Decline Challenge", style=discord.ButtonStyle.danger, emoji="❌")
    async def decline_challenge(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.challenged_id:
            await interaction.response.send_message("This challenge is not for you!", ephemeral=True)
            return
        
        if self.responded:
            await interaction.response.send_message("You already responded to this challenge!", ephemeral=True)
            return
        
        self.responded = True
        
        success, message = duel_manager.decline_challenge(self.challenged_id)
        
        embed = EmbedGenerator.create_embed(
            title="❌ Challenge Declined",
            description=f"<@{self.challenged_id}> declined the duel challenge.",
            color=discord.Color.red()
        )
        embed = EmbedGenerator.finalize_embed(embed)
        
        await interaction.response.edit_message(embed=embed, view=None)


class ElementSelectionView(discord.ui.View):
    """View for selecting hero element for duel."""
    
    def __init__(self, user_id: int, duel_state, is_challenger: bool = True):
        super().__init__(timeout=120)
        self.user_id = user_id
        self.duel_state = duel_state
        self.is_challenger = is_challenger
        
        # Add element buttons
        elements = ["fire", "water", "earth", "air"]
        for element in elements:
            emoji = duel_manager.get_element_emoji(element)
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
            await interaction.response.send_message("This is not your hero selection!", ephemeral=True)
            return
        
        element = interaction.data["custom_id"].split("_")[1]
        
        if self.is_challenger:
            # Challenger selected element, wait for challenged player
            self.duel_state.challenger_element = element
            
            embed = EmbedGenerator.create_embed(
                title="⏳ Waiting for Opponent",
                description=f"<@{self.duel_state.challenger_id}> chose {duel_manager.get_element_emoji(element)} **{element.title()}**\n\nWaiting for <@{self.duel_state.challenged_id}> to select their hero...",
                color=discord.Color.orange()
            )
            embed = EmbedGenerator.finalize_embed(embed)
            
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            # Both players selected, start battle
            success, message, accepted_duel = duel_manager.accept_challenge(self.user_id, element)
            
            if not success:
                await interaction.response.send_message(f"❌ {message}", ephemeral=True)
                return
            
            # Set up heroes for battle
            challenger_hero = global_profile_manager.ensure_hero_exists(self.duel_state.challenger_id, self.duel_state.challenger_element)
            challenged_hero = global_profile_manager.ensure_hero_exists(self.duel_state.challenged_id, element)
            
            challenger_bonuses = global_profile_manager.get_skill_bonuses(self.duel_state.challenger_id)
            challenged_bonuses = global_profile_manager.get_skill_bonuses(self.duel_state.challenged_id)
            
            # Setup the duel
            duel_id = f"{self.duel_state.challenger_id}_{self.duel_state.challenged_id}_{int(self.duel_state.created_at.timestamp())}"
            setup_duel = duel_manager.setup_duel_heroes(
                accepted_duel, challenger_hero, challenged_hero,
                challenger_bonuses, challenged_bonuses
            )
            
            # Create battle view
            battle_view = BattleView(duel_id, setup_duel)
            embed = await battle_view.create_battle_embed()
            
            await interaction.response.edit_message(embed=embed, view=battle_view)


class BattleView(discord.ui.View):
    """View for active duel battle."""
    
    def __init__(self, duel_id: str, duel_state):
        super().__init__(timeout=600)
        self.duel_id = duel_id
        self.duel_state = duel_state
        self._update_buttons()
    
    def _update_buttons(self):
        """Update button states based on current turn."""
        self.clear_items()
        
        if self.duel_state.phase != DuelPhase.BATTLE:
            return
        
        # Attack button
        attack_btn = discord.ui.Button(
            label="Attack",
            style=discord.ButtonStyle.danger,
            emoji="⚔️",
            custom_id="attack"
        )
        attack_btn.callback = self._attack_callback
        self.add_item(attack_btn)
        
        # Forfeit button
        forfeit_btn = discord.ui.Button(
            label="Forfeit",
            style=discord.ButtonStyle.secondary,
            emoji="🏳️",
            custom_id="forfeit"
        )
        forfeit_btn.callback = self._forfeit_callback
        self.add_item(forfeit_btn)
    
    async def _attack_callback(self, interaction: discord.Interaction):
        """Handle attack button click."""
        user_id = interaction.user.id
        
        if user_id not in [self.duel_state.challenger_id, self.duel_state.challenged_id]:
            await interaction.response.send_message("You are not part of this duel!", ephemeral=True)
            return
        
        if self.duel_state.turn_player_id != user_id:
            await interaction.response.send_message("It's not your turn!", ephemeral=True)
            return
        
        # Execute attack
        success, message, action = duel_manager.execute_attack(self.duel_state, user_id)
        
        if not success:
            await interaction.response.send_message(f"❌ {message}", ephemeral=True)
            return
        
        # Update battle display
        if self.duel_state.phase == DuelPhase.RESOLUTION:
            # Battle ended
            await self._handle_battle_end(interaction)
        else:
            # Continue battle
            self._update_buttons()
            embed = await self.create_battle_embed()
            
            # Add action description
            action_text = self._format_action(action)
            
            await interaction.response.edit_message(
                content=action_text,
                embed=embed,
                view=self
            )
    
    async def _forfeit_callback(self, interaction: discord.Interaction):
        """Handle forfeit button click."""
        user_id = interaction.user.id
        
        if user_id not in [self.duel_state.challenger_id, self.duel_state.challenged_id]:
            await interaction.response.send_message("You are not part of this duel!", ephemeral=True)
            return
        
        # Confirm forfeit
        embed = EmbedGenerator.create_embed(
            title="⚠️ Confirm Forfeit",
            description="Are you sure you want to forfeit this duel? This will count as a loss.",
            color=discord.Color.orange()
        )
        embed = EmbedGenerator.finalize_embed(embed)
        
        view = ForfeitConfirmView(self.duel_id, user_id, self)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    async def _handle_battle_end(self, interaction: discord.Interaction):
        """Handle the end of a battle."""
        battle_result = duel_manager.get_battle_result(self.duel_state)
        
        if not battle_result:
            await interaction.response.send_message("Error getting battle result!", ephemeral=True)
            return
        
        # Record results in global profiles
        if battle_result["result_type"].value == "victory":
            rating_changes = global_profile_manager.record_duel_result(
                battle_result["winner_id"],
                battle_result["loser_id"],
                battle_result,
                is_draw=False
            )
        else:
            # Draw
            rating_changes = global_profile_manager.record_duel_result(
                self.duel_state.challenger_id,
                self.duel_state.challenged_id,
                battle_result,
                is_draw=True
            )
        
        # Create victory embed
        embed = await self._create_victory_embed(battle_result, rating_changes)
        
        # Clean up duel
        if self.duel_id in duel_manager.active_duels:
            del duel_manager.active_duels[self.duel_id]
        
        await interaction.response.edit_message(embed=embed, view=None)
        
        # Award participation rewards
        await self._award_duel_rewards(interaction, battle_result, rating_changes)
    
    async def create_battle_embed(self) -> discord.Embed:
        """Create the battle status embed."""
        challenger = self.duel_state.challenger_hero
        challenged = self.duel_state.challenged_hero
        
        # Create HP bars
        challenger_hp_bar = self._create_hp_bar(challenger.current_hp, challenger.max_hp)
        challenged_hp_bar = self._create_hp_bar(challenged.current_hp, challenged.max_hp)
        
        # Determine whose turn it is
        current_player = "Challenger" if self.duel_state.turn_player_id == challenger.user_id else "Challenged"
        turn_emoji = "👈" if self.duel_state.turn_player_id == challenger.user_id else "👉"
        
        title = f"⚔️ Duel Battle - Turn {self.duel_state.current_turn}"
        
        fields = [
            {
                "name": f"{duel_manager.get_element_emoji(challenger.element)} Challenger <@{challenger.user_id}>",
                "value": (
                    f"**{challenger.rarity.title()} {challenger.stars}★**\n"
                    f"HP: {challenger_hp_bar} {challenger.current_hp}/{challenger.max_hp}\n"
                    f"ATK: {challenger.stats['atk']} | DEF: {challenger.stats['def']}"
                ),
                "inline": True
            },
            {
                "name": "VS",
                "value": f"{turn_emoji}\n**{current_player}'s Turn**",
                "inline": True
            },
            {
                "name": f"{duel_manager.get_element_emoji(challenged.element)} Challenged <@{challenged.user_id}>",
                "value": (
                    f"**{challenged.rarity.title()} {challenged.stars}★**\n"
                    f"HP: {challenged_hp_bar} {challenged.current_hp}/{challenged.max_hp}\n"
                    f"ATK: {challenged.stats['atk']} | DEF: {challenged.stats['def']}"
                ),
                "inline": True
            }
        ]
        
        # Add recent actions
        if self.duel_state.battle_log:
            recent_actions = []
            for action in self.duel_state.battle_log[-3:]:  # Last 3 actions
                recent_actions.append(self._format_action(action))
            
            fields.append({
                "name": "📜 Recent Actions",
                "value": "\n".join(recent_actions) if recent_actions else "Battle just started!",
                "inline": False
            })
        
        embed = EmbedGenerator.create_embed(
            title=title,
            description=f"**Current Turn:** <@{self.duel_state.turn_player_id}>\n**Turn Limit:** {self.duel_state.current_turn}/{duel_manager.combat_config['max_turns']}",
            color=discord.Color.red(),
            fields=fields
        )
        
        return EmbedGenerator.finalize_embed(embed)
    
    def _create_hp_bar(self, current_hp: int, max_hp: int) -> str:
        """Create a visual HP bar."""
        if max_hp <= 0:
            return "▱▱▱▱▱▱▱▱▱▱"
        
        hp_percentage = current_hp / max_hp
        filled_bars = int(hp_percentage * 10)
        empty_bars = 10 - filled_bars
        
        if hp_percentage > 0.6:
            bar_char = "🟩"
        elif hp_percentage > 0.3:
            bar_char = "🟨"
        else:
            bar_char = "🟥"
        
        return bar_char * filled_bars + "⬛" * empty_bars
    
    def _format_action(self, action) -> str:
        """Format a battle action for display."""
        attacker_name = f"<@{action.attacker_id}>"
        
        if action.is_miss:
            return f"💨 {attacker_name}'s attack missed!"
        
        damage_text = f"**{action.damage}** damage"
        if action.is_critical:
            damage_text = f"⚡ **CRITICAL!** {action.damage} damage"
        
        effects_text = ""
        if action.effects:
            effects_text = f" ({', '.join(action.effects)})"
        
        return f"⚔️ {attacker_name} deals {damage_text}{effects_text}"
    
    async def _create_victory_embed(self, battle_result: Dict[str, Any], rating_changes: Dict[str, Any]) -> discord.Embed:
        """Create victory/defeat embed."""
        if battle_result["result_type"].value == "draw":
            title = "🤝 Duel Ended in a Draw!"
            color = discord.Color.gold()
            description = "Both fighters fought valiantly but neither could claim victory!"
        else:
            winner_id = battle_result["winner_id"]
            title = f"🏆 <@{winner_id}> Wins the Duel!"
            color = discord.Color.green()
            description = f"Victory achieved in {battle_result['turns_taken']} turns!"
        
        fields = [
            {
                "name": "📊 Battle Summary",
                "value": (
                    f"**Turns:** {battle_result['turns_taken']}\n"
                    f"**Challenger Final HP:** {battle_result['challenger_final_hp']}\n"
                    f"**Challenged Final HP:** {battle_result['challenged_final_hp']}"
                ),
                "inline": True
            },
            {
                "name": "📈 Rating Changes",
                "value": (
                    f"<@{self.duel_state.challenger_id}>: {rating_changes['winner_rating_change']:+d} → {rating_changes['winner_new_rating']}\n"
                    f"<@{self.duel_state.challenged_id}>: {rating_changes['loser_rating_change']:+d} → {rating_changes['loser_new_rating']}"
                ),
                "inline": True
            }
        ]
        
        embed = EmbedGenerator.create_embed(
            title=title,
            description=description,
            color=color,
            fields=fields
        )
        
        return EmbedGenerator.finalize_embed(embed)
    
    async def _award_duel_rewards(self, interaction: discord.Interaction, battle_result: Dict[str, Any], rating_changes: Dict[str, Any]):
        """Award participation rewards for the duel."""
        # Award XP and resources based on participation
        if battle_result["result_type"].value == "victory":
            winner_id = battle_result["winner_id"]
            loser_id = battle_result["loser_id"]
            
            # Winner rewards
            global_profile_manager.add_resources(winner_id, "basic_hero_shards", 2)
            global_profile_manager.add_resources(winner_id, "skill_points", 1)
            
            # Loser rewards (participation)
            global_profile_manager.add_resources(loser_id, "basic_hero_shards", 1)
        else:
            # Draw rewards
            global_profile_manager.add_resources(self.duel_state.challenger_id, "basic_hero_shards", 1)
            global_profile_manager.add_resources(self.duel_state.challenged_id, "basic_hero_shards", 1)


class ForfeitConfirmView(discord.ui.View):
    """Confirmation view for forfeit."""
    
    def __init__(self, duel_id: str, user_id: int, battle_view):
        super().__init__(timeout=30)
        self.duel_id = duel_id
        self.user_id = user_id
        self.battle_view = battle_view
    
    @discord.ui.button(label="Yes, Forfeit", style=discord.ButtonStyle.danger, emoji="🏳️")
    async def confirm_forfeit(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your forfeit confirmation!", ephemeral=True)
            return
        
        success, message = duel_manager.forfeit_duel(self.duel_id, self.user_id)
        
        if success:
            # Handle forfeit as battle end
            await self.battle_view._handle_battle_end(interaction)
        else:
            await interaction.response.send_message(f"❌ {message}", ephemeral=True)
    
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary, emoji="❌")
    async def cancel_forfeit(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your forfeit confirmation!", ephemeral=True)
            return
        
        await interaction.response.edit_message(content="❌ Forfeit cancelled.", embed=None, view=None)


class DuelSystem(commands.Cog):
    """PvP duel system with rating and tournaments."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        # Cleanup expired duels on startup
        duel_manager.cleanup_expired_duels()
    
    duel_group = app_commands.Group(name="duel", description="PvP duel commands")
    
    @duel_group.command(name="challenge", description="Challenge another player to a duel")
    @app_commands.describe(
        player="The player you want to challenge",
        element="Your hero element for the duel"
    )
    @app_commands.choices(element=[
        app_commands.Choice(name="🔥 Fire", value="fire"),
        app_commands.Choice(name="💧 Water", value="water"),
        app_commands.Choice(name="🌍 Earth", value="earth"),
        app_commands.Choice(name="💨 Air", value="air")
    ])
    async def duel_challenge(self, interaction: discord.Interaction, player: discord.Member, element: str):
        if not interaction.guild:
            await interaction.response.send_message("Duels can only be used in servers!", ephemeral=True)
            return
        
        challenger_id = interaction.user.id
        challenged_id = player.id
        
        # Sync resources first
        global_profile_manager.sync_resources_from_minigame(challenger_id, interaction.guild.id)
        global_profile_manager.sync_resources_from_minigame(challenged_id, interaction.guild.id)
        
        # Create challenge
        success, message, duel_state = duel_manager.create_challenge(
            challenger_id, challenged_id, element, interaction.channel.id
        )
        
        if not success:
            await interaction.response.send_message(f"❌ {message}", ephemeral=True)
            return
        
        # Store challenger element
        duel_state.challenger_element = element
        
        # Get hero info for display
        challenger_hero = global_profile_manager.ensure_hero_exists(challenger_id, element)
        challenger_bonuses = global_profile_manager.get_skill_bonuses(challenger_id)
        challenger_stats = player_manager.calculate_stats(challenger_hero, challenger_bonuses)
        
        # Create challenge embed
        embed = EmbedGenerator.create_embed(
            title="⚔️ Duel Challenge!",
            description=f"<@{challenger_id}> challenges <@{challenged_id}> to a duel!",
            color=discord.Color.orange(),
            fields=[
                {
                    "name": f"{duel_manager.get_element_emoji(element)} Challenger's Hero",
                    "value": (
                        f"**Element:** {element.title()}\n"
                        f"**Rarity:** {challenger_hero['rarity'].title()} {player_manager.format_star_display(challenger_hero['stars'])}\n"
                        f"**Stats:** ATK {challenger_stats.current_atk} | DEF {challenger_stats.current_def} | HP {challenger_stats.current_hp}"
                    ),
                    "inline": False
                },
                {
                    "name": "⏰ Time Limit",
                    "value": "This challenge expires in 5 minutes.",
                    "inline": False
                }
            ]
        )
        embed = EmbedGenerator.finalize_embed(embed)
        
        view = DuelChallengeView(challenger_id, challenged_id, duel_state)
        await interaction.response.send_message(embed=embed, view=view)
    
    @duel_group.command(name="stats", description="View duel statistics for yourself or another player")
    @app_commands.describe(player="Player to view stats for (optional)")
    async def duel_stats(self, interaction: discord.Interaction, player: Optional[discord.Member] = None):
        target_user = player or interaction.user
        target_id = target_user.id
        
        # Sync resources if it's the current user
        if interaction.guild and target_id == interaction.user.id:
            global_profile_manager.sync_resources_from_minigame(target_id, interaction.guild.id)
        
        duel_stats = global_profile_manager.get_duel_stats(target_id)
        
        if duel_stats["total_duels"] == 0:
            embed = EmbedGenerator.create_embed(
                title="📊 Duel Statistics",
                description=f"{target_user.display_name} hasn't participated in any duels yet!",
                color=discord.Color.blue()
            )
            embed = EmbedGenerator.finalize_embed(embed)
            await interaction.response.send_message(embed=embed)
            return
        
        # Calculate additional stats
        tier = rating_system.get_tier_from_rating(duel_stats["duel_rating"])
        tier_info = rating_system.get_tier_info(tier)
        rank = global_profile_manager.get_user_duel_rank(target_id)
        
        # Format element stats
        element_lines = []
        for element, stats in duel_stats["element_stats"].items():
            total = stats["wins"] + stats["losses"] + stats["draws"]
            if total > 0:
                emoji = duel_manager.get_element_emoji(element)
                win_rate = (stats["wins"] / total) * 100 if total > 0 else 0
                element_lines.append(f"{emoji} {element.title()}: {stats['wins']}W/{stats['losses']}L/{stats['draws']}D ({win_rate:.1f}%)")
        
        fields = [
            {
                "name": "🏆 Rating & Rank",
                "value": (
                    f"**Rating:** {tier_info['icon']} {duel_stats['duel_rating']} ({tier_info['name']})\n"
                    f"**Global Rank:** #{rank if rank else 'Unranked'}\n"
                    f"**Win Rate:** {duel_stats['win_rate']:.1f}%"
                ),
                "inline": True
            },
            {
                "name": "📈 Record",
                "value": (
                    f"**Total Duels:** {duel_stats['total_duels']}\n"
                    f"**Wins:** {duel_stats['duel_wins']}\n"
                    f"**Losses:** {duel_stats['duel_losses']}\n"
                    f"**Draws:** {duel_stats['duel_draws']}"
                ),
                "inline": True
            },
            {
                "name": "🔥 Streaks",
                "value": (
                    f"**Current Streak:** {duel_stats['current_streak']}\n"
                    f"**Best Streak:** {duel_stats['best_streak']}\n"
                    f"**Favorite Element:** {duel_manager.get_element_emoji(duel_stats['favorite_element'])} {duel_stats['favorite_element'].title() if duel_stats['favorite_element'] else 'None'}"
                ),
                "inline": True
            }
        ]
        
        if element_lines:
            fields.append({
                "name": "⚡ Element Performance",
                "value": "\n".join(element_lines[:4]),  # Show first 4 elements
                "inline": False
            })
        
        embed = EmbedGenerator.create_embed(
            title=f"📊 {target_user.display_name}'s Duel Statistics",
            description=f"Rating: **{duel_stats['duel_rating']}** {tier_info['icon']}",
            color=discord.Color(tier_info['color']),
            fields=fields
        )
        
        await interaction.response.send_message(embed=EmbedGenerator.finalize_embed(embed))
    
    @duel_group.command(name="leaderboard", description="View the duel leaderboard")
    @app_commands.describe(category="Leaderboard category to display")
    @app_commands.choices(category=[
        app_commands.Choice(name="Rating", value="rating"),
        app_commands.Choice(name="Wins", value="wins"),
        app_commands.Choice(name="Win Rate", value="win_rate"),
        app_commands.Choice(name="Best Streak", value="streak")
    ])
    async def duel_leaderboard(self, interaction: discord.Interaction, category: str = "rating"):
        leaderboard = global_profile_manager.get_duel_leaderboard(limit=10, category=category)
        
        if not leaderboard:
            embed = EmbedGenerator.create_embed(
                title="🏆 Duel Leaderboard",
                description="No duel data available yet. Be the first to start dueling!",
                color=discord.Color.gold()
            )
            embed = EmbedGenerator.finalize_embed(embed)
            await interaction.response.send_message(embed=embed)
            return
        
        # Format leaderboard
        leaderboard_lines = []
        for rank, entry in enumerate(leaderboard, 1):
            user_mention = f"<@{entry['user_id']}>"
            tier_info = rating_system.get_tier_info(entry['tier'])
            
            if category == "rating":
                value = f"{entry['duel_rating']} {tier_info['icon']}"
            elif category == "wins":
                value = f"{entry['duel_wins']} wins"
            elif category == "win_rate":
                value = f"{entry['win_rate']:.1f}% ({entry['total_duels']} duels)"
            else:  # streak
                value = f"{entry['best_streak']} streak"
            
            medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"{rank}."
            leaderboard_lines.append(f"{medal} {user_mention} - {value}")
        
        embed = EmbedGenerator.create_embed(
            title=f"🏆 Duel Leaderboard - {category.replace('_', ' ').title()}",
            description="\n".join(leaderboard_lines),
            color=discord.Color.gold()
        )
        
        # Add user's rank if they're not in top 10
        if interaction.guild:
            user_rank = global_profile_manager.get_user_duel_rank(interaction.user.id, category)
            if user_rank and user_rank > 10:
                user_stats = global_profile_manager.get_duel_stats(interaction.user.id)
                embed.add_field(
                    name="Your Rank",
                    value=f"**#{user_rank}** - {user_stats['duel_rating']} rating",
                    inline=False
                )
        
        await interaction.response.send_message(embed=EmbedGenerator.finalize_embed(embed))
    
    @duel_group.command(name="cancel", description="Cancel your outgoing duel challenge")
    async def duel_cancel(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        
        # Find user's outgoing challenge
        for challenged_id, duel_state in duel_manager.pending_challenges.items():
            if duel_state.challenger_id == user_id:
                del duel_manager.pending_challenges[challenged_id]
                await interaction.response.send_message("✅ Your duel challenge has been cancelled.", ephemeral=True)
                return
        
        await interaction.response.send_message("❌ You don't have any pending challenges to cancel.", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(DuelSystem(bot))
