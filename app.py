import streamlit as st
from pages.team_form import show_team_form
from pages.summary import show_summary

page_1 = st.Page(show_team_form, title="Manage Team")
page_2 = st.Page(show_summary, title="Summary") # placeholder

st.session_state.page_1 = page_1
st.session_state.page_2 = page_2

pg = st.navigation([page_1, page_2], position="hidden")
pg.run()