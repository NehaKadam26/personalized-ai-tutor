import streamlit as st
from utils.groq_client import generate_lesson

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

/* Full page warm background */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section[data-testid="stMain"] > div {
    background: #faf8f5 !important;
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

/* ── Page header ── */
.page-header { margin-bottom: 36px; }
.page-title {
    font-family: 'DM Serif Display', serif !important;
    font-size: 34px !important;
    font-weight: 400 !important;
    color: #1a1714 !important;
    margin: 0 0 8px 0 !important;
    letter-spacing: -0.3px !important;
    line-height: 1.2 !important;
    border-bottom: none !important;
    padding-bottom: 0 !important;
    text-transform: none !important;
}
.page-desc {
    font-size: 15px;
    color: #8c8070;
    margin: 0;
    font-weight: 400;
}

/* ── Stats row ── */
.stats-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 28px;
}
.stat-box {
    background: white;
    border: 1px solid #e8e0d5;
    border-radius: 12px;
    padding: 18px 20px;
}
.stat-num {
    font-family: 'DM Serif Display', serif !important;
    font-size: 28px;
    font-weight: 400;
    color: #1a1714;
    line-height: 1;
    letter-spacing: -0.3px;
}
.stat-lbl {
    font-size: 12px;
    color: #b0a090;
    margin-top: 4px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}

/* ── Section divider label ── */
.section-label {
    font-size: 11px;
    font-weight: 600;
    color: #b0a090;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    margin-bottom: 14px;
    margin-top: 28px;
}

/* ── Widget overrides ── */
.stTextInput > label {
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #4a4035 !important;
}
.stTextInput > div > div > input {
    border-radius: 9px !important;
    border: 1px solid #ddd5c8 !important;
    padding: 11px 14px !important;
    font-size: 14px !important;
    font-family: 'DM Sans', sans-serif !important;
    color: #1a1714 !important;
    background: white !important;
}
.stTextInput > div > div > input:focus {
    border-color: #c9a96e !important;
    box-shadow: 0 0 0 3px rgba(201,169,110,0.12) !important;
}
.stTextInput > div > div > input::placeholder {
    color: #c4b8aa !important;
}

