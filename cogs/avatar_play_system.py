"""
Enhanced Avatar Play System - Discord Components v2 Implementation
Centered around Avatar trivia with unique game modes and features.
"""

from __future__ import annotations

import json
import random
import asyncio
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, Optional, List, Tuple, Set
from collections import defaultdict

import discord
from discord import app_commands
from discord.ext import commands

from utils.embed_generator import EmbedGenerator
from utils.global_profile_manager import global_profile_manager

# ---------- Configuration ----------
PLAY_DATA_ROOT = Path("data") / "servers" / "avatar_play" / "servers"
TRIVIA_FILE = Path("data") / "game" / "text_data" / "trivia-questions.txt"

# Game Configuration
GAME_MODES = {
    "quick": {"questions": 3, "time_per_question": 8, "xp_multiplier": 1.0, "description": "Quick 3-question round"},
    "standard": {"questions": 5, "time_per_question": 10, "xp_multiplier": 1.2, "description": "Standard 5-question game"},
    "challenge": {"questions": 8, "time_per_question": 12, "xp_multiplier": 1.5, "description": "Challenging 8-question marathon"},
    "blitz": {"questions": 10, "time_per_question": 5, "xp_multiplier": 2.0, "description": "Lightning-fast 10 questions"},
    "master": {"questions": 15, "time_per_question": 15, "xp_multiplier": 3.0, "description": "Master-level 15-question test"}
}

DIFFICULTY_MODIFIERS = {
    "easy": {"xp_multiplier": 0.8, "description": "Easier questions, reduced XP"},
    "normal": {"xp_multiplier": 1.0, "description": "Standard difficulty"},
    "hard": {"xp_multiplier": 1.5, "description": "Harder questions, bonus XP"},
    "expert": {"xp_multiplier": 2.0, "description": "Expert-level challenge"}
}

# Rewards and Progression
BASE_XP_PER_CORRECT = 75
STREAK_BONUS_MULTIPLIER = 0.1  # +10% per streak
PERFECT_GAME_BONUS = 200
DAILY_BONUS_MULTIPLIER = 2.0

# Achievement thresholds
ACHIEVEMENT_THRESHOLDS = {
    "trivia_novice": 10,      # 10 correct answers
    "trivia_apprentice": 50,  # 50 correct answers
    "trivia_master": 200,     # 200 correct answers
    "trivia_grandmaster": 500,# 500 correct answers
    "streak_warrior": 5,      # 5-question streak
    "streak_legend": 10,      # 10-question streak
    "perfect_player": 3,      # 3 perfect games
    "daily_champion": 7       # 7 days in a row
}


# ---------- Data Management ----------

def ensure_play_storage(guild_id: int) -> Path:
    """Ensure the server directory and server.json exist; return server dir path."""
    server_dir = PLAY_DATA_ROOT / str(guild_id)
    players_dir = server_dir / "players"
    server_json = server_dir / "server.json"

    players_dir.mkdir(parents=True, exist_ok=True)

    if not server_json.exists():
        server_payload = {
            "guild_id": guild_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "play_system_version": "2.0",
            "schema_version": 2,
            "stats": {
                "total_games": 0,
                "total_questions": 0,
                "perfect_games": 0
            }
        }
        server_json.write_text(json.dumps(server_payload, indent=2), encoding="utf-8")

    return server_dir


def get_play_player_path(guild_id: int, user_id: int) -> Path:
    server_dir = ensure_play_storage(guild_id)
    return server_dir / "players" / f"{user_id}.json"


