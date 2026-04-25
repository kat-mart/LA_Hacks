import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(layout="centered", page_title="Project Ideas")

# Minimal Notion-like styling
st.markdown("""
<style>
.block-container {
    max-width: 800px;
    padding-top: 2rem;
}
h1, h2, h3 {
    font-weight: 600;
}
.notion-block {
    border: 1px solid #e5e5e5;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 12px;
    background-color: white;
}
.divider {
    height: 1px;
    background-color: #eee;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("💡 Project Ideas")
st.caption("Generate simple, structured project ideas based on your constraints.")

# Inputs (stacked like Notion)
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
    Generate 3 project ideas.

    Requirements: {requirements}
    Time: {timeframe}
    Difficulty: {difficulty}
    Team size: {team_size}

    Format each idea as:
    Title:
    Description:
    Tech Stack:
    Tasks:

    Keep it clean and concise.
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

# Output parsing into blocks
def display_ideas(text):
    ideas = text.split("Title:")

    for idea in ideas:
        if idea.strip():
            st.markdown(f"""
            <div class="notion-block">
            <strong>Title:</strong> {idea.strip()}
            </div>
            """, unsafe_allow_html=True)

# Show results
if generate_btn:
    result = generate(False)
    display_ideas(result)

if refresh_btn:
    result = generate(True)
    display_ideas(result)