"""
Minigame: Daily command and player onboarding/verification.

This feature is a standalone minigame experience and is not affiliated with Avatar Realms Collide.
"""

from __future__ import annotations

import json
import random
import asyncio
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, Optional, List, Tuple

import discord
from discord import app_commands
from discord.ext import commands

from utils.embed_generator import EmbedGenerator


# ---------- Storage helpers ----------

MINIGAME_ROOT = Path("data") / "servers" / "minigame" / "servers"
# Resolve trivia file relative to repo root (parent of cogs/)
_BASE_DIR = Path(__file__).resolve().parents[1]
TRIVIA_FILE = _BASE_DIR / "data" / "game" / "text_data" / "trivia-questions.txt"
TRIVIA_QUESTIONS_PER_SESSION = 5
TRIVIA_XP_PER_CORRECT = 50
TRIVIA_BASIC_SCROLL_CHANCE = 0.10  # 10%
TRIVIA_EPIC_SCROLL_CHANCE = 0.05   # 5% (increased from 2%)


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
            "trivia": {
                "correct_total": 0,
                "incorrect_total": 0,
                "ace_attempts": 0,
                "sessions_played": 0,
            },
            "last_trivia_at": None,
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


# ---------- Trivia helpers ----------

def _split_blocks_by_blank_lines(text: str) -> List[List[str]]:
    blocks: List[List[str]] = []
    current: List[str] = []
    for line in text.splitlines():
        if line.strip() == "" or line.strip() == "---":
            if current:
                blocks.append(current)
                current = []
        else:
            current.append(line.rstrip())
    if current:
        blocks.append(current)
    return blocks


