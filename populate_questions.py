import sqlite3
from datetime import datetime
from database import get_db_connection, init_db

# Define the database file
DATABASE = 'questions.db'

init_db(DATABASE)

# Questions to add
questions_data = [
    ("What is the capital of France?", "india"),
    ("Name a large desert in Africa.", "singapore"),
    ("What is the smallest continent?", "US"),
    ("Which country has the largest population?", "india"),
    ("What is the largest country in South America?", "singapore"),
    ("Name a river that flows through Egypt.", "singapore"),
    ("Which ocean is the deepest?", "singapore"),
]

def add_questions(database: str, questions: list):
    # Connect to the database
    conn = get_db_connection(DATABASE)
    cursor = conn.cursor()
    
    # Insert each question into the database
    for question, region in questions:
        cursor.execute('INSERT INTO questions (question, region) VALUES (?, ?)', (question, region))
        
    # Commit and close the connection
    conn.commit()
    conn.close()
    print("Questions have been added successfully.")

# Run the function to add questions
if __name__ == "__main__":
    add_questions(DATABASE, questions_data)
