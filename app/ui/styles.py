import streamlit as st

GLOBAL_CSS = """
<style>

/* ===========================================
   LAYOUT GLOBAL - TYPE APPLICATION WEB
   =========================================== */
.main > div {
    max-width: 1180px;
    margin: 0 auto;
}

/* ===========================================
   TABS (principaux et secondaires)
   =========================================== */
div[data-baseweb="tab-list"] {
    gap: 0.4rem;
}

div[data-baseweb="tab-list"] button[role="tab"] {
    padding: 0.5rem 1.2rem;
    border-radius: 999px;
    font-size: 0.95rem;
    font-weight: 500;
    border: none;
}

div[data-baseweb="tab-list"] button[aria-selected="true"] {
    background-color: #FBA032;
    color: #ffffff;
}

div[data-baseweb="tab-list"] button[aria-selected="false"] {
    background-color: #f0f0f0;
    color: #444444;
}

/* ===========================================
   BOUTONS
   =========================================== */
.stButton > button {
    width: 100%;
    padding: 0.6rem 1rem;
    border-radius: 999px;
    border: 1px solid #FBA032;
    background-color: #FBA032 !important;
    border-color: #FBA032 !important;
    color: #ffffff !important;
    font-size: 0.85rem;
    font-weight: 500;
    cursor: pointer;
    transition: 0.15s ease-in-out;
    background-image: none;
}

.stButton > button:hover {
    background-color: #d88622 !important;
    border-color: #d88622 !important;
    color: #ffffff !important;
}

/* Boutons internes Streamlit (baseButton / primary / secondary / submit) */
.stButton button[data-testid^="baseButton"],
.stButton button[kind="primary"],
.stButton button[kind="secondary"],
button[data-testid^="baseButton"],
div[data-testid="stFormSubmitButton"] button,
div[data-testid="stFormSubmitButton"] button[data-testid="baseButton-primary"] {
    background-color: #FBA032 !important;
    border-color: #FBA032 !important;
    color: #ffffff !important;
    background-image: none !important;
    box-shadow: none !important;
    border-radius: 999px;
}

.stButton button[data-testid^="baseButton"]:hover,
.stButton button[kind="primary"]:hover,
.stButton button[kind="secondary"]:hover,
button[data-testid^="baseButton"]:hover,
div[data-testid="stFormSubmitButton"] button:hover,
div[data-testid="stFormSubmitButton"] button[data-testid="baseButton-primary"]:hover {
    background-color: #d88622 !important;
    border-color: #d88622 !important;
    color: #ffffff !important;
    background-image: none !important;
    box-shadow: none !important;
}

/* ===========================================
   CHAMPS (input, select, textarea)
   =========================================== */
.stTextInput input,
.stSelectbox select,
.stTextArea textarea {
    border-radius: 6px;
    padding: 0.45rem 0.6rem;
    font-size: 0.9rem;
}

/* ===========================================
   TITRES PRINCIPAUX (H1 / H2)
   =========================================== */
h1, .stApp h1 {
    font-size: 2.0rem;
    font-weight: 800;
    margin-top: 1.2rem;
    margin-bottom: 1.0rem;
    color: #ffffff;
    background-color: #0F879B;
    padding: 0.9rem 1.2rem;
    border-radius: 10px;
    display: block;
    width: 100%;
}

h2, .stApp h2 {
    font-size: 1.5rem;
    font-weight: 700;
    margin-top: 1.0rem;
    margin-bottom: 0.4rem;
    color: #222;
}

h2::after {
    content: "";
    display: block;
    width: 60px;
    height: 3px;
    background: #FBA032;
    margin-top: 0.25rem;
    border-radius: 2px;
}

/* ===========================================
   TITRES SECONDAIRES (H3 / H4)
   =========================================== */
h3, .stApp h3 {
    font-size: 1.2rem;
    font-weight: 600;
    margin-top: 0.7rem;
    margin-bottom: 0.35rem;
    color: #444;
}

h4, .stApp h4 {
    font-size: 1.05rem;
    font-weight: 550;
    margin-top: 0.5rem;
    margin-bottom: 0.3rem;
    color: #555;
}

/* ===========================================
   TABLES & DATAFRAME
   =========================================== */
.dataframe {
    border-radius: 6px;
    overflow: hidden;
}

/* ===========================================
   DIVERS
   =========================================== */
hr {
    margin: 1rem 0;
}

/* ===========================================
   METRIC CARDS (DASHBOARD)
   =========================================== */
.metric-card {
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    text-align: center;
    transition: transform 0.2s;
    height: 100%;
}
.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0,0,0,0.1);
    border-color: #0F879B;
}
.metric-value {
    font-size: 2.2rem;
    font-weight: 700;
    color: #0F879B;
    margin-bottom: 0.2rem;
}
.metric-label {
    font-size: 0.9rem;
    color: #666;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

</style>
"""

def inject_global_styles():
    """Injecte les styles CSS globaux dans toute l'interface Streamlit."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
