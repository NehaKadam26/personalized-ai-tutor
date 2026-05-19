import streamlit as st
from utils.groq_client import generate_lesson, generate_quiz, explain_answer

st.set_page_config(
    page_title="AI Tutor",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Serif+Display&display=swap');

html, body, [class*="css"], .stMarkdown, p, div, span, label {
    font-family: 'DM Sans', sans-serif !important;
}
#MainMenu, footer { visibility: hidden; }

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section[data-testid="stMain"] > div {
    background: #FFFCF0 !important;
}
.block-container {
    padding-top: 3rem !important;
    padding-bottom: 5rem !important;
    max-width: 800px !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}
[data-testid="stAppViewBlockContainer"] {
    max-width: 800px !important;
    margin: 0 auto !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

/* Page header */
.page-header { margin-bottom: 36px; }
.page-title {
    font-family: 'DM Serif Display', serif !important;
    font-size: 34px !important;
    font-weight: 400 !important;
    color: #6B2D2D !important;
    margin: 0 0 8px 0 !important;
    letter-spacing: -0.3px !important;
    line-height: 1.2 !important;
    border-bottom: none !important;
    padding-bottom: 0 !important;
}
.page-desc { font-size: 15px; color: #C47A7A; margin: 0; font-weight: 400; }

/* Stats */
.stats-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 28px; }
.stat-box { background: #fff; border: 1px solid #f0d0d0; border-radius: 12px; padding: 18px 20px; }
.stat-num { font-family: 'DM Serif Display', serif !important; font-size: 28px; font-weight: 400; color: #A94A4A; line-height: 1; }
.stat-lbl { font-size: 12px; color: #C47A7A; margin-top: 4px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.6px; }

/* Section label */
.section-label { font-size: 11px; font-weight: 600; color: #C47A7A; letter-spacing: 1.4px; text-transform: uppercase; margin-bottom: 14px; }

/* Inputs */
.stTextInput > label { font-size: 13px !important; font-weight: 500 !important; color: #6B2D2D !important; }
.stTextInput > div > div > input {
    border-radius: 9px !important; border: 1px solid #e8b8b8 !important;
    padding: 11px 14px !important; font-size: 14px !important;
    font-family: 'DM Sans', sans-serif !important; color: #3D2020 !important; background: #fff !important;
}
.stTextInput > div > div > input:focus { border-color: #A94A4A !important; box-shadow: 0 0 0 3px rgba(169,74,74,0.12) !important; }
.stTextInput > div > div > input::placeholder { color: #d4a0a0 !important; }
.stSelectbox > label { font-size: 13px !important; font-weight: 500 !important; color: #6B2D2D !important; }
.stSelectbox > div > div { border-radius: 9px !important; border: 1px solid #e8b8b8 !important; background: #fff !important; font-size: 14px !important; }

/* Primary button */
.stButton > button[kind="primary"] {
    background: #A94A4A !important; color: #FFF6DA !important; border: none !important;
    border-radius: 9px !important; padding: 11px 26px !important;
    font-size: 14px !important; font-weight: 600 !important; font-family: 'DM Sans', sans-serif !important;
}
.stButton > button[kind="primary"]:hover { background: #6B2D2D !important; }

/* Secondary buttons */
.stButton > button {
    background: transparent !important; border: 1px solid #e8b8b8 !important;
    color: #C47A7A !important; border-radius: 6px !important; font-size: 13px !important; font-weight: 400 !important;
}
.stButton > button:hover { border-color: #A94A4A !important; color: #A94A4A !important; background: transparent !important; }

/* Badges */
.badge { font-size: 11px; font-weight: 500; padding: 3px 10px; border-radius: 5px; letter-spacing: 0.3px; }
.badge-b { background: #eef4ee; color: #3a6b3a; border: 1px solid #cde0cd; }
.badge-i { background: #fdf5e8; color: #8a6020; border: 1px solid #f0ddb0; }
.badge-a { background: #fdf0ee; color: #8a3020; border: 1px solid #f0c8c0; }

/* History topic */
.hist-topic { font-weight: 500; color: #3D2020; font-size: 14px; }

/* Now studying heading */
.now-learning-bar { text-align: center; padding: 32px 0 0 0; margin-bottom: 32px; }
.now-label { display: block; font-size: 11px; font-weight: 600; color: #C47A7A; text-transform: uppercase; letter-spacing: 1.6px; margin-bottom: 10px; }
.now-topic { display: block; font-family: 'DM Serif Display', serif; font-size: 36px; font-weight: 400; color: #6B2D2D; letter-spacing: -0.4px; line-height: 1.2; margin-bottom: 16px; }
.now-learning-bar::after { content: ''; display: block; width: 60px; height: 2px; background: #A94A4A; margin: 0 auto; border-radius: 2px; }

/* Lesson typography */
.stMarkdown h1 { font-family: 'DM Serif Display', serif !important; font-size: 30px !important; font-weight: 400 !important; color: #6B2D2D !important; margin-top: 36px !important; border-bottom: 1px solid #f0d0d0 !important; padding-bottom: 10px !important; }
.stMarkdown h2 { font-family: 'DM Serif Display', serif !important; font-size: 24px !important; font-weight: 400 !important; color: #6B2D2D !important; margin-top: 32px !important; }
.stMarkdown h3 { font-size: 16px !important; font-weight: 600 !important; color: #3D2020 !important; margin-top: 22px !important; text-transform: none !important; }
.stMarkdown p { font-size: 15px !important; color: #3D2020 !important; line-height: 1.9 !important; }
.stMarkdown li { font-size: 15px !important; color: #3D2020 !important; line-height: 1.8 !important; margin-bottom: 6px !important; }
.stMarkdown strong { color: #6B2D2D !important; font-weight: 600 !important; }
.stMarkdown code { background: #fde8e8 !important; color: #6B2D2D !important; border-radius: 4px !important; padding: 2px 6px !important; font-size: 13px !important; }
.stMarkdown pre { background: #3D2020 !important; border-radius: 10px !important; padding: 18px 22px !important; }
.stMarkdown pre code { background: transparent !important; color: #FFF6DA !important; font-size: 13px !important; padding: 0 !important; }

/* Quiz card */
.quiz-card {
    background: #fff; border: 1px solid #f0d0d0; border-radius: 14px;
    padding: 22px 26px 16px 26px; margin-bottom: 4px;
}
.q-number { font-size: 11px; font-weight: 600; color: #C47A7A; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 8px; }
.q-text { font-size: 16px; font-weight: 500; color: #3D2020; line-height: 1.6; }

/* Score box */
.score-box { text-align: center; padding: 40px 20px; background: #fff; border: 1px solid #f0d0d0; border-radius: 16px; margin: 24px 0; }
.score-num { font-family: 'DM Serif Display', serif; font-size: 64px; font-weight: 400; color: #A94A4A; line-height: 1; }
.score-label { font-size: 14px; color: #C47A7A; margin-top: 8px; }
.score-msg { font-size: 16px; color: #3D2020; margin-top: 16px; font-weight: 500; }

/* Quiz header */
.quiz-header { text-align: center; padding: 32px 0 24px 0; }
.quiz-title { font-family: 'DM Serif Display', serif; font-size: 28px; font-weight: 400; color: #6B2D2D; margin-bottom: 6px; }
.quiz-sub { font-size: 14px; color: #C47A7A; }

.stAlert { border-radius: 10px !important; font-size: 14px !important; }
</style>
""", unsafe_allow_html=True)


# ── Page header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div class="page-title">Your personal AI tutor.</div>
    <p class="page-desc">Enter a topic and get a structured lesson tailored to your level.</p>
</div>
""", unsafe_allow_html=True)


# ── Stats ─────────────────────────────────────────────────────────────────────
lessons_done = len(st.session_state.get("history", []))
scores = [h["score"] for h in st.session_state.get("history", []) if h.get("score") is not None]
avg_score = f"{round(sum(scores)/len(scores))}%" if scores else "—"
quizzes_done = len(scores)

st.markdown(f"""
<div class="stats-row">
    <div class="stat-box"><div class="stat-num">{lessons_done}</div><div class="stat-lbl">Lessons generated</div></div>
    <div class="stat-box"><div class="stat-num">{quizzes_done}</div><div class="stat-lbl">Quizzes taken</div></div>
    <div class="stat-box"><div class="stat-num">{avg_score}</div><div class="stat-lbl">Avg. score</div></div>
</div>
""", unsafe_allow_html=True)


# ── Inputs ────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    topic = st.text_input("Topic", placeholder="e.g. Python lists, How neural networks work, SQL JOINs", max_chars=100)
with col2:
    level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced"])

generate_btn = st.button("Generate lesson", type="primary")


# ── History box ───────────────────────────────────────────────────────────────
history = st.session_state.get("history", [])
if history:
    with st.container(border=True):
        st.markdown('<div class="section-label" style="margin-top:0;margin-bottom:12px">Recent lessons</div>', unsafe_allow_html=True)
        for item in reversed(history[-5:]):
            lvl = item["level"].lower()
            badge_cls = {"beginner": "badge-b", "intermediate": "badge-i", "advanced": "badge-a"}.get(lvl, "badge-b")
            col_a, col_b, col_c, col_d = st.columns([4, 2, 1, 1])
            with col_a:
                st.markdown('<span class="hist-topic">' + item["topic"] + '</span>', unsafe_allow_html=True)
            with col_b:
                st.markdown('<span class="badge ' + badge_cls + '">' + item["level"] + '</span>', unsafe_allow_html=True)
            with col_c:
                score_display = f"{item['score']}%" if item.get("score") is not None else "—"
                st.markdown(f'<span style="font-size:13px;color:#C47A7A">{score_display}</span>', unsafe_allow_html=True)
            with col_d:
                clicked = st.button("↩", key=f"reload_{item['topic']}_{item['level']}")
            if clicked:
                st.session_state["reload_topic"] = item["topic"]
                st.session_state["reload_level"] = item["level"]
                st.rerun()


# ── Handle history reload ─────────────────────────────────────────────────────
if "reload_topic" in st.session_state:
    topic_to_load = st.session_state.pop("reload_topic")
    level_to_load = st.session_state.pop("reload_level")
    with st.spinner(f"Loading lesson on **{topic_to_load}**..."):
        lesson = generate_lesson(topic_to_load, level_to_load.lower())
    st.session_state["lesson"] = lesson
    st.session_state["topic"] = topic_to_load
    st.session_state["level"] = level_to_load
    st.session_state["quiz"] = None
    st.session_state["quiz_answers"] = {}
    st.session_state["quiz_submitted"] = False
    st.rerun()


# ── Generate lesson ───────────────────────────────────────────────────────────
if generate_btn:
    if not topic.strip():
        st.warning("Please enter a topic to continue.")
    else:
        with st.spinner(f"Generating your lesson on **{topic}**..."):
            lesson = generate_lesson(topic, level.lower())
        st.session_state["lesson"] = lesson
        st.session_state["topic"] = topic
        st.session_state["level"] = level
        st.session_state["quiz"] = None
        st.session_state["quiz_answers"] = {}
        st.session_state["quiz_submitted"] = False
        if "history" not in st.session_state:
            st.session_state["history"] = []
        if not any(h["topic"] == topic and h["level"] == level for h in st.session_state["history"]):
            st.session_state["history"].append({"topic": topic, "level": level, "score": None})
        st.rerun()


# ── Lesson + Quiz ─────────────────────────────────────────────────────────────
if "lesson" in st.session_state:

    # Now studying heading
    st.markdown(
        '<div class="now-learning-bar">'
        '<span class="now-label">Now studying</span>'
        '<span class="now-topic">' + st.session_state["topic"] + '</span>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(st.session_state["lesson"])
    st.markdown("---")

    # ── Quiz submitted: show results ──────────────────────────────────────────
    if st.session_state.get("quiz_submitted"):
        quiz = st.session_state["quiz"]
        answers = st.session_state["quiz_answers"]
        correct = sum(1 for i, q in enumerate(quiz) if answers.get(i) == q["answer"])
        total = len(quiz)
        pct = round((correct / total) * 100)

        if pct >= 80:
            msg = "Excellent work! You've got a strong grasp of this topic. 🎯"
        elif pct >= 60:
            msg = "Good effort! Review the explanations below to strengthen your understanding."
        else:
            msg = "Keep going — review the lesson and try again to solidify the concepts."

        st.markdown(f"""
        <div class="score-box">
            <div class="score-num">{pct}%</div>
            <div class="score-label">{correct} of {total} correct</div>
            <div class="score-msg">{msg}</div>
        </div>
        """, unsafe_allow_html=True)

        for i, q in enumerate(quiz):
            user_ans = answers.get(i)
            with st.container(border=True):
                st.markdown(
                    f'<div class="q-number">Question {i+1}</div>'
                    f'<div class="q-text">{q["question"]}</div>',
                    unsafe_allow_html=True
                )
                for opt, text in q["options"].items():
                    if opt == q["answer"] and opt == user_ans:
                        st.markdown(f"**✓ {opt}. {text}**")
                    elif opt == q["answer"]:
                        st.markdown(f"**✓ {opt}. {text}** ← correct")
                    elif opt == user_ans:
                        st.markdown(f"~~{opt}. {text}~~ ✗")
                    else:
                        st.markdown(f"{opt}. {text}")

                explanation = explain_answer(q["question"], user_ans, q["answer"], q["explanation"])
                st.info(explanation)

        # Save score
        for h in st.session_state["history"]:
            if h["topic"] == st.session_state["topic"] and h["level"] == st.session_state["level"]:
                h["score"] = pct
                break

        if st.button("Retake quiz", type="primary"):
            st.session_state["quiz"] = None
            st.session_state["quiz_answers"] = {}
            st.session_state["quiz_submitted"] = False
            st.rerun()

    # ── No quiz yet: show Take quiz button ────────────────────────────────────
    elif st.session_state.get("quiz") is None:
        if st.button("Take the quiz →", type="primary"):
            with st.spinner("Generating quiz questions..."):
                try:
                    quiz = generate_quiz(
                        st.session_state["topic"],
                        st.session_state["level"],
                        st.session_state["lesson"]
                    )
                    st.session_state["quiz"] = quiz
                    st.session_state["quiz_answers"] = {}
                    st.session_state["quiz_submitted"] = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to generate quiz: {e}")

    # ── Quiz loaded: show questions ───────────────────────────────────────────
    else:
        quiz = st.session_state["quiz"]
        st.markdown("""
        <div class="quiz-header">
            <div class="quiz-title">Quiz time</div>
            <div class="quiz-sub">Answer all 5 questions then submit</div>
        </div>
        """, unsafe_allow_html=True)

        for i, q in enumerate(quiz):
            st.markdown(
                f'<div class="quiz-card">'
                f'<div class="q-number">Question {i+1} of {len(quiz)}</div>'
                f'<div class="q-text">{q["question"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )
            options = [f"{k}.  {v}" for k, v in q["options"].items()]
            selected = st.radio("Select answer", options=options, key=f"q_{i}", index=None, label_visibility="collapsed")
            if selected:
                st.session_state["quiz_answers"][i] = selected[0]
            st.markdown("<div style='margin-bottom:12px'></div>", unsafe_allow_html=True)

        answered = len(st.session_state.get("quiz_answers", {}))
        if answered == len(quiz):
            if st.button("Submit quiz", type="primary"):
                st.session_state["quiz_submitted"] = True
                st.rerun()
        else:
            st.caption(f"{answered} of {len(quiz)} questions answered")