def load_play_player(guild_id: int, user_id: int) -> Dict[str, Any]:
    """Load or initialize a player's Avatar Play profile."""
    path = get_play_player_path(guild_id, user_id)
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            pass

    payload = {
        "user_id": user_id,
        "guild_id": guild_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "level": 1,
        "xp": 0,
        "total_xp": 0,
        "avatar_tokens": 0,
        "spirit_energy": 100,
        "stats": {
            "games_played": 0,
            "questions_answered": 0,
            "correct_answers": 0,
            "perfect_games": 0,
            "best_streak": 0,
            "current_streak": 0,
            "favorite_mode": "standard",
            "last_played": None,
            "daily_streak": 0,
            "last_daily": None
        },
        "achievements": [],
        "unlocked_modes": ["quick", "standard"],
        "custom_title": None,
        "preferred_difficulty": "normal",
        "game_history": []
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def save_play_player(guild_id: int, user_id: int, data: Dict[str, Any]) -> None:
    path = get_play_player_path(guild_id, user_id)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


# ---------- Trivia Question Parser ----------

def parse_avatar_trivia_questions() -> List[Dict[str, Any]]:
    """Parse Avatar trivia questions with enhanced categorization."""
    if not TRIVIA_FILE.exists():
        return []

    try:
        content = TRIVIA_FILE.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []

    questions: List[Dict[str, Any]] = []
    lines = content.splitlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
            
        # Try to parse question block
        if not line.endswith('?'):
            i += 1
            continue
            
        question_text = line
        options = []
        correct_answer = None
        
        # Look for options in the next few lines
        j = i + 1
        while j < len(lines) and j < i + 5:  # Max 4 options
            option_line = lines[j].strip()
            if not option_line:
                break
                
            if option_line.startswith(('A)', 'B)', 'C)', 'D)')):
                option_text = option_line[2:].strip()
                if '✅' in option_text:
                    correct_answer = len(options)
                    option_text = option_text.replace('✅', '').strip()
                options.append(option_text)
            j += 1
        
        if len(options) >= 2 and correct_answer is not None:
            # Categorize question based on content
            category = categorize_question(question_text)
            difficulty = estimate_difficulty(question_text, options)
            
            questions.append({
                "question": question_text,
                "options": options,
                "answer_index": correct_answer,
                "category": category,
                "difficulty": difficulty,
                "id": len(questions)
            })
        
        i = j

    return questions


def categorize_question(question: str) -> str:
    """Categorize question based on content."""
    question_lower = question.lower()
    
    if any(word in question_lower for word in ['aang', 'avatar', 'airbending', 'air temple']):
        return 'Avatar & Airbending'
    elif any(word in question_lower for word in ['katara', 'sokka', 'water tribe', 'waterbending']):
        return 'Water Tribe & Waterbending'
    elif any(word in question_lower for word in ['toph', 'earthbending', 'ba sing se', 'earth king']):
        return 'Earth Kingdom & Earthbending'
    elif any(word in question_lower for word in ['zuko', 'azula', 'fire nation', 'firebending', 'ozai']):
        return 'Fire Nation & Firebending'
    elif any(word in question_lower for word in ['spirit', 'avatar state', 'past life']):
        return 'Spirits & Avatar Lore'
    else:
        return 'General Knowledge'


def estimate_difficulty(question: str, options: List[str]) -> str:
    """Estimate question difficulty based on content complexity."""
    question_lower = question.lower()
    
    # Check for specific names or detailed lore
    if any(word in question_lower for word in ['specific', 'exact', 'which episode', 'season']):
        return 'expert'
    elif any(word in question_lower for word in ['master', 'technique', 'advanced']):
        return 'hard'
    elif any(word in question_lower for word in ['who', 'what', 'where', 'main character']):
        return 'easy'
    else:
        return 'normal'


# ---------- Level and XP System ----------

def calculate_level_from_xp(total_xp: int) -> int:
    """Calculate level based on total XP (exponential curve)."""
    if total_xp < 100:
        return 1
    
    level = 1
    xp_needed = 100
    current_xp = total_xp
    
    while current_xp >= xp_needed:
        current_xp -= xp_needed
        level += 1
        xp_needed = int(xp_needed * 1.15)  # 15% increase each level
        
    return level


def calculate_xp_for_level(level: int) -> int:
    """Calculate total XP needed to reach a specific level."""
    if level <= 1:
        return 0
        
    total_xp = 0
    xp_needed = 100
    
    for _ in range(2, level + 1):
        total_xp += xp_needed
        xp_needed = int(xp_needed * 1.15)
        
    return total_xp


def apply_xp_gain(player: Dict[str, Any], base_xp: int, multipliers: Dict[str, float]) -> Dict[str, Any]:
    """Apply XP gain with various multipliers and return level up info."""
    total_multiplier = 1.0
    for mult in multipliers.values():
        total_multiplier *= mult
    
    gained_xp = int(base_xp * total_multiplier)
    old_level = player.get("level", 1)
    old_total_xp = player.get("total_xp", 0)
    
    player["xp"] = player.get("xp", 0) + gained_xp
    player["total_xp"] = old_total_xp + gained_xp
    
    new_level = calculate_level_from_xp(player["total_xp"])
    levels_gained = new_level - old_level
    
    if levels_gained > 0:
        player["level"] = new_level
        # Award tokens on level up
        player["avatar_tokens"] = player.get("avatar_tokens", 0) + (levels_gained * 10)
    
    return {
        "gained_xp": gained_xp,
        "levels_gained": levels_gained,
        "new_level": new_level,
        "total_multiplier": total_multiplier
    }


# ---------- Game Session Management ----------

@dataclass
class GameSession:
    player_id: int
    guild_id: int
    mode: str
    difficulty: str
    questions: List[Dict[str, Any]]
    current_question: int
    correct_answers: int
    start_time: datetime
    streak: int
    time_per_question: int


# ---------- Enhanced Discord Components v2 UI ----------

class EnhancedPlayMainView(discord.ui.View):
    """Main enhanced play interface with Discord Components v2."""
    
    def __init__(self, cog: "AvatarPlaySystem", guild_id: int, user_id: int, player: Dict[str, Any]):
        super().__init__(timeout=300)
        self.cog = cog
        self.guild_id = guild_id
        self.user_id = user_id
        self.player = player
        
        # Setup all components
        self._setup_difficulty_selector()
        self._setup_game_mode_buttons()  
        self._setup_action_buttons()
    
    def _setup_difficulty_selector(self):
        """Setup the difficulty selection dropdown."""
        current_difficulty = self.player.get("preferred_difficulty", "normal")
        
        options = [
            discord.SelectOption(
                label="🟢 Easy", 
                value="easy", 
                description="Simpler questions • 80% XP",
                default=current_difficulty == "easy",
                emoji="🟢"
            ),
            discord.SelectOption(
                label="🟡 Normal", 
                value="normal", 
                description="Standard difficulty • 100% XP",
                default=current_difficulty == "normal",
                emoji="🟡"
            ),
            discord.SelectOption(
                label="🟠 Hard", 
                value="hard", 
                description="Challenging questions • 150% XP",
                default=current_difficulty == "hard",
                emoji="🟠"
            ),
            discord.SelectOption(
                label="🔴 Expert", 
                value="expert", 
                description="Master-level challenges • 200% XP",
                default=current_difficulty == "expert",
                emoji="🔴"
            )
        ]
        
        select = discord.ui.Select(
            placeholder=f"🎚️ Difficulty: {current_difficulty.title()}",
            options=options,
            custom_id="difficulty_select"
        )
        select.callback = self._difficulty_callback
        self.add_item(select)
    
    async def _difficulty_callback(self, interaction: discord.Interaction):
        """Handle difficulty selection."""
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This is not your game session!", ephemeral=True)
            return
        
        difficulty = interaction.data['values'][0]
        self.player["preferred_difficulty"] = difficulty
        save_play_player(self.guild_id, self.user_id, self.player)
        
        # Update the embed with new difficulty
        daily_bonus = self.cog._check_daily_bonus(self.player)
        embed = self.cog._create_main_play_embed(self.player, daily_bonus)
        
        # Update the view to reflect new difficulty
        self.clear_items()
        self._setup_difficulty_selector()
        self._setup_game_mode_buttons()
        self._setup_action_buttons()
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    def _setup_game_mode_buttons(self):
        """Setup game mode selection buttons."""
        unlocked_modes = self.player.get("unlocked_modes", ["quick", "standard"])
        
        # Row 1: Quick, Standard, Challenge
        quick_style = discord.ButtonStyle.success if "quick" in unlocked_modes else discord.ButtonStyle.secondary
        self.add_item(discord.ui.Button(
            label="Quick", 
            emoji="⚡", 
            style=quick_style,
            custom_id="mode_quick",
            disabled="quick" not in unlocked_modes
        ))
        
        standard_style = discord.ButtonStyle.primary if "standard" in unlocked_modes else discord.ButtonStyle.secondary
        self.add_item(discord.ui.Button(
            label="Standard", 
            emoji="🎯", 
            style=standard_style,
            custom_id="mode_standard",
            disabled="standard" not in unlocked_modes
        ))
        
        challenge_style = discord.ButtonStyle.danger if "challenge" in unlocked_modes else discord.ButtonStyle.secondary
        self.add_item(discord.ui.Button(
            label="Challenge", 
            emoji="🔥", 
            style=challenge_style,
            custom_id="mode_challenge",
            disabled="challenge" not in unlocked_modes
        ))
        
        # Row 2: Blitz, Master
        blitz_style = discord.ButtonStyle.success if "blitz" in unlocked_modes else discord.ButtonStyle.secondary
        self.add_item(discord.ui.Button(
            label="Blitz", 
            emoji="💨", 
            style=blitz_style,
            custom_id="mode_blitz",
            disabled="blitz" not in unlocked_modes,
            row=1
        ))
        
        master_style = discord.ButtonStyle.danger if "master" in unlocked_modes else discord.ButtonStyle.secondary
        self.add_item(discord.ui.Button(
            label="Master", 
            emoji="👑", 
            style=master_style,
            custom_id="mode_master",
            disabled="master" not in unlocked_modes,
            row=1
        ))
        
        # Add callbacks for all mode buttons
        for item in self.children:
            if isinstance(item, discord.ui.Button) and item.custom_id and item.custom_id.startswith("mode_"):
                mode = item.custom_id.replace("mode_", "")
                item.callback = self._create_mode_callback(mode)
    
    def _create_mode_callback(self, mode: str):
        """Create callback for game mode buttons."""
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message("❌ This is not your game session!", ephemeral=True)
                return
            
            difficulty = self.player.get("preferred_difficulty", "normal")
            await self.cog.start_game_session(interaction, mode, difficulty)
        
        return callback
    
    def _setup_action_buttons(self):
        """Setup action buttons (stats, leaderboard, etc)."""
        # Row 3: Action buttons
        self.add_item(discord.ui.Button(
            label="Stats", 
            emoji="📊", 
            style=discord.ButtonStyle.secondary,
            custom_id="show_stats",
            row=2
        ))
        
        self.add_item(discord.ui.Button(
            label="Leaderboard", 
            emoji="🏆", 
            style=discord.ButtonStyle.secondary,
            custom_id="show_leaderboard",
            row=2
        ))
        
        self.add_item(discord.ui.Button(
            label="Achievements", 
            emoji="🏅", 
            style=discord.ButtonStyle.secondary,
            custom_id="show_achievements",
            row=2
        ))
        
        self.add_item(discord.ui.Button(
            label="Daily Bonus", 
            emoji="🎁", 
            style=discord.ButtonStyle.success if self.cog._check_daily_bonus(self.player) else discord.ButtonStyle.secondary,
            custom_id="daily_info",
            row=2,
            disabled=not self.cog._check_daily_bonus(self.player)
        ))
        
        # Add callbacks for action buttons
        for item in self.children:
            if isinstance(item, discord.ui.Button) and item.custom_id in ["show_stats", "show_leaderboard", "show_achievements", "daily_info"]:
                if item.custom_id == "show_stats":
                    item.callback = self._stats_callback
                elif item.custom_id == "show_leaderboard":
                    item.callback = self._leaderboard_callback
                elif item.custom_id == "show_achievements":
                    item.callback = self._achievements_callback
                elif item.custom_id == "daily_info":
                    item.callback = self._daily_info_callback
    
    async def _stats_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This is not your game session!", ephemeral=True)
            return
        await self.cog.show_player_stats(interaction)
    
    async def _leaderboard_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This is not your game session!", ephemeral=True)
            return
        await self.cog.show_leaderboard(interaction)
    
    async def _achievements_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This is not your game session!", ephemeral=True)
            return
        await self.cog.show_achievements(interaction)
    
    async def _daily_info_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This is not your game session!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="🎁 Daily Bonus Active!",
            description="Your next game will give **2x XP**!\n\nDaily bonuses reset every 24 hours and help you climb the leaderboard faster!",
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    


class PlayModeSelectView(discord.ui.View):
    """Main play menu with mode selection."""
    
    def __init__(self, cog: "AvatarPlaySystem", guild_id: int, user_id: int):
        super().__init__(timeout=300)
        self.cog = cog
        self.guild_id = guild_id
        self.user_id = user_id
    
    @discord.ui.button(label="⚡ Quick Play", style=discord.ButtonStyle.success, emoji="⚡")
    async def quick_play(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your game session!", ephemeral=True)
            return
        await self.cog.start_game_session(interaction, "quick", "normal")
    
    @discord.ui.button(label="🎯 Standard", style=discord.ButtonStyle.primary, emoji="🎯")
    async def standard_play(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your game session!", ephemeral=True)
            return
        await self.cog.start_game_session(interaction, "standard", "normal")
    
    @discord.ui.button(label="🔥 Challenge", style=discord.ButtonStyle.danger, emoji="🔥")
    async def challenge_play(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your game session!", ephemeral=True)
            return
        
        player = load_play_player(self.guild_id, self.user_id)
        if "challenge" not in player.get("unlocked_modes", []):
            await interaction.response.send_message("🔒 Reach level 5 to unlock Challenge mode!", ephemeral=True)
            return
            
        await self.cog.start_game_session(interaction, "challenge", "hard")
    
    @discord.ui.select(
        placeholder="🎚️ Choose Difficulty...",
        options=[
            discord.SelectOption(label="Easy", value="easy", emoji="🟢", description="Easier questions, 80% XP"),
            discord.SelectOption(label="Normal", value="normal", emoji="🟡", description="Standard difficulty"),
            discord.SelectOption(label="Hard", value="hard", emoji="🟠", description="Harder questions, 150% XP"),
            discord.SelectOption(label="Expert", value="expert", emoji="🔴", description="Expert level, 200% XP")
        ]
    )
    async def difficulty_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your game session!", ephemeral=True)
            return
        
        player = load_play_player(self.guild_id, self.user_id)
        player["preferred_difficulty"] = select.values[0]
        save_play_player(self.guild_id, self.user_id, player)
        
        await interaction.response.send_message(f"✅ Difficulty set to **{select.values[0].title()}**", ephemeral=True)
    
    @discord.ui.button(label="📊 Stats", style=discord.ButtonStyle.secondary, emoji="📊")
    async def view_stats(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your game session!", ephemeral=True)
            return
        await self.cog.show_player_stats(interaction)
    
    @discord.ui.button(label="🏆 Leaderboard", style=discord.ButtonStyle.secondary, emoji="🏆")
    async def view_leaderboard(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your game session!", ephemeral=True)
            return
        await self.cog.show_leaderboard(interaction)


class TriviaGameView(discord.ui.View):
    """Professional interactive trivia game view with proper timer management."""
    
    def __init__(self, cog: "AvatarPlaySystem", session: GameSession):
        super().__init__(timeout=session.time_per_question + 10)  # Extra buffer for safety
        self.cog = cog
        self.session = session
        self.answered = False
        self.countdown_task = None
        self.timer_active = False
        self.start_time = asyncio.get_event_loop().time()
        
        # Cancel any existing timers for this user to prevent stacking
        self._cleanup_existing_timers()
        self.start_countdown()
    
    def _cleanup_existing_timers(self):
        """Clean up any existing timers for this user to prevent stacking."""
        user_id = self.session.player_id
        if user_id in self.cog.active_sessions:
            old_session = self.cog.active_sessions[user_id]
            # Cancel any active view timers
            if hasattr(old_session, 'view') and old_session.view and hasattr(old_session.view, 'countdown_task'):
                if old_session.view.countdown_task and not old_session.view.countdown_task.done():
                    old_session.view.countdown_task.cancel()
    
    def start_countdown(self):
        """Start the professional countdown timer with proper cleanup."""
        # Cancel any existing countdown to prevent multiple timers
        if self.countdown_task and not self.countdown_task.done():
            self.countdown_task.cancel()
        
        if not self.timer_active:
            self.timer_active = True
            self.countdown_task = asyncio.create_task(self._professional_countdown())
    
    async def _professional_countdown(self):
        """Professional countdown timer with precise timing and no stacking."""
        try:
            time_limit = self.session.time_per_question
            
            for remaining in range(time_limit, 0, -1):
                # Check if game was already answered or cancelled
                if self.answered or not self.timer_active:
                    return
                
                # Use precise timing to prevent drift
                next_update = self.start_time + (time_limit - remaining + 1)
                current_time = asyncio.get_event_loop().time()
                sleep_duration = max(0, next_update - current_time)
                
                if sleep_duration > 0:
                    await asyncio.sleep(sleep_duration)
            
            # Time's up - handle timeout only if still active
            if not self.answered and self.timer_active:
                await self._handle_timeout()
                
        except asyncio.CancelledError:
            # Timer was properly cancelled
            self.timer_active = False
        except Exception as e:
            # Log error and clean up
            if self.cog.logger:
                self.cog.logger.error(f"Timer error in trivia game: {e}")
            self.timer_active = False
    
    async def _handle_timeout(self):
        """Handle timeout scenario with proper cleanup."""
        if not self.answered:  # Double-check to prevent race conditions
            self.answered = True
            self.timer_active = False
            self.session.streak = 0
            await self.cog.process_answer(None, self.session, timeout=True)
    
    @discord.ui.button(label="A", style=discord.ButtonStyle.secondary, emoji="🇦")
    async def answer_a(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._process_answer(interaction, 0)
    
    @discord.ui.button(label="B", style=discord.ButtonStyle.secondary, emoji="🇧")
    async def answer_b(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._process_answer(interaction, 1)
    
    @discord.ui.button(label="C", style=discord.ButtonStyle.secondary, emoji="🇨")
    async def answer_c(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._process_answer(interaction, 2)
    
    @discord.ui.button(label="D", style=discord.ButtonStyle.secondary, emoji="🇩")
    async def answer_d(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._process_answer(interaction, 3)
    
    async def _process_answer(self, interaction: discord.Interaction, choice: int):
        """Process player's answer with proper timer cleanup."""
        if interaction.user.id != self.session.player_id:
            await interaction.response.send_message("This is not your game!", ephemeral=True)
            return
        
        if self.answered:
            await interaction.response.send_message("You already answered this question!", ephemeral=True)
            return
        
        # Mark as answered and stop all timers
        self.answered = True
        self.timer_active = False
        
        # Properly cancel the countdown task
        if self.countdown_task and not self.countdown_task.done():
            self.countdown_task.cancel()
        
        await self.cog.process_answer(interaction, self.session, choice)


# ---------- Main Cog ----------

class AvatarPlaySystem(commands.Cog):
    """Enhanced Avatar Play System with trivia focus."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = getattr(bot, "logger", None)
        self.active_sessions: Dict[int, GameSession] = {}
    
    # ---------- Fixed Leaderboard Logic ----------
    
    def _merge_duplicate_users(self, entries: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
        """Merge duplicate user entries by summing their stats."""
        merged = defaultdict(lambda: [0, 0])  # [correct_total, sessions]
        
        for user_id, correct, sessions in entries:
            merged[user_id][0] += correct
            merged[user_id][1] += sessions
        
        return [(user_id, data[0], data[1]) for user_id, data in merged.items()]
    
    @app_commands.command(name="map", description="🗺️ View the complete Avatar world map")
    async def map_command(self, interaction: discord.Interaction):
        """Display the Avatar world map with detailed information."""
        try:
            map_path = Path("assets/images/map/map.webp")
            
            if not map_path.exists():
                await interaction.response.send_message("❌ Map file not found!", ephemeral=True)
                return
            
            # Create detailed map embed
            embed = EmbedGenerator.create_embed(
                title="🗺️ Avatar World Map",
                description="**The Complete Avatar Universe**\n\nExplore the vast world where the Avatar's journey unfolds across two legendary series!",
                color=discord.Color.from_rgb(70, 130, 180)  # Steel blue for map
            )
            
            embed.add_field(
                name="🌍 Four Nations Overview",
                value=(
                    "🔥 **Fire Nation** - Advanced technology and military might\n"
                    "🌊 **Water Tribes** - Southern and Northern polar regions\n" 
                    "🗻 **Earth Kingdom** - Vast territories and strong defenses\n"
                    "💨 **Air Nomads** - Four temples in mountain peaks"
                ),
                inline=False
            )
            
            embed.add_field(
                name="🏙️ Key Locations",
                value=(
                    "🏛️ **Ba Sing Se** - Impenetrable Earth Kingdom capital\n"
                    "🌺 **Republic City** - Modern multicultural metropolis\n"
                    "❄️ **Northern Water Tribe** - Fortress city of ice\n"
                    "🔥 **Fire Nation Capital** - Industrial powerhouse\n"
                    "⛰️ **Air Temples** - Sacred spiritual sanctuaries"
                ),
                inline=True
            )
            
            embed.add_field(
                name="🎯 Trivia Coverage",
                value=(
                    "📍 **All Locations** included in Avatar trivia\n"
                    "🏰 **Cities, temples, and landmarks**\n"
                    "🗺️ **Geography and culture questions**\n"
                    "⚔️ **Historical battles and events**\n"
                    "👥 **Characters from every region**"
                ),
                inline=True
            )
            
            embed.add_field(
                name="🎮 Avatar Play Integration",
                value=(
                    "Use `/play` to test your knowledge of:\n"
                    "• **Regional specialties** and customs\n"
                    "• **Geographic relationships** between locations\n"
                    "• **Cultural differences** across nations\n"
                    "• **Historical significance** of landmarks"
                ),
                inline=False
            )
            
            embed.set_footer(text="🎯 Master the geography to excel in Avatar trivia! | Use /play to start your journey")
            embed = EmbedGenerator.finalize_embed(embed)
            
            # Send map with embed
            with open(map_path, 'rb') as map_file:
                discord_file = discord.File(map_file, filename="avatar_world_map.webp")
                embed.set_image(url="attachment://avatar_world_map.webp")
                await interaction.response.send_message(embed=embed, file=discord_file)
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error in map command: {e}")
            await interaction.response.send_message("❌ Error loading the map. Please try again later.", ephemeral=True)
    
    @app_commands.command(name="play", description="🎮 Enter the Avatar Trivia Arena!")
    async def play_command(self, interaction: discord.Interaction):
        """Main play command with enhanced Discord Components v2 UI."""
        if interaction.guild is None:
            await interaction.response.send_message("❌ Avatar Play can only be used in servers!", ephemeral=True)
            return
        
        guild_id = interaction.guild.id
        user_id = interaction.user.id
        
        # Load or create player
        player = load_play_player(guild_id, user_id)
        
        # Check daily bonus
        daily_bonus = self._check_daily_bonus(player)
        
        # Create main play embed with Components v2
        embed = self._create_main_play_embed(player, daily_bonus)
        view = EnhancedPlayMainView(self, guild_id, user_id, player)
        
        await interaction.response.send_message(embed=embed, view=view)
    
    def _check_daily_bonus(self, player: Dict[str, Any]) -> bool:
        """Check if player gets daily bonus."""
        now = datetime.now(timezone.utc)
        last_daily = player.get("stats", {}).get("last_daily")
        
        if not last_daily:
            return True
        
        try:
            last_dt = datetime.fromisoformat(last_daily.replace("Z", "+00:00"))
            return (now - last_dt).days >= 1
        except:
            return True
    
    def _create_main_play_embed(self, player: Dict[str, Any], daily_bonus: bool) -> discord.Embed:
        """Create the enhanced main play interface embed with Components v2 info."""
        level = player.get("level", 1)
        xp = player.get("xp", 0)
        total_xp = player.get("total_xp", 0)
        tokens = player.get("avatar_tokens", 0)
        energy = player.get("spirit_energy", 100)
        
        stats = player.get("stats", {})
        games = stats.get("games_played", 0)
        correct = stats.get("correct_answers", 0)
        streak = stats.get("best_streak", 0)
        
        # Calculate XP to next level
        next_level_xp = calculate_xp_for_level(level + 1)
        xp_progress = total_xp - calculate_xp_for_level(level)
        xp_needed = next_level_xp - total_xp
        
        current_difficulty = player.get("preferred_difficulty", "normal")
        difficulty_emoji = {"easy": "🟢", "normal": "🟡", "hard": "🟠", "expert": "🔴"}
        
        embed = EmbedGenerator.create_embed(
            title="🎮 Avatar Trivia Arena - Discord Components v2",
            description="🎯 **Interactive Avatar Universe Trivia**\nUse the buttons and dropdown below to play!",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="👤 Player Profile",
            value=f"**Level:** {level} ({xp_progress}/{xp_needed} XP)\n**Tokens:** 🪙 {tokens}\n**Energy:** {'🟢' if energy >= 70 else '🟡' if energy >= 30 else '🔴'} {energy}/100",
            inline=True
        )
        
        embed.add_field(
            name="📊 Performance Stats", 
            value=f"**Games Played:** {games}\n**Correct Answers:** {correct}\n**Best Streak:** {streak}",
            inline=True
        )
        
        embed.add_field(
            name="⚙️ Settings",
            value=f"**Difficulty:** {difficulty_emoji.get(current_difficulty, '🟡')} {current_difficulty.title()}\n**Daily Bonus:** {'🎁 Available!' if daily_bonus else '❌ Used'}",
            inline=True
        )
        
        # Game Mode Status with interactive buttons below
        unlocked = player.get("unlocked_modes", ["quick", "standard"])
        mode_status = []
        for mode_name in ["quick", "standard", "challenge", "blitz", "master"]:
            mode_data = GAME_MODES[mode_name]
            if mode_name in unlocked:
                mode_status.append(f"✅ **{mode_name.title()}** - {mode_data['description']}")
            else:
                unlock_req = self._get_mode_unlock_requirement(mode_name)
                mode_status.append(f"🔒 **{mode_name.title()}** - {unlock_req}")
        
        embed.add_field(
            name="🎮 Game Modes",
            value="\n".join(mode_status),
            inline=False
        )
        
        # Interactive guide
        embed.add_field(
            name="🎛️ How to Play",
            value="🔸 **Select Difficulty** using the dropdown above\n🔸 **Choose Game Mode** using the colorful buttons\n🔸 **View Stats/Achievements** with the action buttons\n🔸 **Answer Questions** with A/B/C/D buttons during games",
            inline=False
        )
        
        if daily_bonus:
            embed.add_field(
                name="🎁 Daily Bonus Active!",
                value="Your next game will give **2x XP**! Click the Daily Bonus button for more info.",
                inline=False
            )
        
        return EmbedGenerator.finalize_embed(embed)
    
    def _get_mode_unlock_requirement(self, mode: str) -> str:
        """Get unlock requirement text for a mode."""
        requirements = {
            "challenge": "Reach Level 5",
            "blitz": "Reach Level 10", 
            "master": "Reach Level 20 or get Trivia Master achievement"
        }
        return requirements.get(mode, "Unknown requirement")
    
    async def start_game_session(self, interaction: discord.Interaction, mode: str, difficulty: str):
        """Start a new trivia game session."""
        guild_id = interaction.guild.id
        user_id = interaction.user.id
        
        # Load questions
        questions = parse_avatar_trivia_questions()
        if not questions:
            await interaction.response.send_message("❌ No trivia questions available!", ephemeral=True)
            return
        
        # Filter by difficulty if specified
        if difficulty != "normal":
            filtered = [q for q in questions if q.get("difficulty", "normal") == difficulty]
            if filtered:
                questions = filtered
        
        # Create game session
        mode_config = GAME_MODES[mode]
        session_questions = random.sample(questions, min(mode_config["questions"], len(questions)))
        
        session = GameSession(
            player_id=user_id,
            guild_id=guild_id,
            mode=mode,
            difficulty=difficulty,
            questions=session_questions,
            current_question=0,
            correct_answers=0,
            start_time=datetime.now(timezone.utc),
            streak=0,
            time_per_question=mode_config["time_per_question"]
        )
        
        self.active_sessions[user_id] = session
        
        # Show first question
        await self._show_question(interaction, session)
    
    async def _show_question(self, interaction: discord.Interaction, session: GameSession):
        """Display current question with enhanced engaging details."""
        question_data = session.questions[session.current_question]
        question_num = session.current_question + 1
        total_questions = len(session.questions)
        
        # Dynamic colors based on progress and streaks
        if session.streak >= 5:
            color = discord.Color.gold()  # Gold for hot streak
            streak_emoji = "🔥"
        elif session.streak >= 3:
            color = discord.Color.orange()  # Orange for good streak
            streak_emoji = "⚡"
        else:
            color = discord.Color.blue()  # Blue for normal
            streak_emoji = "📝"
        
        # Enhanced title with dynamic elements
        title_parts = [f"{streak_emoji} Question {question_num}/{total_questions}"]
        if session.streak >= 3:
            title_parts.append(f"• {session.streak} STREAK!")
        
        embed = EmbedGenerator.create_embed(
            title=" ".join(title_parts),
            description=f"🎯 **{question_data['question']}**",
            color=color
        )
        
        # Enhanced options with styled formatting
        option_emojis = ["🇦", "🇧", "🇨", "🇩"]
        option_styles = ["🔸", "🔹", "🔶", "🔷"]
        
        for i, option in enumerate(question_data["options"][:4]):
            embed.add_field(
                name=f"{option_emojis[i]} Option {chr(65+i)}",
                value=f"{option_styles[i]} **{option}**",
                inline=False
            )
        
        # Dynamic progress section with achievements
        progress_value = f"🎮 **{session.mode.title()}** Mode"
        if session.streak > 0:
            progress_value += f"\n🔥 **{session.streak}** Question Streak"
        else:
            progress_value += f"\n📍 Build your streak!"
        progress_value += f"\n✅ **{session.correct_answers}**/{question_num-1} Correct"
        
        embed.add_field(
            name="📊 Performance",
            value=progress_value,
            inline=True
        )
        
        # Enhanced timer with urgency indicators
        time_emoji = "⏰" if session.time_per_question >= 20 else "⏱️" if session.time_per_question >= 10 else "⚡"
        timer_style = "⏳ Think carefully" if session.time_per_question >= 20 else "💨 Quick thinking" if session.time_per_question >= 10 else "🚀 Lightning fast"
        
        embed.add_field(
            name=f"{time_emoji} Time Challenge",
            value=f"**{session.time_per_question}** seconds\n{timer_style}",
            inline=True
        )
        
        # Enhanced category with lore elements
        category = question_data.get("category", "General")
        difficulty = question_data.get("difficulty", "normal")
        
        # Map categories to Avatar elements
        category_elements = {
            "Characters": "👥 Heroes & Villains",
            "Locations": "🗺️ Four Nations",
            "Elements": "🔥💧🗻💨 Bending Arts",
            "History": "📜 Ancient Wisdom",
            "Culture": "🏮 Traditions",
            "General": "🌟 Avatar Lore"
        }
        
        difficulty_indicators = {
            "easy": "🟢 Novice Level",
            "normal": "🟡 Adept Level", 
            "hard": "🟠 Master Level",
            "expert": "🔴 Avatar Level"
        }
        
        embed.add_field(
            name="🏷️ Challenge Details",
            value=f"{category_elements.get(category, f'🌟 {category}')}\n{difficulty_indicators.get(difficulty, f'⚪ {difficulty.title()}')}",
            inline=True
        )
        
        # Add motivational footer based on performance
        if session.streak >= 5:
            footer_text = f"🔥 ON FIRE! {session.streak} questions in a row! Keep it up, Avatar!"
        elif session.streak >= 3:
            footer_text = f"⚡ Great streak! You're {5-session.streak} away from being on fire!"
        elif session.correct_answers > 0:
            footer_text = f"💪 You've got this! {session.correct_answers} correct so far!"
        else:
            footer_text = "🎯 Every master was once a beginner. Choose wisely!"
        
        embed.set_footer(text=footer_text)
        
        # Add streak bonus indicator
        if session.streak >= 3:
            embed.add_field(
                name="🎁 Streak Bonus Active!",
                value=f"🔥 **+{session.streak}0% XP** for this question!\nKeep the streak alive for massive rewards!",
                inline=False
            )
        
        embed = EmbedGenerator.finalize_embed(embed)
        
        # Create enhanced view with session reference
        view = TriviaGameView(self, session)
        session.view = view  # Store reference for timer cleanup
        
        if interaction.response.is_done():
            await interaction.edit_original_response(embed=embed, view=view)
        else:
            await interaction.response.edit_message(embed=embed, view=view)
    
    async def process_answer(self, interaction: Optional[discord.Interaction], session: GameSession, choice: Optional[int] = None, timeout: bool = False):
        """Process player's answer and continue game."""
        question_data = session.questions[session.current_question]
        correct_answer = question_data["answer_index"]
        is_correct = choice == correct_answer if choice is not None else False
        
        # Update session stats with streak tracking
        if is_correct:
            session.correct_answers += 1
            session.streak += 1
        else:
            # Track previous streak for better feedback
            session.previous_streak = session.streak if hasattr(session, 'streak') else 0
            session.streak = 0
        
        # Show result
        if interaction:
            result_embed = self._create_answer_result_embed(question_data, choice, is_correct, timeout, session)
            await interaction.response.edit_message(embed=result_embed, view=None)
        
        # Move to next question or end game
        session.current_question += 1
        
        if session.current_question < len(session.questions):
            # Next question after a short delay
            await asyncio.sleep(2)
            if interaction:
                await self._show_question(interaction, session)
        else:
            # Game finished
            await self._finish_game(interaction, session)
    
    def _create_answer_result_embed(self, question_data: Dict[str, Any], choice: Optional[int], is_correct: bool, timeout: bool, session: GameSession) -> discord.Embed:
        """Create engaging embed showing answer result with Avatar flair."""
        # Dynamic responses based on streaks and performance
        if timeout:
            title = "⏰ Time's Up!"
            color = discord.Color.orange()
            timeout_messages = [
                "Even Avatar Aang needed time to master the elements!",
                "Like Toph in her first earthbending lesson, timing is everything!",
                "The spirits are patient, but time waits for no one!",
                "Master Iroh would say: 'Slow down and think carefully next time.'"
            ]
            description = f"🏃‍♂️ **{random.choice(timeout_messages)}**"
        elif is_correct:
            if session.streak >= 10:
                title = "🔥 LEGENDARY STREAK! ✅"
                color = discord.Color.gold()
                description = f"**🏆 AVATAR STATE ACTIVATED! {session.streak} in a row!**\n\nYou're channeling the wisdom of all past Avatars!"
            elif session.streak >= 5:
                title = "🔥 ON FIRE! ✅"
                color = discord.Color.gold()
                description = f"**⚡ {session.streak} QUESTION STREAK!**\n\nYour knowledge burns bright like the eternal flame!"
            elif session.streak >= 3:
                title = "⚡ GREAT STREAK! ✅"
                color = discord.Color.orange()
                description = f"**🌟 {session.streak} in a row!**\n\nYou're mastering the Avatar lore like a true scholar!"
            else:
                title = "✅ Correct!"
                color = discord.Color.green()
                correct_messages = [
                    "Wise choice, young Avatar!",
                    "Your knowledge shines like the Aurora Borealis!",
                    "Even Master Piandao would be impressed!",
                    "The spirits smile upon your wisdom!",
                    "Like a true Air Nomad, you found the answer!",
                    "Sharp as Sokka's strategy!",
                    "Brilliant as Katara's waterbending!"
                ]
                description = f"🎯 **{random.choice(correct_messages)}**"
        else:
            title = "❌ Incorrect"
            color = discord.Color.red()
            incorrect_messages = [
                "Even the greatest masters learn from mistakes!",
                "Like Zuko's journey, every failure teaches wisdom!",
                "The path to mastery requires practice!",
                "Uncle Iroh would say: 'Failure is only the opportunity to begin again.'",
                "Every airbender falls before they fly!",
                "Like learning to bend, knowledge takes time!",
                "The Avatar's journey has many lessons to learn!"
            ]
            description = f"📚 **{random.choice(incorrect_messages)}**"
            
            # Add streak broken message if applicable
            if hasattr(session, 'previous_streak') and session.previous_streak > 0:
                description += f"\n\n💔 Your {session.previous_streak}-question streak was broken, but you can start a new one!"
        
        embed = EmbedGenerator.create_embed(title=title, description=description, color=color)
        
        # Show correct answer
        option_letters = ["A", "B", "C", "D"]
        correct_letter = option_letters[question_data["answer_index"]]
        correct_option = question_data["options"][question_data["answer_index"]]
        
        embed.add_field(
            name="✅ Correct Answer",
            value=f"**{correct_letter}) {correct_option}**",
            inline=False
        )
        
        if choice is not None and not is_correct:
            chosen_letter = option_letters[choice] if choice < len(option_letters) else str(choice + 1)
            chosen_option = question_data["options"][choice] if choice < len(question_data["options"]) else "Invalid"
            embed.add_field(
                name="❌ Your Answer",
                value=f"**{chosen_letter}) {chosen_option}**",
                inline=False
            )
        
        # Show current streak
        if session.streak > 0:
            embed.add_field(
                name="🔥 Current Streak",
                value=f"**{session.streak}** correct in a row!",
                inline=True
            )
        
        return EmbedGenerator.finalize_embed(embed)
    
    async def _finish_game(self, interaction: Optional[discord.Interaction], session: GameSession):
        """Finish the game and award rewards."""
        # Remove from active sessions
        if session.player_id in self.active_sessions:
            del self.active_sessions[session.player_id]
        
        # Load player data
        player = load_play_player(session.guild_id, session.player_id)
        
        # Calculate performance metrics
        total_questions = len(session.questions)
        accuracy = (session.correct_answers / total_questions) * 100 if total_questions > 0 else 0
        is_perfect = session.correct_answers == total_questions
        
        # Calculate XP and rewards
        base_xp = session.correct_answers * BASE_XP_PER_CORRECT
        multipliers = {
            "mode": GAME_MODES[session.mode]["xp_multiplier"],
            "difficulty": DIFFICULTY_MODIFIERS[session.difficulty]["xp_multiplier"],
            "streak": 1 + (session.streak * STREAK_BONUS_MULTIPLIER)
        }
        
        # Daily bonus check
        daily_bonus = self._check_daily_bonus(player)
        if daily_bonus:
            multipliers["daily"] = DAILY_BONUS_MULTIPLIER
            player["stats"]["last_daily"] = datetime.now(timezone.utc).isoformat()
            player["stats"]["daily_streak"] = player["stats"].get("daily_streak", 0) + 1
        
        # Perfect game bonus
        if is_perfect and total_questions >= 3:
            base_xp += PERFECT_GAME_BONUS
        
        # Apply XP gain
        xp_result = apply_xp_gain(player, base_xp, multipliers)
        
        # Update player stats
        stats = player.setdefault("stats", {})
        stats["games_played"] = stats.get("games_played", 0) + 1
        stats["questions_answered"] = stats.get("questions_answered", 0) + total_questions
        stats["correct_answers"] = stats.get("correct_answers", 0) + session.correct_answers
        stats["best_streak"] = max(stats.get("best_streak", 0), session.streak)
        stats["last_played"] = datetime.now(timezone.utc).isoformat()
        
        if is_perfect:
            stats["perfect_games"] = stats.get("perfect_games", 0) + 1
        
        # Check for new achievements
        new_achievements = self._check_achievements(player, session, is_perfect)
        
        # Unlock new modes
        self._check_mode_unlocks(player)
        
        # Save player data
        save_play_player(session.guild_id, session.player_id, player)
        
        # Update global profile
        game_stats = {
            "games_played": 1,
            "questions_answered": total_questions,
            "correct_answers": session.correct_answers,
            "xp_gained": xp_result["total_gained"],
            "best_streak": session.streak,
            "perfect_games": 1 if is_perfect else 0
        }
        global_profile_manager.update_global_stats(session.player_id, session.guild_id, game_stats)
        
        # Create results embed
        results_embed = self._create_game_results_embed(session, xp_result, accuracy, is_perfect, new_achievements, daily_bonus)
        
        if interaction:
            await interaction.edit_original_response(embed=results_embed, view=None)
    
    def _check_achievements(self, player: Dict[str, Any], session: GameSession, is_perfect: bool) -> List[str]:
        """Check for new achievements."""
        achievements = player.get("achievements", [])
        new_achievements = []
        
        stats = player.get("stats", {})
        correct_total = stats.get("correct_answers", 0)
        perfect_games = stats.get("perfect_games", 0)
        best_streak = stats.get("best_streak", 0)
        daily_streak = stats.get("daily_streak", 0)
        
        # Check achievement thresholds
        achievement_checks = [
            ("trivia_novice", correct_total >= ACHIEVEMENT_THRESHOLDS["trivia_novice"]),
            ("trivia_apprentice", correct_total >= ACHIEVEMENT_THRESHOLDS["trivia_apprentice"]),
            ("trivia_master", correct_total >= ACHIEVEMENT_THRESHOLDS["trivia_master"]),
            ("trivia_grandmaster", correct_total >= ACHIEVEMENT_THRESHOLDS["trivia_grandmaster"]),
            ("streak_warrior", best_streak >= ACHIEVEMENT_THRESHOLDS["streak_warrior"]),
            ("streak_legend", best_streak >= ACHIEVEMENT_THRESHOLDS["streak_legend"]),
            ("perfect_player", perfect_games >= ACHIEVEMENT_THRESHOLDS["perfect_player"]),
            ("daily_champion", daily_streak >= ACHIEVEMENT_THRESHOLDS["daily_champion"])
        ]
        
        for achievement_name, condition in achievement_checks:
            if condition and achievement_name not in achievements:
                achievements.append(achievement_name)
                new_achievements.append(achievement_name)
                # Award bonus tokens for achievements
                player["avatar_tokens"] = player.get("avatar_tokens", 0) + 50
        
        player["achievements"] = achievements
        return new_achievements
    
    def _check_mode_unlocks(self, player: Dict[str, Any]):
        """Check and unlock new game modes based on level/achievements."""
        level = player.get("level", 1)
        achievements = player.get("achievements", [])
        unlocked_modes = set(player.get("unlocked_modes", ["quick", "standard"]))
        
        # Level-based unlocks
        if level >= 5:
            unlocked_modes.add("challenge")
        if level >= 10:
            unlocked_modes.add("blitz")
        if level >= 20 or "trivia_master" in achievements:
            unlocked_modes.add("master")
        
        player["unlocked_modes"] = list(unlocked_modes)
    
    def _create_game_results_embed(self, session: GameSession, xp_result: Dict[str, Any], accuracy: float, is_perfect: bool, new_achievements: List[str], daily_bonus: bool) -> discord.Embed:
        """Create comprehensive game results embed."""
        if is_perfect:
            title = "🏆 PERFECT GAME!"
            color = discord.Color.gold()
        elif accuracy >= 80:
            title = "🌟 Excellent Performance!"
            color = discord.Color.green()
        elif accuracy >= 60:
            title = "👍 Good Job!"
            color = discord.Color.blue()
        else:
            title = "📚 Keep Learning!"
            color = discord.Color.orange()
        
        embed = EmbedGenerator.create_embed(title=title, color=color)
        
        # Performance stats
        embed.add_field(
            name="📊 Performance",
            value=f"**Correct:** {session.correct_answers}/{len(session.questions)}\n**Accuracy:** {accuracy:.1f}%\n**Best Streak:** {session.streak}",
            inline=True
        )
        
        # XP breakdown
        multiplier_text = f"{xp_result['total_multiplier']:.1f}x"
        if daily_bonus:
            multiplier_text += " (Daily Bonus!)"
        
        embed.add_field(
            name="⭐ XP Earned",
            value=f"**{xp_result['gained_xp']}** XP\nMultiplier: {multiplier_text}",
            inline=True
        )
        
        # Level progress
        if xp_result["levels_gained"] > 0:
            embed.add_field(
                name="🎉 Level Up!",
                value=f"**Level {xp_result['new_level']}**\n+{xp_result['levels_gained']} level(s)!",
                inline=True
            )
        else:
            embed.add_field(
                name="📈 Level Progress",
                value=f"**Level {xp_result['new_level']}**",
                inline=True
            )
        
        # Special bonuses
        bonuses = []
        if is_perfect and len(session.questions) >= 3:
            bonuses.append(f"🏆 Perfect Game: +{PERFECT_GAME_BONUS} XP")
        if daily_bonus:
            bonuses.append("🎁 Daily Bonus: 2x XP")
        
        if bonuses:
            embed.add_field(name="🎁 Bonuses", value="\n".join(bonuses), inline=False)
        
        # New achievements
        if new_achievements:
            achievement_names = {
                "trivia_novice": "🥉 Trivia Novice",
                "trivia_apprentice": "🥈 Trivia Apprentice", 
                "trivia_master": "🥇 Trivia Master",
                "trivia_grandmaster": "👑 Trivia Grandmaster",
                "streak_warrior": "🔥 Streak Warrior",
                "streak_legend": "⚡ Streak Legend",
                "perfect_player": "💎 Perfect Player",
                "daily_champion": "📅 Daily Champion"
            }
            
            achievement_list = "\n".join([achievement_names.get(ach, ach) for ach in new_achievements])
            embed.add_field(name="🏅 New Achievements!", value=achievement_list, inline=False)
        
        embed.add_field(
            name="🎮 Play Again?", 
            value="Use `/play` to start another round!",
            inline=False
        )
        
        return EmbedGenerator.finalize_embed(embed)
    
    async def show_player_stats(self, interaction: discord.Interaction):
        """Show detailed player statistics."""
        guild_id = interaction.guild.id
        user_id = interaction.user.id
        player = load_play_player(guild_id, user_id)
        
        # Calculate derived stats
        stats = player.get("stats", {})
        games = stats.get("games_played", 0)
        questions = stats.get("questions_answered", 0)
        correct = stats.get("correct_answers", 0)
        accuracy = (correct / questions * 100) if questions > 0 else 0
        
        embed = EmbedGenerator.create_embed(
            title=f"📊 {interaction.user.display_name}'s Avatar Trivia Stats",
            color=discord.Color.blue()
        )
        
        # Basic stats
        embed.add_field(
            name="🎮 Game Statistics",
            value=f"**Level:** {player.get('level', 1)}\n**Total XP:** {player.get('total_xp', 0):,}\n**Avatar Tokens:** 🪙 {player.get('avatar_tokens', 0)}",
            inline=True
        )
        
        embed.add_field(
            name="🎯 Performance",
            value=f"**Games Played:** {games}\n**Questions Answered:** {questions}\n**Accuracy:** {accuracy:.1f}%",
            inline=True
        )
        
        embed.add_field(
            name="🔥 Records",
            value=f"**Best Streak:** {stats.get('best_streak', 0)}\n**Perfect Games:** {stats.get('perfect_games', 0)}\n**Daily Streak:** {stats.get('daily_streak', 0)}",
            inline=True
        )
        
        # Achievements
        achievements = player.get("achievements", [])
        if achievements:
            achievement_names = {
                "trivia_novice": "🥉 Trivia Novice",
                "trivia_apprentice": "🥈 Trivia Apprentice",
                "trivia_master": "🥇 Trivia Master", 
                "trivia_grandmaster": "👑 Trivia Grandmaster",
                "streak_warrior": "🔥 Streak Warrior",
                "streak_legend": "⚡ Streak Legend",
                "perfect_player": "💎 Perfect Player",
                "daily_champion": "📅 Daily Champion"
            }
            
            achievement_list = "\n".join([achievement_names.get(ach, ach) for ach in achievements[:10]])
            if len(achievements) > 10:
                achievement_list += f"\n... and {len(achievements) - 10} more!"
            
            embed.add_field(name="🏅 Achievements", value=achievement_list, inline=False)
        
        # Favorite mode and recent activity
        fav_mode = stats.get("favorite_mode", "standard")
        last_played = stats.get("last_played")
        if last_played:
            try:
                last_dt = datetime.fromisoformat(last_played.replace("Z", "+00:00"))
                time_ago = datetime.now(timezone.utc) - last_dt
                if time_ago.days > 0:
                    last_played_str = f"{time_ago.days} days ago"
                elif time_ago.seconds > 3600:
                    last_played_str = f"{time_ago.seconds // 3600} hours ago"
                else:
                    last_played_str = f"{time_ago.seconds // 60} minutes ago"
            except:
                last_played_str = "Unknown"
        else:
            last_played_str = "Never"
        
        embed.add_field(
            name="📈 Activity",
            value=f"**Favorite Mode:** {fav_mode.title()}\n**Last Played:** {last_played_str}",
            inline=False
        )
        
        embed = EmbedGenerator.finalize_embed(embed)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    async def show_achievements(self, interaction: discord.Interaction):
        """Show player's achievements."""
        guild_id = interaction.guild.id
        user_id = interaction.user.id
        player = load_play_player(guild_id, user_id)
        
        achievements = player.get("achievements", [])
        
        embed = EmbedGenerator.create_embed(
            title=f"🏅 {interaction.user.display_name}'s Achievements",
            color=discord.Color.gold()
        )
        
        achievement_names = {
            "trivia_novice": "🥉 Trivia Novice - 10 correct answers",
            "trivia_apprentice": "🥈 Trivia Apprentice - 50 correct answers",
            "trivia_master": "🥇 Trivia Master - 200 correct answers",
            "trivia_grandmaster": "👑 Trivia Grandmaster - 500 correct answers",
            "streak_warrior": "🔥 Streak Warrior - 5-question streak",
            "streak_legend": "⚡ Streak Legend - 10-question streak",
            "perfect_player": "💎 Perfect Player - 3 perfect games",
            "daily_champion": "📅 Daily Champion - 7-day streak"
        }
        
        if achievements:
            unlocked_text = "\n".join([achievement_names.get(ach, ach) for ach in achievements])
            embed.add_field(name="✅ Unlocked", value=unlocked_text, inline=False)
        
        # Show locked achievements
        locked = [name for name in achievement_names.keys() if name not in achievements]
        if locked:
            locked_text = "\n".join([f"🔒 {achievement_names[ach]}" for ach in locked[:5]])
            if len(locked) > 5:
                locked_text += f"\n... and {len(locked) - 5} more!"
            embed.add_field(name="🔒 Locked", value=locked_text, inline=False)
        
        embed.add_field(
            name="📊 Progress", 
            value=f"**{len(achievements)}/{len(achievement_names)}** achievements unlocked",
            inline=False
        )
        
        embed = EmbedGenerator.finalize_embed(embed)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def show_leaderboard(self, interaction: discord.Interaction):
        """Show server leaderboard with enhanced display."""
        guild_id = interaction.guild.id
        
        # Collect all player data from server
        server_dir = ensure_play_storage(guild_id)
        players_dir = server_dir / "players"
        
        entries = []
        for file in players_dir.glob("*.json"):
            try:
                data = json.loads(file.read_text(encoding="utf-8"))
                user_id = data.get("user_id", 0)
                level = data.get("level", 1)
                total_xp = data.get("total_xp", 0)
                stats = data.get("stats", {})
                correct = stats.get("correct_answers", 0)
                games = stats.get("games_played", 0)
                
                if games > 0:  # Only include players who have played
                    entries.append((user_id, level, total_xp, correct, games))
            except:
                continue
        
        if not entries:
            await interaction.response.send_message("📊 No leaderboard data available yet!", ephemeral=True)
            return
        
        # Sort by total XP
        entries.sort(key=lambda x: x[2], reverse=True)
        top_entries = entries[:10]
        
        embed = EmbedGenerator.create_embed(
            title="🏆 Avatar Trivia Leaderboard",
            description=f"Top players in {interaction.guild.name}",
            color=discord.Color.gold()
        )
        
        leaderboard_text = ""
        for rank, (user_id, level, total_xp, correct, games) in enumerate(top_entries, 1):
            accuracy = (correct / (games * 5)) * 100 if games > 0 else 0  # Assuming avg 5 questions per game
            
            rank_emoji = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, f"{rank}.")
            leaderboard_text += f"{rank_emoji} <@{user_id}> - Lv.{level} | {total_xp:,} XP | {accuracy:.1f}% accuracy\n"
        
        embed.add_field(name="Rankings", value=leaderboard_text, inline=False)
        
        embed = EmbedGenerator.finalize_embed(embed)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # ========== Fix for trivia leaderboard duplicates ==========
    
    @app_commands.command(name="trivia_leaderboard_fixed", description="🏆 Show trivia leaderboard (fixed duplicates)")
    @app_commands.describe(scope="Leaderboard scope")
    @app_commands.choices(scope=[
        app_commands.Choice(name="global", value="global"),
        app_commands.Choice(name="server", value="server"),
    ])
    async def fixed_trivia_leaderboard(self, interaction: discord.Interaction, scope: app_commands.Choice[str]):
        """Fixed version of trivia leaderboard that merges duplicates."""
        from cogs.minigame_daily import MINIGAME_ROOT, ensure_server_storage
        
        scope_value = scope.value
        if scope_value not in ("global", "server"):
            await interaction.response.send_message("Invalid scope. Use global or server.", ephemeral=True)
            return

        if interaction.guild is None and scope_value == "server":
            await interaction.response.send_message("Server leaderboard must be used in a server.", ephemeral=True)
            return

        entries: List[Tuple[int, int, int]] = []
        if scope_value == "server":
            guild_id = interaction.guild.id
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
            title=f"🏆 Trivia Leaderboard — {scope_value.title()} (Fixed)",
            description="\n".join(lines),
            color=discord.Color.gold(),
        )
        embed = EmbedGenerator.finalize_embed(embed)
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(AvatarPlaySystem(bot))
