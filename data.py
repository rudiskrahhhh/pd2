import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Izveido tabulas
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        message TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    
    conn.commit()
    conn.close()

def add_user(first_name, last_name, username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('INSERT INTO users (first_name, last_name, username) VALUES (?, ?, ?)', 
                       (first_name, last_name, username))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def add_message(username, message):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (username, message) VALUES (?, ?)', (username, message))
    conn.commit()
    conn.close()

def get_messages():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT m.timestamp, u.first_name, u.last_name, m.message FROM messages m JOIN users u ON m.username = u.username ORDER BY m.timestamp DESC')
    messages = cursor.fetchall()
    conn.close()
    return messages

def get_user_stats():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT u.first_name, u.last_name, COUNT(m.id) as message_count
                      FROM users u LEFT JOIN messages m ON u.username = m.username
                      GROUP BY u.id''')
    stats = cursor.fetchall()
    conn.close()
    return stats
