"""
File Handler utility for Avatar Realms Collide Discord Bot.
Handles file operations, validation, and management.
"""

import os
import shutil
import hashlib
from pathlib import Path
from typing import Optional, List, Dict, Any, Union
import logging
from datetime import datetime, timezone
import aiofiles
import asyncio

class FileHandler:
    """Handles file operations with validation and error handling."""
    
    def __init__(self, base_path: str = "data"):
        self.base_path = Path(base_path)
        self.logger = logging.getLogger(__name__)
        
        # Ensure base directory exists
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def ensure_directory(self, path: Union[str, Path]) -> Path:
        """Ensure a directory exists, creating it if necessary."""
        directory = Path(path) if isinstance(path, str) else path
        directory.mkdir(parents=True, exist_ok=True)
        return directory
    
    def get_file_path(self, *path_parts: str) -> Path:
        """Get a file path relative to the base directory."""
        return self.base_path.joinpath(*path_parts)
    
    def file_exists(self, *path_parts: str) -> bool:
        """Check if a file exists."""
        file_path = self.get_file_path(*path_parts)
        return file_path.exists() and file_path.is_file()
    
    def directory_exists(self, *path_parts: str) -> bool:
        """Check if a directory exists."""
        dir_path = self.get_file_path(*path_parts)
        return dir_path.exists() and dir_path.is_dir()
    
    def create_file(self, *path_parts: str, content: str = "") -> bool:
        """Create a file with optional content."""
        try:
            file_path = self.get_file_path(*path_parts)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"Created file: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error creating file {path_parts}: {e}")
            return False
    
    def read_file(self, *path_parts: str, encoding: str = 'utf-8') -> Optional[str]:
        """Read a file and return its content."""
        try:
            file_path = self.get_file_path(*path_parts)
            if not file_path.exists():
                return None
            
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except Exception as e:
            self.logger.error(f"Error reading file {path_parts}: {e}")
            return None
    
    def write_file(self, *path_parts: str, content: str, encoding: str = 'utf-8') -> bool:
        """Write content to a file."""
        try:
            file_path = self.get_file_path(*path_parts)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            
            self.logger.info(f"Wrote to file: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error writing to file {path_parts}: {e}")
            return False
    
    def delete_file(self, *path_parts: str) -> bool:
        """Delete a file."""
        try:
            file_path = self.get_file_path(*path_parts)
            if file_path.exists():
                file_path.unlink()
                self.logger.info(f"Deleted file: {file_path}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error deleting file {path_parts}: {e}")
            return False
    
    def copy_file(self, source_parts: List[str], dest_parts: List[str]) -> bool:
        """Copy a file from source to destination."""
        try:
            source_path = self.get_file_path(*source_parts)
            dest_path = self.get_file_path(*dest_parts)
            
            if not source_path.exists():
                return False
            
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, dest_path)
            
            self.logger.info(f"Copied file: {source_path} -> {dest_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error copying file: {e}")
            return False
    
    def move_file(self, source_parts: List[str], dest_parts: List[str]) -> bool:
        """Move a file from source to destination."""
        try:
            source_path = self.get_file_path(*source_parts)
            dest_path = self.get_file_path(*dest_parts)
            
            if not source_path.exists():
                return False
            
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source_path), str(dest_path))
            
            self.logger.info(f"Moved file: {source_path} -> {dest_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error moving file: {e}")
            return False
    
    def get_file_size(self, *path_parts: str) -> Optional[int]:
        """Get the size of a file in bytes."""
        try:
            file_path = self.get_file_path(*path_parts)
            if file_path.exists():
                return file_path.stat().st_size
            return None
        except Exception as e:
            self.logger.error(f"Error getting file size {path_parts}: {e}")
            return None
    
    def get_file_hash(self, *path_parts: str, algorithm: str = 'md5') -> Optional[str]:
        """Get the hash of a file."""
        try:
            file_path = self.get_file_path(*path_parts)
            if not file_path.exists():
                return None
            
            hash_obj = hashlib.new(algorithm)
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_obj.update(chunk)
            
            return hash_obj.hexdigest()
        except Exception as e:
            self.logger.error(f"Error getting file hash {path_parts}: {e}")
            return None
    
    def list_files(self, *path_parts: str, pattern: str = "*") -> List[Path]:
        """List files in a directory matching a pattern."""
        try:
            dir_path = self.get_file_path(*path_parts)
            if not dir_path.exists() or not dir_path.is_dir():
                return []
            
            return list(dir_path.glob(pattern))
        except Exception as e:
            self.logger.error(f"Error listing files {path_parts}: {e}")
            return []
    
    def list_directories(self, *path_parts: str) -> List[Path]:
        """List subdirectories in a directory."""
        try:
            dir_path = self.get_file_path(*path_parts)
            if not dir_path.exists() or not dir_path.is_dir():
                return []
            
            return [item for item in dir_path.iterdir() if item.is_dir()]
        except Exception as e:
            self.logger.error(f"Error listing directories {path_parts}: {e}")
            return []
    
    async def async_read_file(self, *path_parts: str, encoding: str = 'utf-8') -> Optional[str]:
        """Asynchronously read a file."""
        try:
            file_path = self.get_file_path(*path_parts)
            if not file_path.exists():
                return None
            
            async with aiofiles.open(file_path, 'r', encoding=encoding) as f:
                return await f.read()
        except Exception as e:
            self.logger.error(f"Error async reading file {path_parts}: {e}")
            return None
    
    async def async_write_file(self, *path_parts: str, content: str, encoding: str = 'utf-8') -> bool:
        """Asynchronously write content to a file."""
        try:
            file_path = self.get_file_path(*path_parts)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            async with aiofiles.open(file_path, 'w', encoding=encoding) as f:
                await f.write(content)
            
            self.logger.info(f"Async wrote to file: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error async writing to file {path_parts}: {e}")
            return False
    
    def backup_file(self, *path_parts: str, backup_suffix: str = ".backup") -> bool:
        """Create a backup of a file."""
        try:
            file_path = self.get_file_path(*path_parts)
            if not file_path.exists():
                return False
            
            backup_path = file_path.with_suffix(file_path.suffix + backup_suffix)
            shutil.copy2(file_path, backup_path)
            
            self.logger.info(f"Created backup: {backup_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error creating backup {path_parts}: {e}")
            return False
    
    def cleanup_old_backups(self, *path_parts: str, max_age_days: int = 30) -> int:
        """Clean up old backup files."""
        try:
            file_path = self.get_file_path(*path_parts)
            backup_pattern = str(file_path.with_suffix(file_path.suffix + ".backup*"))
            backup_files = list(Path(backup_pattern).parent.glob(Path(backup_pattern).name))
            
            cutoff_time = datetime.now(timezone.utc).timestamp() - (max_age_days * 24 * 3600)
            deleted_count = 0
            
            for backup_file in backup_files:
                if backup_file.stat().st_mtime < cutoff_time:
                    backup_file.unlink()
                    deleted_count += 1
            
            if deleted_count > 0:
                self.logger.info(f"Cleaned up {deleted_count} old backup files")
            
            return deleted_count
        except Exception as e:
            self.logger.error(f"Error cleaning up backups {path_parts}: {e}")
            return 0
    
    def validate_image_file(self, *path_parts: str, max_size_mb: int = 10) -> Dict[str, Any]:
        """Validate an image file."""
        try:
            file_path = self.get_file_path(*path_parts)
            if not file_path.exists():
                return {"valid": False, "error": "File does not exist"}
            
            # Check file size
            file_size = file_path.stat().st_size
            max_size_bytes = max_size_mb * 1024 * 1024
            
            if file_size > max_size_bytes:
                return {
                    "valid": False, 
                    "error": f"File too large ({file_size / (1024*1024):.2f}MB > {max_size_mb}MB)"
                }
            
            # Check file extension
            valid_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp'}
            if file_path.suffix.lower() not in valid_extensions:
                return {
                    "valid": False, 
                    "error": f"Invalid file type: {file_path.suffix}"
                }
            
            return {
                "valid": True,
                "size_bytes": file_size,
                "size_mb": file_size / (1024 * 1024),
                "extension": file_path.suffix.lower()
            }
        except Exception as e:
            self.logger.error(f"Error validating image file {path_parts}: {e}")
            return {"valid": False, "error": str(e)}

# Global instance
file_handler = FileHandler()
