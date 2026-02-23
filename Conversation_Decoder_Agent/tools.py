# tools.py
from crewai_tools import FileReadTool
import os

# Create a tool instance WITHOUT hardcoding the path
# We'll pass the file path when the task runs
def make_file_reader_tool():
    # Return a callable tool that expects {"file_path": "..."}
    # FileReadTool can accept file_path via the tool call input
    return FileReadTool()