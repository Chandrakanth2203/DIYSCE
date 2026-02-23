import os
from crewai import Agent
from crewai.llm import LLM
from dotenv import load_dotenv
from crewai_tools import FileReadTool

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
