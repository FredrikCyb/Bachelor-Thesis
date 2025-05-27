import yaml
import os
import shutil

class Config:
    def __init__(self, config_path="config.yaml", example_config_path="config.yaml.example"):
        self.config_path = config_path
        self.example_config_path = example_config_path
        self.config = self._load_config()

    def _load_config(self):
        """Load configuration from file, creating it from example if needed."""
        if not os.path.exists(self.config_path):
            if os.path.exists(self.example_config_path):
                print(f"Config file '{self.config_path}' not found. Creating from example config...")
                shutil.copy2(self.example_config_path, self.config_path)
                print(f"Please update '{self.config_path}' with your actual API keys.")
                exit(1)
            else:
                print(f"Neither '{self.config_path}' nor '{self.example_config_path}' found.")
                print("Please ensure at least one of these files exists.")
                exit(1)

        try:
            with open(self.config_path, 'r') as file:
                return yaml.safe_load(file)
        except yaml.YAMLError as e:
            print(f"Error parsing configuration file: {e}")
            exit(1)

    @property
    def shodan_api_key(self):
        return self.config['api_keys']['shodan']

    @property
    def huggingface_token(self):
        return self.config['api_keys']['huggingface'] 