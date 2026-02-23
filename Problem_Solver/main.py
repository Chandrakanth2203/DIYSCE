import os
from crewai import Crew
from tools import make_file_reader_tool
from agent import problem_solver_agent
from task import problem_solving_task

def main():
    # Resolve the file path robustly
    project_root = os.path.dirname(os.path.abspath(__file__))
    issue_summary_path = os.path.join(project_root, "Problem_Solver/issue_summary_conversation.txt.txt")
    module_corpus_path = os.path.join(project_root, "Module_Corpus")
    user_details_path = os.path.join(project_root, "userDetails_conversation.txt")
    # Sanity-check the file exists
    if not os.path.exists(issue_summary_path):
        raise FileNotFoundError(f"Missing file: {issue_summary_path}")
    if not os.path.exists(module_corpus_path):
        raise FileNotFoundError(f"Missing file: {module_corpus_path}")
    if not os.path.exists(user_details_path):
        raise FileNotFoundError(f"Missing file: {user_details_path}")

    # Create tool & agent
    file_tool = make_file_reader_tool()
    agent = problem_solver_agent(file_tool)
    
    # Create task with the tool bound in the agent; tool can still be listed in task
    task = problem_solving_task(agent=agent, tools=[file_tool])

    crew = Crew(
    agents=[agent],
    tasks=[task],
    memory=False,
    verbose=True
    )

    # Run the crew with the task input variables
    result = crew.kickoff(
        inputs={
        "issue_summary_path": issue_summary_path,
        "module_corpus_path": module_corpus_path,
        "user_details_path": user_details_path
    }
    )
    print("\n=== RESULT ===\n")
    print(result)

if __name__ == "__main__":
    main()
