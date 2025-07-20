import sqlite3
from config import Config

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(Config.DATABASE_PATH)
        self._create_tables()
        
    def _create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS forward_config (
                source_chat INTEGER PRIMARY KEY,
                target_chats TEXT
            )
        """)
        self.conn.commit()
        
    def add_forward_rule(self, source_chat, target_chats):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO forward_config 
            (source_chat, target_chats) VALUES (?, ?)
        """, (source_chat, ",".join(map(str, target_chats))))
        self.conn.commit()
        
    def remove_forward_rule(self, source_chat):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM forward_config WHERE source_chat = ?", (source_chat,))
        self.conn.commit()
        
    def get_forward_rules(self, source_chat=None):
        cursor = self.conn.cursor()
        if source_chat:
            cursor.execute("SELECT source_chat, target_chats FROM forward_config WHERE source_chat = ?", (source_chat,))
        else:
            cursor.execute("SELECT source_chat, target_chats FROM forward_config")
            
        rules = {}
        for row in cursor.fetchall():
            rules[row[0]] = [int(t) for t in row[1].split(",")]
        return rules
    
    def close(self):
        self.conn.close()
