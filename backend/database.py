import sqlite3
import pandas as pd
from datetime import datetime, timedelta

def init_database():
    """Initialize database with necessary tables"""
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    # Create conversation history table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS conversation_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        sql_query TEXT NOT NULL,
        results TEXT NOT NULL,
        explanation TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        expires_at DATETIME NOT NULL
    )
    ''')
    
    # Create data table (for CSV data)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS data (
        id INTEGER PRIMARY KEY AUTOINCREMENT
    )
    ''')
    
    conn.commit()
    conn.close()

def create_database_from_csv(df):
    """Create SQLite database from DataFrame"""
    conn = sqlite3.connect('data.db')
    # Convert DataFrame to SQL table
    df.to_sql('data', conn, if_exists='replace', index=False)
    conn.close()

def execute_query(query):
    """Execute SQL query and return results as DataFrame"""
    try:
        conn = sqlite3.connect('data.db')
        result = pd.read_sql_query(query, conn)
        conn.close()
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
        raise e

def save_conversation(question, sql_query, results, explanation):
    """Save conversation to history with 24-hour expiration"""
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    current_time = datetime.now()
    expires_at = current_time + timedelta(hours=24)
    
    cursor.execute('''
    INSERT INTO conversation_history 
    (question, sql_query, results, explanation, timestamp, expires_at)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (question, sql_query, str(results), explanation, current_time, expires_at))
    
    conn.commit()
    conn.close()

def get_recent_conversations():
    """Get conversations from last 24 hours"""
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    # Clean up expired conversations
    cleanup_expired_conversations()
    
    # Get valid conversations
    cursor.execute('''
    SELECT question, sql_query, results, explanation, timestamp
    FROM conversation_history
    WHERE expires_at > CURRENT_TIMESTAMP
    ORDER BY timestamp DESC
    ''')
    
    conversations = cursor.fetchall()
    conn.close()
    
    return [
        {
            'question': conv[0],
            'sql_query': conv[1],
            'results': conv[2],
            'explanation': conv[3],
            'timestamp': conv[4]
        }
        for conv in conversations
    ]

def cleanup_expired_conversations():
    """Delete conversations older than 24 hours"""
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    DELETE FROM conversation_history
    WHERE expires_at <= CURRENT_TIMESTAMP
    ''')
    
    conn.commit()
    conn.close() 