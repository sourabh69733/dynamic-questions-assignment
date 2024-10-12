import sqlite3
import os

# Initialize SQLite Database
def init_db(db_name: str) -> None:
    """
    Creates a SQLite database and tables for storing question and assignment informations.

    Args:
        db_name (str): The name of the SQLite database file.
    """
    
    if os.path.exists(db_name):
        print(f"Database '{db_name}' already exists.")
        return 1

    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS questions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            question TEXT NOT NULL,
                            region TEXT NOT NULL
                        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS assignments (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            question_id INTEGER NOT NULL,
                            region TEXT NOT NULL,
                            cycle_start TIMESTAMP NOT NULL,
                            FOREIGN KEY (question_id) REFERENCES questions (id)
                        )''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred while creating the database: {e}")
    finally:
        if conn:
            conn.close()

def get_db_connection(db_name: str):
    """
    Returns database connnection instance.
    
    Args:
        db_name (str): The name of the SQLite database file.
    """
    conn = sqlite3.connect(db_name)
    return conn
