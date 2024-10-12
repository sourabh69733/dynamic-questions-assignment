# Dynamic Question Assignment System Architecture

## Overview

The system is designed to assign region-specific questions to users based on a configurable cycle duration.

## Architecture

The architecture consists of the following components:

- **API Layer:** FastAPI handles the incoming HTTP requests.
- **Database Layer:** SQLite is used to store questions and their assignments.
- **Scheduler:** A separate thread that assigns questions periodically.

## Components

### 1. **API Layer**
   - **Framework:** FastAPI
   - **Endpoints:**
     - `POST /add_question/`: Adds a new question to the database.
     - `GET /get_question/{region}`: Retrieves the most recent question for a specified region.
   - **Purpose:** Handles incoming requests, performs validation, and interacts with the database.

### 2. **Database Layer**
   - **Database:** SQLite (for development); consider PostgreSQL or MySQL for production.
   - **Schema:**
     - **questions** table:
       - `id` (Primary Key)
       - `question` (Text)
       - `region` (Text)
     - **assignments** table:
       - `question_id` (Foreign Key referencing questions)
       - `region` (Text)
       - `cycle_start` (Timestamp)
   - **Purpose:** Stores questions and their assignments based on region.

### 3. **Business Logic Layer**
   - **Scheduler:**
     - Automatically assigns new questions to regions based on a defined cycle.
   - **Logic Flow:**
     - When a question is requested:
       1. Retrieve the most recent assigned question for the region.
       2. If no question is found, raise an HTTP exception.
     - Periodically assigns questions to regions in a separate thread.

### 4. **Scheduler**
   - **Functionality:**
     - Runs in a separate thread, assigning questions for each region at specified intervals.
   - **Cycle Duration:** Configurable; default is set to 1 week.

### 5. **Caching Layer (Optional: Not Implemented now)**
   - **Cache:** Redis or Memcached
   - **Purpose:** Store frequently accessed questions or regions to reduce database load and improve response times.

## How to run it?

### Prerequisites

- Python 3.8+
- SQLite (included in Python)

#### Steps
1. **Clone the repository:**
   ```bash
   git clone git@github.com:sourabh69733/dynamic-questions-assignment.git
   cd dynamic-questions-assignment
   ```
2. Add sample questions data to database. Execute python script `populate_questions.py`
```python
  python3 populate_questions.py
```
3. Install dependencies and start fast API server
```bash
  chmod +x ./scripts/setup_and_run_server.sh
  ./scripts/setup_and_run_server.sh
```
4. Now we are ready to consume apis. At this point, we are sure about that we have some sample questions in database and our schedular is running in background.
There are two way you can test/consume apis.
\

a). Run python script at `scripts/run_apis.py`
```python
# To Add more questions
python3 scripts/run_apis.py add

# To Retrive question based on given region
python3 scripts/run_apis.py get
```
b). Open `http://127.0.0.1:8000/docs#/default` in browser.
Here in UI, you can run all apis with input. 

## API Endpoints

### Add Question

`POST /add_question/`

Adds a new question to the database for a specific region.

#### Request Body

```json
{
  "question": "What is the capital of France?",
  "region": "Europe"
}
```
#### Response
Status Code: 200 OK

Body:
```json
{
  "message": "Question added successfully"
}
```

### Retrive question
`GET /get_question/{region}`

Retrieves the most recent question for the specified region.

URL Parameters
- region (string): The region for which the question is being retrieved.

#### Response
- Status Code: 200 OK
- Body:
    ```json
    {
        "question": "What is the capital of France?"
    }

    ```

## Scalability Considerations

- **Database Sharding:** As the user base grows, consider partitioning the database based on regions.
- **Load Balancing:** Distribute incoming requests across multiple API instances.
- **Horizontal Scaling:** Add more API instances and database replicas as needed.
- **Asynchronous Processing:** Use background tasks for question assignments to reduce response times.

