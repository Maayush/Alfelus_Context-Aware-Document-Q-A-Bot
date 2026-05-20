import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_answer(question, context):

    if not context.strip():
        return "No relevant content found."

    prompt = f"""
You are a helpful AI document assistant.

Answer ONLY from the provided context.

If the answer is not present in the context, say:
"I could not find this information in the uploaded document."

Context:
{context}

Question:
{question}

Answer:
"""

    try:

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
        )

        data = response.json()

        print("OPENROUTER RESPONSE:", data)

        # Handle API errors safely
        if "choices" not in data:

            if "error" in data:
                return f"LLM API Error: {data['error']}"

            return "Unexpected API response."

        return data["choices"][0]["message"]["content"]

    except Exception as e:

        print("LLM ERROR:", str(e))

        return f"Error generating answer: {str(e)}"