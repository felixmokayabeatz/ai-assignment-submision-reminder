import google.generativeai as genai
import os
import json

# Load API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
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

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    
    # Extract structured JSON from response
    try:
        result = json.loads(response.text)
        return result["prediction"], result["reminder"]
    except Exception as e:
        return "Unknown", "Stay focused and submit your assignment on time!"

