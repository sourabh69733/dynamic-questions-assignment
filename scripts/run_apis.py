import requests
import sys

# URL of the FastAPI server
BASE_URL = "http://127.0.0.1:8000"

def add_questions():
    """Function to add questions for multiple cycles and regions."""
    # Data for adding questions for multiple cycles
    regions = {
        "singapore": ["Question 10 SG", "Question 20 SG", "Question 30 SG"],
        "us": ["Question 10 US", "Question 20 US", "Question 30 US"]
    }

    # Loop through each region and cycle, adding questions
    for region, questions in regions.items():
        for cycle, question in enumerate(questions, start=1):
            data = {
                "question": question,
                "region": region,
            }
            response = requests.post(f"{BASE_URL}/add_question/", params=data)
            if response.status_code == 200:
                print(f"Added '{question}' for region '{region}'")
            else:
                print(f"Failed to add question for region '{region}', cycle: {response.text}")

def get_questions():
    """Function to retrieve questions for a specific region and cycles."""
    region = input("Enter the region (e.g., 'singapore', 'us'): ")

    url = f"{BASE_URL}/get_question/{region}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(f"'{region}': {data['question']}")
    else:
        print(f"Failed to retrieve question for region '{region}', cycle {response.text}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <add|get>")
        sys.exit(1)

    action = sys.argv[1].lower()

    if action == "add":
        add_questions()
    elif action == "get":
        get_questions()
    else:
        print("Invalid action. Use 'add' to add questions or 'get' to retrieve questions.")
