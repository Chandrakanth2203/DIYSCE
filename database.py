import sqlite3
from pathlib import Path

# Database file path
DB_PATH = "users_database.db"

def initialize_database():
    """Create database and inject sample user data"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            account_status TEXT NOT NULL,
            subscription_type TEXT NOT NULL,
            created_date TEXT NOT NULL,
            last_login TEXT
        )
    ''')
    
    # Check if data already exists
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        # Insert sample user data
        sample_users = [
            ('john_doe', 'john.doe@email.com', 'John Doe', 'active', 'premium', '2023-01-15', '2026-02-15'),
            ('jane_smith', 'jane.smith@email.com', 'Jane Smith', 'active', 'standard', '2023-06-20', '2026-02-10'),
            ('mike_wilson', 'mike.wilson@email.com', 'Mike Wilson', 'inactive', 'trial', '2024-01-10', '2025-12-01'),
            ('sarah_johnson', 'sarah.j@email.com', 'Sarah Johnson', 'active', 'premium', '2022-11-05', '2026-02-18'),
            ('alex_brown', 'alex.brown@email.com', 'Alex Brown', 'suspended', 'standard', '2023-03-12', '2025-08-30'),
        ]
        
        cursor.executemany(
            'INSERT INTO users (username, email, full_name, account_status, subscription_type, created_date, last_login) VALUES (?, ?, ?, ?, ?, ?, ?)',
            sample_users
        )
        conn.commit()
        print("✓ Database initialized with sample user data")
    
    conn.close()

def get_user_by_username(username: str) -> dict:
    """Retrieve user details from database by username"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT user_id, username, email, full_name, account_status, subscription_type, created_date, last_login
        FROM users
        WHERE username = ?
    ''', (username,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            'user_id': result[0],
            'username': result[1],
            'email': result[2],
            'full_name': result[3],
            'account_status': result[4],
            'subscription_type': result[5],
            'created_date': result[6],
            'last_login': result[7]
        }
    return None

def search_users(search_term: str) -> list:
    """Search users by username, email, or full name"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    search_pattern = f"%{search_term}%"
    cursor.execute('''
        SELECT user_id, username, email, full_name, account_status, subscription_type, created_date, last_login
        FROM users
        WHERE username LIKE ? OR email LIKE ? OR full_name LIKE ?
    ''', (search_pattern, search_pattern, search_pattern))
    
    results = cursor.fetchall()
    conn.close()
    
    users = []
    for result in results:
        users.append({
            'user_id': result[0],
            'username': result[1],
            'email': result[2],
            'full_name': result[3],
            'account_status': result[4],
            'subscription_type': result[5],
            'created_date': result[6],
            'last_login': result[7]
        })
    return users

def get_all_users() -> list:
    """Retrieve all users from database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT user_id, username, email, full_name, account_status, subscription_type, created_date, last_login
        FROM users
    ''')
    
    results = cursor.fetchall()
    conn.close()
    
    users = []
    for result in results:
        users.append({
            'user_id': result[0],
            'username': result[1],
            'email': result[2],
            'full_name': result[3],
            'account_status': result[4],
            'subscription_type': result[5],
            'created_date': result[6],
            'last_login': result[7]
        })
    return users