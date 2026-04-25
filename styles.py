import streamlit as st

def apply_global_styles():
    st.markdown("""
    <style>

    /* Font: clean + modern */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');

    /* Background */
    html, body, [data-testid="stApp"] {
        font-family: 'Inter', sans-serif;
        background: radial-gradient(circle at top, #0f172a, #020617 70%);
        color: #e5e7eb;
    }

    /* Container */
    .block-container {
        max-width: 880px;
        padding-top: 2.5rem;
    }

    /* Title */
    h1 {
        font-weight: 600;
        letter-spacing: -0.5px;
        color: #e2e8f0;
    }
    /* Inputs */
    textarea, .stSelectbox, .stSlider {
        border-radius: 10px !important;
    }

    /* Divider */
    .divider {
        height: 1px;
        background: linear-gradient(to right, transparent, #1e293b, transparent);
        margin: 32px 0;
    }

    /* Card (tech panel) */
    .card-block {
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 18px;

        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(148, 163, 184, 0.15);

        backdrop-filter: blur(12px);
        box-shadow: 0 0 0 rgba(0,0,0,0);

        transition: all 0.25s ease;
    }

    /* Glow hover */
    .card-block:hover {
        transform: translateY(-3px);
        border: 1px solid rgba(99, 102, 241, 0.5);
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.25);
    }

    /* Card title */
    .card-block h3 {
        color: #a5b4fc;
        margin-bottom: 10px;
    }

    /* Subtitle */
    .stCaption {
        color: #94a3b8;
    }
                    /* Labels */
    .label {
        font-size: 12px;
        font-weight: 500;
        color: #64748b;
        margin-top: 10px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        padding: 8px 14px;
        font-weight: 500;
        border: 1px solid #27272a;
        background: #111;
        color: #fafafa;
        transition: all 0.15s ease;
    }

    /* Primary */
    .stButton button:first-child {
        background: #fafafa;
        color: #0a0a0a;
        border: none;
    }

    .stButton button:first-child:hover {
        background: #22d3ee;
    }

    /* Secondary */
    .stButton button[kind="secondary"] {
        background: #111;
        color: #a1a1aa;
    }
    .stButton button[kind="secondary"]:hover {
        border: 1px solid #3f3f46;
        color: #e4e4e7;
    }

    /* Inputs */
    textarea {
        background: rgba(2, 6, 23, 0.9) !important;
        border: 1px solid #1e293b !important;
        border-radius: 12px !important;

        font-family: 'JetBrains Mono', monospace;
        font-size: 14px;
    }

    textarea:focus {
        border: 1px solid #22d3ee !important;
        box-shadow: 0 0 10px rgba(34, 211, 238, 0.4);
    }

    /* Selectbox text fix */
    div[data-baseweb="select"] {
        background-color: #020617 !important;
    }

    /* Scrollbar (optional but nice) */
    ::-webkit-scrollbar {
        width: 6px;
    }

    ::-webkit-scrollbar-thumb {
        background: #1e293b;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #334155;
    }
    /* Subtle fade-in animation */
    .card-block {
        animation: fadeIn 0.35s ease;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
    }

                    
    """
    , unsafe_allow_html=True)