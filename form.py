import streamlit as st
import uuid

def get_tech_skills():
    return ["Python", "React", "SQL", "Gemini API", "JavaScript", "C++", "Java", "Rust", "Go", "LangChain"]

def add_member():
    st.session_state.team_ids.append(str(uuid.uuid4()))

def remove_member(mid):
    if len(st.session_state.team_ids) > 1:
        st.session_state.team_ids.remove(mid)

def manage_team():
    if "team_ids" not in st.session_state:
        st.session_state.team_ids = [str(uuid.uuid4())]

    st.subheader("Team Members")
    all_team_data = []

    for mid in st.session_state.team_ids:
        with st.container(border=True):
            # Header Row: Name and Remove Button
            head_col, del_col = st.columns([0.5, 0.1])
            name = head_col.text_input("Name", key=f"name_{mid}", placeholder="Enter name...")
            del_col.button("Remove", key=f"del_{mid}", on_click=remove_member, args=(mid,))

            # Skill Selection
            selected_skills = st.multiselect(
                "Select Tech Skills", 
                get_tech_skills(), 
                key=f"skills_list_{mid}",
                accept_new_options=True
            )

            # Dynamic Skill Sliders
            skill_levels = {}
            if selected_skills:
                st.write("---")
                st.caption(f"Proficiency levels for {name if name else 'this member'}:")
                
                # Split sliders into two columns
                cols = st.columns(2)
                for idx, skill in enumerate(selected_skills):
                    col_idx = idx % 2
                    level = cols[col_idx].select_slider(
                        f"Level: {skill}",
                        options=["Beginner", "Intermediate", "Advanced"],
                        key=f"level_{mid}_{skill}"
                    )
                    skill_levels[skill] = level
            
            all_team_data.append({
                "name": name,
                "skills": skill_levels 
            })

    # Footer Controls
    st.divider()

    col_left, _, _ = st.columns([1, 1, 1]) 
    with col_left:
        st.button("Add Member", on_click=add_member, use_container_width=True)

    _, _, col_right = st.columns([1, 1, 1])
    with col_right:
        if st.button("Submit All", type="primary", use_container_width=True):
            return all_team_data
        
    return None

