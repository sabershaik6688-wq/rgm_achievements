import sqlite3

def init_db():
    # This creates a file named 'dats.db' in your folder
    conn = sqlite3.connect('dats.db')
    cursor = conn.cursor()
    
    # This creates a table to store achievements
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            author_name TEXT NOT NULL,
            academic_year TEXT NOT NULL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_achievement(title, category, author_name, academic_year, description):
    conn = sqlite3.connect('dats.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO achievements (title, category, author_name, academic_year, description)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, category, author_name, academic_year, description))
    conn.commit()
    conn.close()

def get_achievements_by_year(academic_year):
    conn = sqlite3.connect('dats.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM achievements WHERE academic_year = ?', (academic_year,))
    records = cursor.fetchall()
    conn.close()
    return records