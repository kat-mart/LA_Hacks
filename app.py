import streamlit as st
from pages.landing import show_landing_page
from pages.team_form import show_team_form
from pages.geminiAgent1 import main
from pages.tasks import show_tasks_editable
from styles import apply_global_styles

apply_global_styles()

page_0 = st.Page(show_landing_page, title="Welcome")
page_1 = st.Page(show_team_form, title="Manage Team")
page_2 = st.Page(main, title="Project Ideas")
page_3 = st.Page(show_tasks_editable, title="Team Tasks")

st.session_state.page_0 = page_0
st.session_state.page_1 = page_1
st.session_state.page_2 = page_2
st.session_state.page_3 = page_3

pg = st.navigation([page_0, page_1, page_2, page_3], position="hidden")
pg.run()