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
        self.characters_dir = self.data_dir / "characters"
        self.events_dir = self.data_dir / "events"
        
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
        return {
            "Kyoshi": {
                "skills": ["Justice & Punishment", "Meaning of Tears", "Kyoshi War Fans", "Tallest"],
                "notes": "If you're building an all-Earthbender march during the same time as you're building out your Kyoshi, I'd suggest maxing her [Tallest] skill earlier on."
            },
            "Korra": {
                "skills": ["Friendship", "Lost Connection", "Troublemaker", "Raava"],
                "notes": "[Troublemaker] and [Raava] can be swapped if desired."
            },
            "Kuvira": {
                "skills": ["Broken Beliefs", "Great Uniter", "Metal Bending", "Spirit Energy"],
                "notes": "Kuvira's [Metal Bending] skill would be ranked 2nd if you already have a hero with a leader skill in effect. This means you would max [Great Uniter] 3rd or 4th."
            },
            "Iroh": {
                "skills": ["Dragon of the West", "Remorse", "White Lotus Leader", "Taste for the Arts"],
                "notes": None
            },
            "Azula": {
                "skills": ["Blue Flames", "Unhinged", "Composure", "Kemurikage"],
                "notes": "Azula's [Kemurikage] skill would be ranked 2nd to unlock if you have a full march for her right after obtaining her. This means [Unhinged] would be maxed 3rd, and [Composure] 4th."
            },
            "Mako": {
                "skills": ["Father's Momento", "Cool Under Fire", "Motorcycle Cop", "Pro-Bender"],
                "notes": None
            },
            "Bumi": {
                "skills": ["New Power", "Punch", "Bum-Ju!", "Oddball Commander"],
                "notes": None
            },
            "King Bumi": {
                "skills": ["Wave of Earth", "Genomite Ring", "Power of Earth", "King of Omashu"],
                "notes": "[Genomite Ring] and [Power of Earth] can be swapped if desired."
            },
            "Aang": {
                "skills": ["Air Ball", "Intuition", "Glider", "Air Scooter"],
                "notes": "[Glider] and [Air Scooter] can be swapped depending on whether you are already using another hero with a leader skill in your march (Kyoshi, Korra, Kuvira)."
            },
            "Unalaq": {
                "skills": ["Soul Destruction", "Tree of Time", "Ice Drill", "Energy Conversion"],
                "notes": "[Energy Conversion] can be prioritized earlier on if you're building a healing march."
            },
            "Lin Beifong": {
                "skills": ["Grappling Hook", "Justice", "Seismic Sense", "Wrist Blade"],
                "notes": "[Seismic Sense] and [Wrist Blade] can be swapped if desired."
            },
            "Toph": {
                "skills": ["Blind Bandit", "The Fuzzy", "Badgermoles", "Distinguished Family"],
                "notes": None
            },
            "Asami": {
                "skills": ["Best Driver", "Apple of my Eye", "Electric Gloves", "Business Acumen"],
                "notes": None
            },
            "Suki": {
                "skills": ["War Fans", "Kyoshi Warrior", "The Group's Sworn", "Tenkan"],
                "notes": None
            },
            "Teo": {
                "skills": ["Operation Eclipse", "Father's Inventions", "Air Walker", "Force of Will"],
                "notes": None
            },
            "Sokka": {
                "skills": ["Hawky", "Yeah boomerang", "Master Tactician", "Inventor"],
                "notes": "Both [Inventor] and [Master Tactician] are similar in strength, so ideally I would suggest [Master Tactician] be done before [Inventor], but it could be either way."
            },
            "Zuko": {
                "skills": ["virtue and vice", "dancing dragon", "inferiority complex", "blue spirit mask"],
                "notes": None
            },
            "Borte": {
                "skills": ["Fanatic Leader", "High Priest", "Spotting Weakness", "Survival Instinct"],
                "notes": None
            },
            "Tenzin": {
                "skills": ["Awareness", "Oogi", "Tornado", "Thoughtful Defense"],
                "notes": "[Thoughtful Defense] and [Tornado] can be swapped if desired."
            },
            "Katara": {
                "skills": ["Frost Shield", "Blizzard", "Healing Water", "The Painted Lady"],
                "notes": "Putting priority on [The Painted Lady] if you already have enough benders to fill her is acceptable."
            },
            "Kuei": {
                "skills": ["Bosco!", "Peasant Life", "Scarecrow King", "Promise & Trust"],
                "notes": None
            },
            "Yue": {
                "skills": ["Child of the Moon", "Sacrifice", "Spirit Oasis", "Moon Spirit"],
                "notes": None
            },
            "Piandao": {
                "skills": ["Blacksmith", "Calligrapher", "Flaming Swords", "Lotus Tile"],
                "notes": None
            },
            "Roku": {
                "skills": ["Destiny", "Lavabending", "Final Warning", "Calm Mind"],
                "notes": "[Calm Mind] and [Final Warning] can be swapped if desired."
            },
            "Yangchen": {
                "skills": ["Air Sphere", "Cyclone Strike", "Gale", "Hurricane"],
                "notes": "[Gale] and [Hurricane] can be swapped if desired."
            },
            "Meelo": {
                "skills": ["Kid Scooter", "Consensus", "Paint Balloon", "Wind Ball"],
                "notes": None
            }
        }
    
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
            talent_types_file = Path("HeroTalentImages/TalentType.txt")
            if not talent_types_file.exists():
                return None
            
            with open(talent_types_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse the talent type information
            lines = content.split('\n')
            talent_types = {}
            
            for line in lines:
                line = line.strip()
                if ':' in line and not line.startswith('Avatar Realms Collide') and not line.startswith('This document') and not line.startswith('General Talent') and not line.startswith('Dual Purpose') and not line.startswith('Total Points') and not line.startswith('"Drawn-on"') and not line.startswith('"Crossed-out"') and not line.startswith('Future Changes') and not line.startswith('Hero Talent') and not line.startswith('Below is a list'):
                    if line.endswith(':'):
                        continue
                    parts = line.split(':')
                    if len(parts) == 2:
                        char_name = parts[0].strip()
                        talent_type = parts[1].strip()
                        talent_types[char_name.lower()] = talent_type
            
            # Get the talent type for the specific character
            char_name_lower = character_name.lower()
            
            # Handle special cases and variations
            if char_name_lower in ["katara (painted lady)", "painted lady", "katara painted lady"]:
                char_name_lower = "katara (painted lady)"
            elif char_name_lower in ["king bumi", "kingbumi"]:
                char_name_lower = "king bumi"
            elif char_name_lower == "lin beifong":
                char_name_lower = "lin beifong"
            
            if char_name_lower in talent_types:
                return {
                    'character_name': character_name,
                    'talent_type': talent_types[char_name_lower]
                }
            
            return None
            
        except Exception as e:
            print(f"Error reading talent type info: {e}")
            return None

    def get_talent_tree_images(self, character_name: str) -> Optional[Dict[str, str]]:
        """
        Get talent tree images for a specific character.
        
        Args:
            character_name: Name of the character
            
        Returns:
            Dictionary with image paths or None if not found
        """
        try:
            talent_images_dir = Path("assets/images/talents")
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

    def get_troops_data(self) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """
        Parse troops data from troops.txt file.
        
        Returns:
            Dictionary with structure: {element: {tier: troop_data}}
        """
        troops_file = Path("text files/troops.txt")
        
        if not troops_file.exists():
            logger.warning(f"Troops file not found: {troops_file}")
            return {}
        
        troops_data = {}
        current_tier = None
        
        try:
            with open(troops_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                parts = line.split('\t')
                if len(parts) < 2:
                    continue
                
                # Check if this is a tier line (starts with T1, T2, etc.)
                if parts[0].startswith('T') and parts[0][1:].isdigit():
                    current_tier = parts[0]
                    element = parts[1].strip()
                    # For tier lines, unit name is at index 2
                    unit_name = parts[2].strip() if len(parts) > 2 and parts[2].strip() else ''
                    # Recruitment costs start at index 3
                    rec_food = int(parts[3]) if len(parts) > 3 and parts[3].isdigit() else 0
                    rec_wood = int(parts[4]) if len(parts) > 4 and parts[4].isdigit() else 0
                    rec_stone = int(parts[5]) if len(parts) > 5 and parts[5].isdigit() and parts[5] != '-' else 0
                    rec_gold = int(parts[6]) if len(parts) > 6 and parts[6].isdigit() and parts[6] != '-' else 0
                    rec_time = parts[7] if len(parts) > 7 else '0m 0s'
                    # Healing costs start at index 8
                    heal_food = int(parts[8]) if len(parts) > 8 and parts[8].isdigit() else 0
                    heal_wood = int(parts[9]) if len(parts) > 9 and parts[9].isdigit() else 0
                    heal_stone = int(parts[10]) if len(parts) > 10 and parts[10].isdigit() and parts[10] != '-' else 0
                    heal_gold = int(parts[11]) if len(parts) > 11 and parts[11].isdigit() and parts[11] != '-' else 0
                    heal_time = parts[12] if len(parts) > 12 else '0m 0s'
                    # Stats start at index 13
                    power = int(parts[13]) if len(parts) > 13 and parts[13].isdigit() else 0
                    power_diff = int(parts[14]) if len(parts) > 14 and parts[14].isdigit() else 0
                    atk = int(parts[15]) if len(parts) > 15 and parts[15].isdigit() else 0
                    defense = int(parts[16]) if len(parts) > 16 and parts[16].isdigit() else 0
                    health = int(parts[17]) if len(parts) > 17 and parts[17].isdigit() else 0
                    speed = int(parts[18]) if len(parts) > 18 and parts[18].isdigit() else 0
                    load = int(parts[19]) if len(parts) > 19 and parts[19].isdigit() else 0
                # Check if this is an element line for the current tier (starts with element name)
                elif current_tier and parts[0].strip() in ['Water', 'Earth', 'Fire', 'Air']:
                    element = parts[0].strip()
                    # For element lines, unit name is at index 1
                    unit_name = parts[1].strip() if len(parts) > 1 and parts[1].strip() else ''
                    # Recruitment costs start at index 2
                    rec_food = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0
                    rec_wood = int(parts[3]) if len(parts) > 3 and parts[3].isdigit() else 0
                    rec_stone = int(parts[4]) if len(parts) > 4 and parts[4].isdigit() and parts[4] != '-' else 0
                    rec_gold = int(parts[5]) if len(parts) > 5 and parts[5].isdigit() and parts[5] != '-' else 0
                    rec_time = parts[6] if len(parts) > 6 else '0m 0s'
                    # Healing costs start at index 7
                    heal_food = int(parts[7]) if len(parts) > 7 and parts[7].isdigit() else 0
                    heal_wood = int(parts[8]) if len(parts) > 8 and parts[8].isdigit() else 0
                    heal_stone = int(parts[9]) if len(parts) > 9 and parts[9].isdigit() and parts[9] != '-' else 0
                    heal_gold = int(parts[10]) if len(parts) > 10 and parts[10].isdigit() and parts[10] != '-' else 0
                    heal_time = parts[11] if len(parts) > 11 else '0m 0s'
                    # Stats start at index 12
                    power = int(parts[12]) if len(parts) > 12 and parts[12].isdigit() else 0
                    power_diff = int(parts[13]) if len(parts) > 13 and parts[13].isdigit() else 0
                    atk = int(parts[14]) if len(parts) > 14 and parts[14].isdigit() else 0
                    defense = int(parts[15]) if len(parts) > 15 and parts[15].isdigit() else 0
                    health = int(parts[16]) if len(parts) > 16 and parts[16].isdigit() else 0
                    speed = int(parts[17]) if len(parts) > 17 and parts[17].isdigit() else 0
                    load = int(parts[18]) if len(parts) > 18 and parts[18].isdigit() else 0
                else:
                    continue
                
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
                    'healing_costs': {
                        'food': heal_food,
                        'wood': heal_wood,
                        'stone': heal_stone,
                        'gold': heal_gold,
                        'time': heal_time
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
        
        return troops_data 