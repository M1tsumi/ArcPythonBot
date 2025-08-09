"""
Data Migration Utility for Avatar Realms Collide Discord Bot.
Migrates existing server-only data to the new global profile system.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Set, Any
from collections import defaultdict

from .global_profile_manager import global_profile_manager

logger = logging.getLogger(__name__)

class DataMigrationManager:
    """Handles migration of existing data to the global profile system."""
    
    def __init__(self):
        self.avatar_play_root = Path("data/servers/avatar_play/servers")
        self.minigame_root = Path("data/servers/minigame/servers")
    
    def migrate_all_data(self, dry_run: bool = False) -> Dict[str, Any]:
        """
        Migrate all existing player data to global profiles.
        
        Args:
            dry_run: If True, don't actually save data, just report what would be done
            
        Returns:
            Migration report dictionary
        """
        report = {
            "avatar_play": {"users_migrated": 0, "servers_processed": 0, "errors": []},
            "minigame": {"users_migrated": 0, "servers_processed": 0, "errors": []},
            "total_unique_users": 0,
            "dry_run": dry_run
        }
        
        # Track unique users across all systems
        all_users: Set[int] = set()
        
        # Migrate Avatar Play data
        if self.avatar_play_root.exists():
            avatar_users, avatar_report = self._migrate_avatar_play_data(dry_run)
            all_users.update(avatar_users)
            report["avatar_play"] = avatar_report
        
        # Migrate Minigame data
        if self.minigame_root.exists():
            minigame_users, minigame_report = self._migrate_minigame_data(dry_run)
            all_users.update(minigame_users)
            report["minigame"] = minigame_report
        
        report["total_unique_users"] = len(all_users)
        
        if not dry_run:
            # Rebuild global leaderboard cache
            global_profile_manager._build_global_leaderboard(limit=1000, category="total_xp")
            logger.info("Global leaderboard cache rebuilt after migration")
        
        return report
    
    def _migrate_avatar_play_data(self, dry_run: bool) -> tuple[Set[int], Dict[str, Any]]:
        """Migrate Avatar Play system data."""
        report = {"users_migrated": 0, "servers_processed": 0, "errors": []}
        migrated_users: Set[int] = set()
        
        for server_dir in self.avatar_play_root.iterdir():
            if not server_dir.is_dir():
                continue
            
            try:
                guild_id = int(server_dir.name)
                players_dir = server_dir / "players"
                
                if not players_dir.exists():
                    continue
                
                report["servers_processed"] += 1
                server_users = 0
                
                for player_file in players_dir.glob("*.json"):
                    try:
                        user_id = int(player_file.stem)
                        
                        with open(player_file, 'r', encoding='utf-8') as f:
                            player_data = json.load(f)
                        
                        if not dry_run:
                            global_profile_manager.migrate_server_data_to_global(
                                user_id, guild_id, player_data
                            )
                        
                        migrated_users.add(user_id)
                        server_users += 1
                        
                    except (ValueError, json.JSONDecodeError, IOError) as e:
                        error_msg = f"Error migrating Avatar Play user {player_file}: {e}"
                        report["errors"].append(error_msg)
                        logger.error(error_msg)
                
                report["users_migrated"] += server_users
                logger.info(f"Migrated {server_users} Avatar Play users from server {guild_id}")
                
            except ValueError:
                error_msg = f"Invalid server directory name: {server_dir.name}"
                report["errors"].append(error_msg)
                logger.warning(error_msg)
            except Exception as e:
                error_msg = f"Error processing Avatar Play server {server_dir}: {e}"
                report["errors"].append(error_msg)
                logger.error(error_msg)
        
        return migrated_users, report
    
    def _migrate_minigame_data(self, dry_run: bool) -> tuple[Set[int], Dict[str, Any]]:
        """Migrate Minigame system data."""
        report = {"users_migrated": 0, "servers_processed": 0, "errors": []}
        migrated_users: Set[int] = set()
        
        for server_dir in self.minigame_root.iterdir():
            if not server_dir.is_dir():
                continue
            
            try:
                guild_id = int(server_dir.name)
                players_dir = server_dir / "players"
                
                if not players_dir.exists():
                    continue
                
                report["servers_processed"] += 1
                server_users = 0
                
                for player_file in players_dir.glob("*.json"):
                    try:
                        user_id = int(player_file.stem)
                        
                        with open(player_file, 'r', encoding='utf-8') as f:
                            player_data = json.load(f)
                        
                        # Convert minigame data to global profile format
                        if not dry_run:
                            self._migrate_minigame_user(user_id, guild_id, player_data)
                        
                        migrated_users.add(user_id)
                        server_users += 1
                        
                    except (ValueError, json.JSONDecodeError, IOError) as e:
                        error_msg = f"Error migrating Minigame user {player_file}: {e}"
                        report["errors"].append(error_msg)
                        logger.error(error_msg)
                
                report["users_migrated"] += server_users
                logger.info(f"Migrated {server_users} Minigame users from server {guild_id}")
                
            except ValueError:
                error_msg = f"Invalid server directory name: {server_dir.name}"
                report["errors"].append(error_msg)
                logger.warning(error_msg)
            except Exception as e:
                error_msg = f"Error processing Minigame server {server_dir}: {e}"
                report["errors"].append(error_msg)
                logger.error(error_msg)
        
        return migrated_users, report
    
    def _migrate_minigame_user(self, user_id: int, guild_id: int, minigame_data: Dict[str, Any]):
        """Migrate a single minigame user to global profile."""
        # Extract trivia stats from minigame data
        trivia_stats = minigame_data.get("stats", {}).get("trivia", {})
        
        # Convert to Avatar Play equivalent stats
        correct_total = trivia_stats.get("correct_total", 0)
        incorrect_total = trivia_stats.get("incorrect_total", 0)
        sessions_played = trivia_stats.get("sessions_played", 0)
        ace_attempts = trivia_stats.get("ace_attempts", 0)
        
        # Estimate questions answered (assuming 5 questions per session on average)
        estimated_questions = sessions_played * 5
        total_questions = max(estimated_questions, correct_total + incorrect_total)
        
        # Estimate XP (50 XP per correct answer)
        estimated_xp = correct_total * 50
        
        game_stats = {
            "games_played": sessions_played,
            "questions_answered": total_questions,
            "correct_answers": correct_total,
            "xp_gained": estimated_xp,
            "best_streak": 0,  # Not tracked in minigame
            "perfect_games": ace_attempts
        }
        
        # Add minigame achievements to server-specific achievements
        profile = global_profile_manager.load_global_profile(user_id)
        if minigame_data.get("verified", False):
            server_achievements = profile["achievements"]["server_specific"].get(str(guild_id), [])
            if "minigame_verified" not in server_achievements:
                server_achievements.append("minigame_verified")
                profile["achievements"]["server_specific"][str(guild_id)] = server_achievements
        
        # Update global stats
        global_profile_manager.update_global_stats(user_id, guild_id, game_stats)
    
    def get_migration_status(self) -> Dict[str, Any]:
        """Get the current migration status."""
        status = {
            "avatar_play_servers": 0,
            "avatar_play_users": 0,
            "minigame_servers": 0,
            "minigame_users": 0,
            "global_profiles_exist": 0,
            "needs_migration": True
        }
        
        # Count Avatar Play data
        if self.avatar_play_root.exists():
            for server_dir in self.avatar_play_root.iterdir():
                if server_dir.is_dir() and server_dir.name.isdigit():
                    status["avatar_play_servers"] += 1
                    players_dir = server_dir / "players"
                    if players_dir.exists():
                        status["avatar_play_users"] += len(list(players_dir.glob("*.json")))
        
        # Count Minigame data
        if self.minigame_root.exists():
            for server_dir in self.minigame_root.iterdir():
                if server_dir.is_dir() and server_dir.name.isdigit():
                    status["minigame_servers"] += 1
                    players_dir = server_dir / "players"
                    if players_dir.exists():
                        status["minigame_users"] += len(list(players_dir.glob("*.json")))
        
        # Count existing global profiles
        global_profiles_dir = Path("data/users/global_profiles")
        if global_profiles_dir.exists():
            status["global_profiles_exist"] = len(list(global_profiles_dir.glob("*.json")))
        
        # Simple heuristic: if we have global profiles equal to or greater than
        # the sum of unique users from both systems, migration might be complete
        total_potential_users = status["avatar_play_users"] + status["minigame_users"]
        if status["global_profiles_exist"] >= total_potential_users and total_potential_users > 0:
            status["needs_migration"] = False
        
        return status
    
    def create_backup(self, backup_name: str = None) -> str:
        """Create a backup of existing data before migration."""
        from datetime import datetime
        import shutil
        
        if backup_name is None:
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        backup_dir = Path(f"data_backups/{backup_name}")
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Backup Avatar Play data
        if self.avatar_play_root.exists():
            shutil.copytree(
                self.avatar_play_root,
                backup_dir / "avatar_play",
                dirs_exist_ok=True
            )
        
        # Backup Minigame data
        if self.minigame_root.exists():
            shutil.copytree(
                self.minigame_root,
                backup_dir / "minigame",
                dirs_exist_ok=True
            )
        
        logger.info(f"Created backup at {backup_dir}")
        return str(backup_dir)

# Global instance
data_migration_manager = DataMigrationManager()
