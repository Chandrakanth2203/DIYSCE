from crewai import Task

"""
Task for Agent-1: Task Definition for User Issue Summarization
"""
# Define the search task

def read_conversation_task(agent, tools):
    """
    Task expects an input variable: `conversation_file`
    """
    return Task(
    description="""Understand the user's issue by analysing the conversation from the {conversation_file_path} and summarize it in a clear and concise manner.
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
    agent=agent,
    tools= tools,
    async_execution=True,
    output_file="Final_Solution/output_files/issue_summary_conversation.txt"
)

"""
Task for Agent-2: Task Definition for User Details Retrieval from DB
"""

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
    tools=tools,async_execution=True,
    output_file="Final_Solution/output_files/userDetails_conversation.txt"
)

"""
Task for Agent-3: Task Definition for Solution Synthesis and Recommendation
"""
def problem_solving_task(agent, tools, context_tasks):

    return Task(
        description="""Consolidate the issue summary from the read conversation task and user account details from get customer details task responses to provide critical insights and actionable recommendations by collating the information from the {module_corpus_path}.
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
    context=context_tasks,
    output_file="Final_Solution/output_files/problem_solving_output.txt"
    )