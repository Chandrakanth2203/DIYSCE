from crewai import Task
# from agent import  live_agent
from crewai_tools import FileReadTool

"""
Task for Agent-2: Task Definition for User Issue Summarization
"""
conversation_file_path = "testData/conversation.txt"  # Path to the conversation file containing the user's messages and interactions with customer service agents.
db_file_path = "CustomerDB.db" # Path to the database file containing user account information
# Define the search task

def get_customer_details_task(agent, tools):
    """
    Task expects an input variable: `conversation_file and the db`
    """
    return Task(
    description="""Extract user identification details from the conversation in {conversation_file_path} and search the database at {db_file_path} to retrieve the user's account information. 
    Extract the entire row from the DB for the matching user account and present all details as label-value pairs. If the user account is not found, clearly state 'Account not found' with the search criteria used.
     The steps to do that are:
     - Get the user details from the conversation file such as id and name.
     - Using the extracted user details, construct a query to search the database for the user's account information and use contains in the query instead of exact match for anything apart from id and only use name and id to query
     .
     - Retrieve the entire row of user account information from the database for the matching user account.
     - Also print all the details as label-value pairs of all values and also the seperate value of fetched data. 
     For example, if the database has columns like id, name, phone, dob, credits, account_locked_int in the table name - customers
     """,
    expected_output="""A structured report of the user account information with all details presented as label-value pairs:
    - id_str, name, phone, dob, credits_str, locked_str
    If the user account is not found in the database, clearly state: 'Account not found' with the search criteria used.""",
    agent=agent,
    tools=tools,
    output_file="output_files/userDetails_conversation.txt"
)