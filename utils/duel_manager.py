"""
Duel Manager for PvP Combat System.
Handles combat calculations, battle logic, and duel state management.
"""

import json
import random
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class BattleResult(Enum):
    """Battle outcome types."""
    VICTORY = "victory"
    DEFEAT = "defeat"
    DRAW = "draw"
    FORFEIT = "forfeit"

class DuelPhase(Enum):
    """Duel phases."""
    CHALLENGE = "challenge"
    SETUP = "setup"
    BATTLE = "battle"
    RESOLUTION = "resolution"
    COMPLETED = "completed"

@dataclass
class DuelHero:
    """Represents a hero in a duel."""
    user_id: int
    element: str
    stats: Dict[str, int]
    skill_bonuses: Dict[str, float]
    max_hp: int
    current_hp: int
    rarity: str
    stars: int

@dataclass
class BattleAction:
    """Represents a battle action."""
    attacker_id: int
    defender_id: int
    action_type: str
    damage: int
    is_critical: bool
    is_miss: bool
    effects: List[str]

@dataclass
class DuelState:
    """Represents the current state of a duel."""
    challenger_id: int
    challenged_id: int
    challenger_hero: Optional[DuelHero]
    challenged_hero: Optional[DuelHero]
    phase: DuelPhase
    current_turn: int
    turn_player_id: int
    battle_log: List[BattleAction]
    created_at: datetime
    expires_at: datetime
    channel_id: int
    message_id: Optional[int]

