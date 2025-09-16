import sqlite3
import streamlit as st

# Use st.connection for robust, cached connections
@st.cache_resource
def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect('seminar_questions.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def setup_database():
    """Creates the questions table if it doesn't exist."""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()

def add_question(question_text):
    """Adds a new question to the database."""
    conn = get_db_connection()
    conn.execute('INSERT INTO questions (question_text) VALUES (?)', (question_text,))
    conn.commit()

def get_all_questions():
    """Retrieves all questions from the database, newest first."""
    conn = get_db_connection()
    questions = conn.execute('SELECT question_text FROM questions ORDER BY timestamp DESC').fetchall()
    # Extract just the text from the row objects
    return [row['question_text'] for row in questions]

def clear_all_questions():
    """Deletes all questions from the database."""
    conn = get_db_connection()
    conn.execute('DELETE FROM questions')
    conn.commit()
