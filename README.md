# IBM EXA Integration
Powered by [Exa](https://exa.ai)

This project combines IBM WatsonX AI with Exa's web search to create a smart AI assistant that can search the internet and answer questions with up-to-date information.

## What it Does

1. You ask a question
2. The AI (using IBM WatsonX) decides if it needs to search the web
3. If needed, it uses Exa to search the internet
4. The AI then gives you an answer using both the search results and its own knowledge
5. It includes sources and links in its answers

## Features

- Uses IBM WatsonX's Mistral model for smart decision making
- Searches the web using Exa for current information
- Automatically cites sources in answers
- Handles both simple questions and complex topics

## Setup

1. You need two API keys:
   - IBM WatsonX API key
   - Exa API key

2. Create a `.env` file with your keys:
```
IBM_WATSONX_API_KEY=your_ibm_key_here
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
IBM_WATSONX_PROJECT_ID=your_project_id_here
EXA_API_KEY=your_exa_key_here
```

3. Install Python requirements:
```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
pip install -r requirements.txt
```

## How to Use

Run the example:
```bash
python -m src.example
```

Or use in your code:
```python
from src.model import WatsonXModel

# Initialize the model
model = WatsonXModel(exa_api_key="your_exa_key")

# Ask a question
answer = model.ask("What are the latest developments in AI regulation?")
print(answer)
```

## Project Structure

```
ibm-exa/
├── src/
│   ├── client.py      # IBM WatsonX setup
│   ├── exa_client.py  # Web search client
│   ├── model.py       # Main AI model
│   ├── tools.py       # Search tool definition
│   └── example.py     # Usage example
├── .env              # Your API keys
└── requirements.txt  # Python packages needed
```

## How it Works

1. **Tool Calling**: The AI can decide when it needs to search the web for information
2. **Web Search**: Uses Exa's API to find relevant and current information
3. **Smart Answers**: Combines search results with the AI's knowledge

## Requirements

- [Python 3.8](https://www.python.org/downloads/) or higher
- [IBM WatsonX](https://www.ibm.com/products/watsonx-ai) account and API key
- [Exa API](https://dashboard.exa.ai/api-keys) key


