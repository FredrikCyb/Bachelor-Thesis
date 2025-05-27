from language_model import LanguageModel
from huggingface_hub import login
import os

class GemmaModel(LanguageModel):
    def __init__(self, model_path: str, huggingface_token: str):
        self.chat_history = []
        
        if not huggingface_token:
            print("[WARNING] No Hugging Face token found. Make sure you're logged in.")
            os._exit(0)
        login(huggingface_token)
        
        from transformers import AutoModelForCausalLM, AutoTokenizer
        import torch
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto", torch_dtype=torch.bfloat16)

    def generate_response(self, prompt: str) -> str:
        # Add user message to history
        self.chat_history.append({"role": "user", "content": prompt})
        
        # Apply chat template with full history
        formatted_prompt = self.tokenizer.apply_chat_template(self.chat_history, tokenize=False, add_generation_prompt=True)

        inputs = self.tokenizer(formatted_prompt, add_special_tokens=True, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=2000,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.2
        )

        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract the new response by finding the last complete response
        # First, split by "model" to get all responses
        parts = decoded.split("model")
        
        if len(parts) > 1:
            # Get the last part which should be the new response
            last_response = parts[-1].strip()
            
            # If the response starts with "user", it means we got the wrong part
            if last_response.startswith("user"):
                # Try to find the actual response by looking for the last non-user part
                for part in reversed(parts[:-1]):
                    if not part.strip().startswith("user"):
                        last_response = part.strip()
                        break
            
            response = last_response
        else:
            response = decoded.strip()
        
        # Add assistant's response to history
        self.chat_history.append({"role": "assistant", "content": response})

        return response

    def clear_history(self):
        """Clear the chat history."""
        self.chat_history = []