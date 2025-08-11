"""
Cache Handler utility for Avatar Realms Collide Discord Bot.
Handles data caching operations with TTL and memory management.
"""

import time
import logging
from typing import Any, Dict, Optional, List, Tuple
from datetime import datetime, timezone, timedelta
import asyncio
from collections import OrderedDict
import json

class CacheEntry:
    """Represents a single cache entry with metadata."""
    
    def __init__(self, key: str, value: Any, ttl: Optional[int] = None):
        self.key = key
        self.value = value
        self.created_at = time.time()
        self.ttl = ttl
        self.last_accessed = self.created_at
        self.access_count = 0
    
    def is_expired(self) -> bool:
        """Check if the cache entry has expired."""
        if self.ttl is None:
            return False
        return time.time() - self.created_at > self.ttl
    
    def access(self):
        """Mark the entry as accessed."""
        self.last_accessed = time.time()
        self.access_count += 1
    
    def get_age(self) -> float:
        """Get the age of the entry in seconds."""
        return time.time() - self.created_at
    
    def get_time_until_expiry(self) -> Optional[float]:
        """Get time until expiry in seconds."""
        if self.ttl is None:
            return None
        return max(0, self.ttl - self.get_age())

class CacheHandler:
    """Handles data caching with TTL and memory management."""
    
    def __init__(self, max_size: int = 1000, default_ttl: Optional[int] = 3600):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self.logger = logging.getLogger(__name__)
        self.stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0,
            "deletes": 0,
            "expirations": 0
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from cache."""
        entry = self.cache.get(key)
        
        if entry is None:
            self.stats["misses"] += 1
            return default
        
        if entry.is_expired():
            self._remove_entry(key)
            self.stats["misses"] += 1
            self.stats["expirations"] += 1
            return default
        
        # Move to end (LRU)
        self.cache.move_to_end(key)
        entry.access()
        self.stats["hits"] += 1
        return entry.value
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set a value in cache."""
        try:
            # Remove existing entry if it exists
            if key in self.cache:
                self._remove_entry(key)
            
            # Use default TTL if none provided
            if ttl is None:
                ttl = self.default_ttl
            
            # Create new entry
            entry = CacheEntry(key, value, ttl)
            
            # Check if we need to evict entries
            if len(self.cache) >= self.max_size:
                self._evict_entries()
            
            # Add to cache
            self.cache[key] = entry
            self.stats["sets"] += 1
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting cache entry {key}: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete a value from cache."""
        if key in self.cache:
            self._remove_entry(key)
            self.stats["deletes"] += 1
            return True
        return False
    
    def exists(self, key: str) -> bool:
        """Check if a key exists in cache and is not expired."""
        entry = self.cache.get(key)
        if entry is None:
            return False
        
        if entry.is_expired():
            self._remove_entry(key)
            self.stats["expirations"] += 1
            return False
        
        return True
    
    def get_ttl(self, key: str) -> Optional[float]:
        """Get time to live for a key in seconds."""
        entry = self.cache.get(key)
        if entry is None:
            return None
        
        if entry.is_expired():
            self._remove_entry(key)
            return None
        
        return entry.get_time_until_expiry()
    
    def set_ttl(self, key: str, ttl: int) -> bool:
        """Set TTL for an existing key."""
        entry = self.cache.get(key)
        if entry is None:
            return False
        
        entry.ttl = ttl
        entry.created_at = time.time()  # Reset creation time
        return True
    
    def increment(self, key: str, amount: int = 1, ttl: Optional[int] = None) -> Optional[int]:
        """Increment a numeric value in cache."""
        current_value = self.get(key, 0)
        
        if not isinstance(current_value, (int, float)):
            return None
        
        new_value = current_value + amount
        self.set(key, new_value, ttl)
        return new_value
    
    def decrement(self, key: str, amount: int = 1, ttl: Optional[int] = None) -> Optional[int]:
        """Decrement a numeric value in cache."""
        return self.increment(key, -amount, ttl)
    
    def clear(self) -> int:
        """Clear all entries from cache."""
        count = len(self.cache)
        self.cache.clear()
        self.logger.info(f"Cleared {count} cache entries")
        return count
    
    def clear_expired(self) -> int:
        """Clear all expired entries from cache."""
        expired_keys = []
        for key, entry in self.cache.items():
            if entry.is_expired():
                expired_keys.append(key)
        
        for key in expired_keys:
            self._remove_entry(key)
            self.stats["expirations"] += 1
        
        if expired_keys:
            self.logger.info(f"Cleared {len(expired_keys)} expired cache entries")
        
        return len(expired_keys)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_requests = self.stats["hits"] + self.stats["misses"]
        hit_rate = (self.stats["hits"] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            **self.stats,
            "size": len(self.cache),
            "max_size": self.max_size,
            "hit_rate": round(hit_rate, 2),
            "total_requests": total_requests
        }
    
    def get_keys(self, pattern: str = "*") -> List[str]:
        """Get all keys matching a pattern."""
        import fnmatch
        keys = list(self.cache.keys())
        return fnmatch.filter(keys, pattern)
    
    def get_info(self, key: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a cache entry."""
        entry = self.cache.get(key)
        if entry is None:
            return None
        
        if entry.is_expired():
            self._remove_entry(key)
            return None
        
        return {
            "key": entry.key,
            "value": entry.value,
            "created_at": entry.created_at,
            "last_accessed": entry.last_accessed,
            "access_count": entry.access_count,
            "ttl": entry.ttl,
            "age": entry.get_age(),
            "time_until_expiry": entry.get_time_until_expiry(),
            "is_expired": False
        }
    
    def _remove_entry(self, key: str):
        """Remove an entry from cache."""
        if key in self.cache:
            del self.cache[key]
    
    def _evict_entries(self, count: int = 1):
        """Evict entries using LRU policy."""
        for _ in range(min(count, len(self.cache))):
            # Remove oldest entry (first in OrderedDict)
            oldest_key = next(iter(self.cache))
            self._remove_entry(oldest_key)
    
    def cleanup(self):
        """Clean up expired entries and maintain cache size."""
        self.clear_expired()
        
        # If still over max size, evict oldest entries
        if len(self.cache) > self.max_size:
            excess = len(self.cache) - self.max_size
            self._evict_entries(excess)

