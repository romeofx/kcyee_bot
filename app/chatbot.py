import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_response(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful educational tutor."},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"
