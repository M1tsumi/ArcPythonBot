"""
Data parser utility for loading and parsing game data from JSON files.
"""

import json
import os
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class DataParser:
    """Utility class for parsing game data from JSON files."""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the data parser.
        
        Args:
            data_dir: Directory containing data files
        """
        self.data_dir = Path(data_dir)
        self.characters_dir = self.data_dir / "game" / "characters"
        self.events_dir = self.data_dir / "game" / "events"
        self.skill_priorities_dir = self.characters_dir / "skill_priorities"
        self.talent_data_dir = self.characters_dir / "talent_data"
        
        # Cache for loaded data
        self._characters_cache = {}
        self._events_cache = {}
        self._character_list_cache = None
        
    def load_json_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        Load and parse a JSON file.
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            Dict containing the parsed JSON data or None if failed
        """
        try:
            if not file_path.exists():
                logger.warning(f"File not found: {file_path}")
                return None
                
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info(f"Successfully loaded: {file_path}")
                return data
                
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in {file_path}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
            return None
    
    def get_skill_priorities(self) -> Dict[str, Dict[str, Any]]:
        """
        Get skill priorities for all characters.
        
        Returns:
            Dictionary with character names as keys and skill priority data as values
        """
        skill_priorities_file = self.skill_priorities_dir / "skill_priorities.json"
        skill_data = self.load_json_file(skill_priorities_file)
        
        if skill_data and 'skill_priorities' in skill_data:
            return skill_data['skill_priorities']
        
        # Fallback to empty dict if file not found
        logger.warning("Skill priorities file not found, returning empty dict")
        return {}
    
    def get_character_list(self) -> List[Dict[str, Any]]:
        """
        Get the list of all available characters.
        
        Returns:
            List of character dictionaries
        """
        if self._character_list_cache is not None:
            return self._character_list_cache
            
        # Return Avatar characters with their correct primary elements and unlock sources
        avatar_characters = [
            # Firebenders
            {"name": "Zuko", "element": "Fire", "category": "Firebender", "rarity": "Epic", "description": "Fire Nation prince and Firebending master", "unlock_sources": ["Avatar Day Exchange", "Scrolls", "Starter Hero (Fire)", "Trail Shop"]},
            {"name": "Azula", "element": "Fire", "category": "Firebender", "rarity": "Legendary", "description": "Firebending prodigy and Fire Nation princess", "unlock_sources": ["Top Up Rewards", "VIP Chests"]},
            {"name": "Iroh", "element": "Fire", "category": "Firebender", "rarity": "Legendary", "description": "Wise Firebending master and Dragon of the West", "unlock_sources": ["Golden Scroll", "Wheel of Fate"]},
            {"name": "Roku", "element": "Fire", "category": "Avatar", "rarity": "Legendary", "description": "Fire Nation Avatar of balance and wisdom", "unlock_sources": ["Daily Deals", "The Greatest Leader"]},
            {"name": "Asami", "element": "Fire", "category": "Inventor", "rarity": "Epic", "description": "Genius inventor and Fire Nation engineer", "unlock_sources": ["Scrolls"]},
            
            # Waterbenders
            {"name": "Katara", "element": "Water", "category": "Waterbender", "rarity": "Epic", "description": "Master Waterbender and skilled healer", "unlock_sources": ["Avatar Day Exchange", "Scrolls", "Starter Hero (Water)", "Trail Shop"]},
            {"name": "Yue", "element": "Water", "category": "Spirit", "rarity": "Rare", "description": "Moon spirit and Water Tribe princess", "unlock_sources": ["Silver Scroll"]},
            {"name": "Katara (Painted Lady)", "element": "Water", "category": "Waterbender", "rarity": "Legendary", "description": "Katara as the mysterious Painted Lady", "unlock_sources": ["Wheel of Fate"]},
            {"name": "Unalaq", "element": "Water", "category": "Waterbender", "rarity": "Legendary", "description": "Dark Waterbending master and spiritual leader", "unlock_sources": ["Daily Deals", "Unalaq Pass (26 days after server start)"]},
            {"name": "Korra", "element": "Water", "category": "Avatar", "rarity": "Legendary", "description": "Water Tribe Avatar of the modern era", "unlock_sources": ["Hall of Avatars", "Daily Deals", "The Greatest Leader"]},
            {"name": "Sokka", "element": "Water", "category": "Warrior", "rarity": "Epic", "description": "Strategic warrior and tactical leader", "unlock_sources": ["First Hero you unlock", "Scrolls"]},
            
            # Earthbenders
            {"name": "Toph", "element": "Earth", "category": "Earthbender", "rarity": "Epic", "description": "Blind Earthbending master and Metalbender", "unlock_sources": ["Avatar Day Exchange", "Scrolls", "Starter Hero (Earth)", "Trail Shop"]},
            {"name": "Bumi", "element": "Air", "category": "Airbender", "rarity": "Legendary", "description": "Eccentric Airbending master and king", "unlock_sources": ["Expedition", "Golden Scroll", "Login Event", "Trail Shop"]},
            {"name": "King Bumi", "element": "Earth", "category": "Earthbender", "rarity": "Legendary", "description": "Earthbending king and master strategist", "unlock_sources": ["Wheel of Fate"]},
            {"name": "Kyoshi", "element": "Earth", "category": "Avatar", "rarity": "Legendary", "description": "Legendary Earth Kingdom Avatar of justice", "unlock_sources": ["Daily Deals", "The Greatest Leader"]},
            {"name": "Lin Beifong", "element": "Earth", "category": "Earthbender", "rarity": "Legendary", "description": "Metalbending police chief and protector", "unlock_sources": ["Wheel of Fate"]},
            {"name": "Teo", "element": "Earth", "category": "Inventor", "rarity": "Epic", "description": "Air Nomad inventor and mechanical genius", "unlock_sources": ["Expedition", "Scrolls"]},
            
            # Airbenders
            {"name": "Aang", "element": "Air", "category": "Avatar", "rarity": "Legendary", "description": "The last Airbender and Avatar of the world", "unlock_sources": ["Hall of Avatars", "Daily Deals", "The Greatest Leader", "Trail Shop"]},
            {"name": "Tenzin", "element": "Air", "category": "Airbender", "rarity": "Epic", "description": "Airbending master and spiritual teacher", "unlock_sources": ["Avatar Day Exchange", "Scrolls", "Starter Hero (Air)", "Trail Shop"]},
            {"name": "Meelo", "element": "Air", "category": "Airbender", "rarity": "Rare", "description": "Young Airbending prodigy and energetic warrior", "unlock_sources": ["Silver Scroll"]},
            {"name": "Yangchen", "element": "Air", "category": "Avatar", "rarity": "Legendary", "description": "Ancient Air Nomad Avatar of wisdom", "unlock_sources": ["Daily Deals", "The Greatest Leader"]},
            
            # Additional characters with corrected elements and rarities
            {"name": "Suki", "element": "Earth", "category": "Warrior", "rarity": "Epic", "description": "Kyoshi Warrior leader and skilled fighter", "unlock_sources": ["Scrolls", "Rookie Leader Event"]},
            {"name": "Piandao", "element": "Fire", "category": "Warrior", "rarity": "Rare", "description": "Master swordsman and Fire Nation instructor", "unlock_sources": ["Silver Scroll"]},
            {"name": "Borte", "element": "Air", "category": "Warrior", "rarity": "Epic", "description": "Water Tribe warrior and fierce protector", "unlock_sources": ["Borte's Scheme"]},
            {"name": "Kuei", "element": "Earth", "category": "Leader", "rarity": "Rare", "description": "Earth Kingdom king and diplomatic leader", "unlock_sources": ["Silver Scroll"]},
            {"name": "Amon", "element": "Water", "category": "Leader", "rarity": "Legendary", "description": "Equalist leader and revolutionary", "unlock_sources": ["Daily Deals", "The Greatest Leader"]}
        ]
        
        self._character_list_cache = avatar_characters
        return self._character_list_cache
    
    def get_character(self, character_name: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific character.
        
        Args:
            character_name: Name of the character (case-insensitive)
            
        Returns:
            Character data dictionary or None if not found
        """
        # Check cache first
        cache_key = character_name.lower()
        if cache_key in self._characters_cache:
            return self._characters_cache[cache_key]
        
        # Load character list to find the character
        characters = self.get_character_list()
        
        for char in characters:
            if char.get('name', '').lower() == cache_key:
                # Return the character data directly since we have it in the list
                self._characters_cache[cache_key] = char
                return char
        
        return None
    
    def get_character_skills(self, character_name: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get skills for a specific character.
        
        Args:
            character_name: Name of the character
            
        Returns:
            List of skill dictionaries or None if not found
        """
        character = self.get_character(character_name)
        if character and 'skills' in character:
            return character['skills']
        return None
    
    def get_character_talents(self, character_name: str) -> Optional[Dict[str, Any]]:
        """
        Get talent tree for a specific character.
        
        Args:
            character_name: Name of the character
            
        Returns:
            Talent tree data or None if not found
        """
        character = self.get_character(character_name)
        if character and 'talents' in character:
            return character['talents']
        return None

    def get_talent_type_info(self, character_name: str) -> Optional[Dict[str, Any]]:
        """
        Get talent type information for a specific character.
        
        Args:
            character_name: Name of the character
            
        Returns:
            Talent type information or None if not found
        """
        try:
            talent_types_file = self.talent_data_dir / "talent_types.json"
            talent_data = self.load_json_file(talent_types_file)
            
            if not talent_data or 'talent_types' not in talent_data:
                return None
            
            talent_types = talent_data['talent_types']
            
            # Get the talent type for the specific character
            char_name_lower = character_name.lower()
            
            # Handle special cases and variations
            if char_name_lower in ["katara (painted lady)", "painted lady", "katara painted lady"]:
                char_name_lower = "katara (painted lady)"
            elif char_name_lower in ["king bumi", "kingbumi"]:
                char_name_lower = "king bumi"
            elif char_name_lower == "lin beifong":
                char_name_lower = "lin beifong"
            
            # Find matching character (case-insensitive)
            for char_key, talent_type in talent_types.items():
                if char_key.lower() == char_name_lower:
                    return {
                        'character_name': character_name,
                        'talent_type': talent_type,
                        'metadata': talent_data.get('metadata', {})
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Error reading talent type info: {e}")
            return None

    def get_talent_tree_categories(self) -> Dict[str, Any]:
        """
        Get talent tree categories and their descriptions.
        
        Returns:
            Dictionary with talent tree categories and metadata
        """
        try:
            talent_types_file = self.talent_data_dir / "talent_types.json"
            talent_data = self.load_json_file(talent_types_file)
            
            if talent_data and 'tree_categories' in talent_data:
                return {
                    'categories': talent_data['tree_categories'],
                    'metadata': talent_data.get('metadata', {})
                }
            
            return {'categories': {}, 'metadata': {}}
            
        except Exception as e:
            logger.error(f"Error reading talent tree categories: {e}")
            return {'categories': {}, 'metadata': {}}

    def get_talent_tree_images(self, character_name: str) -> Optional[Dict[str, str]]:
        """
        Get talent tree images for a specific character.
        
        Args:
            character_name: Name of the character
            
        Returns:
            Dictionary with image paths or None if not found
        """
        try:
            talent_images_dir = Path("assets/images/characters/talents")
            if not talent_images_dir.exists():
                return None
            
            # Create a mapping of display names to file names
            name_mapping = {
                "kyoshi": "kyoshi",
                "bumi": "bumi",
                "korra": "korra",
                "toph": "toph",
                "azula": "azula",
                "iroh": "iroh",
                "asami": "asami",
                "sokka": "sokka",
                "suki": "suki",
                "zuko": "zuko",
                "katara": "katara",
                "tenzin": "tenzin",
                "teo": "teo",
                "borte": "borte",
                "aang": "aang",
                "kuei": "kuei",
                "meelo": "meelo",
                "piandao": "piandao",
                "yue": "yue",
                "amon": "amon",
                "king bumi": "kingbumi",
                "kingbumi": "kingbumi",
                "yangchen": "yangchen",
                "katara (painted lady)": "katarapaintedlady",
                "painted lady": "katarapaintedlady",
                "katara painted lady": "katarapaintedlady",
                "unalaq": "unalaq",
                "roku": "roku",
                "lin beifong": "linbeifong",
                "linbeifong": "linbeifong"
            }
            
            # Normalize the character name
            char_name_lower = character_name.lower().strip()
            
            # Get the file name from the mapping
            file_name = name_mapping.get(char_name_lower)
            if not file_name:
                return None
            
            # Look for both -1 and -2 versions of the talent tree
            image_1 = None
            image_2 = None
            
            for file_path in talent_images_dir.glob("*.webp"):
                filename = file_path.stem.lower()
                if filename == f"{file_name}-1":
                    image_1 = str(file_path)
                elif filename == f"{file_name}-2":
                    image_2 = str(file_path)
            
            if image_1 or image_2:
                return {
                    'talent_tree_1': image_1,
                    'talent_tree_2': image_2
                }
            
            return None
            
        except Exception as e:
            print(f"Error getting talent tree images: {e}")
            return None

    def get_all_character_names(self) -> List[str]:
        """
        Get all available character names for dropdown.
        
        Returns:
            List of character names
        """
        return [
            "Kyoshi",
            "Bumi",
            "Korra", 
            "Toph",
            "Azula",
            "Iroh",
            "Asami",
            "Sokka",
            "Suki",
            "Zuko",
            "Katara",
            "Tenzin",
            "Teo",
            "Borte",
            "Aang",
            "Kuei",
            "Meelo",
            "Piandao",
            "Yue",
            "Amon",
            "King Bumi",
            "Yangchen",
            "Katara (Painted Lady)",
            "Unalaq",
            "Roku",
            "Lin Beifong"
        ]
    
    def get_events(self, event_type: str = "current") -> List[Dict[str, Any]]:
        """
        Get events of a specific type.
        
        Args:
            event_type: Type of events to get ("current", "past", "all")
            
        Returns:
            List of event dictionaries
        """
        if event_type in self._events_cache:
            return self._events_cache[event_type]
        
        events = []
        
        if event_type in ["current", "all"]:
            current_file = self.events_dir / "current_events.json"
            current_data = self.load_json_file(current_file)
            if current_data and 'events' in current_data:
                events.extend(current_data['events'])
        
        if event_type in ["past", "all"]:
            past_file = self.events_dir / "past_events.json"
            past_data = self.load_json_file(past_file)
            if past_data and 'events' in past_data:
                events.extend(past_data['events'])
        
        self._events_cache[event_type] = events
        return events
    
    def get_event(self, event_name: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific event.
        
        Args:
            event_name: Name of the event (case-insensitive)
            
        Returns:
            Event data dictionary or None if not found
        """
        events = self.get_events("all")
        
        for event in events:
            if event.get('name', '').lower() == event_name.lower():
                return event
        
        return None
    
    def search_characters(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Search for characters by name or description.
        
        Args:
            search_term: Search term to match against character names/descriptions
            
        Returns:
            List of matching character dictionaries
        """
        characters = self.get_character_list()
        search_term = search_term.lower()
        matches = []
        
        for char in characters:
            name = char.get('name', '').lower()
            description = char.get('description', '').lower()
            
            if search_term in name or search_term in description:
                matches.append(char)
        
        return matches
    
    def get_character_names(self) -> List[str]:
        """
        Get a list of all character names.
        
        Returns:
            List of character names
        """
        characters = self.get_character_list()
        return [char.get('name', '') for char in characters if char.get('name')]
    
    def clear_cache(self):
        """Clear all cached data."""
        self._characters_cache.clear()
        self._events_cache.clear()
        self._character_list_cache = None
        logger.info("Data cache cleared")
    
    def reload_data(self):
        """Reload all data from files."""
        self.clear_cache()
        # Force reload by calling get methods
        self.get_character_list()
        self.get_events("all")
        logger.info("Data reloaded from files") 

    def get_troops_data_fixed(self) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """
        Parse troops data from troops.txt file with correct format handling.
        
        Returns:
            Dictionary with structure: {element: {tier: troop_data}}
        """
        troops_file = Path("data/game/text_data/troops.txt")
        
        if not troops_file.exists():
            logger.warning(f"Troops file not found: {troops_file}")
            return {}
        
        troops_data = {}
        
        try:
            with open(troops_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Split content into lines and clean up
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            logger.info(f"Loaded {len(lines)} lines from troops file")
            
            current_tier = None
            
            for i, line in enumerate(lines):
                # Skip header lines
                if line.startswith('Unit') or line.startswith('Research') or line.startswith('Food'):
                    continue
                    
                # Split by tabs and keep all parts (including empty ones)
                parts = line.split('\t')
                
                if len(parts) < 8:
                    continue
                
                # Check if this is a tier line (starts with T1, T2, etc.)
                if parts[0].strip().startswith('T') and parts[0].strip()[1:].isdigit():
                    current_tier = parts[0].strip()
                    continue
                
                # Check if this is an element line (indented under tier)
                if parts[0].strip() in ['Water', 'Earth', 'Fire', 'Air']:
                    element = parts[0].strip()
                    
                    # Determine the column offsets based on the number of parts
                    # Some lines have the tier prefix, others don't
                    if len(parts) >= 20:  # Lines with tier prefix (T2, T3, etc.)
                        unit_name_col = 2
                        food_col = 3
                        wood_col = 4
                        stone_col = 5
                        gold_col = 6
                        time_col = 7
                    else:  # Lines without tier prefix (shifted by 1)
                        unit_name_col = 1
                        food_col = 2
                        wood_col = 3
                        stone_col = 4
                        gold_col = 5
                        time_col = 6
                    
                    # For T1 units, the Research column is empty, so we use the element name
                    # For T2-T6 units, the Research column contains the unit name
                    unit_name = parts[unit_name_col].strip() if len(parts) > unit_name_col and parts[unit_name_col].strip() and parts[unit_name_col].strip() != element and not parts[unit_name_col].strip().isdigit() else element
                    
                    # Recruitment costs using dynamic column indices
                    rec_food = int(parts[food_col].strip()) if len(parts) > food_col and parts[food_col].strip().isdigit() else 0
                    rec_wood = int(parts[wood_col].strip()) if len(parts) > wood_col and parts[wood_col].strip().isdigit() and parts[wood_col].strip() != '-' else 0
                    rec_stone = int(parts[stone_col].strip()) if len(parts) > stone_col and parts[stone_col].strip().isdigit() and parts[stone_col].strip() != '-' else 0
                    rec_gold = int(parts[gold_col].strip()) if len(parts) > gold_col and parts[gold_col].strip().isdigit() and parts[gold_col].strip() != '-' else 0
                    rec_time = parts[time_col].strip() if len(parts) > time_col and parts[time_col].strip() else '0m 0s'
                    
                    # Stats - need to adjust based on the number of parts
                    # For lines with 20 parts: stats start at 13
                    # For lines with 19 parts: stats start at 12
                    if len(parts) >= 20:
                        power_col = 13
                        power_diff_col = 14
                        atk_col = 15
                        def_col = 16
                        health_col = 17
                        speed_col = 18
                        load_col = 19
                    else:
                        power_col = 12
                        power_diff_col = 13
                        atk_col = 14
                        def_col = 15
                        health_col = 16
                        speed_col = 17
                        load_col = 18
                    
                    power = int(parts[power_col].strip()) if len(parts) > power_col and parts[power_col].strip().isdigit() else 0
                    power_diff = int(parts[power_diff_col].strip()) if len(parts) > power_diff_col and parts[power_diff_col].strip().isdigit() else 0
                    atk = int(parts[atk_col].strip()) if len(parts) > atk_col and parts[atk_col].strip().isdigit() else 0
                    defense = int(parts[def_col].strip()) if len(parts) > def_col and parts[def_col].strip().isdigit() else 0
                    health = int(parts[health_col].strip()) if len(parts) > health_col and parts[health_col].strip().isdigit() else 0
                    speed = int(parts[speed_col].strip()) if len(parts) > speed_col and parts[speed_col].strip().isdigit() else 0
                    load = int(parts[load_col].strip()) if len(parts) > load_col and parts[load_col].strip().isdigit() else 0
                    
                    if element not in troops_data:
                        troops_data[element] = {}
                    
                    troop_data = {
                        'tier': current_tier,
                        'element': element,
                        'unit_name': unit_name,
                        'recruitment_costs': {
                            'food': rec_food,
                            'wood': rec_wood,
                            'stone': rec_stone,
                            'gold': rec_gold,
                            'time': rec_time
                        },
                        'power': power,
                        'power_diff': power_diff,
                        'atk': atk,
                        'def': defense,
                        'health': health,
                        'speed': speed,
                        'load': load
                    }
                    
                    troops_data[element][current_tier] = troop_data
                    
        except Exception as e:
            logger.error(f"Error parsing troops data: {e}")
            return {}
        
        logger.info(f"Successfully parsed troops data: {len(troops_data)} elements")
        for element, tiers in troops_data.items():
            logger.info(f"  {element}: {len(tiers)} tiers")
        
        return troops_data

    def get_troops_data(self) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """
        Parse troops data from troops.txt file.
        
        Returns:
            Dictionary with structure: {element: {tier: troop_data}}
        """
        # Use the fixed version for consistency
        return self.get_troops_data_fixed() 