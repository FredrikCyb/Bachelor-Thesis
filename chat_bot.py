from shodan_interface import ShodanInterface
from language_model import LanguageModel
from shodan_processor import ShodanProcessor

class ChatBot:
    def __init__(self, shodan_client: ShodanInterface, lm: LanguageModel):
        self.shodan = shodan_client
        self.lm = lm
        self.processor = ShodanProcessor()

    def handle_query(self, user_input: str) -> str:
        if user_input.lower().startswith("search:"):
            query = user_input[len("search:"):].strip()
            shodan_data = self.shodan.host(query)
            
            # Preprocess the Shodan data
            processed_data = self.processor.preprocess_shodan_data(shodan_data)
            
            # Create a well-structured prompt for analysis
            prompt = self.processor.create_analysis_prompt(processed_data)
            print(prompt)
            
            return self.lm.generate_response(prompt)
        else:
            return self.lm.generate_response(user_input)