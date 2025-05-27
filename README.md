# Shodan Chat Bot

A Python-based chatbot that combines Shodan's powerful internet intelligence with the Gemma language model to provide interactive information about IP addresses and network infrastructure.

## Features

- Interactive chat interface for querying Shodan data
- Powered by Google's Gemma 3 1B language model
- Real-time IP address information lookup
- Command-based interface with clear history and help options
- Modular language model interface allowing easy swapping of different language models

## Prerequisites

- Python 3.8 or higher
- Shodan API key
- Hugging Face token (for accessing the Gemma model)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Boic69/Shodan-Chatbot-Bachelor-Group-67
cd Shodan-Chatbot-Bachelor-Group-67
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Set up configuration:
   - Copy `config.yaml.example` to `config.yaml`
   - Add your Shodan API key and Hugging Face token to `config.yaml`

## Usage

Run the chatbot:
```bash
python main.py
```

### Available Commands

- `search:<ip>` - Search for information about a specific IP address
- `clear` - Clear the chat history
- `help` - Show available commands
- `exit` - Exit the program

You can also chat normally with the bot!

## Project Structure

- `main.py` - Main application entry point
- `chat_bot.py` - Chat bot implementation
- `shodan_client.py` - Shodan API client
- `shodan_processor.py` - Shodan data processing
- `gemma_model.py` - Gemma language model integration
- `config/` - Configuration management
- `config.yaml` - Configuration file (create from config.yaml.example)

## Customizing the Language Model

The chatbot uses a modular interface for language models, making it easy to swap out different models. To use a different language model:

1. Create a new model class that implements the required interface methods (similar to `gemma_model.py`)
2. Import and use your new model class in `chat_bot.py`
3. The system will automatically use your custom model implementation

Example of implementing a new model:
```python
class CustomLanguageModel:
    def __init__(self):
        # Initialize your model here
        pass

    def generate_response(self, prompt: str) -> str:
        # Implement your model's response generation
        return response
```

## Dependencies

- huggingface_hub==0.30.2
- PyYAML==6.0.2
- shodan==1.31.0
- torch==2.6.0
- transformers==4.51.1
- accelerate==1.6.0

## Acknowledgments

- [Shodan](https://www.shodan.io/) for providing the internet intelligence API
- [Google Gemma](https://huggingface.co/google/gemma-3-1b-it) for the language model
