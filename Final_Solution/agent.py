import os
from crewai import Agent
from crewai.llm import LLM
from dotenv import load_dotenv

#Load the API Key from .env file
load_dotenv()

#Initiate the LLM with the API key and other parameters
llm = LLM(
    model = "openai/gpt-4o",
    api_key = os.getenv("LLM_API_KEY"),
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    temperature = 0.1,
    max_tokens = 5000,
    timeout = 120
)

"""
Agent-1: Summarize Caller Issue
Defines the agent that decodes caller messages to summarize the issue reported by the caller
"""

def conversation_analysis_template():
    return """You are a customer service specialist agent who excels at understanding customer's issues and summarizing them clearly.
    Your task is to analyze the conversation to identify the user's issue based on the messages exchanged.
    Extract key details about the issue such as error messages, affected features, and any relevant context provided by the user.
    Extract only the issue in a clear and concise manner"""

# Define the Get User Details Agent

def file_reader_agent(file_read_tool):
    return Agent(
    role="Customer Service Agent",
    goal="Summarize the issue reported by the caller from the conversation",
    backstory="""You are a customer service specialist agent with 10 years of experience who excels at understanding customer's issues
    and summarizing them clearly from the conversation input.""",
    tools=[file_read_tool],
    verbose=True,
    llm=llm,
    system_template=conversation_analysis_template(),
    max_execution_time=300
)


"""
Agent-2: Retrieve Caller Information from DB
Defines the agent that retrieves caller information from the database based on the conversation context
"""

# Define the Get User Details Agent

def user_details_retriever_agent(file_read_tool, db_reader_tool):
    return Agent(
    role="User Details Retriever Agent",
    goal="Retrieve and summarize user details from the db based on the conversation",
    backstory="""You are a database expert with 10 years of experience who excels at 
    extracting user details from the database and summarizing them clearly based on the conversation input.""",
    tools=[file_read_tool, db_reader_tool],
    verbose=True,
    llm=llm,
    max_execution_time=300
)

"""
Agent-3: Problem Solving Agent
Defines the agent that analyzes the caller's issue and user details to provide critical insights and gives the recommendations on how to resolve the issue
"""

# Define the Get User Details Agent
def problem_solver_agent(file_read_tool):
    return Agent(
        role="Problem Solving Agent",
        goal="Understand the caller's issue and user details along with the Module_Corpus to provide critical insights and recommendations on how to resolve the issue",
        backstory="""You are a problem solver agent who excels at understanding the issue summary and providing precise steps to resolve the issue.
         You analyze the issue details and user information to give actionable recommendations to customer service agents.""",
        verbose=True,
        tools=[file_read_tool],
        llm=llm,
        max_execution_time=300
    )

