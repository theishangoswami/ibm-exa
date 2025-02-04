"""
Tools for WatsonX AI tool calling.
"""
import json
from typing import Dict, Any
from .exa_client import ExaSearchClient

def create_web_search_tool() -> Dict[str, Any]:
    """Create the web search tool definition."""
    return {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for current information. Always cite sources.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    }
                },
                "required": ["query"]
            }
        }
    }

class ToolExecutor:
    def __init__(self, exa_client: ExaSearchClient):
        self.exa_client = exa_client
    
    def execute_tool(self, tool_call: Dict[str, Any]) -> str:
        """Execute a tool call and return the result."""
        if tool_call["type"] != "function":
            return "Unsupported tool type"
            
        function_call = tool_call["function"]
        if function_call["name"] == "web_search":
            try:
                # Execute search
                query = json.loads(function_call["arguments"])["query"]
                results = self.exa_client.search(query)
                
                # Format results
                formatted_results = []
                for result in results:
                    formatted_results.append(
                        f"Source: {result['title']}\n"
                        f"URL: {result['url']}\n"
                        f"Content: {result['text']}\n"
                    )
                
                return "\n\n".join(formatted_results)
                
            except Exception as e:
                return f"Error executing web search: {str(e)}"
        
        return "Unknown tool" 