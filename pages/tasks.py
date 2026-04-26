import streamlit as st
import os
import re
import json
import google.generativeai as genai
from dotenv import load_dotenv

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
    # keep model consistent with the rest of the app unless changed elsewhere
    return genai.GenerativeModel("gemma-3-1b-it")

def _safe_parse_json(text: str):
    # remove markdown fences if they appear
    text = re.sub(r"```json|```", "", (text or "")).strip()

    # try to extract the first JSON object/block to be resilient
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        text = match.group(0)

    return json.loads(text)

def _normalize_tasks(tasks_obj, member_names):
    """
    Normalize various agent shapes into:
      { "Member": [ { "task": str, "desc": str, "done": bool }, ... ], ... }
    """
    normalized = {name: [] for name in member_names}

    if not isinstance(tasks_obj, dict):
        return normalized

    for name in member_names:
        raw_list = tasks_obj.get(name, tasks_obj.get(name.lower(), []))
        if not isinstance(raw_list, list):
            raw_list = []
        for item in raw_list:
            if isinstance(item, str):
                normalized[name].append({"task": item, "desc": "", "done": False})
            elif isinstance(item, dict):
                normalized[name].append(
                    {
                        "task": str(item.get("task") or item.get("title") or "Task").strip(),
                        "desc": str(item.get("desc") or item.get("description") or "").strip(),
                        "done": bool(item.get("done", False)),
                    }
                )
    return normalized

def _generate_tasks_for_selected_project():
    idea = st.session_state.get("selected_idea")
    team = st.session_state.get("final_team_data", [])
    if not idea or not isinstance(team, list) or not team:
        return

    member_names = []
    for m in team:
        if isinstance(m, dict) and m.get("name"):
            member_names.append(m["name"])
    if not member_names:
        return

    # Avoid regenerating if we already generated for this idea+team snapshot
    signature = {
        "idea_title": idea.get("title"),
        "idea_desc": idea.get("description"),
        "members": member_names,
    }
    if st.session_state.get("_tasks_signature") == signature and "project_tasks" in st.session_state:
        return

    model = _configure_gemini()

    team_skills_lines = []
    for m in team:
        if not isinstance(m, dict):
            continue
        name = m.get("name") or "User"
        skills = m.get("skills") or {}
        if isinstance(skills, dict) and skills:
            skills_text = ", ".join([f"{k} ({v})" for k, v in skills.items()])
        else:
            skills_text = ""
        team_skills_lines.append(f"{name}: {skills_text}".strip())

    prompt = f"""
You are a strict JSON generator.
Return ONLY valid JSON (no markdown, no commentary).

Create tasks for each team member for this project idea.

Return a JSON object where:
- keys are EXACTLY the member names provided
- values are arrays of task objects
- each task object has: "task" (string), "desc" (string)

Example format:
{{
  "Alice": [{{"task":"Set up API","desc":"Create endpoints for ..."}}],
  "Bob":   [{{"task":"Build UI","desc":"Implement screens for ..."}}]
}}

Project:
Title: {idea.get("title","")}
Description: {idea.get("description","")}
Tech stack: {idea.get("tech_stack","")}
Difficulty: {idea.get("difficulty","")}

Team members (use these names exactly):
{json.dumps(member_names)}

Team skills:
{chr(10).join(team_skills_lines)}

Constraints:
- 3 to 6 tasks per member
- tasks should be specific and non-overlapping
""".strip()

    with st.spinner("Generating tasks for your team..."):
        response = model.generate_content(prompt)

    try:
        tasks_obj = _safe_parse_json(getattr(response, "text", ""))
        st.session_state.project_tasks = _normalize_tasks(tasks_obj, member_names)
        st.session_state._tasks_signature = signature
    except Exception:
        # Keep the UI usable even if generation fails
        st.warning("Couldn’t parse Gemini tasks. Showing editable placeholders instead.")
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
    else:
        st.title(idea["title"])
        st.write(idea["description"])
        st.code(idea["tech_stack"])
        st.write(f"Difficulty: {idea['difficulty']}")

    st.title("Team Workloads")

    # If coming from Gemini project selection, generate real tasks once
    if "final_team_data" in st.session_state and idea:
        _generate_tasks_for_selected_project()

    # Fallback if user navigates here without team/project
    if "project_tasks" not in st.session_state:
        st.session_state.project_tasks = {"Unassigned": [{"task": "New Task", "done": False, "desc": ""}]}

    for member_name, tasks in st.session_state.project_tasks.items():
        completed = len([t for t in tasks if t["done"]])
        total = len(tasks)
        percent = int((completed / total) * 100) if total > 0 else 0
        
        # --- NEW PROGRESS BAR SECTION ---
        # Create a layout for the header
        head_col1, head_col2, head_col3 = st.columns([0.4, 0.6, 0.1])
        head_col1.write(f"**{member_name}**")
        head_col2.progress(percent / 100)
        head_col3.write(f"{percent}%")
        
        with st.expander("View & Edit Tasks", expanded=True):
            for idx, task_item in enumerate(tasks):
                col_check, col_text, col_del = st.columns([0.1, 0.7, 0.2])
                
                widget_key = f"check_{member_name}_{idx}"
                col_check.checkbox(
                    "Done", value=task_item["done"], key=widget_key,
                    label_visibility="collapsed", on_change=update_task_status,
                    args=(member_name, idx, widget_key)
                )
                
                task_item["task"] = col_text.text_input(
                    "Task Name", value=task_item["task"], 
                    key=f"text_{member_name}_{idx}", label_visibility="collapsed"
                )

                # Show Gemini-provided task description (editable)
                task_item["desc"] = col_text.text_area(
                    "Description",
                    value=task_item.get("desc", ""),
                    key=f"desc_{member_name}_{idx}",
                    label_visibility="collapsed",
                    height=68,
                )
                
                col_del.button(
                    "Remove", key=f"del_{member_name}_{idx}", 
                    on_click=remove_task, args=(member_name, idx)
                )

            st.divider()
            st.button(
                f"Add Task", 
                key=f"add_{member_name}", 
                on_click=add_task, args=(member_name,)
            )