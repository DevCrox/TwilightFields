import sqlite3
import os

class GameDatabase:
    def __init__(self, db_path="game_stats.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create the database and tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create wins table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_stats (
                id INTEGER PRIMARY KEY,
                stat_name TEXT UNIQUE,
                stat_value INTEGER DEFAULT 0
            )
        ''')
        
        # Initialize wins counter if it doesn't exist
        cursor.execute('''
            INSERT OR IGNORE INTO game_stats (stat_name, stat_value) 
            VALUES ('wins', 0)
        ''')
        
        conn.commit()
        conn.close()
    
    def add_win(self):
        """Increment win counter by 1"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE game_stats 
            SET stat_value = stat_value + 1 
            WHERE stat_name = 'wins'
        ''')
        
        conn.commit()
        conn.close()
    
    def get_wins(self):
        """Get current win count"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT stat_value FROM game_stats 
            WHERE stat_name = 'wins'
        ''')
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else 0