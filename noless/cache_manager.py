"""Caching system for NoLess with SQLite backend."""

import sqlite3
import json
import hashlib
import time
import os
from typing import Optional, Dict, Any
from pathlib import Path
from datetime import datetime, timedelta


class CacheManager:
    """SQLite-based cache manager for NoLess operations."""

    def __init__(self, cache_dir: Optional[str] = None, ttl_hours: int = 24):
        """
        Initialize cache manager.

        Args:
            cache_dir: Directory for cache database (default: ~/.noless/cache)
            ttl_hours: Time-to-live for cached items in hours
        """
        if cache_dir is None:
            cache_dir = os.path.expanduser("~/.noless")

        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.db_path = self.cache_dir / "cache.db"
        self.ttl = ttl_hours * 3600  # Convert to seconds

        self._init_db()

    def _init_db(self) -> None:
        """Initialize SQLite database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    category TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    expires_at REAL NOT NULL
                )
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_category ON cache(category)
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_expires_at ON cache(expires_at)
            """)

            conn.commit()

    def _generate_key(self, prefix: str, data: str) -> str:
        """Generate cache key from prefix and data."""
        hash_val = hashlib.md5(data.encode()).hexdigest()
        return f"{prefix}:{hash_val}"

    def set(self, key: str, value: Any, category: str = "general") -> None:
        """
        Store value in cache.

        Args:
            key: Cache key
            value: Value to cache (will be JSON serialized)
            category: Category for organization (dataset, llm, validation, etc)
        """
        try:
            now = time.time()
            expires_at = now + self.ttl

            json_value = json.dumps(value)

            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO cache (key, value, category, created_at, expires_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (key, json_value, category, now, expires_at))
                conn.commit()
        except Exception as e:
            print(f"[Warning] Cache write failed: {e}")

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve value from cache if not expired.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/expired
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT value FROM cache
                    WHERE key = ? AND expires_at > ?
                """, (key, time.time()))

                row = cursor.fetchone()
                if row:
                    return json.loads(row[0])
                return None
        except Exception as e:
            print(f"[Warning] Cache read failed: {e}")
            return None

    def get_or_compute(self, key: str, compute_fn, category: str = "general") -> Any:
        """
        Get value from cache or compute it.

        Args:
            key: Cache key
            compute_fn: Function to call if cache miss
            category: Cache category

        Returns:
            Cached or computed value
        """
        cached = self.get(key)
        if cached is not None:
            return cached

        result = compute_fn()
        self.set(key, result, category=category)
        return result

    def invalidate(self, pattern: Optional[str] = None, category: Optional[str] = None) -> int:
        """
        Invalidate cache entries.

        Args:
            pattern: Key pattern to match (% for wildcard)
            category: Category to invalidate

        Returns:
            Number of entries invalidated
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                if pattern and category:
                    cursor = conn.execute("""
                        DELETE FROM cache WHERE key LIKE ? AND category = ?
                    """, (pattern, category))
                elif pattern:
                    cursor = conn.execute("""
                        DELETE FROM cache WHERE key LIKE ?
                    """, (pattern,))
                elif category:
                    cursor = conn.execute("""
                        DELETE FROM cache WHERE category = ?
                    """, (category,))
                else:
                    cursor = conn.execute("DELETE FROM cache")

                conn.commit()
                return cursor.rowcount
        except Exception as e:
            print(f"[Warning] Cache invalidation failed: {e}")
            return 0

    def cleanup_expired(self) -> int:
        """
        Remove expired cache entries.

        Returns:
            Number of entries removed
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    DELETE FROM cache WHERE expires_at < ?
                """, (time.time(),))
                conn.commit()
                return cursor.rowcount
        except Exception as e:
            print(f"[Warning] Cache cleanup failed: {e}")
            return 0

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("SELECT COUNT(*) FROM cache")
                total = cursor.fetchone()[0]

                cursor = conn.execute("""
                    SELECT COUNT(*) FROM cache WHERE expires_at < ?
                """, (time.time(),))
                expired = cursor.fetchone()[0]

                cursor = conn.execute("""
                    SELECT category, COUNT(*) as count FROM cache
                    WHERE expires_at > ?
                    GROUP BY category
                """, (time.time(),))
                by_category = dict(cursor.fetchall())

                return {
                    "total_entries": total,
                    "expired_entries": expired,
                    "valid_entries": total - expired,
                    "by_category": by_category
                }
        except Exception as e:
            print(f"[Warning] Cache stats failed: {e}")
            return {}

    def clear(self) -> None:
        """Clear entire cache."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM cache")
                conn.commit()
        except Exception as e:
            print(f"[Warning] Cache clear failed: {e}")


# Global cache manager instance
_cache_manager: Optional[CacheManager] = None


def get_cache_manager(cache_dir: Optional[str] = None) -> CacheManager:
    """Get or create global cache manager instance."""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager(cache_dir)
    return _cache_manager
