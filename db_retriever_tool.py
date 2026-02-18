"""
DB Retriever Tool - Standalone tool for database operations
"""
from database import (
    initialize_database,
    get_user_by_username,
    search_users,
    get_all_users
)

class DBRetrieverTool:
    """Database retriever tool for accessing user account information"""
    
    def __init__(self):
        initialize_database()
    
    def get_user_account(self, username: str) -> str:
        """
        Search for user account in database by username
        
        Args:
            username: The username to search for
            
        Returns:
            Formatted string with user details or not found message
        """
        user = get_user_by_username(username)
        
        if user:
            return f"""
            User Account Found:
            - User ID: {user['user_id']}
            - Username: {user['username']}
            - Email: {user['email']}
            - Full Name: {user['full_name']}
            - Account Status: {user['account_status']}
            - Subscription Type: {user['subscription_type']}
            - Created Date: {user['created_date']}
            - Last Login: {user['last_login']}
            """
        return f"User account not found for username: {username}"
    
    def search_user_accounts(self, search_term: str) -> str:
        """
        Search for user accounts by username, email, or name
        
        Args:
            search_term: Search term to find matching users
            
        Returns:
            Formatted string with matching user accounts
        """
        users = search_users(search_term)
        
        if users:
            result = f"Found {len(users)} matching user account(s):\n"
            for user in users:
                result += f"\n- {user['username']} ({user['email']}) - Status: {user['account_status']}"
            return result
        return f"No user accounts found matching: {search_term}"
    
    def get_all_user_accounts(self) -> str:
        """
        Retrieve all user accounts from database
        
        Returns:
            Formatted string with all user accounts
        """
        users = get_all_users()
        
        if users:
            result = f"Total user accounts in database: {len(users)}\n"
            for user in users:
                result += f"\n- {user['username']} ({user['email']}) - Status: {user['account_status']}"
            return result
        return "No user accounts found in database"
    
    def file_reader(self, file_path: str) -> str:
        """
        Read content from a file
        
        Args:
            file_path: Path to the file to read
            """
        try:
                with open(file_path, "r") as f:
                    data = f.read()
                    return data
        except FileNotFoundError:
                return f"File not found: {file_path}"
        except Exception as e:
                return f"Error reading file: {e}"