import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re
import datetime
import json
import html
from google.generativeai.types import GenerationConfig

# ---------------- CONFIG ---------------- #
def configure_gemini():
    load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    return genai.GenerativeModel("gemma-4-31b-it")


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
    if not text:
        raise ValueError("Empty response")

    text = text.strip()

    # remove markdown fences
    text = re.sub(r"```json|```", "", text).strip()
    return json.loads(text)


def build_idea_schema():
    return {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "description": {"type": "string"},
                "tech_stack": {"type": "string"},
                "difficulty": {"type": "number"}
            },
            "required": [
                "title",
                "description",
                "tech_stack",
                "difficulty"
            ]
        }
    }


# ---------------- SESSION ---------------- #
def init_session():
    if "history" not in st.session_state:
        st.session_state.history = []
    if "ideas" not in st.session_state:
        st.session_state.ideas = []


# ---------------- INPUT UI ---------------- #
def render_inputs():
    already_have_idea = st.checkbox("I already have a project idea")

    requirements = ""
    user_idea = ""

    if already_have_idea:
        user_idea = st.text_area(
            "Describe your project idea",
            placeholder="Explain your idea briefly..."
        )
    else:
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
        "already_have_idea": already_have_idea,
        "user_idea": user_idea
    }

# ---------------- PROMPT ---------------- #
def build_prompt(inputs, skills_text, refresh=False):
    history_text = "\n".join(st.session_state.history)

    # If user already has an idea
    if (inputs["already_have_idea"] and inputs["user_idea"].strip()):
        return f"""
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

Task:
- Transform the user's project idea into a clean, well-structured project definition
- Improve clarity and expand the description
- Suggest an appropriate tech stack
- Assign a difficulty from 1-10

User project idea:
{inputs['user_idea']}

Time: {inputs['date_range']}
Difficulty preference: {inputs['difficulty']}
Skills: {skills_text}
"""

    # Default project generation prompt
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
- Exactly 3 project ideas
- difficulty is 1–10
- use the user requirements and team skills
- tech_stack is comma-separated
- do not include names

User requirements:
{inputs['requirements']}
Time: {inputs['date_range']}
Difficulty: {inputs['difficulty']}
Skills: {skills_text}
"""

    if refresh:
        prompt += f"\nAvoid repeating:\n{history_text}"

    return prompt

# ---------------- GENERATION ---------------- #
def generate_ideas(*, model, inputs, skills_text, refresh=False):
    prompt = build_prompt(inputs, skills_text, refresh)

    generation_config = GenerationConfig(
        temperature=0.3,
        response_mime_type="application/json",
        response_schema=build_idea_schema(),
    )

    response = model.generate_content(
        prompt,
        generation_config=generation_config
    )

    st.session_state.history.append(response.text)

    try:
        parsed = safe_parse_json(response.text)
        cleaned = []

        if isinstance(parsed, list):
            for idea in parsed:
                if not isinstance(idea, dict):
                    continue

                cleaned.append({
                    "title": str(idea.get("title", "")).strip(),
                    "description": str(idea.get("description", "")).strip(),
                    "tech_stack": str(idea.get("tech_stack", "")).strip(),
                    "difficulty": idea.get("difficulty", 1)
                })
        return cleaned

    except Exception as e:
        st.error("Failed to parse JSON")
        st.text("Raw Gemini response:")
        st.code(response.text)
        print("JSON parse error:", e)
        return []

# ---------------- OUTPUT ---------------- #
def display_ideas(ideas):
    if not isinstance(ideas, list):
        st.error("Invalid format returned")
        return

    for i, idea in enumerate(ideas):
        html_block = f"""
        <div style="
            background-color:#fff9f0;
            padding:16px;
            border-radius:12px;
            margin-bottom:16px;
            border:1px solid #1f2937;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
            border-color:#c27029;
        ">
            <h3 style="color:white;">
                {html.escape(idea['title'])}
            </h3>

            <div style="
                color:#c27029;
                font-size:12px;
                margin-top:10px;
            ">
                DESCRIPTION
            </div>

            <div style="
                color:#423f3f;
                font-size:14px;
            ">
                {html.escape(idea['description'])}
            </div>

            <div style="
                color:#c27029;
                font-size:12px;
                margin-top:10px;
            ">
                TECH STACK
            </div>

            <div style="font-family: monospace; font-size:13px; color:#423f3f;">
                {html.escape(idea['tech_stack'])}
            </div>

            <div style="color:#c27029; font-size:12px; margin-top:10px;">
                DIFFICULTY
            </div>
            <div style="color:#423f3f;">
                {idea['difficulty']}
            </div>
        </div>
        """

        st.html(html_block)
        st.markdown("<div style='margin-top:-10px;'>", unsafe_allow_html=True)
        if st.button("Select Project", key=f"select_{i}"):
            st.session_state.selected_idea = idea
            st.switch_page(st.session_state.page_3)
        st.markdown("</div>", unsafe_allow_html=True)

def set_skills_text(text):
    return text


# ---------------- MAIN APP ---------------- #
def main():
    data = st.session_state.get("final_team_data", [])
    skills_text = ""

    # Build skills text safely
    if isinstance(data, list):
        for member in data:
            skills_text += (f"{member.get('name', 'User')}: ")

            skills_text += ", ".join([
                f"{k} ({v})"
                for k, v in member.get(
                    "skills",
                    {}
                ).items()
            ])
            skills_text += "\n"

    set_skills_text(skills_text)
    print(skills_text)
    configure_page()
    init_session()

    model = configure_gemini()
    inputs = render_inputs()
    generate_btn = False
    refresh_btn = False

    colA, colB = st.columns(2)

    has_ideas = bool(
        st.session_state.get("ideas")
    )

    with colA:
        generate_btn = st.button("Generate")
    with colB:
        refresh_btn = st.button(
            "Refresh",
            disabled=(inputs["already_have_idea"] or not has_ideas)
        )

    # Generate ideas
    if generate_btn:
        message = (
            "Refining your idea..."
            if inputs["already_have_idea"]
            else "Generating project ideas..."
        )

        with st.spinner(message):
            result = generate_ideas(
                model=model,
                inputs=inputs,
                skills_text=skills_text,
                refresh=False
            )

        st.session_state.ideas = result
        st.rerun()

    # Refresh ideas
    if refresh_btn:
        with st.spinner("Refreshing ideas..."):
            result = generate_ideas(
                model=model,
                inputs=inputs,
                skills_text=skills_text,
                refresh=True
            )

        st.session_state.ideas = result
        st.rerun()

    # Display ideas
    if st.session_state.ideas:
        display_ideas(st.session_state.ideas)

    # Back button
    if st.button("Back to Form"):
        if "page_1" in st.session_state:
            st.switch_page(st.session_state.page_1)
        else:
            st.error("Navigation path not found.")