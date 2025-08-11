"""
JSON Handler utility for Avatar Realms Collide Discord Bot.
Handles JSON file operations, validation, and data management.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from datetime import datetime, timezone
import asyncio
import aiofiles

from .file_handler import FileHandler

class JSONHandler:
    """Handles JSON file operations with validation and error handling."""
    
    def __init__(self, file_handler: Optional[FileHandler] = None):
        self.file_handler = file_handler or FileHandler()
        self.logger = logging.getLogger(__name__)
    
    def load_json(self, *path_parts: str, default: Any = None) -> Any:
        """Load JSON data from a file."""
        try:
            content = self.file_handler.read_file(*path_parts)
            if content is None:
                return default
            
            return json.loads(content)
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON decode error in {path_parts}: {e}")
            return default
        except Exception as e:
            self.logger.error(f"Error loading JSON {path_parts}: {e}")
            return default
    
    def save_json(self, data: Any, *path_parts: str, indent: int = 2, ensure_ascii: bool = False) -> bool:
        """Save data to a JSON file."""
        try:
            json_str = json.dumps(data, indent=indent, ensure_ascii=ensure_ascii, default=self._json_serializer)
            return self.file_handler.write_file(*path_parts, content=json_str)
        except Exception as e:
            self.logger.error(f"Error saving JSON {path_parts}: {e}")
            return False
    
    def _json_serializer(self, obj):
        """Custom JSON serializer for datetime objects."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    def update_json(self, updates: Dict[str, Any], *path_parts: str, create_if_missing: bool = True) -> bool:
        """Update specific fields in a JSON file."""
        try:
            current_data = self.load_json(*path_parts, default={})
            if not isinstance(current_data, dict):
                current_data = {}
            
            # Deep merge updates
            self._deep_merge(current_data, updates)
            
            return self.save_json(current_data, *path_parts)
        except Exception as e:
            self.logger.error(f"Error updating JSON {path_parts}: {e}")
            return False
    
    def _deep_merge(self, target: Dict[str, Any], source: Dict[str, Any]):
        """Deep merge two dictionaries."""
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_merge(target[key], value)
            else:
                target[key] = value
    
    def get_value(self, key_path: List[str], *path_parts: str, default: Any = None) -> Any:
        """Get a nested value from JSON using a key path."""
        try:
            data = self.load_json(*path_parts)
            if data is None:
                return default
            
            current = data
            for key in key_path:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    return default
            
            return current
        except Exception as e:
            self.logger.error(f"Error getting value {key_path} from {path_parts}: {e}")
            return default
    
    def set_value(self, key_path: List[str], value: Any, *path_parts: str) -> bool:
        """Set a nested value in JSON using a key path."""
        try:
            data = self.load_json(*path_parts, default={})
            if not isinstance(data, dict):
                data = {}
            
            current = data
            for key in key_path[:-1]:
                if key not in current or not isinstance(current[key], dict):
                    current[key] = {}
                current = current[key]
            
            current[key_path[-1]] = value
            return self.save_json(data, *path_parts)
        except Exception as e:
            self.logger.error(f"Error setting value {key_path} in {path_parts}: {e}")
            return False
    
    def delete_key(self, key_path: List[str], *path_parts: str) -> bool:
        """Delete a key from JSON using a key path."""
        try:
            data = self.load_json(*path_parts)
            if data is None or not isinstance(data, dict):
                return False
            
            current = data
            for key in key_path[:-1]:
                if key not in current or not isinstance(current[key], dict):
                    return False
                current = current[key]
            
            if key_path[-1] in current:
                del current[key_path[-1]]
                return self.save_json(data, *path_parts)
            
            return False
        except Exception as e:
            self.logger.error(f"Error deleting key {key_path} from {path_parts}: {e}")
            return False
    
    def append_to_list(self, list_key: str, item: Any, *path_parts: str) -> bool:
        """Append an item to a list in JSON."""
        try:
            data = self.load_json(*path_parts, default={})
            if not isinstance(data, dict):
                data = {}
            
            if list_key not in data or not isinstance(data[list_key], list):
                data[list_key] = []
            
            data[list_key].append(item)
            return self.save_json(data, *path_parts)
        except Exception as e:
            self.logger.error(f"Error appending to list {list_key} in {path_parts}: {e}")
            return False
    
    def remove_from_list(self, list_key: str, item: Any, *path_parts: str) -> bool:
        """Remove an item from a list in JSON."""
        try:
            data = self.load_json(*path_parts)
            if data is None or not isinstance(data, dict):
                return False
            
            if list_key not in data or not isinstance(data[list_key], list):
                return False
            
            if item in data[list_key]:
                data[list_key].remove(item)
                return self.save_json(data, *path_parts)
            
            return False
        except Exception as e:
            self.logger.error(f"Error removing from list {list_key} in {path_parts}: {e}")
            return False
    
    def increment_counter(self, counter_key: str, increment: int = 1, *path_parts: str) -> Optional[int]:
        """Increment a counter in JSON."""
        try:
            data = self.load_json(*path_parts, default={})
            if not isinstance(data, dict):
                data = {}
            
            if counter_key not in data:
                data[counter_key] = 0
            
            if not isinstance(data[counter_key], (int, float)):
                data[counter_key] = 0
            
            data[counter_key] += increment
            
            if self.save_json(data, *path_parts):
                return data[counter_key]
            return None
        except Exception as e:
            self.logger.error(f"Error incrementing counter {counter_key} in {path_parts}: {e}")
            return None
    
    def validate_json_schema(self, data: Any, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Validate JSON data against a simple schema."""
        errors = []
        
        def validate_field(value, field_schema, path=""):
            if "type" in field_schema:
                expected_type = field_schema["type"]
                if expected_type == "dict" and not isinstance(value, dict):
                    errors.append(f"{path}: Expected dict, got {type(value).__name__}")
                elif expected_type == "list" and not isinstance(value, list):
                    errors.append(f"{path}: Expected list, got {type(value).__name__}")
                elif expected_type == "str" and not isinstance(value, str):
                    errors.append(f"{path}: Expected str, got {type(value).__name__}")
                elif expected_type == "int" and not isinstance(value, int):
                    errors.append(f"{path}: Expected int, got {type(value).__name__}")
                elif expected_type == "float" and not isinstance(value, (int, float)):
                    errors.append(f"{path}: Expected float, got {type(value).__name__}")
                elif expected_type == "bool" and not isinstance(value, bool):
                    errors.append(f"{path}: Expected bool, got {type(value).__name__}")
            
            if "required" in field_schema and field_schema["required"] and value is None:
                errors.append(f"{path}: Required field is missing or null")
            
            if "min" in field_schema and isinstance(value, (int, float)) and value < field_schema["min"]:
                errors.append(f"{path}: Value {value} is less than minimum {field_schema['min']}")
            
            if "max" in field_schema and isinstance(value, (int, float)) and value > field_schema["max"]:
                errors.append(f"{path}: Value {value} is greater than maximum {field_schema['max']}")
            
            if "min_length" in field_schema and isinstance(value, (str, list)) and len(value) < field_schema["min_length"]:
                errors.append(f"{path}: Length {len(value)} is less than minimum {field_schema['min_length']}")
            
            if "max_length" in field_schema and isinstance(value, (str, list)) and len(value) > field_schema["max_length"]:
                errors.append(f"{path}: Length {len(value)} is greater than maximum {field_schema['max_length']}")
        
        def validate_object(obj, obj_schema, path=""):
            if not isinstance(obj, dict):
                errors.append(f"{path}: Expected dict, got {type(obj).__name__}")
                return
            
            for field_name, field_schema in obj_schema.get("fields", {}).items():
                field_path = f"{path}.{field_name}" if path else field_name
                field_value = obj.get(field_name)
                validate_field(field_value, field_schema, field_path)
        
        validate_object(data, schema)
        return {"valid": len(errors) == 0, "errors": errors}
    
    async def async_load_json(self, *path_parts: str, default: Any = None) -> Any:
        """Asynchronously load JSON data from a file."""
        try:
            content = await self.file_handler.async_read_file(*path_parts)
            if content is None:
                return default
            
            return json.loads(content)
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON decode error in {path_parts}: {e}")
            return default
        except Exception as e:
            self.logger.error(f"Error async loading JSON {path_parts}: {e}")
            return default
    
    async def async_save_json(self, data: Any, *path_parts: str, indent: int = 2, ensure_ascii: bool = False) -> bool:
        """Asynchronously save data to a JSON file."""
        try:
            json_str = json.dumps(data, indent=indent, ensure_ascii=ensure_ascii, default=self._json_serializer)
            return await self.file_handler.async_write_file(*path_parts, content=json_str)
        except Exception as e:
            self.logger.error(f"Error async saving JSON {path_parts}: {e}")
            return False
    
    def backup_json(self, *path_parts: str) -> bool:
        """Create a backup of a JSON file."""
        return self.file_handler.backup_file(*path_parts)
    
    def get_json_info(self, *path_parts: str) -> Dict[str, Any]:
        """Get information about a JSON file."""
        try:
            file_path = self.file_handler.get_file_path(*path_parts)
            if not file_path.exists():
                return {"exists": False}
            
            data = self.load_json(*path_parts)
            file_size = self.file_handler.get_file_size(*path_parts)
            
            return {
                "exists": True,
                "size_bytes": file_size,
                "size_mb": file_size / (1024 * 1024) if file_size else 0,
                "data_type": type(data).__name__,
                "is_dict": isinstance(data, dict),
                "is_list": isinstance(data, list),
                "dict_keys": list(data.keys()) if isinstance(data, dict) else None,
                "list_length": len(data) if isinstance(data, list) else None
            }
        except Exception as e:
            self.logger.error(f"Error getting JSON info {path_parts}: {e}")
            return {"exists": False, "error": str(e)}

# Global instance
json_handler = JSONHandler()
