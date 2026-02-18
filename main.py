import os
from crewai import Crew
from database import initialize_database
from agents import live_agent,user_details_agent, problem_solver
from tasks import issue_decoding_task, search_user_task, problem_solving_task
import threading


os.environ["CREWAI_STORAGE_DIR"] = (
    os.path.expanduser("~") + "/.crewai_db_retriever_storage"
)

# Initialize database
initialize_database()

# Define the Crew with Agent-2 and search task
diysce_crew = Crew(
    agents=[live_agent, user_details_agent, problem_solver],
    tasks=[issue_decoding_task, search_user_task, problem_solving_task],
    memory=False,
    verbose=True
)

threads = [live_agent, user_details_agent]

for i in range(2):
    t = threading.Thread(target=threads[i].run, args=(f"Thread-{i}",))
    t.start()


def search_user_account(username: str, file_path: str):
    print(f"\n{'='*60}")
    print(f"Searching for user account: {username}")
    print(f"{'='*60}\n")
    
    # Execute the crew with the search task
    result = diysce_crew.kickoff(
        inputs={"username": username, "file_path":file_path}
    )
    
    return result

if __name__ == "__main__":
    # Example searches
    test_usernames = ["john_doe", "jane_smith", "unknown_user"]
    
    for username in test_usernames:
        search_user_account(username)
        print("\n")