class AsyncCacheHandler:
    """Asynchronous cache handler with background cleanup."""
    
    def __init__(self, max_size: int = 1000, default_ttl: Optional[int] = 3600, cleanup_interval: int = 300):
        self.cache_handler = CacheHandler(max_size, default_ttl)
        self.cleanup_interval = cleanup_interval
        self.cleanup_task: Optional[asyncio.Task] = None
        self.logger = logging.getLogger(__name__)
    
    async def start(self):
        """Start the background cleanup task."""
        if self.cleanup_task is None or self.cleanup_task.done():
            self.cleanup_task = asyncio.create_task(self._cleanup_loop())
            self.logger.info("Started async cache cleanup task")
    
    async def stop(self):
        """Stop the background cleanup task."""
        if self.cleanup_task and not self.cleanup_task.done():
            self.cleanup_task.cancel()
            try:
                await self.cleanup_task
            except asyncio.CancelledError:
                pass
            self.logger.info("Stopped async cache cleanup task")
    
    async def _cleanup_loop(self):
        """Background cleanup loop."""
        while True:
            try:
                await asyncio.sleep(self.cleanup_interval)
                self.cache_handler.cleanup()
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in cache cleanup loop: {e}")
    
    async def get(self, key: str, default: Any = None) -> Any:
        """Async get operation."""
        return self.cache_handler.get(key, default)
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Async set operation."""
        return self.cache_handler.set(key, value, ttl)
    
    async def delete(self, key: str) -> bool:
        """Async delete operation."""
        return self.cache_handler.delete(key)
    
    async def exists(self, key: str) -> bool:
        """Async exists check."""
        return self.cache_handler.exists(key)
    
    async def clear(self) -> int:
        """Async clear operation."""
        return self.cache_handler.clear()
    
    async def clear_expired(self) -> int:
        """Async clear expired operation."""
        return self.cache_handler.clear_expired()
    
    async def get_stats(self) -> Dict[str, Any]:
        """Async get stats operation."""
        return self.cache_handler.get_stats()
    
    def get_sync_handler(self) -> CacheHandler:
        """Get the underlying sync cache handler."""
        return self.cache_handler

# Global instances
cache_handler = CacheHandler()
async_cache_handler = AsyncCacheHandler()
