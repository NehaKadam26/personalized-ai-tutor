def get_lesson_prompt(topic: str, level: str = "beginner") -> str:
    level_guidance = {
        "beginner": "Use simple language and relatable analogies. Assume the reader knows nothing. Build concepts from scratch.",
        "intermediate": "Assume basic familiarity. Skip basic definitions, go deeper into how and why things work.",
        "advanced": "Assume strong prior knowledge. Focus on edge cases, best practices, tradeoffs, and expert-level insights."
    }.get(level, "Use clear, appropriate language for the level.")

    return f"""
You are an expert tutor creating a high-quality lesson on the following:

Topic: {topic}
Level: {level}

Level guidance: {level_guidance}

RULES:
- Do NOT write long paragraphs. Break content into short paragraphs (2-3 sentences max), bullet points, and examples.
- Actually teach — do not say "in this section we will cover...". Get straight to the point.
- For technical topics, include short code snippets with a 1-2 line explanation. Put code on its own line.
- Use real-world examples or analogies to illustrate ideas.
- Keep each section focused and scannable — mix short paragraphs with bullet points.
- Do not use emojis other than the ones specified in the format below.
- IMPORTANT: Always complete every section fully. Never cut off mid-sentence or leave a section unfinished.

FORMAT (follow exactly):

## 🎯 Learning Objectives
- 3-4 specific things the learner will understand or be able to do

## 📚 Lesson Outline

### 1. [Section Title]
[2-3 sentence intro to the concept]

[Bullet points or short explanation of key points]
- Point 1
- Point 2
- Point 3

[One concrete example or analogy, kept brief]

### 2. [Section Title]
[Same structure as above]

### 3. [Section Title]
[Same structure as above]

### 4. [Section Title]
[Same structure as above]

## 💡 Key Concepts to Remember
- **Concept**: one clear sentence
- **Concept**: one clear sentence
- **Concept**: one clear sentence

## 🔓 What You'll Be Able to Do After This Lesson
- Outcome 1
- Outcome 2
- Outcome 3
"""


def get_quiz_prompt(topic: str, level: str, lesson_content: str) -> str:
    return f"""
You are an expert tutor. Based on the lesson below, generate a 5-question multiple choice quiz.

Topic: {topic}
Level: {level}

Lesson:
{lesson_content}

RULES:
- Each question must test understanding, not just memorization.
- Questions should be based strictly on the lesson content above.
- Each question has exactly 4 options labeled A, B, C, D.
- Only one option is correct.
- Vary the difficulty slightly across questions.
- Do not repeat similar questions.
- Return ONLY valid JSON. No explanation, no markdown, no code fences.

Return this exact JSON structure:
[
  {{
    "question": "Question text here?",
    "options": {{
      "A": "First option",
      "B": "Second option",
      "C": "Third option",
      "D": "Fourth option"
    }},
    "answer": "A",
    "explanation": "Brief explanation of why this is correct and others are wrong."
  }}
]
"""


def get_explanation_prompt(question: str, user_answer: str, correct_answer: str, explanation: str) -> str:
    return f"""
A student answered a quiz question. Give a short, factual response — no encouragement, no filler phrases.

Question: {question}
Student's answer: {user_answer}
Correct answer: {correct_answer}
Explanation: {explanation}

If correct: Confirm it's correct and state why in 1 sentence.
If wrong: State what the correct answer is and why in 1-2 sentences. Do not say things like "don't worry", "great try", or "easy mistake". Just explain the fact.

No bullet points. Plain prose only.
"""