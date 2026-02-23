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

