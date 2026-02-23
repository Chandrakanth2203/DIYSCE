import os
from crewai import Crew, Process
from tools import make_file_reader_tool, read_from_database
from agent import file_reader_agent, problem_solver_agent, user_details_retriever_agent
from task import get_customer_details_task, problem_solving_task, read_conversation_task

def main():
    # File Paths for Inputs - Resolve the file paths robustly
    project_root = os.path.dirname(os.path.abspath(__file__))
    conversation_path = os.path.join(project_root, "conversation")
    # issue_summary_path = os.path.join(project_root, "Problem_Solver/issue_summary_conversation.txt.txt")
    module_corpus_path = os.path.join(project_root, "Module_Corpus")
    db_file_path  = os.path.join(project_root, "CustomerDB.db" )
    # user_details_path = os.path.join(project_root, "userDetails_conversation.txt")
    # Sanity-check the file exists
    if not os.path.exists(conversation_path):
        raise FileNotFoundError(f"Missing file: {conversation_path}")
    # if not os.path.exists(issue_summary_path):
    #     raise FileNotFoundError(f"Missing file: {issue_summary_path}")
    if not os.path.exists(module_corpus_path):
        raise FileNotFoundError(f"Missing file: {module_corpus_path}")
    if not os.path.exists(db_file_path):
        raise FileNotFoundError(f"Missing file: {db_file_path}")
    # if not os.path.exists(user_details_path):
    #     raise FileNotFoundError(f"Missing file: {user_details_path}")

    #Tools Needed for the Agent
    file_tool = make_file_reader_tool()
    db_tool = read_from_database

    #Agents for the Crew
    conversation_decoder_agent = file_reader_agent(file_tool)
    user_details_agent = user_details_retriever_agent(file_tool, db_tool)
    problem_solution_agent = problem_solver_agent(file_tool)
    
    #Tasks for the Crew - can have multiple tasks
    conversation_decode_task = read_conversation_task(agent=conversation_decoder_agent, tools=[file_tool])
    user_details_task = get_customer_details_task(agent=user_details_agent, tools=[file_tool,db_tool])
    problem_solution_task = problem_solving_task(agent=problem_solution_agent, tools=[file_tool],context_tasks=[conversation_decode_task, user_details_task])

    crew = Crew (
        name = "DIYSCE_Bot",
    agents=[conversation_decoder_agent, user_details_agent, problem_solution_agent],
    tasks=[conversation_decode_task, user_details_task, problem_solution_task],
    # agents=[conversation_decoder_agent, user_details_agent],
    # tasks=[conversation_decode_task, user_details_task],
    process=Process.sequential,
    memory=False,
    verbose=True
    )

    # Run the crew with the task input variables
    result = crew.kickoff(
        inputs={
         "conversation_file_path": conversation_path,
         "db_file_path" : db_file_path,
        # # "issue_summary_path": issue_summary_path,
        "module_corpus_path": module_corpus_path,
        # # "user_details_path": user_details_path
        }
    )
    print("\n=== RESULT ===\n")
    print(result)

if __name__ == "__main__":
    main()
