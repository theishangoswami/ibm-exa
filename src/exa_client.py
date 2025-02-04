"""
Exa search client for web search capabilities.
"""
import logging
from typing import List, Dict, Any
from exa_py import Exa

# Set up detailed logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExaSearchClient:
    """Client for performing web searches using Exa."""
    
    def __init__(self, api_key: str):
        """Initialize the Exa client with API key."""
        self.client = Exa(api_key=api_key)
    
    def search(self, query: str, num_results: int = 3) -> List[Dict[str, Any]]:
        """
        Perform a web search and return formatted results.
        
        Args:
            query: Search query
            num_results: Number of results to return (default: 5)
            
        Returns:
            List of search results with title, text, and URL
        """
        try:
            logger.info(f"Searching Exa for: {query}")
            response = self.client.search_and_contents(
                query,
                type="auto",
                num_results=5,
                text=True,
            )
            
            logger.debug(f"Raw Exa response: {response}")
            
            # Extract and format relevant information from the raw JSON response
            formatted_results = []
            
            # Handle both dictionary and object responses
            results = []
            if isinstance(response, dict):
                results = response.get('data', {}).get('results', [])
            else:
                # If response is an object, try to access results directly
                results = getattr(response, 'results', [])
            
            for result in results:
                # Handle both dict and object access
                if isinstance(result, dict):
                    text = result.get('text', '')
                    title = result.get('title', 'No title')
                    url = result.get('url', '')
                    score = result.get('score', 0.0)
                    published_date = result.get('publishedDate', '')
                else:
                    text = getattr(result, 'text', '')
                    title = getattr(result, 'title', 'No title')
                    url = getattr(result, 'url', '')
                    score = getattr(result, 'score', 0.0)
                    published_date = getattr(result, 'publishedDate', '')
                
                if text:  # Only add results with text content
                    formatted_results.append({
                        "title": title,
                        "text": text[:500] + "..." if len(text) > 500 else text,
                        "url": url,
                        "score": score,
                        "published_date": published_date
                    })
            
            logger.info(f"Found {len(formatted_results)} results")
            if not formatted_results:
                logger.warning("No results found in the response")
                
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching Exa: {str(e)}", exc_info=True)
            return [] 