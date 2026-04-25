import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re
import datetime
import json
import html

# ---------------- CONFIG ---------------- #
def configure_gemini():
    load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    return genai.GenerativeModel("gemma-3-1b-it")


def configure_page():
    st.set_page_config(layout="centered", page_title="Project Ideas")
    st.title("Project Ideas")
    st.caption("Generate simple, structured project ideas based on your constraints.")

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
    if "ideas" not in st.session_state:
        st.session_state.ideas = []


# ---------------- INPUT UI ---------------- #
def render_inputs():
    requirements = st.text_area(
        "Requirements",
        placeholder="e.g. AI app, beginner-friendly, useful for students"
    )

    default_start = get_todays_date()
    default_end = default_start + datetime.timedelta(days=7)

    difficulty = st.selectbox("Difficulty", ["Beginner", "Easy", "Medium", "Hard"])

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

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    return {
        "requirements": requirements,
        "difficulty": difficulty,
        "date_range": (start_date, end_date),
    }


# ---------------- GENERATION ---------------- #
def build_prompt(inputs, skills_text, refresh=False):
    history_text = "\n".join(st.session_state.history)

    prompt = f"""
You are a strict JSON generator.

Return ONLY valid JSON.

[
  {{
    "title": "string",
    "description": "string",
    "tech_stack": "string",
    "difficulty": number
  }}
]

Constraints:
- Exactly 3 project ideas, in JSON format as specified above
- difficulty is 1–10
- use the user requirements and team skills to guide the ideas you generate
- tech_stack is comma-separated, simply list out the tech stack as a string
- do not include any names of users or team members in the ideas you generate

User requirements:
{inputs['requirements']}
Time: {inputs['date_range']}
Difficulty: {inputs['difficulty']}
Skills: {skills_text}
"""

    if refresh:
        prompt += f"\nAvoid repeating:\n{history_text}"

    return prompt

def generate_ideas(*, model, inputs, skills_text, refresh=False):
    prompt = build_prompt(inputs, skills_text, refresh)
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
        html_block = f"""
        <div style="
            background-color:#0f172a;
            padding:16px;
            border-radius:12px;
            margin-bottom:16px;
            border:1px solid #1f2937;
        ">
            <h3 style="color:white;">{idea['title']}</h3>

            <div style="color:#94a3b8; font-size:12px; margin-top:10px;">
                DESCRIPTION
            </div>
            <div style="color:#a1a1aa; font-size:14px;">
                {idea['description']}
            </div>

            <div style="color:#94a3b8; font-size:12px; margin-top:10px;">
                TECH STACK
            </div>
            <div style="font-family: monospace; font-size:13px; color:#d4d4d8;">
                {idea['tech_stack']}
            </div>

            <div style="color:#94a3b8; font-size:12px; margin-top:10px;">
                DIFFICULTY
            </div>
            <div style="color:#a1a1aa;">
                {idea['difficulty']}
            </div>
        </div>
        """

        st.html(html_block)

def render_buttons():
    colA, colB = st.columns(2)
    with colA:
        generate_btn = st.button("Generate")
    with colB:
        refresh_btn = st.button("Refresh")

    return generate_btn, refresh_btn


# ---------------- MAIN APP ---------------- #
def main():
    data = st.session_state.get("final_team_data", {"skills": ""})    
    skills_text = ""

    for member in data:
        skills_text += f"{member['name']}: "
        skills_text += ", ".join(
            [f"{k} ({v})" for k, v in member["skills"].items()]
        )
        skills_text += "\n"
    print(skills_text)

    configure_page()
    init_session()

    model = configure_gemini()
    inputs = render_inputs()
    generate_btn, refresh_btn = render_buttons()

    st.divider()

    if st.session_state.ideas:
        display_ideas(st.session_state.ideas)

    if st.button("Back to Form"):
        st.switch_page(st.session_state.page_1) 

    if generate_btn:
        result = generate_ideas(
        model=model,
        inputs=inputs,
        skills_text=skills_text,
        refresh=False
    )
        st.session_state.ideas = result
        display_ideas(result)

    if refresh_btn:
        result = generate_ideas(
        model=model,
        inputs=inputs,
        skills_text=skills_text,
        refresh=True
    )
        st.session_state.ideas = result
        display_ideas(result)