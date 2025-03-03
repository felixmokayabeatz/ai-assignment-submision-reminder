import google.generativeai as genai
import os
import json
from django.conf import settings

# Load API key
GEMINI_API_KEY = settings.GEMINI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)


def get_reminder_message(submission_history):
    """
    Uses Google Gemini AI to analyze submission history and generate a personalized reminder.
    """
    prompt = f"""
    A student has a history of submitting assignments {submission_history} days before deadlines.
    Predict if they will submit the next assignment early, on time, or late.
    Also, generate a personalized motivational reminder.
    Return a JSON response in the format:
    {{"prediction": "...", "reminder": "..."}}
    """

    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    response = model.generate_content(prompt)
    
    try:
        # Extract the AI response text properly
        result_text = response.candidates[0].content.parts[0].text
        
        # Remove all formatting markers (like ```json and ```)
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
            
        # Parse the cleaned JSON
        result = json.loads(result_text)
        
        return result.get("prediction", "Unknown"), result.get("reminder", "Stay focused and submit your assignment on time!")
    except Exception as e:
        print(f"Error parsing response: {e}")  # Debugging
        print(f"Raw response text: {response.candidates[0].content.parts[0].text}")  # Log the raw response
        return "Unknown", "Stay focused and submit your assignment on time!"