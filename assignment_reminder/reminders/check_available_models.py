import os
import google.generativeai as genai
from dotenv import load_dotenv

# Get the absolute path of the parent directory where .env is located
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../assignment_reminder"))  # Adjust based on depth

print(BASE_DIR)
# Load .env from the parent directory
dotenv_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path)

# Get API key
api_key = os.getenv("GEMINI_API_KEY")  

if not api_key:
    raise ValueError("🚨 GEMINI_API_KEY is missing. Check your .env file!")

genai.configure(api_key=api_key)

# List available models
available_models = genai.list_models()
for model in available_models:
    print(model.name)
