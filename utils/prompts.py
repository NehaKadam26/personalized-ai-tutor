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