"""
Minigame: Daily command and player onboarding/verification.

This feature is a standalone minigame experience and is not affiliated with Avatar Realms Collide.
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

import discord
from discord import app_commands
from discord.ext import commands

from utils.embed_generator import EmbedGenerator


# ---------- Storage helpers ----------

MINIGAME_ROOT = Path("data") / "minigame" / "servers"


def ensure_server_storage(guild_id: int) -> Path:
    """Ensure the server directory and server.json exist; return server dir path."""
    server_dir = MINIGAME_ROOT / str(guild_id)
    players_dir = server_dir / "players"
    server_json = server_dir / "server.json"

    players_dir.mkdir(parents=True, exist_ok=True)

    if not server_json.exists():
        server_payload = {
            "guild_id": guild_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "notes": "Storage for the Minigame system (not affiliated with Avatar Realms Collide)",
            "schema_version": 1,
        }
        server_json.write_text(json.dumps(server_payload, indent=2), encoding="utf-8")

    return server_dir


def get_player_path(guild_id: int, user_id: int) -> Path:
    server_dir = ensure_server_storage(guild_id)
    return server_dir / "players" / f"{user_id}.json"


def load_player(guild_id: int, user_id: int) -> Dict[str, Any]:
    """Load or initialize a player's profile for the minigame."""
    path = get_player_path(guild_id, user_id)
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            # If corrupted, reset safely
            pass

    payload = {
        "user_id": user_id,
        "guild_id": guild_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "verified": False,
        "accepted_terms": False,
        "verified_at": None,
        "xp": 0,
        "level": 1,
        "scrolls": {"basic": 0, "epic": 0},
        "inventory": {
            "basic_hero_shards": 0,
            "epic_hero_shards": 0,
            "skill_points": 0,
        },
        "stats": {
            "daily_uses": 0,
            "last_daily_at": None,
        },
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def save_player(guild_id: int, user_id: int, data: Dict[str, Any]) -> None:
    path = get_player_path(guild_id, user_id)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


# ---------- Leveling helpers ----------

def xp_needed_for_next_level(current_level: int) -> int:
    """XP needed to go from current_level to current_level+1.

    Formula: 100 + 25 * (level - 1)^2 (gentle quadratic growth)
    """
    level_minus_one = max(0, current_level - 1)
    return 100 + 25 * (level_minus_one * level_minus_one)


def apply_xp_and_level(player: Dict[str, Any], gained_xp: int) -> Dict[str, Any]:
    player["xp"] = int(player.get("xp", 0)) + int(gained_xp)
    # Level up while we have enough XP
    leveled_up = 0
    while True:
        current_level = int(player.get("level", 1))
        needed = xp_needed_for_next_level(current_level)
        # Compute XP toward current level: we model levels based on remaining bucket, so subtract per level
        if player["xp"] >= needed:
            player["xp"] -= needed
            player["level"] = current_level + 1
            leveled_up += 1
        else:
            break

    return {"leveled_up": leveled_up, "xp_to_next": xp_needed_for_next_level(player.get("level", 1)) - player.get("xp", 0)}


# ---------- UI: Verification View ----------

class VerificationView(discord.ui.View):
    def __init__(self, guild_id: int, user_id: int):
        super().__init__(timeout=120)
        self.guild_id = guild_id
        self.user_id = user_id

    @discord.ui.button(label="I am not a bot — I Agree", style=discord.ButtonStyle.success, emoji="✅")
    async def agree(self, interaction: discord.Interaction, button: discord.ui.Button):  # type: ignore[override]
        if interaction.user is None or interaction.user.id != self.user_id:
            await interaction.response.send_message("Only the requesting user can verify this.", ephemeral=True)
            return

        player = load_player(self.guild_id, self.user_id)
        if not player.get("verified"):
            player["verified"] = True
            player["accepted_terms"] = True
            player["verified_at"] = datetime.now(timezone.utc).isoformat()
            save_player(self.guild_id, self.user_id, player)

        embed = EmbedGenerator.create_embed(
            title="Verification Complete",
            description=(
                "You have acknowledged the Anti-Bot statement.\n\n"
                "This is a separate Minigame and has no affiliation with Avatar Realms Collide.\n\n"
                "You can now run /daily to receive XP and a chance at Scrolls."
            ),
            color=discord.Color.green(),
        )
        embed = EmbedGenerator.finalize_embed(embed)

        await interaction.response.edit_message(embed=embed, view=None)


# ---------- Cog ----------


class MinigameDaily(commands.Cog):
    """Minigame system: /daily onboarding, verification, and rewards."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = getattr(bot, "logger", None)

    @app_commands.command(name="daily", description="Minigame: Verify and claim daily XP with a chance at Scrolls")
    @app_commands.checks.cooldown(1, 3.0)  # basic spam protection; not a per-day lockout
    async def daily(self, interaction: discord.Interaction):
        if interaction.guild is None:
            embed = EmbedGenerator.create_embed(
                title="Guild Only",
                description="This minigame can only be used inside a server.",
                color=discord.Color.red(),
            )
            embed = EmbedGenerator.finalize_embed(embed)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        guild_id = interaction.guild.id
        user_id = interaction.user.id if interaction.user else 0

        # Ensure storage exists
        ensure_server_storage(guild_id)
        player = load_player(guild_id, user_id)

        # If not verified, ask for verification with button
        if not player.get("verified"):
            disclaimer = (
                "⚠️ This is a community-run Minigame and is not affiliated with Avatar Realms Collide.\n\n"
                "By pressing the button below, you confirm you are not using bots or automation for this Minigame."
                " If any form of botting is detected, your Minigame Account Data may be reset."
            )

            embed = EmbedGenerator.create_embed(
                title="Minigame Verification Required",
                description=disclaimer,
                color=discord.Color.orange(),
                fields=[
                    {
                        "name": "What is this?",
                        "value": (
                            "A lightweight, opt-in Minigame: use /daily to gain 1–100 XP and sometimes receive Scrolls."
                        ),
                        "inline": False,
                    },
                    {
                        "name": "Anti-Bot Notice",
                        "value": (
                            "Use of automation is prohibited. Agreeing acknowledges that detected botting can reset your Account Data."
                        ),
                        "inline": False,
                    },
                    {
                        "name": "Affiliation",
                        "value": "This Minigame has no affiliation with Avatar Realms Collide.",
                        "inline": False,
                    },
                ],
            )
            embed = EmbedGenerator.finalize_embed(embed)

            view = VerificationView(guild_id=guild_id, user_id=user_id)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
            return

        # Enforce 24h cooldown based on stats.last_daily_at
        now = datetime.now(timezone.utc)
        last_daily_iso = player.get("stats", {}).get("last_daily_at")
        if last_daily_iso:
            try:
                last_dt = datetime.fromisoformat(last_daily_iso.replace("Z", "+00:00")).astimezone(timezone.utc)
            except Exception:
                last_dt = None
            if last_dt is not None:
                elapsed = now - last_dt
                if elapsed < timedelta(hours=24):
                    remaining = timedelta(hours=24) - elapsed
                    total_seconds = int(remaining.total_seconds())
                    if total_seconds < 0:
                        total_seconds = 0
                    hours = total_seconds // 3600
                    minutes = (total_seconds % 3600) // 60
                    seconds = total_seconds % 60
                    time_left = f"{hours}h {minutes:02d}m {seconds:02d}s"
                    cooldown_embed = EmbedGenerator.create_embed(
                        title="Daily Cooldown",
                        description=f"You can claim your daily again in {time_left}.",
                        color=discord.Color.orange(),
                    )
                    cooldown_embed = EmbedGenerator.finalize_embed(cooldown_embed)
                    await interaction.response.send_message(embed=cooldown_embed, ephemeral=True)
                    return

        # Already verified: grant XP and roll for scrolls
        gained_xp = random.randint(1, 100)
        level_result = apply_xp_and_level(player, gained_xp)

        # Scroll rolls: 35% Basic, 15% Epic (independent)
        basic_drop = random.random() < 0.35
        epic_drop = random.random() < 0.15
        if basic_drop:
            player.setdefault("scrolls", {}).setdefault("basic", 0)
            player["scrolls"]["basic"] += 1
        if epic_drop:
            player.setdefault("scrolls", {}).setdefault("epic", 0)
            player["scrolls"]["epic"] += 1

        # Update stats
        stats = player.setdefault("stats", {})
        stats["daily_uses"] = int(stats.get("daily_uses", 0)) + 1
        stats["last_daily_at"] = datetime.now(timezone.utc).isoformat()

        save_player(guild_id, user_id, player)

        # Build result embed
        level_text = (
            f"Level {player.get('level', 1)}"
            + (f" (+{level_result['leveled_up']} levels)" if level_result.get("leveled_up", 0) > 0 else "")
        )

        rewards_lines = [f"XP gained: **{gained_xp}**"]
        if basic_drop:
            rewards_lines.append("You received a **Basic Scroll** 📜")
        if epic_drop:
            rewards_lines.append("You received an **Epic Scroll** 🟣📜")
        if not (basic_drop or epic_drop):
            rewards_lines.append("No scrolls dropped this time — good luck next run!")

        progress_line = (
            f"XP to next level: **{max(0, level_result.get('xp_to_next', 0))}** (Next req: {xp_needed_for_next_level(player.get('level', 1))})"
        )

        embed = EmbedGenerator.create_embed(
            title="Minigame Daily Rewards",
            description=(
                "This is a standalone Minigame (not affiliated with Avatar Realms Collide)."
            ),
            color=discord.Color.green(),
            fields=[
                {"name": "Your Level", "value": level_text, "inline": True},
                {"name": "Rewards", "value": "\n".join(rewards_lines), "inline": False},
                {"name": "Progress", "value": progress_line, "inline": False},
                {
                    "name": "Inventory",
                    "value": f"Basic Scrolls: **{player['scrolls'].get('basic', 0)}**\nEpic Scrolls: **{player['scrolls'].get('epic', 0)}**",
                    "inline": True,
                },
            ],
        )
        embed = EmbedGenerator.finalize_embed(embed)

        if interaction.response.is_done():
            await interaction.followup.send(embed=embed)
        else:
            await interaction.response.send_message(embed=embed)


    # ---------- /play command and interactive game loop ----------

    def build_play_embed(self, player: Dict[str, Any]) -> discord.Embed:
        level = int(player.get("level", 1))
        current_xp = int(player.get("xp", 0))
        max_xp = xp_needed_for_next_level(level)
        scrolls = player.get("scrolls", {})
        inv = player.get("inventory", {})

        fields = [
            {"name": "Your Level", "value": f"Level {level}", "inline": True},
            {"name": "XP", "value": f"{current_xp} / {max_xp}", "inline": True},
            {
                "name": "Scrolls",
                "value": f"Basic: **{scrolls.get('basic', 0)}**\nEpic: **{scrolls.get('epic', 0)}**",
                "inline": True,
            },
            {
                "name": "Inventory",
                "value": (
                    f"Basic Hero Shards: **{inv.get('basic_hero_shards', 0)}**\n"
                    f"Epic Hero Shards: **{inv.get('epic_hero_shards', 0)}**\n"
                    f"Skill Points: **{inv.get('skill_points', 0)}**"
                ),
                "inline": False,
            },
        ]

        embed = EmbedGenerator.create_embed(
            title="Minigame — Play",
            description="Use your scrolls to roll rewards. This is a standalone Minigame (not affiliated with Avatar Realms Collide).",
            color=discord.Color.blurple(),
            fields=fields,
        )
        return EmbedGenerator.finalize_embed(embed)

    class PlayView(discord.ui.View):
        def __init__(self, parent: "MinigameDaily", guild_id: int, user_id: int):
            super().__init__(timeout=300)
            self.parent = parent
            self.guild_id = guild_id
            self.user_id = user_id

        async def interaction_guard(self, interaction: discord.Interaction) -> bool:
            if interaction.user is None or interaction.user.id != self.user_id:
                await interaction.response.send_message("Only the requesting player can use these controls.", ephemeral=True)
                return False
            return True

        @discord.ui.button(label="Roll", style=discord.ButtonStyle.success, emoji="🎲")
        async def roll(self, interaction: discord.Interaction, button: discord.ui.Button):  # type: ignore[override]
            if not await self.interaction_guard(interaction):
                return
            # Show scroll choice view
            player = load_player(self.guild_id, self.user_id)
            choice_embed = EmbedGenerator.create_embed(
                title="Choose Scroll to Roll",
                description="Pick which scroll to use for your roll.",
                color=discord.Color.green(),
                fields=[
                    {
                        "name": "Availability",
                        "value": (
                            f"Basic: **{player.get('scrolls', {}).get('basic', 0)}**\n"
                            f"Epic: **{player.get('scrolls', {}).get('epic', 0)}**"
                        ),
                        "inline": False,
                    }
                ],
            )
            choice_embed = EmbedGenerator.finalize_embed(choice_embed)
            await interaction.response.edit_message(embed=choice_embed, view=self.parent.RollChoiceView(self.parent, self.guild_id, self.user_id))

        @discord.ui.button(label="Refresh", style=discord.ButtonStyle.secondary, emoji="🔄")
        async def refresh(self, interaction: discord.Interaction, button: discord.ui.Button):  # type: ignore[override]
            if not await self.interaction_guard(interaction):
                return
            player = load_player(self.guild_id, self.user_id)
            await interaction.response.edit_message(embed=self.parent.build_play_embed(player), view=self)

        @discord.ui.button(label="Close", style=discord.ButtonStyle.danger, emoji="🗑️")
        async def close(self, interaction: discord.Interaction, button: discord.ui.Button):  # type: ignore[override]
            if not await self.interaction_guard(interaction):
                return
            await interaction.response.edit_message(view=None)

    class RollChoiceView(discord.ui.View):
        def __init__(self, parent: "MinigameDaily", guild_id: int, user_id: int):
            super().__init__(timeout=180)
            self.parent = parent
            self.guild_id = guild_id
            self.user_id = user_id

        async def interaction_guard(self, interaction: discord.Interaction) -> bool:
            if interaction.user is None or interaction.user.id != self.user_id:
                await interaction.response.send_message("Only the requesting player can use these controls.", ephemeral=True)
                return False
            return True

        @discord.ui.button(label="Use Basic Scroll", style=discord.ButtonStyle.primary, emoji="📜")
        async def use_basic(self, interaction: discord.Interaction, button: discord.ui.Button):  # type: ignore[override]
            if not await self.interaction_guard(interaction):
                return
            player = load_player(self.guild_id, self.user_id)
            if player.get("scrolls", {}).get("basic", 0) <= 0:
                await interaction.response.send_message("You have no Basic Scrolls.", ephemeral=True)
                return

            # Consume one Basic scroll
            player["scrolls"]["basic"] = player["scrolls"].get("basic", 0) - 1

            # Rewards: one of five choices
            reward_type = random.choice(["xp", "basic3", "basic5", "epic1", "skill1"])
            reward_text: str
            if reward_type == "xp":
                gained = random.randint(100, 500)
                self.parent._apply_xp(player, gained)
                reward_text = f"Gained **{gained} XP**!"
            elif reward_type == "basic3":
                player["inventory"]["basic_hero_shards"] = player["inventory"].get("basic_hero_shards", 0) + 3
                reward_text = "Received **3 Basic Hero Shards**!"
            elif reward_type == "basic5":
                player["inventory"]["basic_hero_shards"] = player["inventory"].get("basic_hero_shards", 0) + 5
                reward_text = "Received **5 Basic Hero Shards**!"
            elif reward_type == "epic1":
                player["inventory"]["epic_hero_shards"] = player["inventory"].get("epic_hero_shards", 0) + 1
                reward_text = "Received **1 Epic Hero Shard**!"
            else:  # skill1
                player["inventory"]["skill_points"] = player["inventory"].get("skill_points", 0) + 1
                reward_text = "Received **1 Skill Point**!"

            save_player(self.guild_id, self.user_id, player)

            # Show summary and return to play view
            summary_embed = EmbedGenerator.create_embed(
                title="Roll Result (Basic)",
                description=reward_text,
                color=discord.Color.gold(),
            )
            summary_embed = EmbedGenerator.finalize_embed(summary_embed)

            view = self.parent.PlayView(self.parent, self.guild_id, self.user_id)
            await interaction.response.edit_message(embed=self.parent.build_play_embed(player), view=view)
            # Send a separate message with the reward text (public)
            await interaction.followup.send(embed=summary_embed)

        @discord.ui.button(label="Use Epic Scroll", style=discord.ButtonStyle.primary, emoji="🟣")
        async def use_epic(self, interaction: discord.Interaction, button: discord.ui.Button):  # type: ignore[override]
            if not await self.interaction_guard(interaction):
                return
            player = load_player(self.guild_id, self.user_id)
            if player.get("scrolls", {}).get("epic", 0) <= 0:
                await interaction.response.send_message("You have no Epic Scrolls.", ephemeral=True)
                return

            # Placeholder: Epic rolls to be defined later
            await interaction.response.send_message("Epic Scroll rewards are coming soon!", ephemeral=True)

        @discord.ui.button(label="Back", style=discord.ButtonStyle.secondary, emoji="⬅️")
        async def back(self, interaction: discord.Interaction, button: discord.ui.Button):  # type: ignore[override]
            if not await self.interaction_guard(interaction):
                return
            player = load_player(self.guild_id, self.user_id)
            await interaction.response.edit_message(embed=self.parent.build_play_embed(player), view=self.parent.PlayView(self.parent, self.guild_id, self.user_id))

    def _apply_xp(self, player: Dict[str, Any], gained: int) -> None:
        apply_xp_and_level(player, gained)

    @app_commands.command(name="play", description="Minigame: Open the game panel to view stats and roll scrolls")
    @app_commands.checks.cooldown(1, 3.0)
    async def play(self, interaction: discord.Interaction):
        if interaction.guild is None:
            embed = EmbedGenerator.create_embed(
                title="Guild Only",
                description="This minigame can only be used inside a server.",
                color=discord.Color.red(),
            )
            embed = EmbedGenerator.finalize_embed(embed)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        guild_id = interaction.guild.id
        user_id = interaction.user.id if interaction.user else 0

        ensure_server_storage(guild_id)
        player = load_player(guild_id, user_id)

        if not player.get("verified"):
            disclaimer = (
                "⚠️ This is a community-run Minigame and is not affiliated with Avatar Realms Collide.\n\n"
                "By pressing the button below, you confirm you are not using bots or automation for this Minigame."
                " If any form of botting is detected, your Minigame Account Data may be reset."
            )
            embed = EmbedGenerator.create_embed(
                title="Minigame Verification Required",
                description=disclaimer,
                color=discord.Color.orange(),
            )
            embed = EmbedGenerator.finalize_embed(embed)
            view = VerificationView(guild_id=guild_id, user_id=user_id)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
            return

        embed = self.build_play_embed(player)
        view = self.PlayView(self, guild_id, user_id)
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot: commands.Bot):
    await bot.add_cog(MinigameDaily(bot))


