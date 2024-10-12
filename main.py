from fastapi import FastAPI, HTTPException
from database import get_db_connection, init_db
from datetime import datetime, timedelta
import sqlite3
from pydantic import BaseModel
import schedule
import time
import threading

app = FastAPI()

DATABASE = 'questions.db'
SCHEDULE_CYCLE_DAYS = 1

# Initialize the database
init_db(DATABASE)

class Question(BaseModel):
    question: str
    region: str


@app.post("/add_question/")
async def add_question(question: str, region: str):
    """
    Adds a new question to the database for a specific region and cycle.

    Args:
        question (str): The question to be added.
        region (str): The region associated with the question.
        cycle (int): The cycle number for which the question is applicable.

    Returns:
        dict: A message indicating the successful addition of the question.
    """
    conn = get_db_connection(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO questions (question, region) VALUES (?, ?)",
                   (question, region))
    conn.commit()
    conn.close()
    return {"message": "Question added successfully"}

@app.get("/get_question/{region}")
def get_question(region: str):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''SELECT q.question 
                      FROM questions q 
                      JOIN assignments a ON q.id = a.question_id 
                      WHERE a.region = ? 
                      ORDER BY a.cycle_start DESC 
                      LIMIT 1''', (region,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"question": row[0]}
    raise HTTPException(status_code=404, detail="Question not found for the current cycle")

def assign_questions_for_cycle():
    print('Assigning question to a new cycle')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Get available regions
    cursor.execute("SELECT DISTINCT region FROM questions")
    regions = cursor.fetchall()
    
    for region in regions:
        region_name = region[0]
        
        # Get the next unassigned question for this region
        cursor.execute('''SELECT id FROM questions 
                          WHERE region = ? AND id NOT IN 
                              (SELECT question_id FROM assignments WHERE region = ?)
                          LIMIT 1''', (region_name, region_name))
        question_row = cursor.fetchone()
        
        if question_row:
            question_id = question_row[0]
            now = datetime.now()
            
            # Assign the question for the current cycle
            cursor.execute('''INSERT INTO assignments (question_id, region, cycle_start)
                              VALUES (?, ?, ?)''', (question_id, region_name, now))
            conn.commit()
    
    conn.close()

# Scheduler job
def scheduler_job():
    while True:
        assign_questions_for_cycle()  # Assign questions for all regions
        time.sleep(SCHEDULE_CYCLE_DAYS * 24 * 60 * 60)  # Sleep for one week (7 days)

# Function to run the scheduler in a separate thread
def start_scheduler():
    scheduler_thread = threading.Thread(target=scheduler_job)
    scheduler_thread.start()

# Start the scheduler when the FastAPI app starts
@app.on_event("startup")
async def startup_event():
    start_scheduler()
    # Initial assignment
    # assign_questions_for_cycle()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
