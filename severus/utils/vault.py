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
    ''', (name, item_type, str(file_path), project, email))
    
    conn.commit()
    conn.close()

def item_exists(vault_path, name):
    conn = sqlite3.connect(vault_path)
    cursor = conn.execute('SELECT COUNT(*) FROM vault WHERE name = ?', (name,))
    exists = cursor.fetchone()[0] > 0
    conn.close()
    return exists

def update_vault_item(vault_path, name, item_type=None, file_path=None, project=None, email=None):
    """Update existing vault item with new values (only updates non-None fields)"""
    conn = sqlite3.connect(vault_path)
    
    # Build dynamic update query based on provided fields
    update_fields = []
    params = []
    
    if item_type is not None:
        update_fields.append("type = ?")
        params.append(item_type)
    
    if file_path is not None:
        update_fields.append("file_path = ?")
        params.append(str(file_path))
    
    if project is not None:
        update_fields.append("project = ?")
        params.append(project)
    
    if email is not None:
        update_fields.append("email = ?")
        params.append(email)
    
    # Always update the timestamp
    update_fields.append("created_at = CURRENT_TIMESTAMP")
    
    # Add name for WHERE clause
    params.append(name)
    
    query = f"UPDATE vault SET {', '.join(update_fields)} WHERE name = ?"
    
    conn.execute(query, params)
    conn.commit()
    conn.close()

def get_env_items_by_project(vault_path, project_name):
    conn = sqlite3.connect(vault_path)
    cursor = conn.execute(
        'SELECT name, file_path FROM vault WHERE type = "env" AND (project = ? OR name LIKE ?)',
        (project_name, f"{project_name}-env%")
    )
    env_items = cursor.fetchall()
    conn.close()
    return env_items

def get_all_vault_items(vault_path):
    conn = sqlite3.connect(vault_path)
    cursor = conn.execute('SELECT name, type, created_at FROM vault ORDER BY type, name')
    items = [{'name': row[0], 'type': row[1], 'created_at': row[2]} for row in cursor.fetchall()]
    conn.close()
    return items