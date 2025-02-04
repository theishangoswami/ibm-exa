"""
IBM WatsonX AI client configuration and setup.
"""
import os
from dotenv import load_dotenv
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials

class WatsonXClient:
    """Wrapper for IBM WatsonX AI client with project ID handling."""
    
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        
        # Get credentials from environment variables
        self.api_key = os.getenv('IBM_WATSONX_API_KEY')
        self.url = os.getenv('IBM_WATSONX_URL')
        self.project_id = os.getenv('IBM_WATSONX_PROJECT_ID')
        
        if not all([self.api_key, self.url, self.project_id]):
            raise ValueError(
                "Missing required environment variables. "
                "Please ensure IBM_WATSONX_API_KEY, IBM_WATSONX_URL, and IBM_WATSONX_PROJECT_ID "
                "are set in .env file"
            )
        
        # Create credentials object
        self.credentials = Credentials(
            url=self.url,
            api_key=self.api_key
        )
        
        # Create API client
        self.client = APIClient(credentials=self.credentials, project_id=self.project_id)

def get_client() -> WatsonXClient:
    """
    Create and return a configured IBM WatsonX AI client.
    
    Returns:
        WatsonXClient: Configured IBM WatsonX AI client wrapper
    
    Raises:
        ValueError: If required environment variables are not set
    """
    return WatsonXClient() 