"""
Example of WatsonX AI tool calling.
"""
import os
from dotenv import load_dotenv
from .model import WatsonXModel

def main():
    # Load Exa API key
    load_dotenv()
    exa_api_key = os.getenv('EXA_API_KEY')
    
    if not exa_api_key:
        print("Error: EXA_API_KEY not found in environment variables")
        return
    
    # Initialize model
    model = WatsonXModel(exa_api_key=exa_api_key)
    
    # Ask a question that requires web search
    question = "What are the latest developments in AI regulation in 2024?"
    print("\nQuestion:", question)
    print("Processing...")
    
    # Get response using tool calling
    answer = model.ask(question)
    print("\nAnswer:", answer)

if __name__ == "__main__":
    main() 