import streamlit as st

def apply_global_styles():
    st.markdown("""
    <style>
    /* ─── Google Fonts ─────────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Lato:wght@300;400;700&display=swap');

    /* ─── CSS Variables — Beige Whimsical Palette ───────────────────── */
    :root {
        --bg:           #f5f0e8;
        --bg-surface:   #fdf8f0;
        --bg-card:      #fff9f0;
        --border:       #e0d4bb;
        --border-soft:  #ede4d0;
        --text-primary: #3b2f1e;
        --text-secondary:#7a6650;
        --text-muted:   #b09a80;
        --accent:       #c8813a;
        --accent-soft:  #f0d9bc;
        --accent-hover: #a8622a;
        --success:      #6a9a72;
        --danger:       #b85c4a;
        --highlight:    #e8c98a;
        --shadow:       rgba(100, 70, 30, 0.12);
        --shadow-md:    rgba(100, 70, 30, 0.18);
    }

    /* ─── Dark Mode Override ─────────────────────────────────────────── */
    @media (prefers-color-scheme: dark) {
        :root {
            --bg:           #1e1810;
            --bg-surface:   #261e14;
            --bg-card:      #2e2418;
            --border:       #3d3020;
            --border-soft:  #352a1c;
            --text-primary: #f0e6d2;
            --text-secondary:#c8a880;
            --text-muted:   #8a7060;
            --accent:       #d4923f;
            --accent-soft:  #3d2a18;
            --accent-hover: #e8a84a;
            --success:      #7aaa82;
            --danger:       #c8725a;
            --highlight:    #5a4420;
            --shadow:       rgba(0, 0, 0, 0.35);
            --shadow-md:    rgba(0, 0, 0, 0.5);
        }
    }

    /* ─── Streamlit Dark Mode Support ───────────────────────────────── */
    [data-theme="dark"] {
        --bg:           #1e1810;
        --bg-surface:   #261e14;
        --bg-card:      #2e2418;
        --border:       #3d3020;
        --border-soft:  #352a1c;
        --text-primary: #f0e6d2;
        --text-secondary:#c8a880;
        --text-muted:   #8a7060;
        --accent:       #d4923f;
        --accent-soft:  #3d2a18;
        --accent-hover: #e8a84a;
        --success:      #7aaa82;
        --danger:       #c8725a;
        --highlight:    #5a4420;
        --shadow:       rgba(0, 0, 0, 0.35);
        --shadow-md:    rgba(0, 0, 0, 0.5);
    }

    /* ─── Base & App Shell ───────────────────────────────────────────── */
    html, body, [class*="css"] {
        font-family: 'Lato', Georgia, serif;
        color: var(--text-primary);
    }

    .stApp {
        background-color: var(--bg) !important;
        background-image:
            radial-gradient(ellipse at 20% 10%, rgba(200, 129, 58, 0.06) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 90%, rgba(168, 140, 100, 0.06) 0%, transparent 50%);
    }

    /* ─── Main Content Block ─────────────────────────────────────────── */
    .main .block-container {
        padding: 2.5rem 2rem 4rem;
        max-width: 860px;
        background-color: var(--bg-surface);
        border-radius: 20px;
        border: 1px solid var(--border-soft);
        box-shadow: 0 4px 24px var(--shadow);
        margin-top: 1.5rem;
    }

    /* ─── Typography ─────────────────────────────────────────────────── */
    h1, h2, h3, h4 {
        font-family: 'Playfair Display', Georgia, serif !important;
        color: var(--text-primary) !important;
        letter-spacing: -0.01em;
    }

    h1 {
        font-size: 2.2rem !important;
        font-weight: 600 !important;
        border-bottom: 2px solid var(--border) !important;
        padding-bottom: 0.6rem !important;
        margin-bottom: 0.25rem !important;
    }

    h2 { font-size: 1.6rem !important; }
    h3 { font-size: 1.25rem !important; }

    p, li, label, .stMarkdown {
        color: var(--text-secondary);
        line-height: 1.75;
        font-size: 0.95rem;
    }

    /* ─── Caption / Subtext ──────────────────────────────────────────── */
    .stCaption, [data-testid="stCaptionContainer"] {
        color: var(--text-muted) !important;
        font-style: italic;
        font-size: 0.85rem !important;
    }

    /* ─── Buttons ────────────────────────────────────────────────────── */
    .stButton > button {
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: 12px !important;
        padding: 0.5rem 1.4rem !important;
        font-family: 'Lato', serif !important;
        font-size: 0.9rem !important;
        font-weight: 400 !important;
        letter-spacing: 0.02em !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px var(--shadow) !important;
    }

    .stButton > button:hover {
        background-color: var(--accent-soft) !important;
        border-color: var(--accent) !important;
        color: var(--accent) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 14px var(--shadow-md) !important;
    }

    /* Primary button */
    .stButton > button[kind="primary"] {
        background-color: var(--accent) !important;
        color: #fff !important;
        border-color: var(--accent) !important;
        font-weight: 700 !important;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: var(--accent-hover) !important;
        border-color: var(--accent-hover) !important;
        color: #fff !important;
    }

    /* ─── Text Inputs & Text Areas ───────────────────────────────────── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: var(--bg-card) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        font-family: 'Lato', serif !important;
        font-size: 0.93rem !important;
        padding: 0.55rem 0.85rem !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgba(200, 129, 58, 0.15) !important;
        outline: none !important;
    }

    /* ─── Selectbox & Multiselect ────────────────────────────────────── */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background-color: var(--bg-card) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
    }

    /* Dropdown options */
    [data-baseweb="popover"] ul {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
    }

    [data-baseweb="popover"] li:hover {
        background-color: var(--accent-soft) !important;
    }

    /* Multiselect tags */
    [data-baseweb="tag"] {
        background-color: var(--accent-soft) !important;
        border: 1px solid var(--accent) !important;
        border-radius: 20px !important;
        color: var(--accent) !important;
        font-size: 0.82rem !important;
    }

    /* ─── Slider ─────────────────────────────────────────────────────── */
    .stSlider > div > div > div > div {
        background-color: var(--accent) !important;
    }

    .stSlider [data-baseweb="slider"] > div > div:last-child > div {
        background-color: var(--accent) !important;
        border: 2px solid var(--accent-hover) !important;
    }

    /* ─── Checkbox ───────────────────────────────────────────────────── */
    .stCheckbox > label > div:first-child {
        border: 1.5px solid var(--border) !important;
        border-radius: 6px !important;
        background-color: var(--bg-card) !important;
    }

    .stCheckbox > label > div[data-checked="true"] {
        background-color: var(--accent) !important;
        border-color: var(--accent) !important;
    }

    /* ─── Date Input ─────────────────────────────────────────────────── */
    .stDateInput > div > div > input {
        background-color: var(--bg-card) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
    }

    /* ─── Progress Bar ───────────────────────────────────────────────── */
    .stProgress > div > div > div > div {
        background-color: var(--accent) !important;
        border-radius: 99px !important;
    }

    .stProgress > div > div > div {
        background-color: var(--accent-soft) !important;
        border-radius: 99px !important;
    }

    /* ─── Expander ───────────────────────────────────────────────────── */
    .streamlit-expanderHeader {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-soft) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        font-family: 'Lato', serif !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.02em !important;
    }

    .streamlit-expanderContent {
        background-color: var(--bg-surface) !important;
        border: 1px solid var(--border-soft) !important;
        border-top: none !important;
        border-radius: 0 0 10px 10px !important;
        padding: 1rem !important;
    }

    /* ─── Container / Card ───────────────────────────────────────────── */
    [data-testid="stVerticalBlock"] > div[data-testid="element-container"] > div[data-testid="stVerticalBlock"] {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-soft) !important;
        border-radius: 14px !important;
        padding: 1.2rem !important;
        box-shadow: 0 2px 10px var(--shadow) !important;
        margin-bottom: 0.75rem !important;
    }

    /* stContainer with border */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: var(--bg-card) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: 14px !important;
        padding: 1rem !important;
        box-shadow: 0 2px 10px var(--shadow) !important;
        margin-bottom: 0.75rem !important;
    }

    /* ─── Divider ────────────────────────────────────────────────────── */
    hr {
        border: none !important;
        border-top: 1.5px dashed var(--border) !important;
        margin: 1.5rem 0 !important;
        opacity: 0.7 !important;
    }

    /* ─── Code Block ─────────────────────────────────────────────────── */
    .stCode, code, pre {
        background-color: var(--highlight) !important;
        border-radius: 8px !important;
        border: 1px solid var(--border) !important;
        color: var(--text-primary) !important;
        font-size: 0.85rem !important;
    }

    /* ─── Spinner ────────────────────────────────────────────────────── */
    .stSpinner > div {
        border-color: var(--accent) transparent transparent transparent !important;
    }

    /* ─── Alerts / Info / Error ──────────────────────────────────────── */
    .stAlert {
        border-radius: 10px !important;
        border: 1px solid var(--border) !important;
        font-family: 'Lato', serif !important;
    }

    /* ─── Sidebar ────────────────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background-color: var(--bg-surface) !important;
        border-right: 1.5px solid var(--border) !important;
    }

    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] p {
        color: var(--text-secondary) !important;
    }

    /* ─── Label Text ─────────────────────────────────────────────────── */
    .stTextInput label, .stTextArea label, .stSelectbox label,
    .stMultiSelect label, .stSlider label, .stDateInput label,
    .stCheckbox label, .stRadio label {
        color: var(--text-secondary) !important;
        font-family: 'Lato', serif !important;
        font-weight: 700 !important;
        font-size: 0.82rem !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
        margin-bottom: 0.25rem !important;
    }

    /* ─── Whimsical Decorative Divider Utility ───────────────────────── */
    .divider {
        height: 1px;
        background: linear-gradient(to right, transparent, var(--border), transparent);
        margin: 1.5rem 0;
    }

    /* ─── Scrollbar ──────────────────────────────────────────────────── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg); border-radius: 99px; }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 99px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent); }

    /* ─── Column gap fix ──────────────────────────────────────────────── */
    [data-testid="column"] { gap: 0.5rem; }

    </style>
    """, unsafe_allow_html=True)