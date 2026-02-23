
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Fetch the API key
api_key = os.getenv("LLM_API_KEY")

print("Your API key is:", api_key)
