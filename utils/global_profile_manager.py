"""
Global Profile Manager for Avatar Realms Collide Discord Bot.
Handles global user profiles, cross-server statistics, and leaderboard caching.
"""

import json
import asyncio
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
import logging
from .player_manager import player_manager
from .skill_manager import skill_manager
from .rating_system import rating_system

logger = logging.getLogger(__name__)

class GlobalProfileManager:
    """Manages global user profiles and cross-server statistics."""
    
    def __init__(self):
        self.global_profiles_dir = Path("data/users/global_profiles")
        self.leaderboard_cache_dir = Path("data/users/leaderboards")
        self.server_rankings_dir = self.leaderboard_cache_dir / "server_rankings"
        
        # Ensure directories exist
        self.global_profiles_dir.mkdir(parents=True, exist_ok=True)
        self.leaderboard_cache_dir.mkdir(parents=True, exist_ok=True)
        self.server_rankings_dir.mkdir(parents=True, exist_ok=True)
        
        # Cache for loaded profiles
        self._profile_cache = {}
        self._cache_timeout = 300  # 5 minutes
        self._last_cache_clear = datetime.now(timezone.utc)
    
    def _clear_cache_if_needed(self):
        """Clear cache if it's been too long since last clear."""
        now = datetime.now(timezone.utc)
        if (now - self._last_cache_clear).total_seconds() > self._cache_timeout:
            self._profile_cache.clear()
            self._last_cache_clear = now
    
    def load_global_profile(self, user_id: int) -> Dict[str, Any]:
        """
        Load or create a global user profile.
        
        Args:
            user_id: Discord user ID
            
        Returns:
            Global profile data dictionary
        """
        self._clear_cache_if_needed()
        
        # Check cache first
        if user_id in self._profile_cache:
            return self._profile_cache[user_id].copy()
        
        profile_file = self.global_profiles_dir / f"{user_id}.json"
        
        if profile_file.exists():
            try:
                with open(profile_file, 'r', encoding='utf-8') as f:
                    profile = json.load(f)
                    self._profile_cache[user_id] = profile
                    return profile.copy()
            except (json.JSONDecodeError, IOError) as e:
                logger.error(f"Error loading global profile for user {user_id}: {e}")
        
        # Create new profile
        profile = self._create_default_profile(user_id)
        self.save_global_profile(user_id, profile)
        return profile.copy()
    
    def _create_default_profile(self, user_id: int) -> Dict[str, Any]:
        """Create a default global profile for a new user."""
        return {
            "user_id": user_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "global_stats": {
                "total_games_played": 0,
                "total_questions_answered": 0,
                "total_correct_answers": 0,
                "total_xp": 0,
                "global_level": 1,
                "best_streak_ever": 0,
                "perfect_games_total": 0,
                "servers_played": [],
                "favorite_difficulty": "normal",
                "last_global_activity": None,
                "total_playtime_minutes": 0
            },
            "heroes": {
                "primary_element": None,
                "owned_heroes": {}
            },
            "skills": skill_manager.get_default_skills(),
            "resources": {
                "basic_hero_shards": 0,
                "epic_hero_shards": 0,
                "skill_points": 0
            },
            "duel_stats": {
                "total_duels": 0,
                "duel_wins": 0,
                "duel_losses": 0,
                "duel_draws": 0,
                "win_rate": 0.0,
                "current_streak": 0,
                "best_streak": 0,
                "duel_rating": 1000,
                "total_damage_dealt": 0,
                "total_damage_taken": 0,
                "favorite_element": None,
                "element_stats": {
                    "fire": {"wins": 0, "losses": 0, "draws": 0},
                    "water": {"wins": 0, "losses": 0, "draws": 0},
                    "earth": {"wins": 0, "losses": 0, "draws": 0},
                    "air": {"wins": 0, "losses": 0, "draws": 0}
                },
                "recent_duels": [],
                "achievements": [],
                "last_duel_at": None
            },
            "achievements": {
                "global": [],
                "server_specific": {}
            },
            "preferences": {
                "display_name": None,
                "custom_title": None,
                "privacy_settings": {
                    "show_on_global_leaderboard": True,
                    "show_server_stats": True,
                    "allow_cross_server_comparison": True
                }
            },
            "version": "1.1"
        }
    
    def save_global_profile(self, user_id: int, profile: Dict[str, Any]):
        """
        Save a global user profile.
        
        Args:
            user_id: Discord user ID
            profile: Profile data to save
        """
        try:
            profile["last_updated"] = datetime.now(timezone.utc).isoformat()
            profile_file = self.global_profiles_dir / f"{user_id}.json"
            
            with open(profile_file, 'w', encoding='utf-8') as f:
                json.dump(profile, f, indent=2)
            
            # Update cache
            self._profile_cache[user_id] = profile.copy()
            
        except IOError as e:
            logger.error(f"Error saving global profile for user {user_id}: {e}")
    
    def update_global_stats(self, user_id: int, guild_id: int, game_stats: Dict[str, Any]):
        """
        Update global statistics from a completed game.
        
        Args:
            user_id: Discord user ID
            guild_id: Discord guild ID
            game_stats: Game statistics to add to global stats
        """
        profile = self.load_global_profile(user_id)
        global_stats = profile["global_stats"]
        
        # Update statistics
        global_stats["total_games_played"] += game_stats.get("games_played", 0)
        global_stats["total_questions_answered"] += game_stats.get("questions_answered", 0)
        global_stats["total_correct_answers"] += game_stats.get("correct_answers", 0)
        global_stats["total_xp"] += game_stats.get("xp_gained", 0)
        global_stats["best_streak_ever"] = max(
            global_stats["best_streak_ever"], 
            game_stats.get("best_streak", 0)
        )
        global_stats["perfect_games_total"] += game_stats.get("perfect_games", 0)
        global_stats["last_global_activity"] = datetime.now(timezone.utc).isoformat()
        
        # Add server to played servers if not already there
        if str(guild_id) not in global_stats["servers_played"]:
            global_stats["servers_played"].append(str(guild_id))
        
        # Update global level based on total XP
        global_stats["global_level"] = self._calculate_global_level(global_stats["total_xp"])
        
        # Check for global achievements
        self._check_global_achievements(profile)
        
        self.save_global_profile(user_id, profile)
    
    def _calculate_global_level(self, total_xp: int) -> int:
        """Calculate global level based on total XP using exponential curve."""
        if total_xp <= 0:
            return 1
        
        # XP curve: level = floor(sqrt(total_xp / 100)) + 1
        # This means: Level 1: 0-99 XP, Level 2: 100-399 XP, Level 3: 400-899 XP, etc.
        import math
        return int(math.sqrt(total_xp / 100)) + 1
    
    def _check_global_achievements(self, profile: Dict[str, Any]):
        """Check and award global achievements."""
        global_stats = profile["global_stats"]
        achievements = profile["achievements"]["global"]
        
        # Achievement definitions
        achievement_thresholds = {
            "global_novice": {"total_correct_answers": 25},
            "global_apprentice": {"total_correct_answers": 100},
            "global_expert": {"total_correct_answers": 500},
            "global_master": {"total_correct_answers": 1000},
            "global_grandmaster": {"total_correct_answers": 2500},
            "streak_champion": {"best_streak_ever": 15},
            "streak_legend": {"best_streak_ever": 25},
            "perfect_master": {"perfect_games_total": 10},
            "perfect_legend": {"perfect_games_total": 25},
            "server_explorer": {"servers_played": 3},
            "server_nomad": {"servers_played": 5},
            "dedicated_player": {"total_games_played": 100},
            "addicted_player": {"total_games_played": 500},
            "trivia_god": {"total_games_played": 1000}
        }
        
        # Check each achievement
        for achievement_id, requirements in achievement_thresholds.items():
            if achievement_id not in achievements:
                # Check if requirements are met
                requirements_met = True
                for stat_name, required_value in requirements.items():
                    if stat_name == "servers_played":
                        actual_value = len(global_stats[stat_name])
                    else:
                        actual_value = global_stats.get(stat_name, 0)
                    
                    if actual_value < required_value:
                        requirements_met = False
                        break
                
                if requirements_met:
                    achievements.append(achievement_id)
    
    def get_global_leaderboard(self, limit: int = 50, category: str = "total_xp") -> List[Dict[str, Any]]:
        """
        Get global leaderboard rankings.
        
        Args:
            limit: Maximum number of entries to return
            category: Statistic to sort by
            
        Returns:
            List of leaderboard entries
        """
        # Check for cached leaderboard
        cache_file = self.leaderboard_cache_dir / "global_cache.json"
        cache_age_limit = 600  # 10 minutes
        
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                
                # Check if cache is still valid
                last_updated = datetime.fromisoformat(cache_data["last_updated"].replace('Z', '+00:00'))
                if (datetime.now(timezone.utc) - last_updated).total_seconds() < cache_age_limit:
                    rankings = cache_data.get("rankings", [])
                    return self._sort_leaderboard(rankings, category)[:limit]
            except (json.JSONDecodeError, IOError, KeyError) as e:
                logger.warning(f"Error reading global leaderboard cache: {e}")
        
        # Build fresh leaderboard
        return self._build_global_leaderboard(limit, category)
    
    def _build_global_leaderboard(self, limit: int, category: str) -> List[Dict[str, Any]]:
        """Build global leaderboard from all user profiles."""
        entries = []
        
        for profile_file in self.global_profiles_dir.glob("*.json"):
            try:
                with open(profile_file, 'r', encoding='utf-8') as f:
                    profile = json.load(f)
                
                # Skip if user opts out of global leaderboard
                if not profile.get("preferences", {}).get("privacy_settings", {}).get("show_on_global_leaderboard", True):
                    continue
                
                global_stats = profile.get("global_stats", {})
                
                # Only include users who have played games
                if global_stats.get("total_games_played", 0) == 0:
                    continue
                
                # Calculate accuracy
                total_questions = global_stats.get("total_questions_answered", 0)
                correct_answers = global_stats.get("total_correct_answers", 0)
                accuracy = (correct_answers / total_questions * 100) if total_questions > 0 else 0
                
                entry = {
                    "user_id": profile["user_id"],
                    "global_level": global_stats.get("global_level", 1),
                    "total_xp": global_stats.get("total_xp", 0),
                    "total_correct": correct_answers,
                    "total_games": global_stats.get("total_games_played", 0),
                    "accuracy": round(accuracy, 1),
                    "best_streak": global_stats.get("best_streak_ever", 0),
                    "perfect_games": global_stats.get("perfect_games_total", 0),
                    "servers_count": len(global_stats.get("servers_played", [])),
                    "display_name": profile.get("preferences", {}).get("display_name"),
                    "custom_title": profile.get("preferences", {}).get("custom_title")
                }
                entries.append(entry)
                
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Error reading profile {profile_file}: {e}")
                continue
        
        # Sort and cache
        sorted_entries = self._sort_leaderboard(entries, category)
        self._cache_global_leaderboard(sorted_entries)
        
        return sorted_entries[:limit]
    
    def _sort_leaderboard(self, entries: List[Dict[str, Any]], category: str) -> List[Dict[str, Any]]:
        """Sort leaderboard entries by the specified category."""
        sort_key_map = {
            "total_xp": "total_xp",
            "accuracy": "accuracy",
            "best_streak": "best_streak",
            "total_games": "total_games",
            "perfect_games": "perfect_games",
            "global_level": "global_level"
        }
        
        sort_key = sort_key_map.get(category, "total_xp")
        return sorted(entries, key=lambda x: x.get(sort_key, 0), reverse=True)
    
    def _cache_global_leaderboard(self, entries: List[Dict[str, Any]]):
        """Cache the global leaderboard for faster access."""
        try:
            cache_data = {
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "rankings": entries
            }
            
            cache_file = self.leaderboard_cache_dir / "global_cache.json"
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2)
                
        except IOError as e:
            logger.error(f"Error caching global leaderboard: {e}")
    
    def get_user_global_rank(self, user_id: int, category: str = "total_xp") -> Optional[int]:
        """Get a user's rank in the global leaderboard."""
        leaderboard = self.get_global_leaderboard(limit=1000, category=category)
        
        for rank, entry in enumerate(leaderboard, 1):
            if entry["user_id"] == user_id:
                return rank
        
        return None
    
    def migrate_server_data_to_global(self, user_id: int, guild_id: int, server_data: Dict[str, Any]):
        """
        Migrate existing server-specific data to global profile.
        
        Args:
            user_id: Discord user ID
            guild_id: Discord guild ID  
            server_data: Existing server player data
        """
        profile = self.load_global_profile(user_id)
        
        # Extract stats from server data
        server_stats = server_data.get("stats", {})
        game_stats = {
            "games_played": server_stats.get("games_played", 0),
            "questions_answered": server_stats.get("questions_answered", 0),
            "correct_answers": server_stats.get("correct_answers", 0),
            "xp_gained": server_data.get("total_xp", 0),
            "best_streak": server_stats.get("best_streak", 0),
            "perfect_games": server_stats.get("perfect_games", 0)
        }
        
        # Add server achievements
        server_achievements = server_data.get("achievements", [])
        if server_achievements:
            profile["achievements"]["server_specific"][str(guild_id)] = server_achievements
        
        # Update global stats
        self.update_global_stats(user_id, guild_id, game_stats)
        
        logger.info(f"Migrated data for user {user_id} from server {guild_id} to global profile")
    
    # Hero management methods
    def ensure_hero_exists(self, user_id: int, element: str) -> Dict[str, Any]:
        """Ensure a hero exists for the given element and return hero data."""
        profile = self.load_global_profile(user_id)
        
        if element not in profile["heroes"]["owned_heroes"]:
            # Create new hero
            hero_data = player_manager.get_default_hero_data(element)
            profile["heroes"]["owned_heroes"][element] = hero_data
            
            # Set as primary if it's the first hero
            if not profile["heroes"]["primary_element"]:
                profile["heroes"]["primary_element"] = element
            
            self.save_global_profile(user_id, profile)
        
        return profile["heroes"]["owned_heroes"][element]
    
    def get_hero(self, user_id: int, element: str) -> Optional[Dict[str, Any]]:
        """Get hero data for a specific element."""
        profile = self.load_global_profile(user_id)
        return profile["heroes"]["owned_heroes"].get(element)
    
    def update_hero(self, user_id: int, element: str, hero_data: Dict[str, Any]):
        """Update hero data for a specific element."""
        profile = self.load_global_profile(user_id)
        profile["heroes"]["owned_heroes"][element] = hero_data
        self.save_global_profile(user_id, profile)
    
    def set_primary_element(self, user_id: int, element: str) -> bool:
        """Set the primary element for a user."""
        profile = self.load_global_profile(user_id)
        
        # Ensure hero exists for this element
        if element not in profile["heroes"]["owned_heroes"]:
            self.ensure_hero_exists(user_id, element)
            profile = self.load_global_profile(user_id)
        
        profile["heroes"]["primary_element"] = element
        self.save_global_profile(user_id, profile)
        return True
    
    def get_primary_hero(self, user_id: int) -> Optional[Tuple[str, Dict[str, Any]]]:
        """Get the primary hero data."""
        profile = self.load_global_profile(user_id)
        primary_element = profile["heroes"]["primary_element"]
        
        if primary_element and primary_element in profile["heroes"]["owned_heroes"]:
            return primary_element, profile["heroes"]["owned_heroes"][primary_element]
        
        return None
    
    # Resource management methods
    def get_resources(self, user_id: int) -> Dict[str, int]:
        """Get user's current resources."""
        profile = self.load_global_profile(user_id)
        return profile.get("resources", {
            "basic_hero_shards": 0,
            "epic_hero_shards": 0,
            "skill_points": 0
        })
    
    def update_resources(self, user_id: int, resources: Dict[str, int]):
        """Update user's resources."""
        profile = self.load_global_profile(user_id)
        profile["resources"] = resources
        self.save_global_profile(user_id, profile)
    
    def add_resources(self, user_id: int, resource_type: str, amount: int):
        """Add resources to user's inventory."""
        profile = self.load_global_profile(user_id)
        current = profile.get("resources", {})
        current[resource_type] = current.get(resource_type, 0) + amount
        profile["resources"] = current
        self.save_global_profile(user_id, profile)
    
    # Skill management methods
    def get_skills(self, user_id: int) -> Dict[str, Dict[str, bool]]:
        """Get user's current skill tree progress."""
        profile = self.load_global_profile(user_id)
        return profile.get("skills", skill_manager.get_default_skills())
    
    def update_skills(self, user_id: int, skills: Dict[str, Dict[str, bool]]):
        """Update user's skill tree progress."""
        profile = self.load_global_profile(user_id)
        profile["skills"] = skills
        self.save_global_profile(user_id, profile)
    
    def get_skill_bonuses(self, user_id: int) -> Dict[str, float]:
        """Get total skill bonuses for a user."""
        skills = self.get_skills(user_id)
        return skill_manager.calculate_total_bonuses(skills)
    
    # Hero upgrade methods
    def upgrade_hero(self, user_id: int, element: str) -> Tuple[bool, str]:
        """Attempt to upgrade a hero."""
        # Ensure hero exists
        hero_data = self.ensure_hero_exists(user_id, element)
        resources = self.get_resources(user_id)
        
        # Try upgrade
        success, message, new_hero_data, new_resources = player_manager.upgrade_hero(hero_data, resources)
        
        if success:
            # Update both hero and resources
            self.update_hero(user_id, element, new_hero_data)
            self.update_resources(user_id, new_resources)
        
        return success, message
    
    # Skill upgrade methods
    def unlock_skill(self, user_id: int, element: str, tier: int) -> Tuple[bool, str]:
        """Attempt to unlock a skill."""
        skills = self.get_skills(user_id)
        resources = self.get_resources(user_id)
        skill_points = resources.get("skill_points", 0)
        
        # Try unlock
        success, message, new_skills, remaining_points = skill_manager.unlock_skill(element, tier, skills, skill_points)
        
        if success:
            # Update both skills and resources
            self.update_skills(user_id, new_skills)
            resources["skill_points"] = remaining_points
            self.update_resources(user_id, resources)
        
        return success, message
    
    # Sync resources from minigame system
    def sync_resources_from_minigame(self, user_id: int, guild_id: int):
        """Sync resources from minigame profile to global profile."""
        from cogs.minigame_daily import load_player
        
        try:
            minigame_player = load_player(guild_id, user_id)
            minigame_inventory = minigame_player.get("inventory", {})
            
            # Add resources to global profile (don't overwrite, add to existing)
            for resource_type, amount in minigame_inventory.items():
                if amount > 0:
                    self.add_resources(user_id, resource_type, amount)
                    
            # Clear minigame inventory after sync
            minigame_player["inventory"] = {
                "basic_hero_shards": 0,
                "epic_hero_shards": 0,
                "skill_points": 0
            }
            
            # Save updated minigame profile
            from cogs.minigame_daily import save_player
            save_player(guild_id, user_id, minigame_player)
            
            logger.info(f"Synced resources from minigame for user {user_id}")
            
        except Exception as e:
            logger.error(f"Error syncing resources from minigame for user {user_id}: {e}")
    
    # Duel statistics methods
    def get_duel_stats(self, user_id: int) -> Dict[str, Any]:
        """Get user's duel statistics."""
        profile = self.load_global_profile(user_id)
        return profile.get("duel_stats", {
            "total_duels": 0,
            "duel_wins": 0,
            "duel_losses": 0,
            "duel_draws": 0,
            "win_rate": 0.0,
            "current_streak": 0,
            "best_streak": 0,
            "duel_rating": 1000,
            "total_damage_dealt": 0,
            "total_damage_taken": 0,
            "favorite_element": None,
            "element_stats": {
                "fire": {"wins": 0, "losses": 0, "draws": 0},
                "water": {"wins": 0, "losses": 0, "draws": 0},
                "earth": {"wins": 0, "losses": 0, "draws": 0},
                "air": {"wins": 0, "losses": 0, "draws": 0}
            },
            "recent_duels": [],
            "achievements": [],
            "last_duel_at": None
        })
    
    def update_duel_stats(self, user_id: int, duel_stats: Dict[str, Any]):
        """Update user's duel statistics."""
        profile = self.load_global_profile(user_id)
        profile["duel_stats"] = duel_stats
        self.save_global_profile(user_id, profile)
    
    def record_duel_result(self, winner_id: int, loser_id: int, battle_result: Dict[str, Any], is_draw: bool = False):
        """Record the result of a duel for both participants."""
        from .duel_manager import BattleResult
        
        # Get current stats for both players
        winner_stats = self.get_duel_stats(winner_id)
        loser_stats = self.get_duel_stats(loser_id) if not is_draw else self.get_duel_stats(loser_id)
        
        # Update total duels for both
        winner_stats["total_duels"] += 1
        winner_stats["last_duel_at"] = datetime.now(timezone.utc).isoformat()
        
        if not is_draw:
            loser_stats["total_duels"] += 1
            loser_stats["last_duel_at"] = datetime.now(timezone.utc).isoformat()
        
        # Calculate rating changes
        winner_rating_change, loser_rating_change = rating_system.calculate_rating_change(
            winner_stats["duel_rating"],
            loser_stats["duel_rating"] if not is_draw else winner_stats["duel_rating"],
            winner_stats["total_duels"] - 1,
            loser_stats["total_duels"] - 1 if not is_draw else winner_stats["total_duels"] - 1,
            is_draw
        )
        
        if is_draw:
            # Handle draw
            winner_stats["duel_draws"] += 1
            winner_stats["current_streak"] = 0
            winner_stats["duel_rating"] += winner_rating_change
            
            # For draws, both players get same treatment
            loser_stats = self.get_duel_stats(loser_id)
            loser_stats["total_duels"] += 1
            loser_stats["duel_draws"] += 1
            loser_stats["current_streak"] = 0
            loser_stats["duel_rating"] += loser_rating_change
            loser_stats["last_duel_at"] = datetime.now(timezone.utc).isoformat()
        else:
            # Handle win/loss
            winner_stats["duel_wins"] += 1
            winner_stats["current_streak"] += 1
            winner_stats["best_streak"] = max(winner_stats["best_streak"], winner_stats["current_streak"])
            winner_stats["duel_rating"] += winner_rating_change
            
            loser_stats["duel_losses"] += 1
            loser_stats["current_streak"] = 0
            loser_stats["duel_rating"] += loser_rating_change
        
        # Update win rates
        if winner_stats["total_duels"] > 0:
            winner_stats["win_rate"] = (winner_stats["duel_wins"] / winner_stats["total_duels"]) * 100
        
        if not is_draw and loser_stats["total_duels"] > 0:
            loser_stats["win_rate"] = (loser_stats["duel_wins"] / loser_stats["total_duels"]) * 100
        
        # Update element statistics
        winner_element = battle_result.get("challenger_element") if winner_id == battle_result.get("winner_id") else battle_result.get("challenged_element")
        loser_element = battle_result.get("challenged_element") if winner_id == battle_result.get("winner_id") else battle_result.get("challenger_element")
        
        if winner_element:
            if is_draw:
                winner_stats["element_stats"][winner_element]["draws"] += 1
            else:
                winner_stats["element_stats"][winner_element]["wins"] += 1
        
        if loser_element and not is_draw:
            loser_stats["element_stats"][loser_element]["losses"] += 1
        elif loser_element and is_draw:
            loser_stats["element_stats"][loser_element]["draws"] += 1
        
        # Update favorite element (most used)
        winner_stats["favorite_element"] = self._calculate_favorite_element(winner_stats["element_stats"])
        if not is_draw:
            loser_stats["favorite_element"] = self._calculate_favorite_element(loser_stats["element_stats"])
        
        # Add to recent duels (keep last 10)
        duel_summary = {
            "opponent_id": loser_id if not is_draw else (loser_id if winner_id != loser_id else winner_id),
            "result": "win" if not is_draw else "draw",
            "element_used": winner_element,
            "opponent_element": loser_element,
            "rating_change": winner_rating_change,
            "date": datetime.now(timezone.utc).isoformat()
        }
        
        winner_stats["recent_duels"].insert(0, duel_summary)
        winner_stats["recent_duels"] = winner_stats["recent_duels"][:10]
        
        if not is_draw:
            loser_summary = duel_summary.copy()
            loser_summary["opponent_id"] = winner_id
            loser_summary["result"] = "loss"
            loser_summary["element_used"] = loser_element
            loser_summary["opponent_element"] = winner_element
            loser_summary["rating_change"] = loser_rating_change
            
            loser_stats["recent_duels"].insert(0, loser_summary)
            loser_stats["recent_duels"] = loser_stats["recent_duels"][:10]
        
        # Check for achievements
        self._check_duel_achievements(winner_stats)
        if not is_draw:
            self._check_duel_achievements(loser_stats)
        
        # Save updated stats
        self.update_duel_stats(winner_id, winner_stats)
        if not is_draw:
            self.update_duel_stats(loser_id, loser_stats)
        else:
            self.update_duel_stats(loser_id, loser_stats)
        
        return {
            "winner_rating_change": winner_rating_change,
            "loser_rating_change": loser_rating_change,
            "winner_new_rating": winner_stats["duel_rating"],
            "loser_new_rating": loser_stats["duel_rating"]
        }
    
    def _calculate_favorite_element(self, element_stats: Dict[str, Dict[str, int]]) -> Optional[str]:
        """Calculate the most used element."""
        element_totals = {}
        for element, stats in element_stats.items():
            total = stats["wins"] + stats["losses"] + stats["draws"]
            if total > 0:
                element_totals[element] = total
        
        if not element_totals:
            return None
        
        return max(element_totals, key=element_totals.get)
    
    def _check_duel_achievements(self, duel_stats: Dict[str, Any]):
        """Check and award duel achievements."""
        current_achievements = set(duel_stats.get("achievements", []))
        new_achievements = []
        
        # Achievement definitions
        achievement_checks = [
            ("first_blood", lambda stats: stats["duel_wins"] >= 1),
            ("dueling_novice", lambda stats: stats["total_duels"] >= 10),
            ("dueling_veteran", lambda stats: stats["total_duels"] >= 50),
            ("dueling_master", lambda stats: stats["total_duels"] >= 100),
            ("unstoppable", lambda stats: stats["best_streak"] >= 5),
            ("dominator", lambda stats: stats["best_streak"] >= 10),
            ("legend", lambda stats: stats["best_streak"] >= 15),
            ("element_master_fire", lambda stats: stats["element_stats"]["fire"]["wins"] >= 10),
            ("element_master_water", lambda stats: stats["element_stats"]["water"]["wins"] >= 10),
            ("element_master_earth", lambda stats: stats["element_stats"]["earth"]["wins"] >= 10),
            ("element_master_air", lambda stats: stats["element_stats"]["air"]["wins"] >= 10),
            ("silver_rank", lambda stats: stats["duel_rating"] >= 1200),
            ("gold_rank", lambda stats: stats["duel_rating"] >= 1400),
            ("platinum_rank", lambda stats: stats["duel_rating"] >= 1600),
            ("diamond_rank", lambda stats: stats["duel_rating"] >= 1800),
            ("master_rank", lambda stats: stats["duel_rating"] >= 2000),
        ]
        
        for achievement_id, check_func in achievement_checks:
            if achievement_id not in current_achievements and check_func(duel_stats):
                new_achievements.append(achievement_id)
                current_achievements.add(achievement_id)
        
        duel_stats["achievements"] = list(current_achievements)
        return new_achievements
    
    def get_duel_leaderboard(self, limit: int = 50, category: str = "rating") -> List[Dict[str, Any]]:
        """Get duel leaderboard rankings."""
        entries = []
        
        for profile_file in self.global_profiles_dir.glob("*.json"):
            try:
                with open(profile_file, 'r', encoding='utf-8') as f:
                    profile = json.load(f)
                
                duel_stats = profile.get("duel_stats", {})
                
                # Only include users who have dueled
                if duel_stats.get("total_duels", 0) == 0:
                    continue
                
                entry = {
                    "user_id": profile["user_id"],
                    "duel_rating": duel_stats.get("duel_rating", 1000),
                    "total_duels": duel_stats.get("total_duels", 0),
                    "duel_wins": duel_stats.get("duel_wins", 0),
                    "duel_losses": duel_stats.get("duel_losses", 0),
                    "win_rate": duel_stats.get("win_rate", 0.0),
                    "best_streak": duel_stats.get("best_streak", 0),
                    "favorite_element": duel_stats.get("favorite_element"),
                    "display_name": profile.get("preferences", {}).get("display_name"),
                    "tier": rating_system.get_tier_from_rating(duel_stats.get("duel_rating", 1000))
                }
                entries.append(entry)
                
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Error reading profile {profile_file}: {e}")
                continue
        
        # Sort by category
        if category == "rating":
            entries.sort(key=lambda x: x["duel_rating"], reverse=True)
        elif category == "wins":
            entries.sort(key=lambda x: x["duel_wins"], reverse=True)
        elif category == "win_rate":
            entries.sort(key=lambda x: (x["win_rate"], x["total_duels"]), reverse=True)
        elif category == "streak":
            entries.sort(key=lambda x: x["best_streak"], reverse=True)
        
        return entries[:limit]
    
    def get_user_duel_rank(self, user_id: int, category: str = "rating") -> Optional[int]:
        """Get user's rank in the duel leaderboard."""
        leaderboard = self.get_duel_leaderboard(limit=1000, category=category)
        
        for rank, entry in enumerate(leaderboard, 1):
            if entry["user_id"] == user_id:
                return rank
        
        return None

# Global instance
global_profile_manager = GlobalProfileManager()
