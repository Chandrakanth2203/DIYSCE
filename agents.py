import os
from crew.ai import Agent
from crewai.llm import LLM
from dotenv import load_dotenv
from db_retriever_tool import DBRetrieverTool

load_dotenv()

llm = LLM(
    model = "openai/gpt-4o",
    api_key = os.getenv("OPENAI_API_KEY"),
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    temperature = 0.1,
    max_tokens = 5000,
    timeout = 120
)


"""
Agent-1: Summarize Caller Issue
Defines the agent that decodes caller messages to summarize the issue reported by the caller
"""

# Initialize the DB retriever tool
db_tool = DBRetrieverTool()
# Define the Get User Details Agent
live_agent = Agent(
    role="Customer Service Agent",
    goal="Summarize the issue reported by the caller from the conversation",
    backstory="You are a customer service specialist agent who excels at understanding customer's issues and summarizing them clearly.",
    tools=[
        {
            "name": "file_reader",
            "description": "Read file and give the context to the Agent",
            "function": db_tool.file_reader('Conversation_File.txt')
        },
    ],
    verbose=True
)

"""
Agent-2: Get User Details
Defines the agent that retrieves user information from database
"""


# Define the Get User Details Agent
user_details_agent = Agent(
    role="User Details Retriever",
    goal="Search and retrieve user account information from the database based on provided search criteria",
    backstory="""You are a database specialist agent who excels at retrieving accurate user account information. 
    You understand the importance of data accuracy and provide detailed account information to support customer service and system administration. 
    You can search by username, email, or name and provide comprehensive account details.""",
    tools=[
        {
            "name": "get_user_account",
            "description": "Search for a specific user account by username in the database",
            "function": db_tool.get_user_account
        },
        {
            "name": "search_user_accounts", 
            "description": "Search for user accounts by username, email, or full name",
            "function": db_tool.search_user_accounts
        },
        {
            "name": "get_all_user_accounts",
            "description": "Retrieve all user accounts from the database",
            "function": db_tool.get_all_user_accounts
        }
    ],
    verbose=True
)

"""
Agent-3: Critical Thinker Agent
Defines the agent that analyzes the caller's issue and user details to provide critical insights and gives the recommendations on how to resolve the issue
"""

# Define the Get User Details Agent
problem_solver = Agent(
    role="Critical Thinker Agent",
    goal="Understand the caller's issue and user details to provide critical insights and recommendations on how to resolve the issue",
    backstory="""You are a problem solver agent who excels at understanding the issue summary and providing precise steps to resolve the issue.
     You analyze the issue details and user information to give actionable recommendations to customer service agents.""",
    verbose=True
)