# team_form.py
import streamlit as st
import uuid

def get_tech_skills():
    return ["Python", "React", "SQL", "Gemini API", "JavaScript", "C++", "Java", "Rust", "Go", "LangChain"]

def add_member():
    if "team_ids" not in st.session_state:
        st.session_state.team_ids = []
    st.session_state.team_ids.append(str(uuid.uuid4()))

def remove_member(mid):
    if len(st.session_state.team_ids) > 1:
        st.session_state.team_ids.remove(mid)
        # Clean up stored data for this ID if it exists
        if mid in st.session_state.team_data_store:
            del st.session_state.team_data_store[mid]

def show_team_form():
    st.title("Step 1: Create Team")
    
    if "team_ids" not in st.session_state:
        st.session_state.team_ids = [str(uuid.uuid4())]
    if "team_data_store" not in st.session_state:
        st.session_state.team_data_store = {}

    all_team_data = []

    for mid in st.session_state.team_ids:
        existing = st.session_state.team_data_store.get(mid, {"name": "", "skills": {}})

        with st.container(border=True):
            head_col, del_col = st.columns([0.5, 0.1])
            name = head_col.text_input("Name", value=existing["name"], key=f"name_{mid}")
            del_col.button("Remove", key=f"del_{mid}", on_click=remove_member, args=(mid,))

            # Base tech skills
            base_options = get_tech_skills()
            # Add any custom skills previously saved for this member to the options list
            saved_skills = list(existing["skills"].keys())
            combined_options = list(set(base_options + saved_skills))

            selected_skills = st.multiselect(
                "Skills", 
                options=combined_options, # custom saved skills
                default=saved_skills, 
                key=f"skills_{mid}",
                accept_new_options=True # enables typing new skills
            )
            
            skill_levels = {}
            if selected_skills:
                cols = st.columns(2)
                for idx, skill in enumerate(selected_skills):
                    prev_level = existing["skills"].get(skill, "Beginner")
                    level = cols[idx % 2].select_slider(
                        f"{skill}", 
                        options=["Beginner", "Intermediate", "Advanced"], 
                        value=prev_level, 
                        key=f"lvl_{mid}_{skill}"
                    )
                    skill_levels[skill] = level
            
            current_member = {"name": name, "skills": skill_levels}
            st.session_state.team_data_store[mid] = current_member
            all_team_data.append(current_member)

    st.divider()

    col_add, _, col_next = st.columns([1,1,1])
    
    col_add.button("Add Member", on_click=add_member, use_container_width=True)
    
    if col_next.button("Next", type="primary", use_container_width=True):
        st.session_state.final_team_data = all_team_data
        st.switch_page(st.session_state.page_2)
    

