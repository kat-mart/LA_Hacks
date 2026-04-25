import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re
import datetime
import json


# ---------------- CONFIG ---------------- #
def configure_gemini():
    load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    return genai.GenerativeModel("gemini-2.5-flash")


def configure_page():
    st.set_page_config(layout="centered", page_title="Project Ideas")
    st.title("Project Ideas")
    st.caption("Generate simple, structured project ideas based on your constraints.")


# ---------------- STYLES ---------------- #
def apply_styles():
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

/* Subtitle */
.stCaption {
    color: #94a3b8;
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

                
"""
, unsafe_allow_html=True)


# ---------------- UTILITIES ---------------- #
def get_todays_date():
    return datetime.date.today()


def set_max_date():
    return datetime.date(get_todays_date().year + 3, 12, 31)


def clean_text(text):
    text = re.sub(r"\*+", "", text)
    text = re.sub(r"\n\s*\n", "\n", text)
    return text.strip()


def safe_parse_json(text):
    # remove markdown fences if they appear
    text = re.sub(r"```json|```", "", text).strip()

    # extract first JSON block only
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        text = match.group(0)

    return json.loads(text)


# ---------------- SESSION ---------------- #
def init_session():
    if "history" not in st.session_state:
        st.session_state.history = []


# ---------------- INPUT UI ---------------- #
def render_inputs():
    requirements = st.text_area(
        "Requirements",
        placeholder="e.g. AI app, beginner-friendly, useful for students"
    )

    default_start = get_todays_date()
    default_end = default_start + datetime.timedelta(days=7)

    col1, col2 = st.columns(2)

    with col1:
        difficulty = st.selectbox(
            "Difficulty",
            ["Beginner", "Easy", "Medium", "Hard"]
        )

        date_range = st.date_input(
            "Project timeline",
            value=(default_start, default_end),
            min_value=default_start,
            max_value=set_max_date(),
            format="MM/DD/YYYY"
        )

    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = None, None

    with col2:
        team_size = st.slider("Team Size", 1, 10, 3)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    return {
        "requirements": requirements,
        "difficulty": difficulty,
        "date_range": (start_date, end_date),
        "team_size": team_size
    }


# ---------------- GENERATION ---------------- #
def build_prompt(inputs, refresh=False):
    history_text = "\n".join(st.session_state.history)

    prompt = f"""
You are a strict JSON generator.

Return ONLY valid JSON.

No markdown. No HTML. No explanations. No extra text.

Output must be a list of 3 objects:

[
  {{
    "title": "string",
    "description": "string",
    "tech_stack": "string",
    "difficulty": number
  }}
]

Constraints:
- Exactly 3 project ideas
- difficulty is 1–10
- tech_stack is comma-separated

User requirements:
{inputs['requirements']}
Time: {inputs['date_range']}
Difficulty: {inputs['difficulty']}
Team size: {inputs['team_size']}
"""

    if refresh:
        prompt += f"\nAvoid repeating:\n{history_text}"

    return prompt

def generate_ideas(model, inputs, refresh=False):
    prompt = build_prompt(inputs, refresh)
    response = model.generate_content(prompt)

    st.session_state.history.append(response.text)

    try:
        return safe_parse_json(response.text)
    except Exception as e:
        st.error("Failed to parse JSON")
        st.text(response.text)
        return []


# ---------------- OUTPUT ---------------- #
def display_ideas(ideas):
    if not isinstance(ideas, list):
        st.error("Invalid format returned")
        return

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
                {idea['tech_stack']}
            </div>

            <div class="label">Difficulty</div>
            <div style="color:#a1a1aa; font-size:14px;">
                {idea['difficulty']}
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_buttons():
    colA, colB = st.columns(2)
    with colA:
        generate_btn = st.button("Generate")
    with colB:
        refresh_btn = st.button("Refresh")

    return generate_btn, refresh_btn


# ---------------- MAIN APP ---------------- #
def main():
    configure_page()
    apply_styles()
    init_session()

    model = configure_gemini()
    inputs = render_inputs()
    generate_btn, refresh_btn = render_buttons()

    if generate_btn:
        result = generate_ideas(model, inputs, refresh=False)
        display_ideas(result)

    if refresh_btn:
        result = generate_ideas(model, inputs, refresh=True)
        display_ideas(result)


if __name__ == "__main__":
    main()