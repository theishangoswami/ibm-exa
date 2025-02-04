"""
Example usage of the WatsonX AI model with web search capabilities.
"""
import os
import logging
from dotenv import load_dotenv
from .model import WatsonXModel, AvailableModels

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    print("Starting WatsonX AI example...")
    
    # Load environment variables
    load_dotenv()
    exa_api_key = os.getenv('EXA_API_KEY')
    
    if not exa_api_key:
        print("Error: EXA_API_KEY not found in environment variables")
        return
    
    try:
        # Initialize model with Exa search capability
        print("\nInitializing Mixtral model with web search...")
        model = WatsonXModel(exa_api_key=exa_api_key)
        
        # Example 1: Current events question with web search
        question = "What is the recent project stargate?"
        print("\n=== Example 1: Current Events Question (With Web Search) ===")
        print("Question:", question)
        print("Searching and thinking...")
        
        answer = model.ask_with_search(question)
       
        print("\nAnswer:", answer)
     
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        print("\nAn error occurred while running the example. Please check the logs for details.")

if __name__ == "__main__":
    main()
    print("\nExample completed!") 