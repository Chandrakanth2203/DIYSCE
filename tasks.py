from crewai import Task
from agents import user_details_agent, live_agent, problem_solver
from Conversation_File import Conversation_File



"""
Task for Agent-1: Task Definition for User Issue Summarization
"""
# Define the search task
issue_decoding_task = Task(
    description="""Understand the user's issue by analysing the conversation
     The steps to do that are:
    - Analyze the conversation to identify the user's issue based on the messages exchanged.
    - Extract key details about the issue such as error messages, affected features, and any relevant context provided by the user.
    - Summarize the issue in a clear and concise manner, highlighting the main problem and any critical information that can help in troubleshooting.
    - Provide a comprehensive summary of the user's issue that can be easily understood by customer service agents and technical support teams.""",
    expected_output="""A clear and concise summary of the user's issue based on the conversation analysis, including:
    - Main problem identified
    - Key details and context about the issue
    - Any error messages or affected features mentioned by the user
    The summary should be comprehensive and provide enough information for customer service agents to understand the issue and take appropriate action.""",
    agent=live_agent
)

"""
Task for Agent-2: Task Definition for User Account Search
"""
# Define the search task
search_user_task = Task(
    description="""Search for the user's account in the database. 
    Use the username provided to retrieve detailed account information including:
    - User ID and contact information
    - Account status and subscription type
    - Account creation date and last login
    
    Provide a comprehensive summary of the user account details found.
    If the user account is not found, clearly state that the account does not exist.""",
    expected_output="""A detailed report of the user account information including all available details such as:
    - Complete user identification (ID, username, email)
    - Account status (active, inactive, suspended)
    - Subscription information
    - Account timeline (created date, last login)
    
    If no account is found, provide a clear not-found message.""",
    agent=user_details_agent
)

"""
Task for Agent-3: Task Definition for Problem Solving and Recommendations
"""
# Define the search task
problem_solving_task = Task(
    description="""Consolidate the issue summary from Agent-1 and user account details from Agent-2 to provide critical insights and actionable recommendations.
     The steps to do that are:
    - Analyze the issue summary to understand the user's problem and its context.
    - Review the user account details to identify any relevant information that may impact the issue (e.g., account status, subscription type).
    - Provide critical insights into the potential causes of the issue based on the information available.
    - Offer clear and actionable recommendations on how to resolve the issue, including any necessary steps for troubleshooting or escalation.""",
    expected_output="""A clear and concise summary of the solution to the user's issue based on the conversation analysis, including:
    - Critical insights into the potential causes of the issue
    - Actionable recommendations for resolving the issue with a step by step guide for the customer to follow directly.
    The summary should provide a clear path to resolution and be easily understood by customer without having to reach out to an agent again.""",
    context=[
        issue_decoding_task,
        search_user_task
    ],
    agent=problem_solver
)