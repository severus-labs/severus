import sqlite3

def create_vault_db(vault_path):
    conn = sqlite3.connect(vault_path)
    
    # Create table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS vault (
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

def insert_vault_item(vault_path, name, item_type, file_path, project=None, email=None):
    conn = sqlite3.connect(vault_path)
    
    conn.execute('''
        INSERT OR REPLACE INTO vault (name, type, file_path, project, email)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, item_type, file_path, project, email))
    
    conn.commit()
    conn.close()