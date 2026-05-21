import os
import json
from groq import Groq
from dotenv import load_dotenv
from utils.prompts import get_lesson_prompt, get_quiz_prompt, get_explanation_prompt
import streamlit as st

load_dotenv()

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)


def generate_lesson(topic: str, level: str = "beginner") -> str:
    prompt = get_lesson_prompt(topic, level)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful and knowledgeable tutor who creates clear, structured lessons."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=1500,
    )
    return response.choices[0].message.content


def generate_quiz(topic: str, level: str, lesson_content: str) -> list:
    prompt = get_quiz_prompt(topic, level, lesson_content)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a quiz generator. You return only valid JSON arrays, no markdown, no explanation."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.5,
        max_tokens=2000,
    )
    raw = response.choices[0].message.content.strip()
    # Strip markdown fences if model adds them despite instructions
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def explain_answer(question: str, user_answer: str, correct_answer: str, explanation: str) -> str:
    prompt = get_explanation_prompt(question, user_answer, correct_answer, explanation)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a concise tutor giving direct, factual feedback on a quiz answer."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=200,
    )
    return response.choices[0].message.content