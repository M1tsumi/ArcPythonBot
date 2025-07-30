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
    
    def get_character_list(self) -> List[Dict[str, Any]]:
        """
        Get the list of all available characters.
        
        Returns:
            List of character dictionaries
        """
        if self._character_list_cache is not None:
            return self._character_list_cache
            
        character_list_file = self.characters_dir / "character_list.json"
        data = self.load_json_file(character_list_file)
        
        if data and 'characters' in data:
            self._character_list_cache = data['characters']
            return self._character_list_cache
        else:
            logger.error("Failed to load character list")
            return []
    
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
                # Load detailed character data
                char_id = char.get('id')
                if char_id:
                    char_file = self.characters_dir / f"character_{char_id}.json"
                    char_data = self.load_json_file(char_file)
                    
                    if char_data:
                        # Merge basic info with detailed data
                        char_data.update(char)
                        self._characters_cache[cache_key] = char_data
                        return char_data
                
                # If no detailed file, return basic info
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
            talent_images_dir = Path("HeroTalentImages")
            if not talent_images_dir.exists():
                return None
            
            # Normalize character name for file matching
            char_name_lower = character_name.lower().replace(' ', '').replace('(', '').replace(')', '')
            
            # Handle special cases for file matching
            if "paintedlady" in char_name_lower or "painted lady" in character_name.lower():
                char_name_lower = "katarapaintedlady"
            elif "kingbumi" in char_name_lower or "king bumi" in character_name.lower():
                char_name_lower = "kingbumi"
            elif "linbeifong" in char_name_lower or "lin beifong" in character_name.lower():
                char_name_lower = "linbeifong"
            
            # Look for both -1 and -2 versions of the talent tree
            image_1 = None
            image_2 = None
            
            for file_path in talent_images_dir.glob("*.webp"):
                filename = file_path.stem.lower()
                if filename.startswith(char_name_lower) and filename.endswith('-1'):
                    image_1 = str(file_path)
                elif filename.startswith(char_name_lower) and filename.endswith('-2'):
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