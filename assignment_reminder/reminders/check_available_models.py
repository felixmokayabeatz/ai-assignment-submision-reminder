import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")  # ✅ Get API key directly

if not api_key:
    raise ValueError("🚨 GEMINI_API_KEY is missing. Check your .env file!")

genai.configure(api_key=api_key)

# List available models
available_models = genai.list_models()
for model in available_models:
    print(model.name)
