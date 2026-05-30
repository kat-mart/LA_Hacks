import streamlit as st
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from google.generativeai.types import GenerationConfig

# --- CALLBACKS ---
def add_task(member_name):
    new_task = {"task": "New Task", "done": False, "desc": "Edit details here"}
    st.session_state.project_tasks[member_name].append(new_task)

def remove_task(member_name, task_idx):
    st.session_state.project_tasks[member_name].pop(task_idx)

def update_task_status(member_name, task_idx, widget_key):
    st.session_state.project_tasks[member_name][task_idx]["done"] = st.session_state[widget_key]

# --- GEMINI TASK GENERATION ---
def _configure_gemini():
    load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    return genai.GenerativeModel("gemma-4-31b-it")

# --- JSON PARSING ---
def _safe_parse_json(text: str):
    if not text:
        raise ValueError("Empty response")

    text = text.strip()

    # remove markdown fences if model still adds them
    if text.startswith("```"):
        lines = text.splitlines()

        if len(lines) >= 3:
            text = "\n".join(lines[1:-1])

    return json.loads(text)


# --- NORMALIZATION ---
def _normalize_tasks(tasks_obj, member_names):
    """
    Normalize Gemini output into:
    {
        "Member": [
            {"task": str, "desc": str, "done": bool}
        ]
    }
    """

    normalized = {name: [] for name in member_names}

    if not isinstance(tasks_obj, dict):
        return normalized

    for name in member_names:
        raw_list = (
            tasks_obj.get(name) or tasks_obj.get(name.lower()) or []
        )

        if not isinstance(raw_list, list):
            raw_list = []

        for item in raw_list:
            if isinstance(item, str):
                normalized[name].append({"task": item.strip(), "desc": "", "done": False})
            elif isinstance(item, dict):
                task_name = str(item.get("task") or item.get("title") or "Task").strip()

                task_desc = str(
                    item.get("desc") or item.get("description") or ""
                ).strip()

                normalized[name].append({
                    "task": task_name, "desc": task_desc, "done": False
                })
    return normalized


# --- SCHEMA CREATION ---
def _build_response_schema(member_names):

    task_schema = {
        "type": "object",
        "properties": {
            "task": {"type": "string"}, "desc": {"type": "string"}
        },
        "required": ["task", "desc"]
    }

    properties = {}

    for name in member_names:
        properties[name] = {"type": "array", "items": task_schema}

    return {"type": "object", "properties": properties}


# --- TASK GENERATION ---
def _generate_tasks_for_selected_project():

    idea = st.session_state.get("selected_idea")
    team = st.session_state.get("final_team_data", [])

    if not idea or not isinstance(team, list) or not team:
        return

    # collect member names
    member_names = []

    for member in team:
        if isinstance(member, dict) and member.get("name"):
            member_names.append(member["name"])

    if not member_names:
        return

    # avoid unnecessary regeneration
    signature = {
        "idea_title": idea.get("title"),
        "idea_desc": idea.get("description"),
        "members": member_names,
    }

    if (
        st.session_state.get("_tasks_signature") == signature
        and "project_tasks" in st.session_state
    ):
        return

    model = _configure_gemini()

    # format team skills
    team_skills_lines = []

    for member in team:

        if not isinstance(member, dict):
            continue

        name = member.get("name") or "User"
        skills = member.get("skills") or {}

        if isinstance(skills, dict) and skills:
            skills_text = ", ".join([
                f"{skill} ({level})"
                for skill, level in skills.items()
            ])
        else:
            skills_text = "No skills listed"

        team_skills_lines.append(
            f"{name}: {skills_text}"
        )

    prompt = f"""
Generate project tasks for each team member.

Project:
Title: {idea.get("title", "")}

Description:
{idea.get("description", "")}

Tech Stack:
{idea.get("tech_stack", "")}

Difficulty:
{idea.get("difficulty", "")}

Team Members:
{member_names}

Skills:
{chr(10).join(team_skills_lines)}

Requirements:
- 3 to 6 tasks per member
- tasks should be specific
- tasks should not overlap heavily
- descriptions should be concise
""".strip()

    response_schema = _build_response_schema(member_names)

    generation_config = GenerationConfig(
        temperature=0.2,
        response_mime_type="application/json",
        response_schema=response_schema,
    )

    with st.spinner("Generating tasks for your team..."):

        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )

    # --- PARSE ---
    try:

        tasks_obj = _safe_parse_json(response.text)

        st.session_state.project_tasks = _normalize_tasks(tasks_obj, member_names)

        st.session_state._tasks_signature = signature

    except Exception as e:

        print("Gemini parsing error:", e)
        print("Raw response:", getattr(response, "text", ""))

        # fallback placeholder tasks
        st.warning(
            "Couldn't parse Gemini tasks. Showing editable placeholders instead."
        )

        st.session_state.project_tasks = {
            name: [{"task": "New Task", "done": False, "desc": "Edit details here"}]
            for name in member_names
        }

        st.session_state._tasks_signature = signature


# --- MAIN RENDER ---
def show_tasks_editable():

    idea = st.session_state.get("selected_idea")

    if not idea:
        st.error("No project selected")
        return

    # --- PROJECT INFO ---
    st.title(idea["title"])

    st.write(idea["description"])

    st.code(idea["tech_stack"])

    st.write(f"Difficulty: {idea['difficulty']}")

    st.title("Team Workloads")

    # generate tasks
    if "final_team_data" in st.session_state:
        _generate_tasks_for_selected_project()

    # fallback state
    if "project_tasks" not in st.session_state:

        st.session_state.project_tasks = {
            "Unassigned": [{"task": "New Task", "done": False, "desc": ""}]
        }

    # --- RENDER MEMBERS ---
    for member_name, tasks in st.session_state.project_tasks.items():

        completed = len([
            task for task in tasks
            if task["done"]
        ])

        total = len(tasks)

        percent = (
            int((completed / total) * 100)
            if total > 0 else 0
        )

        # header row
        head_col1, head_col2, head_col3 = st.columns([0.4, 0.6, 0.1])

        head_col1.write(f"**{member_name}**")

        head_col2.progress(percent / 100)

        head_col3.write(f"{percent}%")

        with st.expander("View & Edit Tasks", expanded=True):
            for idx, task_item in enumerate(tasks):
                col_check, col_text, col_del = st.columns([0.1, 0.7, 0.2])
                widget_key = f"check_{member_name}_{idx}"

                col_check.checkbox(
                    "Done",
                    value=task_item["done"],
                    key=widget_key,
                    label_visibility="collapsed",
                    on_change=update_task_status,
                    args=(member_name, idx, widget_key)
                )

                task_item["task"] = col_text.text_input(
                    "Task Name",
                    value=task_item["task"],
                    key=f"text_{member_name}_{idx}",
                    label_visibility="collapsed"
                )

                task_item["desc"] = col_text.text_area(
                    "Description",
                    value=task_item.get("desc", ""),
                    key=f"desc_{member_name}_{idx}",
                    label_visibility="collapsed",
                    height=68,
                )

                col_del.button("Remove", key=f"del_{member_name}_{idx}", on_click=remove_task, args=(member_name, idx))

            st.divider()
            st.button("Add Task", key=f"add_{member_name}", on_click=add_task, args=(member_name,))