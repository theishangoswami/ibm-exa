"""
Test the WatsonX AI client configuration.
"""
import os
import pytest
from src.client import get_client
from ibm_watsonx_ai import APIClient

def test_get_client_with_env_vars(monkeypatch):
    """Test client creation with environment variables."""
    # Mock environment variables
    monkeypatch.setenv('IBM_WATSONX_API_KEY', 'test-key')
    monkeypatch.setenv('IBM_WATSONX_URL', 'https://test-url.com')
    
    # Get client
    client = get_client()
    
    # Assert client is created correctly
    assert isinstance(client, APIClient)

def test_get_client_missing_env_vars(monkeypatch):
    """Test client creation fails without environment variables."""
    # Clear environment variables
    monkeypatch.delenv('IBM_WATSONX_API_KEY', raising=False)
    monkeypatch.delenv('IBM_WATSONX_URL', raising=False)
    
    # Assert error is raised
    with pytest.raises(ValueError):
        get_client() 