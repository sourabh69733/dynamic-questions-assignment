from fastapi import FastAPI, HTTPException
from database import get_db_connection, init_db
from datetime import datetime, timedelta
import sqlite3

app = FastAPI()

DB_NAME = 'questions.db'

# Initialize the database
init_db(DB_NAME)

@app.post("/add_question/")
async def add_question(question: str, region: str, cycle: int):
    """
    Adds a new question to the database for a specific region and cycle.

    Args:
        question (str): The question to be added.
        region (str): The region associated with the question.
        cycle (int): The cycle number for which the question is applicable.

    Returns:
        dict: A message indicating the successful addition of the question.
    """
    conn = get_db_connection(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO questions (question, region, cycle) VALUES (?, ?, ?)", (question, region, cycle))
    conn.commit()
    conn.close()
    return {"message": "Question added successfully"}

@app.get("/get_question/{region}")
async def get_question(region: str):
    """
    Retrieves a question for the specified region. If no question has been assigned
    for the current cycle, assigns a new one from the database based on the region and cycle.

    Args:
        region (str): The region for which the question is being retrieved.

    Returns:
        dict: The region and the question assigned to it.

    Raises:
        HTTPException: If no question is found for the specified region and cycle.
    """
    conn = get_db_connection(DB_NAME)
    cursor = conn.cursor()
    now = datetime.now()
    cursor.execute("SELECT * FROM assignments WHERE region = ?", (region,))
    row = cursor.fetchone()
    
    if not row or (now - datetime.fromisoformat(row[3])) >= timedelta(weeks=1):
        cursor.execute("SELECT id, question FROM questions WHERE region = ? AND cycle = ?", (region, row[2] + 1 if row else 1))
        question_row = cursor.fetchone()
        if question_row:
            cursor.execute("INSERT OR REPLACE INTO assignments (region, question_id, cycle, last_assigned) VALUES (?, ?, ?, ?)", 
                           (region, question_row[0], row[2] + 1 if row else 1, now))
            conn.commit()
            question = question_row[1]
        else:
            conn.close()
            raise HTTPException(status_code=404, detail="No question found for the region or cycle")
    else:
        question_id = row[1]
        cursor.execute("SELECT id, question FROM questions WHERE id = ?", (question_id, ))
        question_row = cursor.fetchone()
        question = question_row[1]
    
    conn.close()
    return {"region": region, "question": question}