class DuelManager:
    """Manages PvP duels and combat calculations."""
    
    def __init__(self):
        self.data_dir = Path("data/game/duels")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Active duels storage (in-memory for now)
        self.active_duels: Dict[str, DuelState] = {}
        self.pending_challenges: Dict[int, DuelState] = {}  # challenged_user_id -> duel_state
        
        # Load combat configuration
        self._load_combat_data()
    
    def _load_combat_data(self):
        """Load combat formulas and configurations."""
        # Element advantages (attacker -> defender -> multiplier)
        self.element_advantages = {
            "fire": {"air": 1.15, "water": 0.9, "earth": 1.0, "fire": 1.0},
            "water": {"fire": 1.15, "earth": 0.9, "air": 1.0, "water": 1.0},
            "earth": {"water": 1.15, "air": 0.9, "fire": 1.0, "earth": 1.0},
            "air": {"earth": 1.15, "fire": 0.9, "water": 1.0, "air": 1.0}
        }
        
        # Combat constants
        self.combat_config = {
            "base_accuracy": 0.95,
            "min_damage_ratio": 0.1,
            "critical_multiplier": 1.5,
            "defense_reduction": 0.6,
            "max_turns": 15,
            "turn_timeout": 30,  # seconds
            "challenge_timeout": 300  # 5 minutes
        }
    
    def create_challenge(self, challenger_id: int, challenged_id: int, challenger_element: str, channel_id: int) -> Tuple[bool, str, Optional[DuelState]]:
        """Create a new duel challenge."""
        # Validation checks
        if challenger_id == challenged_id:
            return False, "You cannot duel yourself!", None
        
        if challenged_id in self.pending_challenges:
            return False, "That player already has a pending challenge!", None
        
        if self._is_user_in_active_duel(challenger_id):
            return False, "You are already in an active duel!", None
        
        if self._is_user_in_active_duel(challenged_id):
            return False, "That player is already in an active duel!", None
        
        # Create duel state
        from datetime import timedelta
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=self.combat_config["challenge_timeout"])
        
        duel_state = DuelState(
            challenger_id=challenger_id,
            challenged_id=challenged_id,
            challenger_hero=None,
            challenged_hero=None,
            phase=DuelPhase.CHALLENGE,
            current_turn=0,
            turn_player_id=0,
            battle_log=[],
            created_at=datetime.now(timezone.utc),
            expires_at=expires_at,
            channel_id=channel_id,
            message_id=None
        )
        
        # Store pending challenge
        self.pending_challenges[challenged_id] = duel_state
        
        return True, "Challenge created successfully!", duel_state
    
    def accept_challenge(self, user_id: int, challenged_element: str) -> Tuple[bool, str, Optional[DuelState]]:
        """Accept a pending challenge."""
        if user_id not in self.pending_challenges:
            return False, "You don't have any pending challenges!", None
        
        duel_state = self.pending_challenges[user_id]
        
        # Check if challenge expired
        if datetime.now(timezone.utc) > duel_state.expires_at:
            del self.pending_challenges[user_id]
            return False, "Challenge has expired!", None
        
        # Move to setup phase
        duel_state.phase = DuelPhase.SETUP
        
        # Remove from pending and add to active
        del self.pending_challenges[user_id]
        duel_id = f"{duel_state.challenger_id}_{duel_state.challenged_id}_{int(duel_state.created_at.timestamp())}"
        self.active_duels[duel_id] = duel_state
        
        return True, "Challenge accepted! Preparing for battle...", duel_state
    
    def decline_challenge(self, user_id: int) -> Tuple[bool, str]:
        """Decline a pending challenge."""
        if user_id not in self.pending_challenges:
            return False, "You don't have any pending challenges!"
        
        del self.pending_challenges[user_id]
        return True, "Challenge declined."
    
    def setup_duel_heroes(self, duel_state: DuelState, challenger_hero_data: Dict[str, Any], challenged_hero_data: Dict[str, Any],
                         challenger_bonuses: Dict[str, float], challenged_bonuses: Dict[str, float]) -> DuelState:
        """Setup heroes for the duel with their stats and bonuses."""
        from .player_manager import player_manager
        
        # Create challenger hero
        challenger_stats = player_manager.calculate_stats(challenger_hero_data, challenger_bonuses)
        duel_state.challenger_hero = DuelHero(
            user_id=duel_state.challenger_id,
            element=challenger_hero_data["element"],
            stats={
                "atk": challenger_stats.current_atk,
                "def": challenger_stats.current_def,
                "hp": challenger_stats.current_hp
            },
            skill_bonuses=challenger_bonuses,
            max_hp=challenger_stats.current_hp,
            current_hp=challenger_stats.current_hp,
            rarity=challenger_hero_data["rarity"],
            stars=challenger_hero_data["stars"]
        )
        
        # Create challenged hero
        challenged_stats = player_manager.calculate_stats(challenged_hero_data, challenged_bonuses)
        duel_state.challenged_hero = DuelHero(
            user_id=duel_state.challenged_id,
            element=challenged_hero_data["element"],
            stats={
                "atk": challenged_stats.current_atk,
                "def": challenged_stats.current_def,
                "hp": challenged_stats.current_hp
            },
            skill_bonuses=challenged_bonuses,
            max_hp=challenged_stats.current_hp,
            current_hp=challenged_stats.current_hp,
            rarity=challenged_hero_data["rarity"],
            stars=challenged_hero_data["stars"]
        )
        
        # Determine turn order based on speed
        challenger_speed = self._calculate_speed(duel_state.challenger_hero)
        challenged_speed = self._calculate_speed(duel_state.challenged_hero)
        
        if challenger_speed >= challenged_speed:
            duel_state.turn_player_id = duel_state.challenger_id
        else:
            duel_state.turn_player_id = duel_state.challenged_id
        
        duel_state.phase = DuelPhase.BATTLE
        duel_state.current_turn = 1
        
        return duel_state
    
    def _calculate_speed(self, hero: DuelHero) -> int:
        """Calculate hero's speed for turn order."""
        base_speed = 100
        level_bonus = (self._get_hero_level(hero) * 2)
        speed_bonus = int(hero.skill_bonuses.get("speed_bonus", 0) * 100)
        return base_speed + level_bonus + speed_bonus + random.randint(0, 10)
    
    def _get_hero_level(self, hero: DuelHero) -> int:
        """Get effective hero level for calculations."""
        rarity_levels = {"rare": 0, "epic": 2, "legendary": 5}
        return rarity_levels.get(hero.rarity, 0) + hero.stars
    
    def execute_attack(self, duel_state: DuelState, attacker_id: int) -> Tuple[bool, str, BattleAction]:
        """Execute an attack action in the duel."""
        if duel_state.phase != DuelPhase.BATTLE:
            return False, "Duel is not in battle phase!", None
        
        if duel_state.turn_player_id != attacker_id:
            return False, "It's not your turn!", None
        
        # Get attacker and defender
        if attacker_id == duel_state.challenger_id:
            attacker = duel_state.challenger_hero
            defender = duel_state.challenged_hero
        else:
            attacker = duel_state.challenged_hero
            defender = duel_state.challenger_hero
        
        # Calculate damage and effects
        action = self._calculate_attack(attacker, defender)
        
        # Apply damage
        if not action.is_miss:
            defender.current_hp = max(0, defender.current_hp - action.damage)
        
        # Add to battle log
        duel_state.battle_log.append(action)
        
        # Check for victory
        battle_end = False
        message = ""
        
        if defender.current_hp <= 0:
            duel_state.phase = DuelPhase.RESOLUTION
            battle_end = True
            message = f"<@{attacker_id}> wins the duel!"
        elif duel_state.current_turn >= self.combat_config["max_turns"]:
            duel_state.phase = DuelPhase.RESOLUTION
            battle_end = True
            # Determine winner by HP percentage
            challenger_hp_pct = (duel_state.challenger_hero.current_hp / duel_state.challenger_hero.max_hp)
            challenged_hp_pct = (duel_state.challenged_hero.current_hp / duel_state.challenged_hero.max_hp)
            
            if challenger_hp_pct > challenged_hp_pct:
                message = f"<@{duel_state.challenger_id}> wins by timeout!"
            elif challenged_hp_pct > challenger_hp_pct:
                message = f"<@{duel_state.challenged_id}> wins by timeout!"
            else:
                message = "The duel ends in a draw!"
        else:
            # Switch turns
            if duel_state.turn_player_id == duel_state.challenger_id:
                duel_state.turn_player_id = duel_state.challenged_id
            else:
                duel_state.turn_player_id = duel_state.challenger_id
                duel_state.current_turn += 1
        
        # Apply healing if applicable
        self._apply_healing(attacker)
        if not battle_end:
            self._apply_healing(defender)
        
        success_msg = f"Attack successful! {message}" if battle_end else "Attack executed!"
        return True, success_msg, action
    
    def _calculate_attack(self, attacker: DuelHero, defender: DuelHero) -> BattleAction:
        """Calculate attack damage and effects."""
        # Base accuracy check
        accuracy = self.combat_config["base_accuracy"]
        evasion = defender.skill_bonuses.get("evasion_bonus", 0)
        hit_chance = max(0.1, accuracy - evasion)
        
        is_miss = random.random() > hit_chance
        is_critical = False
        damage = 0
        effects = []
        
        if not is_miss:
            # Calculate base damage
            base_damage = attacker.stats["atk"] - (defender.stats["def"] * self.combat_config["defense_reduction"])
            base_damage = max(attacker.stats["atk"] * self.combat_config["min_damage_ratio"], base_damage)
            
            # Element advantage
            element_multiplier = self.element_advantages.get(attacker.element, {}).get(defender.element, 1.0)
            base_damage *= element_multiplier
            
            # Critical hit check
            crit_chance = attacker.skill_bonuses.get("crit_bonus", 0)
            if random.random() < crit_chance:
                is_critical = True
                base_damage *= self.combat_config["critical_multiplier"]
                effects.append("CRITICAL HIT!")
            
            # Damage reduction
            dmg_reduction = defender.skill_bonuses.get("dmg_reduction_bonus", 0)
            base_damage *= (1 - dmg_reduction)
            
            damage = max(1, int(base_damage))
            
            # Add element advantage effect
            if element_multiplier > 1.0:
                effects.append("SUPER EFFECTIVE!")
            elif element_multiplier < 1.0:
                effects.append("Not very effective...")
        
        return BattleAction(
            attacker_id=attacker.user_id,
            defender_id=defender.user_id,
            action_type="attack",
            damage=damage,
            is_critical=is_critical,
            is_miss=is_miss,
            effects=effects
        )
    
    def _apply_healing(self, hero: DuelHero):
        """Apply HP regeneration if applicable."""
        hp_regen = hero.skill_bonuses.get("hp_regen_bonus", 0)
        if hp_regen > 0:
            heal_amount = int(hero.max_hp * hp_regen)
            hero.current_hp = min(hero.max_hp, hero.current_hp + heal_amount)
    
    def get_battle_result(self, duel_state: DuelState) -> Dict[str, Any]:
        """Determine the final battle result."""
        if duel_state.phase != DuelPhase.RESOLUTION:
            return None
        
        challenger_hp = duel_state.challenger_hero.current_hp
        challenged_hp = duel_state.challenged_hero.current_hp
        
        # Determine winner
        if challenger_hp > 0 and challenged_hp <= 0:
            winner_id = duel_state.challenger_id
            loser_id = duel_state.challenged_id
            result_type = BattleResult.VICTORY
        elif challenged_hp > 0 and challenger_hp <= 0:
            winner_id = duel_state.challenged_id
            loser_id = duel_state.challenger_id
            result_type = BattleResult.VICTORY
        else:
            # Draw or timeout decision
            challenger_hp_pct = challenger_hp / duel_state.challenger_hero.max_hp
            challenged_hp_pct = challenged_hp / duel_state.challenged_hero.max_hp
            
            if challenger_hp_pct > challenged_hp_pct:
                winner_id = duel_state.challenger_id
                loser_id = duel_state.challenged_id
                result_type = BattleResult.VICTORY
            elif challenged_hp_pct > challenger_hp_pct:
                winner_id = duel_state.challenged_id
                loser_id = duel_state.challenger_id
                result_type = BattleResult.VICTORY
            else:
                winner_id = None
                loser_id = None
                result_type = BattleResult.DRAW
        
        return {
            "winner_id": winner_id,
            "loser_id": loser_id,
            "result_type": result_type,
            "turns_taken": duel_state.current_turn,
            "battle_log": duel_state.battle_log,
            "challenger_final_hp": challenger_hp,
            "challenged_final_hp": challenged_hp,
            "challenger_element": duel_state.challenger_hero.element,
            "challenged_element": duel_state.challenged_hero.element
        }
    
    def forfeit_duel(self, duel_id: str, user_id: int) -> Tuple[bool, str]:
        """Forfeit an active duel."""
        if duel_id not in self.active_duels:
            return False, "Duel not found!"
        
        duel_state = self.active_duels[duel_id]
        
        if user_id not in [duel_state.challenger_id, duel_state.challenged_id]:
            return False, "You are not part of this duel!"
        
        # Set result as forfeit
        duel_state.phase = DuelPhase.RESOLUTION
        
        # Determine winner (opponent of forfeiter)
        if user_id == duel_state.challenger_id:
            winner_id = duel_state.challenged_id
        else:
            winner_id = duel_state.challenger_id
        
        return True, f"<@{user_id}> forfeited the duel. <@{winner_id}> wins!"
    
    def cleanup_expired_duels(self):
        """Clean up expired challenges and inactive duels."""
        now = datetime.now(timezone.utc)
        
        # Clean expired challenges
        expired_challenges = [user_id for user_id, duel in self.pending_challenges.items() 
                            if now > duel.expires_at]
        for user_id in expired_challenges:
            del self.pending_challenges[user_id]
        
        # Clean very old active duels (24+ hours)
        expired_duels = [duel_id for duel_id, duel in self.active_duels.items()
                        if (now - duel.created_at).total_seconds() > 86400]
        for duel_id in expired_duels:
            del self.active_duels[duel_id]
    
    def _is_user_in_active_duel(self, user_id: int) -> bool:
        """Check if user is in any active duel."""
        for duel in self.active_duels.values():
            if user_id in [duel.challenger_id, duel.challenged_id]:
                return True
        return False
    
    def get_user_active_duel(self, user_id: int) -> Optional[Tuple[str, DuelState]]:
        """Get user's active duel if any."""
        for duel_id, duel in self.active_duels.items():
            if user_id in [duel.challenger_id, duel.challenged_id]:
                return duel_id, duel
        return None
    
    def get_pending_challenge(self, user_id: int) -> Optional[DuelState]:
        """Get user's pending challenge if any."""
        return self.pending_challenges.get(user_id)
    
    def get_element_emoji(self, element: str) -> str:
        """Get emoji for element."""
        emoji_map = {
            "fire": "🔥",
            "water": "💧",
            "earth": "🌍",
            "air": "💨"
        }
        return emoji_map.get(element, "⚔️")

# Global instance
duel_manager = DuelManager()
