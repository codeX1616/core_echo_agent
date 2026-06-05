import sqlite3
import json
from datetime import datetime

class ContextDB:
    def __init__(self, db_path="context.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
        
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                role TEXT,
                content TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS state (
                id INTEGER PRIMARY KEY,
                key TEXT UNIQUE,
                value TEXT
            )
        ''')
        self.conn.commit()
        
    def add_memory(self, role, content):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO memory (timestamp, role, content) VALUES (?, ?, ?)",
                       (datetime.now().isoformat(), role, content))
        self.conn.commit()
        
    def get_recent_memory(self, turns=10):
        cursor = self.conn.cursor()
        cursor.execute("SELECT role, content FROM memory ORDER BY id DESC LIMIT ?", (turns,))
        return cursor.fetchall()[::-1]
        
    def get_markdown_context(self):
        memories = self.get_recent_memory()
        md = "# Recent Conversation History\n\n"
        for role, content in memories:
            md += f"**{role.capitalize()}**: {content}\n\n"
        return md
