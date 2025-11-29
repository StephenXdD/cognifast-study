import streamlit as st

def apply_custom_css():
    """Applies custom CSS for the Google Sleek theme."""
    st.markdown("""
    <style>
/* ============================
   FONT IMPORTS
============================ */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

:root {
    /* Soft Neo-Minimal Color System */
    --primary-color: #5A67D8;      /* Soft Lavender Blue */
    --primary-hover: #434DBD;      /* Darkened Lavender */
    --primary-tint: #EEF0FF;       /* Very Light Indigo */

    --bg-page: #FAFAFA;
    --bg-sidebar: #F4F4F7;
    --bg-card: #FFFFFF;

    --text-heading: #1F1F29;
    --text-body: #32323D;
    --text-subtle: #6D6D78;

    --border-light: #E2E2EA;
    --border-strong: #C7C7D2;

    --hover-bg: #F1F1F7;

    --shadow-card: 0 2px 6px rgba(0,0,0,0.06);
}

/* ============================
   GLOBAL APP STYLING
============================ */
.stApp {
    background-color: var(--bg-page);
    font-family: 'Roboto', sans-serif;
    color: var(--text-body);
}

/* HEADINGS */
h1, h2, h3 {
    color: var(--text-heading) !important;
    font-weight: 500 !important;
}

/* GENERAL TEXT */
p, li, div {
    color: var(--text-body);
}

/* ============================
   BUTTONS (Material Style)
============================ */
.stButton > button {
    width: 100%;
    height: 3.1em;
    border-radius: 16px;
    border: none;
    background-color: var(--primary-color);
    color: white;
    font-weight: 500;
    letter-spacing: 0.3px;
    transition: 0.2s ease;
    box-shadow: 0 1px 3px rgba(0,0,0,0.12);
}

.stButton > button:hover {
    background-color: var(--primary-hover);
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.stButton > button:active {
    transform: scale(0.98);
}

/* ============================
   CARD ELEMENTS
============================ */
.flashcard, .question-box {
    background-color: var(--bg-card);
    padding: 24px;
    border-radius: 10px;
    border: 1px solid var(--border-light);
    box-shadow: var(--shadow-card);
    transition: 0.2s ease;
}

.flashcard:hover, .question-box:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

/* ============================
   RADIO OPTIONS (Vertical)
============================ */
div[role="radiogroup"] {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

div[role="radiogroup"] label {
    background-color: var(--bg-card);
    padding: 14px 16px;
    border-radius: 8px;
    border: 1px solid var(--border-light);
    cursor: pointer;
    transition: 0.2s ease;
}

div[role="radiogroup"] label:hover {
    background-color: var(--hover-bg);
    border-color: var(--border-strong);
}

div[role="radiogroup"] label[data-checked="true"] {
    background-color: var(--primary-tint);
    border-color: var(--primary-color);
    color: var(--primary-hover);
}

/* ============================
   SIDEBAR
============================ */
section[data-testid="stSidebar"] {
    background-color: var(--bg-sidebar);
    border-right: 1px solid var(--border-light);
}

section[data-testid="stSidebar"] * {
    color: var(--text-body);
}

/* ============================
   INPUT FIELDS
============================ */
.stTextInput > div > div > input {
    background-color: var(--bg-sidebar);
    border-radius: 6px;
    border: 1px solid var(--border-light);
    padding: 10px;
    color: var(--text-body);
}

.stTextInput > div > div > input:focus {
    border-color: var(--primary-color);
    background-color: #fff;
    box-shadow: none;
}

/* ============================
   TABS
============================ */
.stTabs [data-baseweb="tab-list"] {
    gap: 24px;
    border-bottom: 1px solid var(--border-light);
}

.stTabs [data-baseweb="tab"] {
    color: var(--text-subtle);
    padding: 6px 16px;
    border: none;
    border-bottom: 2px solid transparent;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    background-color: transparent;
}

.stTabs [aria-selected="true"] {
    color: var(--primary-color) !important;
    border-bottom: 2px solid var(--primary-color);
}

/* ============================
   FILE UPLOADER
============================ */
[data-testid="stFileUploader"] {
    border: 1px dashed var(--border-light);
    padding: 20px;
    border-radius: 10px;
    background-color: var(--bg-card);
    transition: 0.2s ease;
}

[data-testid="stFileUploader"]:hover {
    border-color: var(--primary-color);
    background-color: var(--primary-tint);
}
</style>

    """, unsafe_allow_html=True)