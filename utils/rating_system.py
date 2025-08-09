"""
Rating System for Duel Management.
Handles ELO-style rating calculations and tier management.
"""

import logging
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class RatingTier(Enum):
    """Rating tier classifications."""
    BRONZE = "Bronze"
    SILVER = "Silver"
    GOLD = "Gold"
    PLATINUM = "Platinum"
    DIAMOND = "Diamond"
    MASTER = "Master"

@dataclass
class RatingChange:
    """Represents a rating change from a duel."""
    old_rating: int
    new_rating: int
    change: int
    tier_changed: bool
    new_tier: RatingTier

@dataclass
class SeasonStats:
    """Season statistics for a player."""
    season_id: str
    rating: int
    peak_rating: int
    games_played: int
    wins: int
    losses: int
    draws: int
    tier: RatingTier
    rank_in_tier: int

class RatingSystem:
    """Manages player ratings and tier progression."""
    
    def __init__(self):
        # Rating tier thresholds
        self.tier_thresholds = {
            RatingTier.BRONZE: (0, 1199),
            RatingTier.SILVER: (1200, 1399),
            RatingTier.GOLD: (1400, 1599),
            RatingTier.PLATINUM: (1600, 1799),
            RatingTier.DIAMOND: (1800, 1999),
            RatingTier.MASTER: (2000, 9999)
        }
        
        # ELO calculation constants
        self.k_factor_base = 32
        self.rating_difference_divisor = 400
        self.provisional_games = 10  # Games with higher K-factor
        
        # Starting rating
        self.starting_rating = 1000
    
    def get_tier_from_rating(self, rating: int) -> RatingTier:
        """Get tier based on rating."""
        for tier, (min_rating, max_rating) in self.tier_thresholds.items():
            if min_rating <= rating <= max_rating:
                return tier
        return RatingTier.BRONZE
    
    def get_tier_info(self, tier: RatingTier) -> Dict[str, Any]:
        """Get information about a tier."""
        tier_info = {
            RatingTier.BRONZE: {
                "name": "Bronze",
                "color": 0xCD7F32,
                "icon": "🥉",
                "description": "Novice Duelist"
            },
            RatingTier.SILVER: {
                "name": "Silver", 
                "color": 0xC0C0C0,
                "icon": "🥈",
                "description": "Skilled Fighter"
            },
            RatingTier.GOLD: {
                "name": "Gold",
                "color": 0xFFD700,
                "icon": "🥇",
                "description": "Elite Warrior"
            },
            RatingTier.PLATINUM: {
                "name": "Platinum",
                "color": 0xE5E4E2,
                "icon": "💎",
                "description": "Master Duelist"
            },
            RatingTier.DIAMOND: {
                "name": "Diamond",
                "color": 0xB9F2FF,
                "icon": "💠",
                "description": "Legendary Champion"
            },
            RatingTier.MASTER: {
                "name": "Master",
                "color": 0xFF6B6B,
                "icon": "👑",
                "description": "Grandmaster"
            }
        }
        return tier_info.get(tier, tier_info[RatingTier.BRONZE])
    
    def calculate_rating_change(self, winner_rating: int, loser_rating: int, 
                              winner_games: int, loser_games: int, is_draw: bool = False) -> Tuple[int, int]:
        """Calculate rating change using ELO system."""
        # Calculate K-factor (higher for new players)
        winner_k = self._get_k_factor(winner_games)
        loser_k = self._get_k_factor(loser_games)
        
        # Expected score calculation
        winner_expected = 1 / (1 + 10 ** ((loser_rating - winner_rating) / self.rating_difference_divisor))
        loser_expected = 1 - winner_expected
        
        if is_draw:
            # Draw: both get 0.5 points
            winner_score = 0.5
            loser_score = 0.5
        else:
            # Win/Loss: winner gets 1, loser gets 0
            winner_score = 1.0
            loser_score = 0.0
        
        # Calculate rating changes
        winner_change = int(winner_k * (winner_score - winner_expected))
        loser_change = int(loser_k * (loser_score - loser_expected))
        
        return winner_change, loser_change
    
    def _get_k_factor(self, games_played: int) -> int:
        """Get K-factor based on games played."""
        if games_played < self.provisional_games:
            return self.k_factor_base * 1.5  # Higher K-factor for new players
        elif games_played < 50:
            return self.k_factor_base
        else:
            return self.k_factor_base * 0.75  # Lower K-factor for experienced players
    
    def apply_rating_change(self, current_rating: int, rating_change: int, 
                          games_played: int) -> RatingChange:
        """Apply rating change and determine tier changes."""
        old_rating = current_rating
        new_rating = max(0, current_rating + rating_change)  # Can't go below 0
        
        old_tier = self.get_tier_from_rating(old_rating)
        new_tier = self.get_tier_from_rating(new_rating)
        tier_changed = old_tier != new_tier
        
        return RatingChange(
            old_rating=old_rating,
            new_rating=new_rating,
            change=rating_change,
            tier_changed=tier_changed,
            new_tier=new_tier
        )
    
    def get_leaderboard_position(self, user_rating: int, all_ratings: List[int]) -> int:
        """Get user's position in the leaderboard."""
        sorted_ratings = sorted(all_ratings, reverse=True)
        try:
            return sorted_ratings.index(user_rating) + 1
        except ValueError:
            return len(sorted_ratings) + 1
    
    def calculate_tier_progress(self, rating: int) -> Dict[str, Any]:
        """Calculate progress within current tier."""
        current_tier = self.get_tier_from_rating(rating)
        min_rating, max_rating = self.tier_thresholds[current_tier]
        
        # Special case for Master tier (no upper limit)
        if current_tier == RatingTier.MASTER:
            progress_percentage = 100.0
            rating_needed = 0
        else:
            progress = rating - min_rating
            tier_range = max_rating - min_rating
            progress_percentage = (progress / tier_range) * 100
            rating_needed = max_rating + 1 - rating
        
        return {
            "current_tier": current_tier,
            "rating": rating,
            "tier_min": min_rating,
            "tier_max": max_rating if current_tier != RatingTier.MASTER else None,
            "progress_percentage": progress_percentage,
            "rating_needed_next_tier": max(0, rating_needed)
        }
    
    def get_seasonal_rewards(self, tier: RatingTier, peak_rating: int) -> Dict[str, Any]:
        """Get seasonal rewards based on tier achieved."""
        rewards = {
            RatingTier.BRONZE: {
                "basic_hero_shards": 3,
                "epic_hero_shards": 0,
                "skill_points": 0,
                "title": None
            },
            RatingTier.SILVER: {
                "basic_hero_shards": 5,
                "epic_hero_shards": 3,
                "skill_points": 2,
                "title": None
            },
            RatingTier.GOLD: {
                "basic_hero_shards": 8,
                "epic_hero_shards": 5,
                "skill_points": 3,
                "title": "Gold Duelist"
            },
            RatingTier.PLATINUM: {
                "basic_hero_shards": 12,
                "epic_hero_shards": 8,
                "skill_points": 5,
                "title": "Platinum Warrior"
            },
            RatingTier.DIAMOND: {
                "basic_hero_shards": 18,
                "epic_hero_shards": 12,
                "skill_points": 8,
                "title": "Diamond Champion"
            },
            RatingTier.MASTER: {
                "basic_hero_shards": 25,
                "epic_hero_shards": 18,
                "skill_points": 12,
                "title": "Grandmaster"
            }
        }
        
        base_rewards = rewards.get(tier, rewards[RatingTier.BRONZE])
        
        # Bonus rewards for high peak ratings
        if peak_rating >= 2200:
            base_rewards["epic_hero_shards"] += 5
            base_rewards["skill_points"] += 3
        elif peak_rating >= 2000:
            base_rewards["epic_hero_shards"] += 3
            base_rewards["skill_points"] += 2
        
        return base_rewards
    
    def get_matchmaking_range(self, rating: int, games_played: int) -> Tuple[int, int]:
        """Get rating range for matchmaking."""
        if games_played < self.provisional_games:
            # Wider range for new players
            range_size = 300
        elif rating < 1200:
            range_size = 200
        elif rating < 1600:
            range_size = 150
        else:
            range_size = 100
        
        min_rating = max(0, rating - range_size)
        max_rating = rating + range_size
        
        return min_rating, max_rating
    
    def calculate_achievement_progress(self, duel_stats: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Calculate achievement progress based on duel stats."""
        achievements = []
        
        total_duels = duel_stats.get("total_duels", 0)
        duel_wins = duel_stats.get("duel_wins", 0)
        current_streak = duel_stats.get("current_streak", 0)
        best_streak = duel_stats.get("best_streak", 0)
        duel_rating = duel_stats.get("duel_rating", self.starting_rating)
        
        # Achievement definitions
        achievement_defs = [
            {"id": "first_blood", "name": "First Blood", "desc": "Win your first duel", "target": 1, "current": min(1, duel_wins)},
            {"id": "dueling_novice", "name": "Dueling Novice", "desc": "Play 10 duels", "target": 10, "current": total_duels},
            {"id": "dueling_veteran", "name": "Dueling Veteran", "desc": "Play 50 duels", "target": 50, "current": total_duels},
            {"id": "unstoppable", "name": "Unstoppable", "desc": "Win 5 duels in a row", "target": 5, "current": min(5, best_streak)},
            {"id": "dominator", "name": "Dominator", "desc": "Win 10 duels in a row", "target": 10, "current": min(10, best_streak)},
            {"id": "silver_rank", "name": "Silver Rank", "desc": "Reach Silver tier (1200 rating)", "target": 1200, "current": duel_rating},
            {"id": "gold_rank", "name": "Gold Rank", "desc": "Reach Gold tier (1400 rating)", "target": 1400, "current": duel_rating},
            {"id": "diamond_rank", "name": "Diamond Rank", "desc": "Reach Diamond tier (1800 rating)", "target": 1800, "current": duel_rating},
        ]
        
        for ach in achievement_defs:
            progress = min(100, (ach["current"] / ach["target"]) * 100)
            completed = ach["current"] >= ach["target"]
            
            achievements.append({
                "id": ach["id"],
                "name": ach["name"],
                "description": ach["desc"],
                "progress": progress,
                "completed": completed,
                "current": ach["current"],
                "target": ach["target"]
            })
        
        return achievements
    
    def format_rating_display(self, rating: int, games_played: int = 0) -> str:
        """Format rating for display."""
        tier = self.get_tier_from_rating(rating)
        tier_info = self.get_tier_info(tier)
        
        if games_played < self.provisional_games:
            return f"🔸 Unranked ({rating})"
        else:
            return f"{tier_info['icon']} {tier_info['name']} ({rating})"
    
    def get_rating_color(self, rating: int) -> int:
        """Get color for rating tier."""
        tier = self.get_tier_from_rating(rating)
        return self.get_tier_info(tier)["color"]

# Global instance
rating_system = RatingSystem()
