"""
File Handler utility for Avatar Realms Collide Discord Bot.
Handles file operations, validation, and management.
"""

import os
import json
import aiofiles
import asyncio
from pathlib import Path
from typing import Any, Dict, Optional, Union
import logging

logger = logging.getLogger(__name__)

class FileHandler:
    """Synchronous file handler for basic file operations."""
    
    def __init__(self, base_path: str = "data"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def ensure_directory(self, directory: str) -> Path:
        """Ensure a directory exists and return the path."""
        dir_path = self.base_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path
    
    def write_json(self, file_path: str, data: Any, indent: int = 2) -> bool:
        """Write data to a JSON file."""
        try:
            full_path = self.base_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Error writing JSON file {file_path}: {e}")
            return False
    
    def read_json(self, file_path: str, default: Any = None) -> Any:
        """Read data from a JSON file."""
        try:
            full_path = self.base_path / file_path
            if not full_path.exists():
                return default
            
            with open(full_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading JSON file {file_path}: {e}")
            return default
    
    def write_text(self, file_path: str, content: str, encoding: str = 'utf-8') -> bool:
        """Write text content to a file."""
        try:
            full_path = self.base_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, 'w', encoding=encoding) as f:
                f.write(content)
            return True
        except Exception as e:
            logger.error(f"Error writing text file {file_path}: {e}")
            return False
    
    def read_text(self, file_path: str, encoding: str = 'utf-8', default: str = "") -> str:
        """Read text content from a file."""
        try:
            full_path = self.base_path / file_path
            if not full_path.exists():
                return default
            
            with open(full_path, 'r', encoding=encoding) as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading text file {file_path}: {e}")
            return default
    
    def write_binary(self, file_path: str, content: bytes) -> bool:
        """Write binary content to a file."""
        try:
            full_path = self.base_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, 'wb') as f:
                f.write(content)
            return True
        except Exception as e:
            logger.error(f"Error writing binary file {file_path}: {e}")
            return False
    
    def read_binary(self, file_path: str) -> Optional[bytes]:
        """Read binary content from a file."""
        try:
            full_path = self.base_path / file_path
            if not full_path.exists():
                return None
            
            with open(full_path, 'rb') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading binary file {file_path}: {e}")
            return None
    
    def file_exists(self, file_path: str) -> bool:
        """Check if a file exists."""
        return (self.base_path / file_path).exists()
    
    def delete_file(self, file_path: str) -> bool:
        """Delete a file."""
        try:
            full_path = self.base_path / file_path
            if full_path.exists():
                full_path.unlink()
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {e}")
            return False

class AsyncFileHandler:
    """Asynchronous file handler for non-blocking file operations."""
    
    def __init__(self, base_path: str = "data"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self._executor = None
    
    def _get_executor(self):
        """Get or create a thread executor for blocking operations."""
        if self._executor is None:
            self._executor = asyncio.get_event_loop().run_in_executor
        return self._executor
    
    async def ensure_directory(self, directory: str) -> Path:
        """Ensure a directory exists and return the path."""
        dir_path = self.base_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path
    
    async def write_json(self, file_path: str, data: Any, indent: int = 2) -> bool:
        """Write data to a JSON file asynchronously."""
        try:
            full_path = self.base_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            async with aiofiles.open(full_path, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(data, indent=indent, ensure_ascii=False))
            return True
        except Exception as e:
            logger.error(f"Error writing JSON file {file_path}: {e}")
            return False
    
    async def read_json(self, file_path: str, default: Any = None) -> Any:
        """Read data from a JSON file asynchronously."""
        try:
            full_path = self.base_path / file_path
            if not full_path.exists():
                return default
            
            async with aiofiles.open(full_path, 'r', encoding='utf-8') as f:
                content = await f.read()
                return json.loads(content)
        except Exception as e:
            logger.error(f"Error reading JSON file {file_path}: {e}")
            return False
    
    async def write_text(self, file_path: str, content: str, encoding: str = 'utf-8') -> bool:
        """Write text content to a file asynchronously."""
        try:
            full_path = self.base_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            async with aiofiles.open(full_path, 'w', encoding=encoding) as f:
                await f.write(content)
            return True
        except Exception as e:
            logger.error(f"Error writing text file {file_path}: {e}")
            return False
    
    async def read_text(self, file_path: str, encoding: str = 'utf-8', default: str = "") -> str:
        """Read text content from a file asynchronously."""
        try:
            full_path = self.base_path / file_path
            if not full_path.exists():
                return default
            
            async with aiofiles.open(full_path, 'r', encoding=encoding) as f:
                return await f.read()
        except Exception as e:
            logger.error(f"Error reading text file {file_path}: {e}")
            return default
    
    async def write_binary(self, file_path: str, content: bytes) -> bool:
        """Write binary content to a file asynchronously."""
        try:
            full_path = self.base_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            async with aiofiles.open(full_path, 'wb') as f:
                await f.write(content)
            return True
        except Exception as e:
            logger.error(f"Error writing binary file {file_path}: {e}")
            return False
    
    async def read_binary(self, file_path: str) -> Optional[bytes]:
        """Read binary content from a file asynchronously."""
        try:
            full_path = self.base_path / file_path
            if not full_path.exists():
                return None
            
            async with aiofiles.open(full_path, 'rb') as f:
                return await f.read()
        except Exception as e:
            logger.error(f"Error reading binary file {file_path}: {e}")
            return None
    
    async def file_exists(self, file_path: str) -> bool:
        """Check if a file exists."""
        return (self.base_path / file_path).exists()
    
    async def delete_file(self, file_path: str) -> bool:
        """Delete a file."""
        try:
            full_path = self.base_path / file_path
            if full_path.exists():
                full_path.unlink()
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {e}")
            return False

# Global instances
file_handler = FileHandler()
async_file_handler = AsyncFileHandler()
