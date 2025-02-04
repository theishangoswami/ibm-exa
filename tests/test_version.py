"""
Test version information.
"""
from src import __version__

def test_version():
    """Test that version is a string."""
    assert isinstance(__version__, str) 