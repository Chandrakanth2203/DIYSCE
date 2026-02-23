import os
from crewai import Crew
from tools import make_file_reader_tool
from agent import file_reader_agent
from task import read_conversation_task

def main():
    # Resolve the file path robustly
    project_root = os.path.dirname(os.path.abspath(__file__))
    conversation_path = os.path.join(project_root, "conversation")

    # Sanity-check the file exists
    if not os.path.exists(conversation_path):
        raise FileNotFoundError(f"Missing file: {conversation_path}")

    # Create tool & agent
    file_tool = make_file_reader_tool()
    agent = file_reader_agent(file_tool)
    
    # Create task with the tool bound in the agent; tool can still be listed in task
    task = read_conversation_task(agent=agent, tools=[file_tool])

    crew = Crew(
        agents=[agent],
        tasks=[task],
        memory=False,
        verbose=True
    )

    # Run the crew with the task input variables
    result = crew.kickoff(
        inputs={
         "conversation_file_path": conversation_path
        }
    )
    print("\n=== RESULT ===\n")
    print(result)

if __name__ == "__main__":
    main()
