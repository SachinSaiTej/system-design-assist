"""Reference store for caching web references."""
import sqlite3
import json
import hashlib
from typing import List, Optional, Dict
from datetime import datetime, timedelta
import logging
import os

logger = logging.getLogger(__name__)

# Cache expiry: 7 days
CACHE_EXPIRY_DAYS = 7


class ReferenceStore:
    """Simple SQLite-based store for caching reference summaries."""
    
    def __init__(self, db_path: str = "data/reference_cache.db"):
        """Initialize the reference store."""
        # Ensure data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize the database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS references (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query_hash TEXT UNIQUE NOT NULL,
                query_text TEXT NOT NULL,
                references_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_query_hash ON references(query_hash)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_expires_at ON references(expires_at)
        """)
        
        conn.commit()
        conn.close()
        
        # Clean up expired entries
        self._cleanup_expired()
    
    def _hash_query(self, query: str) -> str:
        """Generate hash for a query."""
        return hashlib.md5(query.encode()).hexdigest()
    
    def _cleanup_expired(self):
        """Remove expired cache entries."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM references WHERE expires_at < ?", (datetime.now(),))
            deleted = cursor.rowcount
            conn.commit()
            conn.close()
            if deleted > 0:
                logger.info(f"🧹 Cleaned up {deleted} expired cache entries")
        except Exception as e:
            logger.error(f"Error cleaning up expired entries: {str(e)}")
    
    def get(self, query: str) -> Optional[List[Dict]]:
        """
        Get cached references for a query.
        
        Args:
            query: Search query
            
        Returns:
            List of reference dictionaries or None if not found/expired
        """
        query_hash = self._hash_query(query)
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT references_json, expires_at 
                FROM references 
                WHERE query_hash = ?
            """, (query_hash,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                references_json, expires_at = row
                expires_at_dt = datetime.fromisoformat(expires_at)
                
                if expires_at_dt > datetime.now():
                    # Cache hit
                    references = json.loads(references_json)
                    logger.info(f"✅ Cache hit for query: {query[:50]}...")
                    return references
                else:
                    # Expired, delete it
                    self._delete(query_hash)
                    logger.info(f"⏰ Cache expired for query: {query[:50]}...")
            
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving from cache: {str(e)}")
            return None
    
    def set(self, query: str, references: List[Dict]):
        """
        Cache references for a query.
        
        Args:
            query: Search query
            references: List of reference dictionaries
        """
        query_hash = self._hash_query(query)
        expires_at = datetime.now() + timedelta(days=CACHE_EXPIRY_DAYS)
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            references_json = json.dumps(references)
            
            cursor.execute("""
                INSERT OR REPLACE INTO references 
                (query_hash, query_text, references_json, expires_at)
                VALUES (?, ?, ?, ?)
            """, (query_hash, query, references_json, expires_at.isoformat()))
            
            conn.commit()
            conn.close()
            
            logger.info(f"💾 Cached {len(references)} references for query: {query[:50]}...")
            
        except Exception as e:
            logger.error(f"Error caching references: {str(e)}")
    
    def _delete(self, query_hash: str):
        """Delete a cache entry."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM references WHERE query_hash = ?", (query_hash,))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error deleting cache entry: {str(e)}")

