import streamlit as st

# --- CALLBACKS ---
def add_task(member_name):
    new_task = {"task": "New Task", "done": False, "desc": "Edit details here"}
    st.session_state.project_tasks[member_name].append(new_task)

def remove_task(member_name, task_idx):
    st.session_state.project_tasks[member_name].pop(task_idx)

def update_task_status(member_name, task_idx, widget_key):
    st.session_state.project_tasks[member_name][task_idx]["done"] = st.session_state[widget_key]

def parse_skills():
    ## skills_text is output like 
    # kelly: Rust (Intermediate), React (Beginner)
    # jeff: Gemini API (Advanced), SQL (Beginner)
    pass

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

    if "project_tasks" not in st.session_state:
        st.session_state.project_tasks = {
            "Alice": [{"task": "Backend API", "done": False, "desc": "Setup FastAPI"}],
            "Bob": [{"task": "Login Page", "done": False, "desc": "Build basic UI"}]
        }

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