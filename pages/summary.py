# summary.py
import streamlit as st

def show_summary():
    st.title("Team Summary")

    if "final_team_data" not in st.session_state or not st.session_state.final_team_data:
        st.warning("No team members found! Please go back and fill out the form.")
        if st.button("Back to Form"):
            st.switch_page(st.session_state.page_objects['form'])
        return

    data = st.session_state.final_team_data
    
    st.divider()

    # Detailed Member View
    for member in data:
        with st.expander(f"{member['name'] if member['name'] else 'Unnamed Member'}", expanded=True):
            if not member['skills']:
                st.write("No skills selected.")
            else:
                # Display skills
                cols = st.columns(len(member['skills']))
                for idx, (skill, level) in enumerate(member['skills'].items()):
                    with cols[idx]:
                        st.markdown(f"**{skill}**")
                        st.caption(level)

    # Navigation
    st.divider()
    if st.button("Back to Form"):
        st.switch_page(st.session_state.page_1) 