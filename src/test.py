"""
Simple test file for WatsonX AI setup.
"""
from .client import get_client

def main():
    print("Testing WatsonX AI setup...")
    
    try:
        # Try to initialize the client
        client_wrapper = get_client()
        print("✓ Successfully connected to WatsonX AI")
        print(f"✓ Using project ID: {client_wrapper.project_id}")
        print("✓ Connection test complete!")
        
    except Exception as e:
        print("✗ Error:", str(e))

if __name__ == "__main__":
    main() 