.stSelectbox > label {
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #4a4035 !important;
}
.stSelectbox > div > div {
    border-radius: 9px !important;
    border: 1px solid #ddd5c8 !important;
    background: white !important;
    font-size: 14px !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Button ── */
.stButton > button[kind="primary"] {
    background: #1a1714 !important;
    color: #fdf9f6 !important;
    border: none !important;
    border-radius: 9px !important;
    padding: 11px 26px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    font-family: 'DM Sans', sans-serif !important;
    letter-spacing: 0.1px !important;
}
.stButton > button[kind="primary"]:hover {
    background: #2e2825 !important;
}

/* ── History box ── */
.history-section {
    background: white;
    border: 1px solid #e8e0d5;
    border-radius: 14px;
    padding: 20px 26px;
    margin-bottom: 16px;
    margin-top: 8px;
}

/* Wrap each history row so the border shows correctly */
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
    background: white !important;
    border: 1px solid #e8e0d5 !important;
    border-radius: 14px !important;
    padding: 16px 20px !important;
}
.history-empty {
    font-size: 13px;
    color: #c4b8aa;
    font-style: italic;
}
.hist-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid #f2ede7;
    font-size: 14px;
}
.hist-row:last-child { border-bottom: none; }
.hist-topic { font-weight: 500; color: #1a1714; }

/* ── Badges ── */
.badge {
    font-size: 11px;
    font-weight: 500;
    padding: 3px 10px;
    border-radius: 5px;
    letter-spacing: 0.3px;
}
.badge-b { background: #eef4ee; color: #3a6b3a; border: 1px solid #cde0cd; }
.badge-i { background: #fdf5e8; color: #8a6020; border: 1px solid #f0ddb0; }
.badge-a { background: #fdf0ee; color: #8a3020; border: 1px solid #f0c8c0; }

/* ── Now studying heading ── */
.now-learning-bar {
    text-align: center;
    padding: 32px 0 0 0;
    background: transparent;
    border: none;
    margin-bottom: 32px;
    margin-top: 8px;
}
.now-dot { display: none; }
.now-label {
    display: block;
    font-size: 11px;
    font-weight: 600;
    color: #b0a090;
    text-transform: uppercase;
    letter-spacing: 1.6px;
    margin-bottom: 10px;
}
.now-topic {
    display: block;
    font-family: 'DM Serif Display', serif;
    font-size: 36px;
    font-weight: 400;
    color: #1a1714;
    letter-spacing: -0.4px;
    line-height: 1.2;
    margin-bottom: 16px;
}
.now-learning-bar::after {
    content: '';
    display: block;
    width: 60px;
    height: 2px;
    background: #c9a96e;
    margin: 0 auto;
    border-radius: 2px;
}

/* ── Lesson content typography ── */
.stMarkdown h1 {
    font-family: 'DM Serif Display', serif !important;
    font-size: 30px !important;
    font-weight: 400 !important;
    color: #1a1714 !important;
    margin-top: 36px !important;
    margin-bottom: 14px !important;
    letter-spacing: -0.3px !important;
    border-bottom: 1px solid #ede6db !important;
    padding-bottom: 10px !important;
}
.stMarkdown h2 {
    font-family: 'DM Serif Display', serif !important;
    font-size: 24px !important;
    font-weight: 400 !important;
    color: #1a1714 !important;
    margin-top: 32px !important;
    margin-bottom: 12px !important;
    letter-spacing: -0.2px !important;
}
.stMarkdown h3 {
    font-size: 16px !important;
    font-weight: 600 !important;
    color: #3d3530 !important;
    margin-top: 22px !important;
    margin-bottom: 8px !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
}
.stMarkdown p {
    font-size: 15px !important;
    color: #3d3530 !important;
    line-height: 1.9 !important;
    font-weight: 400 !important;
}
.stMarkdown li {
    font-size: 15px !important;
    color: #3d3530 !important;
    line-height: 1.8 !important;
    margin-bottom: 6px !important;
}
.stMarkdown strong {
    color: #1a1714 !important;
    font-weight: 600 !important;
}
.stMarkdown code {
    background: #f2ede6 !important;
    color: #5a3e28 !important;
    border-radius: 4px !important;
    padding: 2px 6px !important;
    font-size: 13px !important;
}
.stMarkdown pre {
    background: #1e1b18 !important;
    border-radius: 10px !important;
    padding: 18px 22px !important;
}
.stMarkdown pre code {
    background: transparent !important;
    color: #e8dfd4 !important;
    font-size: 13px !important;
    padding: 0 !important;
}

/* ── Lesson footer ── */
.lesson-footer-plain {
    margin-top: 32px;
    padding-top: 16px;
    border-top: 1px solid #ede6db;
    font-size: 12px;
    color: #b0a090;
    font-weight: 500;
    letter-spacing: 0.2px;
}

/* ── History reload button ── */
.history-section .stButton > button {
    background: transparent !important;
    border: 1px solid #e0d8ce !important;
    color: #b0a090 !important;
    border-radius: 6px !important;
    padding: 2px 10px !important;
    font-size: 13px !important;
    font-weight: 400 !important;
    line-height: 1.6 !important;
    min-height: unset !important;
}
.history-section .stButton > button:hover {
    border-color: #c9a96e !important;
    color: #c9a96e !important;
    background: transparent !important;
}

/* ── Alert ── */
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
st.markdown(f"""
<div class="stats-row">
    <div class="stat-box">
        <div class="stat-num">{lessons_done}</div>
        <div class="stat-lbl">Lessons generated</div>
    </div>
    <div class="stat-box">
        <div class="stat-num">0</div>
        <div class="stat-lbl">Quizzes taken</div>
    </div>
    <div class="stat-box">
        <div class="stat-num">—</div>
        <div class="stat-lbl">Avg. score</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Inputs (no wrapper box — Streamlit widgets can't go inside custom HTML) ───
col1, col2 = st.columns([3, 1])
with col1:
    topic = st.text_input(
        "Topic",
        placeholder="e.g. Python lists, How neural networks work, SQL JOINs",
        max_chars=100
    )
with col2:
    level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced"])

generate_btn = st.button("Generate lesson", type="primary")


# ── History box ────────────────────────────────────────────────────────────────
history = st.session_state.get("history", [])
if history:
    with st.container(border=True):
        st.markdown('<div class="section-label" style="margin-top:0;margin-bottom:12px">Recent lessons</div>', unsafe_allow_html=True)
        for item in reversed(history[-5:]):
            lvl = item["level"].lower()
            badge_cls = {"beginner": "badge-b", "intermediate": "badge-i", "advanced": "badge-a"}.get(lvl, "badge-b")
            col_a, col_b, col_c = st.columns([5, 2, 1])
            with col_a:
                st.markdown('<span class="hist-topic">' + item["topic"] + '</span>', unsafe_allow_html=True)
            with col_b:
                st.markdown('<span class="badge ' + badge_cls + '">' + item["level"] + '</span>', unsafe_allow_html=True)
            with col_c:
                clicked = st.button("↩", key=f"reload_{item['topic']}_{item['level']}")
            if clicked:
                st.session_state["reload_topic"] = item["topic"]
                st.session_state["reload_level"] = item["level"]
                st.rerun()

# ── Handle history reload outside columns ─────────────────────────────────────
if "reload_topic" in st.session_state:
    topic_to_load = st.session_state.pop("reload_topic")
    level_to_load = st.session_state.pop("reload_level")
    with st.spinner(f"Loading lesson on **{topic_to_load}**..."):
        lesson = generate_lesson(topic_to_load, level_to_load.lower())
    st.session_state["lesson"] = lesson
    st.session_state["topic"] = topic_to_load
    st.session_state["level"] = level_to_load
    st.rerun()


# ── Generate logic ─────────────────────────────────────────────────────────────
if generate_btn:
    if not topic.strip():
        st.warning("Please enter a topic to continue.")
    else:
        with st.spinner(f"Generating your lesson on **{topic}**..."):
            lesson = generate_lesson(topic, level.lower())

        st.session_state["lesson"] = lesson
        st.session_state["topic"] = topic
        st.session_state["level"] = level

        if "history" not in st.session_state:
            st.session_state["history"] = []
        if not any(h["topic"] == topic and h["level"] == level for h in st.session_state["history"]):
            st.session_state["history"].append({"topic": topic, "level": level})

        st.rerun()


# ── Lesson output ──────────────────────────────────────────────────────────────
if "lesson" in st.session_state:
    lvl = st.session_state["level"].lower()
    badge_cls = {"beginner": "badge-b", "intermediate": "badge-i", "advanced": "badge-a"}.get(lvl, "badge-b")

    bar_html = (
        '<div class="now-learning-bar">'
        '<span class="now-label">Now studying</span>'
        '<span class="now-topic">' + st.session_state["topic"] + '</span>'
        '</div>'
    )
    st.markdown(bar_html, unsafe_allow_html=True)

    st.markdown(st.session_state["lesson"])

    st.markdown('<div class="lesson-footer-plain">Quiz for this lesson — coming in Day 3</div>', unsafe_allow_html=True)