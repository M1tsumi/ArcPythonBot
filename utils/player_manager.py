"""
Player Manager for Hero Upgrade System.
Handles player progression, stat calculations, and upgrade logic.
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class UpgradeCost:
    """Represents the cost to upgrade a player."""
    basic_hero_shards: int
    epic_hero_shards: int

@dataclass
class PlayerStats:
    """Represents a player's stats."""
    base_atk: int
    base_def: int
    base_hp: int
    current_atk: int
    current_def: int
    current_hp: int

class PlayerManager:
    """Manages player progression and upgrades."""
    
    def __init__(self):
        self.data_dir = Path("data/game/players")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Load player progression data
        self._load_progression_data()
    
    def _load_progression_data(self):
        """Load player progression and stat data."""
        # Player progression costs (Basic Hero Shards, Epic Hero Shards)
        self.upgrade_costs = {
            # From Rare 1★ to higher tiers
            ("rare", 1): UpgradeCost(10, 0),  # Rare 1★ → Rare 2★
            ("rare", 2): UpgradeCost(15, 5),  # Rare 2★ → Epic 1★
            ("epic", 1): UpgradeCost(20, 8),  # Epic 1★ → Epic 2★
            ("epic", 2): UpgradeCost(25, 12), # Epic 2★ → Epic 3★
            ("epic", 3): UpgradeCost(30, 20), # Epic 3★ → Legendary 1★
            ("legendary", 1): UpgradeCost(0, 15), # Legendary 1★ → 2★
            ("legendary", 2): UpgradeCost(0, 20), # Legendary 2★ → 3★
            ("legendary", 3): UpgradeCost(0, 25), # Legendary 3★ → 4★
            ("legendary", 4): UpgradeCost(0, 30), # Legendary 4★ → 5★
            ("legendary", 5): UpgradeCost(0, 40), # Legendary 5★ → 6★
        }
        
        # Base stats by element
        self.base_stats = {
            "fire": {"base_atk": 100, "base_def": 80, "base_hp": 120},
            "water": {"base_atk": 85, "base_def": 95, "base_hp": 140},
            "earth": {"base_atk": 90, "base_def": 110, "base_hp": 130},
            "air": {"base_atk": 110, "base_def": 75, "base_hp": 115}
        }
    
    def get_default_hero_data(self, element: str) -> Dict[str, Any]:
        """Get default hero data for a new player."""
        base_stats = self.base_stats.get(element, self.base_stats["fire"])
        
        return {
            "rarity": "rare",
            "stars": 1,
            "level": 1,
            "element": element,
            "stats": {
                "base_atk": base_stats["base_atk"],
                "base_def": base_stats["base_def"],
                "base_hp": base_stats["base_hp"],
                "current_atk": base_stats["base_atk"],
                "current_def": base_stats["base_def"],
                "current_hp": base_stats["base_hp"]
            }
        }
    
    def calculate_stats(self, hero_data: Dict[str, Any], skill_bonuses: Dict[str, float] = None) -> PlayerStats:
        """Calculate current stats based on star level and skill bonuses."""
        if skill_bonuses is None:
            skill_bonuses = {}
        
        rarity = hero_data.get("rarity", "rare")
        stars = hero_data.get("stars", 1)
        base_stats = hero_data.get("stats", {})
        
        # Calculate star level (total progression)
        star_level = self._get_total_star_level(rarity, stars)
        
        # Base stat multiplier from star progression (15% per star level)
        star_multiplier = 1 + (star_level - 1) * 0.15
        
        # Apply star multiplier to base stats
        base_atk = base_stats.get("base_atk", 100)
        base_def = base_stats.get("base_def", 80)
        base_hp = base_stats.get("base_hp", 120)
        
        current_atk = int(base_atk * star_multiplier)
        current_def = int(base_def * star_multiplier)
        current_hp = int(base_hp * star_multiplier)
        
        # Apply skill bonuses
        atk_bonus = skill_bonuses.get("atk_bonus", 0)
        def_bonus = skill_bonuses.get("def_bonus", 0)
        hp_bonus = skill_bonuses.get("hp_bonus", 0)
        all_stats_bonus = skill_bonuses.get("all_stats_bonus", 0)
        
        current_atk = int(current_atk * (1 + atk_bonus + all_stats_bonus))
        current_def = int(current_def * (1 + def_bonus + all_stats_bonus))
        current_hp = int(current_hp * (1 + hp_bonus + all_stats_bonus))
        
        return PlayerStats(
            base_atk=base_atk,
            base_def=base_def,
            base_hp=base_hp,
            current_atk=current_atk,
            current_def=current_def,
            current_hp=current_hp
        )
    
    def _get_total_star_level(self, rarity: str, stars: int) -> int:
        """Convert rarity + stars to total star level for stat calculations."""
        if rarity == "rare":
            return stars  # 1-2
        elif rarity == "epic":
            return 2 + stars  # 3-5
        elif rarity == "legendary":
            return 5 + stars  # 6-11
        return 1
    
    def get_upgrade_cost(self, hero_data: Dict[str, Any]) -> Optional[UpgradeCost]:
        """Get the cost to upgrade a hero to the next level."""
        rarity = hero_data.get("rarity", "rare")
        stars = hero_data.get("stars", 1)
        
        # Check if already at max level
        if rarity == "legendary" and stars >= 6:
            return None
        
        return self.upgrade_costs.get((rarity, stars))
    
    def get_next_tier_info(self, hero_data: Dict[str, Any]) -> Optional[Tuple[str, int]]:
        """Get the next tier (rarity, stars) after upgrade."""
        rarity = hero_data.get("rarity", "rare")
        stars = hero_data.get("stars", 1)
        
        if rarity == "rare":
            if stars == 1:
                return ("rare", 2)
            elif stars == 2:
                return ("epic", 1)
        elif rarity == "epic":
            if stars < 3:
                return ("epic", stars + 1)
            elif stars == 3:
                return ("legendary", 1)
        elif rarity == "legendary":
            if stars < 6:
                return ("legendary", stars + 1)
        
        return None  # Already at max
    
    def can_upgrade(self, hero_data: Dict[str, Any], resources: Dict[str, int]) -> Tuple[bool, str]:
        """Check if a hero can be upgraded with current resources."""
        cost = self.get_upgrade_cost(hero_data)
        if not cost:
            return False, "Hero is already at maximum level (Legendary 6★)"
        
        basic_shards = resources.get("basic_hero_shards", 0)
        epic_shards = resources.get("epic_hero_shards", 0)
        
        if basic_shards < cost.basic_hero_shards:
            needed = cost.basic_hero_shards - basic_shards
            return False, f"Need {needed} more Basic Hero Shards"
        
        if epic_shards < cost.epic_hero_shards:
            needed = cost.epic_hero_shards - epic_shards
            return False, f"Need {needed} more Epic Hero Shards"
        
        return True, "Ready to upgrade!"
    
    def upgrade_hero(self, hero_data: Dict[str, Any], resources: Dict[str, int]) -> Tuple[bool, str, Dict[str, Any], Dict[str, int]]:
        """
        Upgrade a hero and return updated data.
        
        Returns:
            (success, message, updated_hero_data, updated_resources)
        """
        can_upgrade, message = self.can_upgrade(hero_data, resources)
        if not can_upgrade:
            return False, message, hero_data, resources
        
        cost = self.get_upgrade_cost(hero_data)
        next_tier = self.get_next_tier_info(hero_data)
        
        if not cost or not next_tier:
            return False, "Upgrade failed", hero_data, resources
        
        # Deduct resources
        new_resources = resources.copy()
        new_resources["basic_hero_shards"] -= cost.basic_hero_shards
        new_resources["epic_hero_shards"] -= cost.epic_hero_shards
        
        # Update hero data
        new_hero_data = hero_data.copy()
        new_hero_data["rarity"] = next_tier[0]
        new_hero_data["stars"] = next_tier[1]
        
        # Recalculate stats
        stats = self.calculate_stats(new_hero_data)
        new_hero_data["stats"].update({
            "current_atk": stats.current_atk,
            "current_def": stats.current_def,
            "current_hp": stats.current_hp
        })
        
        rarity_display = next_tier[0].title()
        star_display = "★" * next_tier[1]
        success_message = f"Successfully upgraded to {rarity_display} {star_display}!"
        
        return True, success_message, new_hero_data, new_resources
    
    def get_all_elements(self) -> List[str]:
        """Get list of all available elements."""
        return list(self.base_stats.keys())
    
    def get_element_emoji(self, element: str) -> str:
        """Get emoji for an element."""
        emoji_map = {
            "fire": "🔥",
            "water": "💧", 
            "earth": "🌍",
            "air": "💨"
        }
        return emoji_map.get(element, "⭐")
    
    def get_rarity_color(self, rarity: str) -> int:
        """Get color code for rarity."""
        color_map = {
            "rare": 0x3498db,     # Blue
            "epic": 0x9b59b6,     # Purple
            "legendary": 0xf39c12  # Orange/Gold
        }
        return color_map.get(rarity, 0x95a5a6)
    
    def format_star_display(self, stars: int) -> str:
        """Format stars for display."""
        return "★" * stars

# Global instance
player_manager = PlayerManager()
