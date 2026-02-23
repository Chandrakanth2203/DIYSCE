from crewai import Task
# from agent import  live_agent

"""
Task for Agent-1: Task Definition for User Issue Summarization
"""
issue_summary_path = "issue_summary_conversation.txt"  # Path to the conversation file containing the user's messages and interactions with customer service agents.
module_corpus_path = "Module_Corpus" # Path to the database file containing user account information
user_details_path = "userDetails_conversation.txt" # Path to the database file containing user account information
# Define the search task

def problem_solving_task(agent, tools):

    return Task(
        description="""Consolidate the issue summary from {issue_summary_path} and user account details from {user_details_path} to provide critical insights and actionable recommendations by collating the information from the {module_corpus_path}.
     The steps to do that are:
    - Analyze the issue summary to understand the user's problem and its context.
    - Review the user account details to identify any relevant information that may impact the issue (e.g., account status, subscription type).
    - Provide critical insights into the potential causes of the issue based on the information available.
    - Offer clear and actionable recommendations on how to resolve the issue, including any necessary steps for troubleshooting or escalation.""",
        expected_output="""A clear and concise summary of the solution to the user's issue based on the conversation analysis, including:
    - Critical insights into the potential causes of the issue
    - Actionable recommendations for resolving the issue with a step by step guide for the customer to follow directly.
    The summary should provide a clear path to resolution and be easily understood by customer without having to reach out to an agent again.""",
    agent=agent,
    tools=tools,
    output_file="output_files/problem_solving_output.txt"
    )