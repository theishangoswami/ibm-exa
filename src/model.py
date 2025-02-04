"""
IBM WatsonX AI model interface for text generation.
"""
import logging
from typing import Optional, List, Dict, Any
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

from .client import get_client
from .exa_client import ExaSearchClient

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Available models in your environment
class AvailableModels:
    MIXTRAL = "mistralai/mixtral-8x7b-instruct-v01"
    LLAMA_70B = "meta-llama/llama-3-3-70b-instruct"
    GRANITE = "ibm/granite-13b-instruct-v2"

class WatsonXModel:
    """A simple interface for interacting with WatsonX AI models."""
    
    def __init__(self, model_id=AvailableModels.MIXTRAL, exa_api_key: Optional[str] = None):
        """
        Initialize the model with default parameters.
        
        Args:
            model_id: The ID of the model to use
            exa_api_key: Optional API key for Exa web search
        """
        logger.info(f"Initializing WatsonX model with {model_id}...")
        self.client_wrapper = get_client()
        
        # Initialize Exa client if API key provided
        self.exa_client = ExaSearchClient(exa_api_key) if exa_api_key else None
        
        # Default generation parameters
        self.params = {
            GenParams.MAX_NEW_TOKENS: 250,  # Maximum length of generated text
            GenParams.MIN_NEW_TOKENS: 1,    # Minimum length of generated text
            GenParams.TEMPERATURE: 0.7,     # Controls randomness (0.0-1.0)
            GenParams.TOP_P: 0.9,          # Controls diversity of generated text
            GenParams.TOP_K: 50,           # Controls vocabulary size for generation
        }
        
        try:
            # Initialize the model
            self.model = ModelInference(
                model_id=model_id,
                credentials=self.client_wrapper.credentials,
                project_id=self.client_wrapper.project_id,
                params=self.params
            )
            logger.info("Model initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing model: {str(e)}")
            raise
    
    def ask_with_search(self, question: str, num_results: int = 3) -> str:
        """
        Ask a question with web search enhancement.
        
        Args:
            question: The question to ask
            num_results: Number of search results to use
            
        Returns:
            The model's response as a string
        """
        logger.info(f"Processing question with web search: {question}")
        
        if not self.exa_client:
            return self.ask(question)
        
        try:
            # Perform web search
            search_results = self.exa_client.search(question, num_results)
            
            if not search_results:
                return self.ask(question)
            
            # Construct prompt with search results
            prompt = self._construct_search_prompt(question, search_results)
            
            # Generate response
            response = self.model.generate_text(prompt=prompt)
            logger.info("Response received successfully")
            return response.strip()
            
        except Exception as e:
            error_msg = f"Error generating response with search: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    def _construct_search_prompt(self, question: str, search_results: List[Dict[str, Any]]) -> str:
        """Construct a prompt that includes search results."""
        prompt = (
            "You are a knowledgeable AI assistant with access to recent information from web searches. "
            "Your task is to provide accurate, up-to-date answers based on the search results provided, "
            "while also drawing on your general knowledge.\n\n"
            f"Question: {question}\n\n"
            "Here are relevant search results from the web:\n\n"
        )
        
        for i, result in enumerate(search_results, 1):
            prompt += f"[Source {i}]\n"
            prompt += f"Title: {result['title']}\n"
            if result.get('published_date'):
                prompt += f"Published: {result['published_date']}\n"
            prompt += f"URL: {result['url']}\n"
            prompt += f"Content: {result['text']}\n\n"
        
        prompt += (
            "Instructions:\n"
            "1. Synthesize information from the search results and your knowledge\n"
            "2. Cite sources when using specific information from search results\n"
            "3. Consider the publication dates when assessing information relevance\n"
            "4. If search results are outdated or irrelevant, rely on your general knowledge\n"
            "5. Be clear about what information comes from searches vs. your knowledge\n\n"
            "Answer: "
        )
        
        return prompt
    
    def ask(self, question: str) -> str:
        """
        Ask a question to the model and get a response.
        
        Args:
            question: The question to ask
            
        Returns:
            The model's response as a string
        """
        logger.info(f"Asking question: {question}")
        try:
            response = self.model.generate_text(prompt=question)
            logger.info("Response received successfully")
            return response.strip()
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    def chat(self, messages: list) -> str:
        """
        Have a chat conversation with the model.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            
        Returns:
            The model's response as a string
        """
        logger.info("Starting chat conversation")
        try:
            response = self.model.chat(messages=messages)
            logger.info("Chat response received successfully")
            return response['choices'][0]['message']['content'].strip()
        except Exception as e:
            error_msg = f"Error in chat: {str(e)}"
            logger.error(error_msg)
            return error_msg 