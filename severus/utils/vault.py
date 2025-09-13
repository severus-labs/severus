import sqlite3
from pathlib import Path

def create_vault_db(vault_path):
    conn = sqlite3.connect(vault_path)
    
    # Create table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS vault_items (
            id INTEGER PRIMARY KEY,
            email TEXT,
            name TEXT UNIQUE,
            type TEXT, -- 'secret', 'note', 'env'
            file_path TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            project TEXT
        )
    ''')
    
    conn.commit()
    conn.close()