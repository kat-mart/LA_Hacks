import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(layout="centered", page_title="Project Ideas")

st.markdown("""
<style>

/* Font: clean + modern */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');

/* Background */
html, body, [data-testid="stApp"] {
    font-family: 'Inter', sans-serif;
    background: radial-gradient(circle at top, #0f172a, #020617 70%);
    color: #e5e7eb;
}

/* Container */
.block-container {
    max-width: 880px;
    padding-top: 2.5rem;
}

/* Title */
h1 {
    font-weight: 600;
    letter-spacing: -0.5px;
    color: #e2e8f0;
}

/* Subtitle */
.stCaption {
    color: #94a3b8;
}

/* Inputs */
textarea, .stSelectbox, .stSlider {
    border-radius: 10px !important;
}

/* Divider */
.divider {
    height: 1px;
    background: linear-gradient(to right, transparent, #1e293b, transparent);
    margin: 32px 0;
}

/* Card (tech panel) */
.card-block {
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 18px;

    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(148, 163, 184, 0.15);

    backdrop-filter: blur(12px);
    box-shadow: 0 0 0 rgba(0,0,0,0);

    transition: all 0.25s ease;
}

/* Glow hover */
.card-block:hover {
    transform: translateY(-3px);
    border: 1px solid rgba(99, 102, 241, 0.5);
    box-shadow: 0 0 20px rgba(99, 102, 241, 0.25);
}

/* Card title */
.card-block h3 {
    color: #a5b4fc;
    margin-bottom: 10px;
}

/* Labels */
.label {
    font-size: 12px;
    font-weight: 500;
    color: #64748b;
    margin-top: 10px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Buttons */
.stButton > button {
    border-radius: 8px;
    padding: 8px 14px;
    font-weight: 500;
    border: 1px solid #27272a;
    background: #111;
    color: #fafafa;
    transition: all 0.15s ease;
}

/* Primary */
.stButton button:first-child {
    background: #fafafa;
    color: #0a0a0a;
    border: none;
}

.stButton button:first-child:hover {
    background: #22d3ee;
}

/* Secondary */
.stButton button[kind="secondary"] {
    background: #111;
    color: #a1a1aa;
}

.stButton button[kind="secondary"]:hover {
    border: 1px solid #3f3f46;
    color: #e4e4e7;
}

/* Inputs */
textarea {
    background: rgba(2, 6, 23, 0.9) !important;
    border: 1px solid #1e293b !important;
    border-radius: 12px !important;

    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
}

textarea:focus {
    border: 1px solid #22d3ee !important;
    box-shadow: 0 0 10px rgba(34, 211, 238, 0.4);
}

/* Selectbox text fix */
div[data-baseweb="select"] {
    background-color: #020617 !important;
}

/* Scrollbar (optional but nice) */
::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-thumb {
    background: #1e293b;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #334155;
}

/* Subtle fade-in animation */
.card-block {
    animation: fadeIn 0.35s ease;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
}

</style>
""", unsafe_allow_html=True)


# Title
st.title("Project Ideas")
st.caption("Generate simple, structured project ideas based on your constraints.")

# Inputs
requirements = st.text_area("Requirements", placeholder="e.g. AI app, beginner-friendly, useful for students")

col1, col2 = st.columns(2)
with col1:
    difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
    timeframe = st.selectbox("Time", ["1 day", "1 week", "1 month"])
with col2:
    team_size = st.slider("Team Size", 1, 10, 3)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Session state
if "history" not in st.session_state:
    st.session_state.history = []

def generate(refresh=False):
    history_text = "\n".join(st.session_state.history)

    prompt = f"""
    Do not chat with me, just give the ideas in a clear format. Use the following constraints if they were given by the user.
    Generate exactly 3 project ideas.

    Return in STRICT format. No markdown. No asterisks. No HTML.

    Each idea MUST follow:

    Title: <one line>
    Description: <one paragraph>
    Tech Stack: <comma separated tools>
    Difficulty Rating (1-10): <number>

    ---

    Requirements: {requirements}
    Time: {timeframe}
    Difficulty: {difficulty}
    Team size: {team_size}
    """

    if refresh:
        prompt += f"\nAvoid repeating:\n{history_text}"

    response = model.generate_content(prompt)
    st.session_state.history.append(response.text)

    return response.text

# Buttons
colA, colB = st.columns(2)
with colA:
    generate_btn = st.button("Generate")
with colB:
    refresh_btn = st.button("Refresh")

def clean_text(text):
    # remove markdown bold/asterisks
    text = re.sub(r"\*+", "", text)

    # normalize spacing
    text = re.sub(r"\n\s*\n", "\n", text)

    return text.strip()

def parse_ideas(text):
    text = clean_text(text)

    pattern = r"Title:\s*(.*?)\n(?:Description:\s*(.*?)\n)?(?:Tech Stack:\s*(.*?)\n)?(?:Difficulty Rating \(1-10\):\s*(.*?))(?=\nTitle:|\Z)"

    matches = re.findall(pattern, text, re.DOTALL)

    ideas = []
    for title, desc, tech, difficulty in matches:
        ideas.append({
            "title": title.strip(),
            "description": (desc or "").strip(),
            "tech": (tech or "").strip(),
            "difficulty": difficulty.strip()
        })

    return ideas

# Output parsing into blocks
def display_ideas(text):
    ideas = parse_ideas(text)

    for idea in ideas:
        st.markdown(f"""
        <div class="card-block">
            <h3>{idea['title']}</h3>

            <div class="label">Description</div>
            <div style="color:#a1a1aa; font-size:14px;">
                {idea['description']}
            </div>

            <div class="label">Tech Stack</div>
            <div style="font-family: monospace; font-size:13px; color:#d4d4d8;">
                {idea['tech']}
            </div>

            <div class="label">Difficulty</div>
            <div style="color:#a1a1aa; font-size:14px;">
                {idea['difficulty']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# Show results
if generate_btn:
    result = generate(False)
    display_ideas(result)

if refresh_btn:
    result = generate(True)
    display_ideas(result)