import streamlit as st

from form import manage_team

st.title("Hello World!")
st.write("This is my first Streamlit app.")

team_info = manage_team()

if team_info:
    st.success(f"Processing data for {len(team_info)} members!")
    st.write(team_info)