def parse_trivia_questions() -> List[Dict[str, Any]]:
    """Parse trivia questions from TRIVIA_FILE.

    Expected block format (per question):
      Q: <question text>
      A: <option A>
      B: <option B>
      C: <option C>
      D: <option D>
      Answer: A|B|C|D

    Alternative single-line format:
      Question|OptionA|OptionB|OptionC|OptionD|A
    """
    if not TRIVIA_FILE.exists():
        return []

    try:
        content = TRIVIA_FILE.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []

    questions: List[Dict[str, Any]] = []
    for block in _split_blocks_by_blank_lines(content):
        # Try key-value format
        q_text: Optional[str] = None
        options: Dict[str, str] = {}
        answer_letter: Optional[str] = None
        for raw in block:
            line = raw.strip()
            if line.lower().startswith("q:") or line.lower().startswith("question:"):
                q_text = line.split(":", 1)[1].strip()
            elif len(line) > 2 and line[1] == ":" and line[0].upper() in ["A", "B", "C", "D"]:
                options[line[0].upper()] = line.split(":", 1)[1].strip()
            elif line.lower().startswith("answer:"):
                ans = line.split(":", 1)[1].strip().upper()
                if ans in ["A", "B", "C", "D"]:
                    answer_letter = ans

        if q_text and len(options) == 4 and answer_letter:
            opts_in_order = [options.get("A", ""), options.get("B", ""), options.get("C", ""), options.get("D", "")]
            questions.append({
                "question": q_text,
                "options": opts_in_order,
                "answer_index": {"A": 0, "B": 1, "C": 2, "D": 3}[answer_letter],
            })
            continue

        # Try pipe format
        if len(block) == 1 and "|" in block[0]:
            parts = [p.strip() for p in block[0].split("|")]
            if len(parts) == 6:
                q_text = parts[0]
                opts_in_order = parts[1:5]
                ans_letter = parts[5].upper()
                if ans_letter in ["A", "B", "C", "D"]:
                    questions.append({
                        "question": q_text,
                        "options": opts_in_order,
                        "answer_index": {"A": 0, "B": 1, "C": 2, "D": 3}[ans_letter],
                    })
            continue

        # Try list format like:
        # Question text
        # A) Option text [✅]
        # B) Option text
        # C) Option text
        if block:
            q_text = block[0].strip()
            opt_lines = [ln.strip() for ln in block[1:] if ln.strip()]
            # Gather options in order A-D if present
            option_map: Dict[str, Tuple[str, bool]] = {}
            for ln in opt_lines:
                if len(ln) >= 3 and ln[1] == ')' and ln[0].upper() in ['A', 'B', 'C', 'D']:
                    letter = ln[0].upper()
                    text = ln[3:].strip()
                    is_correct = '✅' in text
                    text = text.replace('✅', '').strip()
                    option_map[letter] = (text, is_correct)
            if q_text and option_map:
                ordered_letters = [ltr for ltr in ['A', 'B', 'C', 'D'] if ltr in option_map]
                options_list: List[str] = [option_map[ltr][0] for ltr in ordered_letters]
                correct_indices = [i for i, ltr in enumerate(ordered_letters) if option_map[ltr][1]]
                answer_index = correct_indices[0] if correct_indices else 0
                if len(options_list) >= 2:  # require at least 2 options
                    questions.append({
                        "question": q_text,
                        "options": options_list,
                        "answer_index": answer_index,
                    })
    return questions


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

        # Scroll rolls: 35% Basic, 20% Epic (improved rates)
        basic_drop = random.random() < 0.35
        epic_drop = random.random() < 0.20
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

        @discord.ui.button(label="Trivia", style=discord.ButtonStyle.primary, emoji="🧠")
        async def trivia(self, interaction: discord.Interaction, button: discord.ui.Button):  # type: ignore[override]
            if not await self.interaction_guard(interaction):
                return
            # Start a trivia session in-channel using ephemeral messages
            player = load_player(self.guild_id, self.user_id)
            # 1-minute cooldown per user for trivia
            now = datetime.now(timezone.utc)
            last_trivia_iso = player.get("stats", {}).get("last_trivia_at")
            if last_trivia_iso:
                try:
                    last_dt = datetime.fromisoformat(last_trivia_iso.replace("Z", "+00:00")).astimezone(timezone.utc)
                except Exception:
                    last_dt = None
                if last_dt is not None and (now - last_dt) < timedelta(minutes=1):
                    remaining = timedelta(minutes=1) - (now - last_dt)
                    secs = int(remaining.total_seconds())
                    await interaction.response.send_message(f"Trivia is on cooldown for {secs}s.", ephemeral=True)
                    return

            questions = parse_trivia_questions()
            if not questions:
                await interaction.response.send_message("No trivia questions are configured yet.", ephemeral=True)
                return

            session_questions = random.sample(questions, k=min(TRIVIA_QUESTIONS_PER_SESSION, len(questions)))
            view = self.parent._EphemeralTriviaView(self.parent, self.guild_id, self.user_id, session_questions)
            first_embed = view.build_current_embed(seconds_left=10)

            # Set cooldown timestamp at start
            stats = player.setdefault("stats", {})
            stats["last_trivia_at"] = now.isoformat()
            save_player(self.guild_id, self.user_id, player)

            await interaction.response.send_message(embed=first_embed, view=view, ephemeral=True)
            try:
                msg = await interaction.original_response()
                view.set_message(msg)
                view.start_countdown()
            except Exception:
                pass

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

            # Consume one Epic scroll
            player["scrolls"]["epic"] = player["scrolls"].get("epic", 0) - 1

            # Epic scroll rewards (better than basic)
            reward_type = random.choice(["xp_large", "basic_large", "epic_medium", "skill_multiple", "mixed"])
            reward_text: str
            if reward_type == "xp_large":
                gained = random.randint(500, 1500)
                self.parent._apply_xp(player, gained)
                reward_text = f"Gained **{gained} XP**!"
            elif reward_type == "basic_large":
                amount = random.randint(8, 15)
                player["inventory"]["basic_hero_shards"] = player["inventory"].get("basic_hero_shards", 0) + amount
                reward_text = f"Received **{amount} Basic Hero Shards**!"
            elif reward_type == "epic_medium":
                amount = random.randint(3, 8)
                player["inventory"]["epic_hero_shards"] = player["inventory"].get("epic_hero_shards", 0) + amount
                reward_text = f"Received **{amount} Epic Hero Shards**!"
            elif reward_type == "skill_multiple":
                amount = random.randint(2, 5)
                player["inventory"]["skill_points"] = player["inventory"].get("skill_points", 0) + amount
                reward_text = f"Received **{amount} Skill Points**!"
            else:  # mixed
                basic_shards = random.randint(3, 6)
                epic_shards = random.randint(1, 3)
                skill_points = random.randint(1, 2)
                player["inventory"]["basic_hero_shards"] = player["inventory"].get("basic_hero_shards", 0) + basic_shards
                player["inventory"]["epic_hero_shards"] = player["inventory"].get("epic_hero_shards", 0) + epic_shards
                player["inventory"]["skill_points"] = player["inventory"].get("skill_points", 0) + skill_points
                reward_text = f"Received **{basic_shards} Basic Shards**, **{epic_shards} Epic Shards**, and **{skill_points} Skill Points**!"

            save_player(self.guild_id, self.user_id, player)

            # Show summary and return to play view
            summary_embed = EmbedGenerator.create_embed(
                title="Roll Result (Epic)",
                description=reward_text,
                color=discord.Color.purple(),
            )
            summary_embed = EmbedGenerator.finalize_embed(summary_embed)

            view = self.parent.PlayView(self.parent, self.guild_id, self.user_id)
            await interaction.response.edit_message(embed=self.parent.build_play_embed(player), view=view)
            # Send a separate message with the reward text (public)
            await interaction.followup.send(embed=summary_embed)

        @discord.ui.button(label="Back", style=discord.ButtonStyle.secondary, emoji="⬅️")
        async def back(self, interaction: discord.Interaction, button: discord.ui.Button):  # type: ignore[override]
            if not await self.interaction_guard(interaction):
                return
            player = load_player(self.guild_id, self.user_id)
            await interaction.response.edit_message(embed=self.parent.build_play_embed(player), view=self.parent.PlayView(self.parent, self.guild_id, self.user_id))

    def _apply_xp(self, player: Dict[str, Any], gained: int) -> None:
        apply_xp_and_level(player, gained)

    @app_commands.command(name="minigame", description="Minigame: Open the game panel to view stats and roll scrolls")
    @app_commands.checks.cooldown(1, 3.0)
    async def minigame(self, interaction: discord.Interaction):
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

    # ---------- Trivia Leaderboard ----------

    # Trivia command group: /trivia leaderboard, /trivia validate
    trivia_group = app_commands.Group(name="trivia", description="Minigame Trivia commands")

    def _merge_duplicate_users(self, entries: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
        """Merge duplicate user entries by summing their stats."""
        from collections import defaultdict
        merged = defaultdict(lambda: [0, 0])  # [correct_total, sessions]
        
        for user_id, correct, sessions in entries:
            merged[user_id][0] += correct
            merged[user_id][1] += sessions
        
        return [(user_id, data[0], data[1]) for user_id, data in merged.items()]

    @trivia_group.command(name="leaderboard", description="Show trivia leaderboard (global or server)")
    @app_commands.describe(scope="Leaderboard scope")
    @app_commands.choices(scope=[
        app_commands.Choice(name="global", value="global"),
        app_commands.Choice(name="server", value="server"),
    ])
    async def trivia_leaderboard(self, interaction: discord.Interaction, scope: app_commands.Choice[str]):
        scope_value = scope.value
        if scope_value not in ("global", "server"):
            await interaction.response.send_message("Invalid scope. Use global or server.", ephemeral=True)
            return

        if interaction.guild is None and scope_value == "server":
            await interaction.response.send_message("Server leaderboard must be used in a server.", ephemeral=True)
            return

        entries: List[Tuple[int, int, int]] = []
        if scope_value == "server":
            guild_id = interaction.guild.id  # type: ignore[union-attr]
            server_dir = ensure_server_storage(guild_id)
            players_dir = server_dir / "players"
            for file in players_dir.glob("*.json"):
                try:
                    data = json.loads(file.read_text(encoding="utf-8"))
                except Exception:
                    continue
                stats = data.get("stats", {}).get("trivia", {})
                correct_total = int(stats.get("correct_total", 0))
                sessions = int(stats.get("sessions_played", 0))
                if correct_total > 0 or sessions > 0:
                    entries.append((int(data.get("user_id", 0)), correct_total, sessions))
        else:
            if not MINIGAME_ROOT.exists():
                await interaction.response.send_message("No trivia data available yet.", ephemeral=True)
                return
            for server_dir in MINIGAME_ROOT.glob("*/"):
                players_dir = server_dir / "players"
                for file in players_dir.glob("*.json"):
                    try:
                        data = json.loads(file.read_text(encoding="utf-8"))
                    except Exception:
                        continue
                    stats = data.get("stats", {}).get("trivia", {})
                    correct_total = int(stats.get("correct_total", 0))
                    sessions = int(stats.get("sessions_played", 0))
                    if correct_total > 0 or sessions > 0:
                        entries.append((int(data.get("user_id", 0)), correct_total, sessions))

        if not entries:
            await interaction.response.send_message("No trivia data available yet.", ephemeral=True)
            return

        # FIX: Merge duplicates before sorting
        entries = self._merge_duplicate_users(entries)
        entries.sort(key=lambda x: (-x[1], x[2]))
        top_entries = entries[:10]
        lines = []
        for rank, (uid, correct, sess) in enumerate(top_entries, start=1):
            user_mention = f"<@{uid}>"
            lines.append(f"**{rank}.** {user_mention} — Correct: **{correct}**, Sessions: {sess}")

        embed = EmbedGenerator.create_embed(
            title=f"Trivia Leaderboard — {scope_value.title()}",
            description="\n".join(lines),
            color=discord.Color.gold(),
        )
        embed = EmbedGenerator.finalize_embed(embed)
        await interaction.response.send_message(embed=embed)

    # Root-level alias for quick access without the /trivia group
    @app_commands.command(name="trivia_leaderboard", description="Show trivia leaderboard (global or server)")
    @app_commands.describe(scope="Leaderboard scope")
    @app_commands.choices(scope=[
        app_commands.Choice(name="global", value="global"),
        app_commands.Choice(name="server", value="server"),
    ])
    async def trivia_leaderboard_root(self, interaction: discord.Interaction, scope: app_commands.Choice[str]):
        # Reuse the same implementation as the grouped command (now with duplicates fix)
        await self.trivia_leaderboard.callback(self, interaction, scope)

    @trivia_group.command(name="validate", description="Validate trivia file and preview a question")
    async def trivia_validate(self, interaction: discord.Interaction):
        questions = parse_trivia_questions()
        count = len(questions)
        description = [
            f"Parsed questions: **{count}**",
            f"File path: `{TRIVIA_FILE}`",
            f"Exists: **{TRIVIA_FILE.exists()}**",
        ]
        if count > 0:
            q = random.choice(questions)
            opts = "\n".join([f"- {opt}" for opt in q.get("options", [])])
            description.append("\nSample Question:")
            description.append(q.get("question", ""))
            description.append("Options:\n" + opts)
        embed = EmbedGenerator.create_embed(
            title="Trivia Validation",
            description="\n".join(description),
            color=discord.Color.teal(),
        )
        embed = EmbedGenerator.finalize_embed(embed)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # Convenience top-level command for validation in case group isn't visible yet
    @app_commands.command(name="trivia_validate", description="Validate trivia file and preview a question")
    async def trivia_validate_root(self, interaction: discord.Interaction):
        await self.trivia_validate.callback(self, interaction)  # reuse same logic

    # ---------- Trivia game loop ----------

    class _EphemeralTriviaView(discord.ui.View):
        def __init__(self, parent: "MinigameDaily", guild_id: int, user_id: int, questions: List[Dict[str, Any]]):
            super().__init__(timeout=300)
            self.parent = parent
            self.guild_id = guild_id
            self.user_id = user_id
            self.questions = questions
            self.index = 0
            self.correct_count = 0
            self.incorrect_count = 0
            self.time_per_question = 10
            self.seconds_left = self.time_per_question
            self.message: Optional[discord.Message] = None
            self.countdown_task: Optional[asyncio.Task] = None
            self._awaiting_answer = True
            self._rebuild_buttons()

        def set_message(self, msg: discord.Message) -> None:
            self.message = msg

        def _option_letters(self) -> List[str]:
            return ["A", "B", "C", "D"]

        def current_question(self) -> Dict[str, Any]:
            return self.questions[self.index]

        def build_current_embed(self, *, seconds_left: Optional[int] = None) -> discord.Embed:
            q = self.current_question()
            secs = seconds_left if seconds_left is not None else self.time_per_question
            option_fields: List[Dict[str, Any]] = []
            letters = self._option_letters()
            for idx, opt_text in enumerate(q["options"]):
                letter = letters[idx] if idx < len(letters) else str(idx + 1)
                option_fields.append({"name": letter, "value": opt_text, "inline": False})
            embed = EmbedGenerator.create_embed(
                title=f"Trivia Question {self.index + 1}/{len(self.questions)} — {secs}s",
                description=q["question"],
                color=discord.Color.blue(),
                fields=option_fields,
            )
            return EmbedGenerator.finalize_embed(embed)

        def _rebuild_buttons(self) -> None:
            # Clear existing
            for item in list(self.children):
                self.remove_item(item)
            # Build buttons for current question
            q = self.current_question()
            letters = self._option_letters()
            for idx in range(len(q["options"])):
                label = letters[idx] if idx < len(letters) else str(idx + 1)
                btn = discord.ui.Button(label=label, style=discord.ButtonStyle.secondary)

                async def on_click(interaction: discord.Interaction, choice_idx: int = idx):
                    if interaction.user is None or interaction.user.id != self.user_id:
                        await interaction.response.send_message("This question is not for you.", ephemeral=True)
                        return
                    # Acknowledge quickly to avoid interaction timeout
                    try:
                        await interaction.response.defer(ephemeral=True)
                    except Exception:
                        pass
                    if not self._awaiting_answer:
                        return
                    self._awaiting_answer = False
                    # Stop countdown
                    if self.countdown_task and not self.countdown_task.done():
                        self.countdown_task.cancel()
                        try:
                            await self.countdown_task
                        except asyncio.CancelledError:
                            pass
                    is_correct = (choice_idx == self.current_question()["answer_index"])
                    if is_correct:
                        self.correct_count += 1
                    else:
                        self.incorrect_count += 1

                    # Next question or finish
                    self.index += 1
                    if self.index < len(self.questions):
                        # Reset state and show next question
                        self.seconds_left = self.time_per_question
                        self._awaiting_answer = True
                        self._rebuild_buttons()
                        try:
                            if self.message is not None:
                                await self.message.edit(embed=self.build_current_embed(seconds_left=self.seconds_left), view=self)
                        finally:
                            self.start_countdown()
                    else:
                        await self._finish_and_summarize()

                btn.callback = on_click  # type: ignore[assignment]
                self.add_item(btn)

        def start_countdown(self) -> None:
            # Cancel any existing task
            if self.countdown_task and not self.countdown_task.done():
                self.countdown_task.cancel()
            self.seconds_left = self.time_per_question
            self.countdown_task = asyncio.create_task(self._run_countdown())

        async def _run_countdown(self) -> None:
            try:
                while self.seconds_left > 0 and self._awaiting_answer:
                    if self.message is not None:
                        try:
                            await self.message.edit(embed=self.build_current_embed(seconds_left=self.seconds_left), view=self)
                        except Exception:
                            pass
                    await asyncio.sleep(1)
                    self.seconds_left -= 1
                # If still awaiting answer after countdown ends, treat as incorrect and advance
                if self._awaiting_answer:
                    self._awaiting_answer = False
                    self.incorrect_count += 1
                    self.index += 1
                    if self.index < len(self.questions):
                        self.seconds_left = self.time_per_question
                        self._awaiting_answer = True
                        self._rebuild_buttons()
                        if self.message is not None:
                            try:
                                await self.message.edit(embed=self.build_current_embed(seconds_left=self.seconds_left), view=self)
                            except Exception:
                                pass
                        self.start_countdown()
                    else:
                        await self._finish_and_summarize()
            except asyncio.CancelledError:
                # Normal on user answer
                pass

        async def _finish_and_summarize(self) -> None:
            # Stop timer if running
            if self.countdown_task and not self.countdown_task.done():
                self.countdown_task.cancel()
                try:
                    await self.countdown_task
                except asyncio.CancelledError:
                    pass
            # Update stats and rewards
            player = load_player(self.guild_id, self.user_id)
            player_stats = player.setdefault("stats", {}).setdefault("trivia", {})
            player_stats["correct_total"] = int(player_stats.get("correct_total", 0)) + self.correct_count
            player_stats["incorrect_total"] = int(player_stats.get("incorrect_total", 0)) + self.incorrect_count
            player_stats["sessions_played"] = int(player_stats.get("sessions_played", 0)) + 1
            if self.incorrect_count == 0 and self.correct_count > 0:
                player_stats["ace_attempts"] = int(player_stats.get("ace_attempts", 0)) + 1

            gained_xp = TRIVIA_XP_PER_CORRECT * self.correct_count
            level_result = apply_xp_and_level(player, gained_xp)

            drops: List[str] = []
            if random.random() < TRIVIA_BASIC_SCROLL_CHANCE:
                player.setdefault("scrolls", {}).setdefault("basic", 0)
                player["scrolls"]["basic"] += 1
                drops.append("Basic Scroll 📜")
            if random.random() < TRIVIA_EPIC_SCROLL_CHANCE:
                player.setdefault("scrolls", {}).setdefault("epic", 0)
                player["scrolls"]["epic"] += 1
                drops.append("Epic Scroll 🟣📜")

            save_player(self.guild_id, self.user_id, player)

            summary_lines = [
                f"Correct: **{self.correct_count}**",
                f"Incorrect: **{self.incorrect_count}**",
                f"XP gained: **{gained_xp}**",
            ]
            summary_lines.append("Drops: " + (", ".join(drops) if drops else "None"))
            summary = EmbedGenerator.create_embed(
                title="Trivia Results",
                description="\n".join(summary_lines),
                color=discord.Color.green(),
            )
            summary = EmbedGenerator.finalize_embed(summary)
            # Clear buttons
            for item in list(self.children):
                self.remove_item(item)
            if self.message is not None:
                try:
                    await self.message.edit(embed=summary, view=self)
                except Exception:
                    pass
            self.stop()

    async def run_trivia_session(self, dm_channel: discord.DMChannel, user: discord.User | discord.Member, guild_id: int, user_id: int):
        questions = parse_trivia_questions()
        if not questions:
            await dm_channel.send("No trivia questions are configured yet. Please ask an admin to populate 'text files/trivia-questions.txt'.")
            return

        # Choose 5 questions at random (or fewer if not enough)
        session_questions = random.sample(questions, k=min(TRIVIA_QUESTIONS_PER_SESSION, len(questions)))
        correct_count = 0
        incorrect_count = 0

        for index, q in enumerate(session_questions, start=1):
            # Build fields dynamically for available options
            option_fields: List[Dict[str, Any]] = []
            option_letters = ["A", "B", "C", "D"]
            for idx, opt_text in enumerate(q["options"]):
                letter = option_letters[idx] if idx < len(option_letters) else str(idx + 1)
                option_fields.append({"name": letter, "value": opt_text, "inline": False})

            embed = EmbedGenerator.create_embed(
                title=f"Trivia Question {index}/{len(session_questions)}",
                description=q["question"],
                color=discord.Color.blue(),
                fields=option_fields,
            )
            embed = EmbedGenerator.finalize_embed(embed)

            view = self._build_trivia_question_view(correct_index=q["answer_index"], user_id=user_id, options_count=len(q["options"]))
            await dm_channel.send(embed=embed, view=view)

            # Wait for the view to complete (button disables on answer)
            try:
                await view.wait()
            except Exception:
                pass

            if view.answer_correct is True:
                correct_count += 1
            elif view.answer_correct is False:
                incorrect_count += 1
            else:
                # If no answer, count as incorrect
                incorrect_count += 1

        # Tally results and reward
        player = load_player(guild_id, user_id)
        player_stats = player.setdefault("stats", {}).setdefault("trivia", {})
        # Maintain totals
        player_stats["correct_total"] = int(player_stats.get("correct_total", 0)) + correct_count
        player_stats["incorrect_total"] = int(player_stats.get("incorrect_total", 0)) + incorrect_count
        player_stats["sessions_played"] = int(player_stats.get("sessions_played", 0)) + 1
        if incorrect_count == 0 and correct_count > 0:
            player_stats["ace_attempts"] = int(player_stats.get("ace_attempts", 0)) + 1

        # XP: per correct
        gained_xp = TRIVIA_XP_PER_CORRECT * correct_count
        level_result = apply_xp_and_level(player, gained_xp)

        # Low-chance scroll drops
        drops: List[str] = []
        if random.random() < TRIVIA_BASIC_SCROLL_CHANCE:
            player.setdefault("scrolls", {}).setdefault("basic", 0)
            player["scrolls"]["basic"] += 1
            drops.append("Basic Scroll 📜")
        if random.random() < TRIVIA_EPIC_SCROLL_CHANCE:
            player.setdefault("scrolls", {}).setdefault("epic", 0)
            player["scrolls"]["epic"] += 1
            drops.append("Epic Scroll 🟣📜")

        # Bonus duel participation reward
        if self.correct_count >= 4:  # Near perfect score
            from utils.global_profile_manager import global_profile_manager
            duel_stats = global_profile_manager.get_duel_stats(user_id)
            if duel_stats.get("total_duels", 0) > 0:  # Has dueled before
                if random.random() < 0.1:  # 10% chance for duelists
                    player["inventory"]["skill_points"] = player["inventory"].get("skill_points", 0) + 1
                    drops.append("Bonus Skill Point (Duelist Reward) ⭐")

        save_player(guild_id, user_id, player)

        # Summary embed to DM
        summary_lines = [
            f"Correct: **{correct_count}**",
            f"Incorrect: **{incorrect_count}**",
            f"XP gained: **{gained_xp}**",
        ]
        if drops:
            summary_lines.append("Drops: " + ", ".join(drops))
        else:
            summary_lines.append("Drops: None")

        summary = EmbedGenerator.create_embed(
            title="Trivia Results",
            description="\n".join(summary_lines),
            color=discord.Color.green(),
        )
        summary = EmbedGenerator.finalize_embed(summary)
        await dm_channel.send(embed=summary)

        # Also update the original Play panel in guild with refreshed stats if desired (skipped here)

    class _TriviaQuestionView(discord.ui.View):
        def __init__(self, correct_index: int, user_id: int, options_count: int):
            super().__init__(timeout=60)
            self.correct_index = correct_index
            self.user_id = user_id
            self.answer_correct: Optional[bool] = None

            option_letters = ["A", "B", "C", "D"]

            for idx in range(options_count):
                label = option_letters[idx] if idx < len(option_letters) else str(idx + 1)
                button = discord.ui.Button(label=label, style=discord.ButtonStyle.secondary)

                async def callback(interaction: discord.Interaction, choice_idx: int = idx):
                    if interaction.user is None or interaction.user.id != self.user_id:
                        await interaction.response.send_message("This question is not for you.", ephemeral=True)
                        return
                    is_correct = (choice_idx == self.correct_index)
                    self.answer_correct = is_correct
                    for item in self.children:
                        if isinstance(item, discord.ui.Button):
                            item.disabled = True
                    if is_correct:
                        await interaction.response.edit_message(content="✅ Correct!", view=self)
                    else:
                        await interaction.response.edit_message(content="❌ Incorrect.", view=self)
                    self.stop()

                button.callback = callback  # type: ignore[assignment]
                self.add_item(button)

    def _build_trivia_question_view(self, correct_index: int, user_id: int, options_count: int) -> "MinigameDaily._TriviaQuestionView":
        return self._TriviaQuestionView(correct_index, user_id, options_count)

async def setup(bot: commands.Bot):
    # Add cog and ensure the /trivia command group is registered on the command tree
    cog = MinigameDaily(bot)
    await bot.add_cog(cog)
    try:
        # Remove any pre-existing 'trivia' command (command or group) to avoid signature mismatch
        existing = bot.tree.get_command("trivia")
        if existing is not None:
            bot.tree.remove_command("trivia")
    except Exception:
        pass
    try:
        bot.tree.add_command(cog.trivia_group)
    except Exception:
        # If already added or any issue occurs, ignore; on_ready will sync the tree
        pass


