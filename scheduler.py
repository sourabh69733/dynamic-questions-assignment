import schedule
import time
from database import get_db_connection
from datetime import datetime, timedelta

# Function to update assignments on a weekly basis
def update_assignments():
    conn = get_db_connection()
    cursor = conn.cursor()
    regions = cursor.execute("SELECT DISTINCT region FROM questions").fetchall()
    for region_tuple in regions:
        region = region_tuple[0]
        cursor.execute("SELECT cycle FROM assignments WHERE region = ?", (region,))
        row = cursor.fetchone()
        current_cycle = row[0] if row else 0
        new_cycle = current_cycle + 1
        cursor.execute("SELECT id FROM questions WHERE region = ? AND cycle = ?", (region, new_cycle))
        question_row = cursor.fetchone()
        if question_row:
            cursor.execute("INSERT OR REPLACE INTO assignments (region, question_id, cycle, last_assigned) VALUES (?, ?, ?, ?)", 
                           (region, question_row[0], new_cycle, datetime.now()))
    conn.commit()
    conn.close()

# Schedule the task to run weekly
schedule.every().monday.at("19:00").do(update_assignments)

# Run scheduler in the background
while True:
    schedule.run_pending()
    time.sleep(1)
