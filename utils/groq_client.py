import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def test_connection():
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "Say: Groq connection successful!"}],
        temperature=0.5,
        max_tokens=50,
    )
    print(response.choices[0].message.content)

if __name__ == "__main__":
    test_connection()