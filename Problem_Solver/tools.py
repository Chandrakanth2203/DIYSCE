from crewai_tools import FileReadTool
from crewai.tools import tool
import sqlite3

# Create a file reader tool instance
def make_file_reader_tool():
    # Return a callable tool that expects {"file_path": "..."}
    # FileReadTool can accept file_path via the tool call input
    return FileReadTool()

# Create a database reader tool using crewai's @tool decorator



@tool
def read_from_database(query: str, db_path: str = "CustomerDB.db") -> str:
        """
        Executes a query on the database and returns results.
        Args:
            query: SQL or search query to execute on the database
            db_path: Path to the SQLite database file
        """
        try:
            # Connect to the database
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            
            # Execute the query
            cur.execute(query)
            rows = cur.fetchall()
            
            # Close the connection
            cur.close()
            conn.close()
            
            # Format results as a string
            if rows:
                return str(rows)
            else:
                return "No results found for the query."
        except Exception as e:
            return f"Error executing query: {str(e)}"
    
# def db_reader_tool():
#     """Factory function that returns a database reader tool"""
#     @tool("Database Reader")
#     def read_from_database(query: str, db_path: str = "CustomerDB.db") -> str:
#         """
#         Executes a query on the database and returns results.
#         Args:
#             query: SQL or search query to execute on the database
#         """
#         # Placeholder for database reading
#         # In a real implementation, this would connect to a database and execute the query
#         return f"Results for query: {query}"
    
#     return read_from_database

# def db_reader_tool(query):
#     # Placeholder for a database reader tool
#     # In a real implementation, this would connect to a database and execute the query
#     # For this example, we'll just return a mock response
#     return f"Results for query: {query}"  