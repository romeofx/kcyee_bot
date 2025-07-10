import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_response(message):
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return "❌ Missing API key."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Educational Tutor Bot"
    }

    messages = [
        {"role": "system", "content": "You are a helpful tutor. Be clear, simple, and focused."},
        {"role": "user", "content": message}
    ]

    try:
        res = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json={
                "model": "mistralai/mistral-7b-instruct",
                "messages": messages
            }
        )
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"❌ Error: {str(e)}"
