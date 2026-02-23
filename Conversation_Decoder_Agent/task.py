from crewai import Task
# from agent import  live_agent

"""
Task for Agent-1: Task Definition for User Issue Summarization
"""
conversation_file_path = "testData/conversation.txt"  # Path to the conversation file containing the user's messages and interactions with customer service agents.
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
    output_file="output_files/issue_summary_conversation.txt"
)