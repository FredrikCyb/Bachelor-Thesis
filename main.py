from config.config import Config
from chat_bot import ChatBot
from shodan_client import ShodanClient
from gemma_model import GemmaModel

def print_help():
    print("\nAvailable commands:")
    print("  search:<ip>  - Search for information about a specific IP address")
    print("  clear       - Clear the chat history")
    print("  help        - Show this help message")
    print("  exit        - Exit the program")
    print("\nYou can also just chat normally with the bot!")

def main():
    config = Config()
    
    shodan_client = ShodanClient(config.shodan_api_key)
    language_model = GemmaModel(
        model_path="google/gemma-3-1b-it", 
        huggingface_token=config.huggingface_token
    )
    bot = ChatBot(shodan_client, language_model)

    print("\n=== Shodan Chat Bot ===")
    print_help()
    print("\n" + "="*50)

    while True:
        try:
            query = input("\nYou: ").strip()
            
            if not query:
                continue
                
            if query.lower() == 'exit':
                print("\nGoodbye!")
                break
            elif query.lower() == 'clear':
                language_model.clear_history()
                print("\nChat history cleared!")
                continue
            elif query.lower() == 'help':
                print_help()
                continue
            
            response = bot.handle_query(query)
            print("\nBot:", response)
            print("-"*50)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please try again or type 'help' for available commands.")

if __name__ == "__main__":
    main()