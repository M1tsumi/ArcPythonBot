"""
Skill Manager for Skill Tree System.
Handles skill upgrades, bonuses, and tree management.
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class Skill:
    """Represents a skill in the skill tree."""
    name: str
    tier: int
    cost: int
    description: str
    bonuses: Dict[str, float]
    element: str

@dataclass
class SkillBonuses:
    """Aggregated skill bonuses."""
    atk_bonus: float = 0.0
    def_bonus: float = 0.0
    hp_bonus: float = 0.0
    all_stats_bonus: float = 0.0
    crit_bonus: float = 0.0
    speed_bonus: float = 0.0
    evasion_bonus: float = 0.0
    hp_regen_bonus: float = 0.0
    dmg_reduction_bonus: float = 0.0

class SkillManager:
    """Manages skill trees and upgrades."""
    
    def __init__(self):
        self.data_dir = Path("data/game/skills")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Load skill tree data
        self._load_skill_data()
    
    def _load_skill_data(self):
        """Load skill tree definitions."""
        self.skills = {
            "fire": {
                1: Skill("Flame Strike", 1, 1, "+10% ATK", {"atk_bonus": 0.10}, "fire"),
                2: Skill("Fire Wall", 2, 2, "+15% DEF", {"def_bonus": 0.15}, "fire"),
                3: Skill("Blazing Fury", 3, 3, "+20% ATK, +10% Crit", {"atk_bonus": 0.20, "crit_bonus": 0.10}, "fire"),
                4: Skill("Inferno Mastery", 4, 5, "+25% All Stats", {"all_stats_bonus": 0.25}, "fire")
            },
            "water": {
                1: Skill("Water Whip", 1, 1, "+15% HP", {"hp_bonus": 0.15}, "water"),
                2: Skill("Healing Stream", 2, 2, "+10% HP Regen", {"hp_regen_bonus": 0.10}, "water"),
                3: Skill("Tidal Force", 3, 3, "+20% DEF, +15% HP", {"def_bonus": 0.20, "hp_bonus": 0.15}, "water"),
                4: Skill("Ocean Mastery", 4, 5, "+25% All Stats", {"all_stats_bonus": 0.25}, "water")
            },
            "earth": {
                1: Skill("Rock Throw", 1, 1, "+15% DEF", {"def_bonus": 0.15}, "earth"),
                2: Skill("Stone Armor", 2, 2, "+20% DEF, +5% DMG Reduction", {"def_bonus": 0.20, "dmg_reduction_bonus": 0.05}, "earth"),
                3: Skill("Earthquake", 3, 3, "+15% ATK, +20% DEF", {"atk_bonus": 0.15, "def_bonus": 0.20}, "earth"),
                4: Skill("Mountain Mastery", 4, 5, "+25% All Stats", {"all_stats_bonus": 0.25}, "earth")
            },
            "air": {
                1: Skill("Wind Blade", 1, 1, "+10% ATK, +5% Speed", {"atk_bonus": 0.10, "speed_bonus": 0.05}, "air"),
                2: Skill("Air Shield", 2, 2, "+10% Evasion", {"evasion_bonus": 0.10}, "air"),
                3: Skill("Tornado Strike", 3, 3, "+25% ATK, +10% Crit", {"atk_bonus": 0.25, "crit_bonus": 0.10}, "air"),
                4: Skill("Storm Mastery", 4, 5, "+25% All Stats", {"all_stats_bonus": 0.25}, "air")
            }
        }
    
    def get_skill(self, element: str, tier: int) -> Optional[Skill]:
        """Get a specific skill by element and tier."""
        return self.skills.get(element, {}).get(tier)
    
    def get_element_skills(self, element: str) -> Dict[int, Skill]:
        """Get all skills for an element."""
        return self.skills.get(element, {})
    
    def can_unlock_skill(self, element: str, tier: int, current_skills: Dict[str, Dict[str, bool]], skill_points: int) -> Tuple[bool, str]:
        """Check if a skill can be unlocked."""
        skill = self.get_skill(element, tier)
        if not skill:
            return False, "Skill not found"
        
        # Check if already unlocked
        if current_skills.get(element, {}).get(f"tier_{tier}", False):
            return False, "Skill already unlocked"
        
        # Check skill points
        if skill_points < skill.cost:
            needed = skill.cost - skill_points
            return False, f"Need {needed} more Skill Points"
        
        # Check prerequisites (must have previous tier)
        if tier > 1:
            prev_tier_unlocked = current_skills.get(element, {}).get(f"tier_{tier-1}", False)
            if not prev_tier_unlocked:
                prev_skill = self.get_skill(element, tier - 1)
                prev_name = prev_skill.name if prev_skill else f"Tier {tier-1}"
                return False, f"Must unlock {prev_name} first"
        
        return True, "Ready to unlock!"
    
    def unlock_skill(self, element: str, tier: int, current_skills: Dict[str, Dict[str, bool]], skill_points: int) -> Tuple[bool, str, Dict[str, Dict[str, bool]], int]:
        """
        Unlock a skill and return updated data.
        
        Returns:
            (success, message, updated_skills, remaining_skill_points)
        """
        can_unlock, message = self.can_unlock_skill(element, tier, current_skills, skill_points)
        if not can_unlock:
            return False, message, current_skills, skill_points
        
        skill = self.get_skill(element, tier)
        if not skill:
            return False, "Skill not found", current_skills, skill_points
        
        # Update skills
        new_skills = {}
        for elem in current_skills:
            new_skills[elem] = current_skills[elem].copy()
        
        if element not in new_skills:
            new_skills[element] = {
                "tier_1": False,
                "tier_2": False,
                "tier_3": False,
                "tier_4": False
            }
        
        new_skills[element][f"tier_{tier}"] = True
        
        # Deduct skill points
        remaining_points = skill_points - skill.cost
        
        success_message = f"Successfully unlocked {skill.name}! {skill.description}"
        
        return True, success_message, new_skills, remaining_points
    
    def calculate_total_bonuses(self, current_skills: Dict[str, Dict[str, bool]]) -> Dict[str, float]:
        """Calculate total bonuses from all unlocked skills."""
        total_bonuses = {
            "atk_bonus": 0.0,
            "def_bonus": 0.0,
            "hp_bonus": 0.0,
            "all_stats_bonus": 0.0,
            "crit_bonus": 0.0,
            "speed_bonus": 0.0,
            "evasion_bonus": 0.0,
            "hp_regen_bonus": 0.0,
            "dmg_reduction_bonus": 0.0
        }
        
        for element, element_skills in current_skills.items():
            for tier_key, is_unlocked in element_skills.items():
                if is_unlocked:
                    tier = int(tier_key.split("_")[1])
                    skill = self.get_skill(element, tier)
                    if skill:
                        for bonus_type, bonus_value in skill.bonuses.items():
                            total_bonuses[bonus_type] += bonus_value
        
        return total_bonuses
    
    def get_skill_tree_progress(self, current_skills: Dict[str, Dict[str, bool]]) -> Dict[str, Any]:
        """Get progress statistics for skill trees."""
        progress = {
            "total_unlocked": 0,
            "total_available": 0,
            "by_element": {},
            "skill_points_spent": 0
        }
        
        for element in self.skills:
            element_progress = {
                "unlocked": 0,
                "total": len(self.skills[element]),
                "skills": []
            }
            
            element_skills = current_skills.get(element, {})
            for tier in range(1, 5):
                skill = self.get_skill(element, tier)
                is_unlocked = element_skills.get(f"tier_{tier}", False)
                
                if skill:
                    element_progress["skills"].append({
                        "tier": tier,
                        "name": skill.name,
                        "unlocked": is_unlocked,
                        "cost": skill.cost,
                        "description": skill.description
                    })
                    
                    if is_unlocked:
                        element_progress["unlocked"] += 1
                        progress["skill_points_spent"] += skill.cost
            
            progress["by_element"][element] = element_progress
            progress["total_unlocked"] += element_progress["unlocked"]
            progress["total_available"] += element_progress["total"]
        
        return progress
    
    def get_available_upgrades(self, current_skills: Dict[str, Dict[str, bool]], skill_points: int) -> List[Dict[str, Any]]:
        """Get list of skills that can be unlocked with current skill points."""
        available = []
        
        for element in self.skills:
            for tier in range(1, 5):
                can_unlock, message = self.can_unlock_skill(element, tier, current_skills, skill_points)
                if can_unlock:
                    skill = self.get_skill(element, tier)
                    if skill:
                        available.append({
                            "element": element,
                            "tier": tier,
                            "skill": skill,
                            "cost": skill.cost
                        })
        
        # Sort by cost (cheapest first)
        available.sort(key=lambda x: x["cost"])
        return available
    
    def get_element_emoji(self, element: str) -> str:
        """Get emoji for an element."""
        emoji_map = {
            "fire": "🔥",
            "water": "💧",
            "earth": "🌍", 
            "air": "💨"
        }
        return emoji_map.get(element, "⭐")
    
    def get_tier_emoji(self, tier: int, unlocked: bool = False) -> str:
        """Get emoji for skill tier status."""
        if unlocked:
            return "✅"
        elif tier == 1:
            return "🟢"  # Available
        else:
            return "🔒"  # Locked
    
    def format_skill_description(self, skill: Skill) -> str:
        """Format skill description with bonuses."""
        parts = [skill.description]
        
        if skill.bonuses:
            bonus_parts = []
            for bonus_type, value in skill.bonuses.items():
                if value > 0:
                    if bonus_type.endswith("_bonus"):
                        stat_name = bonus_type.replace("_bonus", "").replace("_", " ").title()
                        bonus_parts.append(f"+{value*100:.0f}% {stat_name}")
            
            if bonus_parts:
                parts.append(f"({', '.join(bonus_parts)})")
        
        return " ".join(parts)
    
    def get_default_skills(self) -> Dict[str, Dict[str, bool]]:
        """Get default skill tree state for new players."""
        return {
            "fire": {"tier_1": False, "tier_2": False, "tier_3": False, "tier_4": False},
            "water": {"tier_1": False, "tier_2": False, "tier_3": False, "tier_4": False},
            "earth": {"tier_1": False, "tier_2": False, "tier_3": False, "tier_4": False},
            "air": {"tier_1": False, "tier_2": False, "tier_3": False, "tier_4": False}
        }

# Global instance
skill_manager = SkillManager()
