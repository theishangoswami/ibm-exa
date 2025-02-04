"""
IBM WatsonX AI model interface with tool calling.
"""
import logging
from typing import Optional
from ibm_watsonx_ai.foundation_models import ModelInference

from .client import get_client
from .tools import create_web_search_tool, ToolExecutor
from .exa_client import ExaSearchClient

logger = logging.getLogger(__name__)

class WatsonXModel:
    def __init__(self, exa_api_key: Optional[str] = None):
        """Initialize the model with tool calling capabilities."""
        self.client_wrapper = get_client()
        
        # Initialize Exa client and tool executor
        self.exa_client = ExaSearchClient(exa_api_key) if exa_api_key else None
        self.tool_executor = ToolExecutor(self.exa_client) if self.exa_client else None
        
        # Initialize the model (using Mistral for tool calling)
        self.model = ModelInference(
            model_id="mistralai/mistral-large",
            credentials=self.client_wrapper.credentials,
            project_id=self.client_wrapper.project_id
        )
    
    def ask(self, question: str) -> str:
        """Ask a question using tool calling."""
        if not self.tool_executor:
            return "Exa API key not provided"
        
        try:
            # Initial message with the question
            messages = [{"role": "user", "content": question}]
            
            # Define available tools
            tools = [create_web_search_tool()]
            
            # Get model's response with tool calls
            response = self.model.chat(messages=messages, tools=tools)
            
            # Check if model wants to use tools
            if "choices" in response and response["choices"]:
                choice = response["choices"][0]
                if "message" in choice and "tool_calls" in choice["message"]:
                    tool_calls = choice["message"]["tool_calls"]
                    
                    # Execute tool calls and get results
                    tool_results = []
                    for tool_call in tool_calls:
                        result = self.tool_executor.execute_tool(tool_call)
                        tool_results.append(result)
                    
                    # Add tool results to conversation
                    messages.extend([
                        {
                            "role": "assistant",
                            "content": None,
                            "tool_calls": tool_calls
                        },
                        {
                            "role": "tool",
                            "content": "\n\n".join(tool_results),
                            "tool_call_id": tool_calls[0]["id"]
                        }
                    ])
                    
                    # Get final response using tool results
                    final_response = self.model.chat(messages=messages)
                    if "choices" in final_response and final_response["choices"]:
                        return final_response["choices"][0]["message"]["content"].strip()
            
            return "No response generated"
            
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return f"Error: {str(e)}" 