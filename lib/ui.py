# lib/ui.py
import streamlit as st

ZAMBIA = {
    "green":  "#198A00",
    "green_light": "#2BA300",
    "red":    "#D10000",
    "red_light": "#E60000",
    "black":  "#000000",
    "orange": "#FF9500",
    "orange_light": "#FFB84D",
    "ink":    "#F3F4F6",
    "paper":  "#0A0A0A",
    "panel":  "#1A1A1A",
    "accent": "#FF6B35",
    "gold":   "#FFD700",
}

def apply_brand():
    p = ZAMBIA
    st.markdown(
        f"""
        <style>
        /* Force dark theme - hide theme switcher */
        [data-testid="stHeader"] button[kind="header"],
        [data-testid="stHeader"] button[aria-label*="theme"],
        [data-testid="stHeader"] button[aria-label*="Theme"],
        section[data-testid="stSidebar"] button[aria-label*="theme"],
        section[data-testid="stSidebar"] button[aria-label*="Theme"] {{
            display: none !important;
        }}
        
        /* Main App Background with Zambian Gradient */
        .stApp {{ 
            background: linear-gradient(135deg, {p["black"]} 0%, {p["panel"]} 50%, {p["black"]} 100%);
            color: {p["ink"]};
        }}
        
        /* Ensure all text is visible */
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {{
            color: {p["ink"]} !important;
        }}
        
        .stApp p, .stApp div, .stApp span, .stApp label {{
            color: {p["ink"]} !important;
        }}
        
        /* Streamlit specific elements */
        .stMarkdown {{
            color: {p["ink"]} !important;
        }}
        
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {{
            color: {p["ink"]} !important;
        }}
        
        .stMarkdown p {{
            color: {p["ink"]} !important;
        }}
        
        /* Header Styling */
        .stApp > header {{
            background: linear-gradient(90deg, {p["green"]} 0%, {p["green_light"]} 100%);
            border-bottom: 3px solid {p["orange"]};
        }}
        
        /* Main Content Area */
        section.main > div {{ 
            padding-top: 1rem;
            background: transparent;
        }}
        
        /* Cards with Zambian Theme */
        .card {{
            background: linear-gradient(145deg, {p["panel"]} 0%, #2A2A2A 100%);
            border-radius: 15px;
            padding: 20px;
            border: 2px solid {p["green"]};
            box-shadow: 0 8px 32px rgba(25, 138, 0, 0.2);
            color: {p["ink"]} !important;
        }}
        
        .card h1, .card h2, .card h3, .card h4, .card h5, .card h6 {{
            color: {p["ink"]} !important;
        }}
        
        .card p, .card div, .card span {{
            color: {p["ink"]} !important;
        }}
        
        /* Hero Section */
        .hero h1 {{ 
            margin: 0.5rem 0;
            font-size: 2.5rem;
            background: linear-gradient(45deg, {p["green"]}, {p["orange"]});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        /* Subtle Text */
        .subtle {{ 
            opacity: 0.9;
            font-size: 1rem;
            color: {p["orange_light"]};
        }}
        
        /* Primary Buttons - Zambian Green */
        .stButton > button {{
            background: linear-gradient(45deg, {p["green"]}, {p["green_light"]}) !important;
            color: white !important;
            border-radius: 12px !important;
            font-weight: 700 !important;
            border: 2px solid {p["green"]} !important;
            box-shadow: 0 4px 15px rgba(25, 138, 0, 0.3) !important;
            transition: all 0.3s ease !important;
        }}
        
        .stButton > button:hover {{
            background: linear-gradient(45deg, {p["green_light"]}, {p["green"]}) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(25, 138, 0, 0.4) !important;
        }}
        
        /* Secondary Buttons - Zambian Orange */
        .stButton > button[kind="secondary"] {{
            background: linear-gradient(45deg, {p["orange"]}, {p["orange_light"]}) !important;
            color: {p["black"]} !important;
            border: 2px solid {p["orange"]} !important;
        }}
        
        /* Success Messages */
        .stSuccess {{
            background: linear-gradient(135deg, {p["green"]}, {p["green_light"]}) !important;
            border: 2px solid {p["green"]} !important;
            border-radius: 12px !important;
        }}
        
        /* Info Messages */
        .stInfo {{
            background: linear-gradient(135deg, {p["orange"]}, {p["orange_light"]}) !important;
            border: 2px solid {p["orange"]} !important;
            border-radius: 12px !important;
            color: {p["black"]} !important;
        }}
        
        /* Warning Messages */
        .stWarning {{
            background: linear-gradient(135deg, {p["red"]}, {p["red_light"]}) !important;
            border: 2px solid {p["red"]} !important;
            border-radius: 12px !important;
        }}
        
        /* Error Messages */
        .stError {{
            background: linear-gradient(135deg, {p["red"]}, {p["red_light"]}) !important;
            border: 2px solid {p["red"]} !important;
            border-radius: 12px !important;
        }}
        
        /* Pills with Zambian Colors */
        .pill {{ 
            display: inline-block;
            padding: 0.5rem 1rem;
            border-radius: 25px;
            background: linear-gradient(45deg, {p["green"]}, {p["green_light"]});
            color: white;
            font-weight: 600;
            border: 2px solid {p["green"]};
        }}
        
        /* Input Fields */
        .stTextInput > div > div > input {{
            background: {p["panel"]} !important;
            border: 2px solid {p["green"]} !important;
            border-radius: 10px !important;
            color: {p["ink"]} !important;
        }}
        
        .stTextInput > div > div > input:focus {{
            border-color: {p["orange"]} !important;
            box-shadow: 0 0 10px rgba(255, 149, 0, 0.3) !important;
        }}
        
        /* Select Boxes */
        .stSelectbox > div > div > div {{
            background: {p["panel"]} !important;
            border: 2px solid {p["green"]} !important;
            border-radius: 10px !important;
        }}
        
        /* DataFrames */
        .stDataFrame {{
            border: 2px solid {p["green"]} !important;
            border-radius: 12px !important;
        }}
        
        /* Sidebar */
        .stSidebar {{
            background: linear-gradient(180deg, {p["black"]} 0%, {p["panel"]} 100%) !important;
            border-right: 3px solid {p["green"]} !important;
        }}
        
        /* Metric Cards */
        .metric-card {{
            background: linear-gradient(145deg, {p["panel"]}, #2A2A2A);
            border: 2px solid {p["green"]};
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(25, 138, 0, 0.2);
        }}
        
        /* Zambian Flag Colors Accent */
        .zambia-accent {{
            background: linear-gradient(90deg, {p["green"]} 33%, {p["red"]} 33%, {p["red"]} 66%, {p["orange"]} 66%);
            height: 4px;
            border-radius: 2px;
        }}
        
        /* Streamlit containers and columns */
        .stContainer {{
            color: {p["ink"]} !important;
        }}
        
        .stColumn {{
            color: {p["ink"]} !important;
        }}
        
        /* Ensure all Streamlit elements are visible */
        .element-container {{
            color: {p["ink"]} !important;
        }}
        
        .element-container h1, .element-container h2, .element-container h3, .element-container h4, .element-container h5, .element-container h6 {{
            color: {p["ink"]} !important;
        }}
        
        .element-container p, .element-container div, .element-container span {{
            color: {p["ink"]} !important;
        }}
        
        /* Specific Streamlit components */
        .stSelectbox label, .stTextInput label, .stTextArea label {{
            color: {p["ink"]} !important;
        }}
        
        .stRadio label, .stCheckbox label {{
            color: {p["ink"]} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def top_nav():
    """Persistent top nav bar with true page links."""
    c1, c2, c3, c4, c5, c6, c7 = st.columns([1.2,1,1,1,1,1,1])
    with c1: st.page_link("streamlit_app.py", label="Home", icon="🏠")
    with c2: st.page_link("pages/1_Agenda.py", label="Agenda", icon="🗓️")
    with c3: st.page_link("pages/2_Speakers.py", label="Speakers", icon="🎤")
    with c4: st.page_link("pages/3_Exhibitors.py", label="Exhibitors", icon="🏢")
    with c5: st.page_link("pages/4_Sponsors.py", label="Sponsors", icon="🤝")
    with c6: st.page_link("pages/5_Materials.py", label="Materials", icon="📁")
    with c7: st.page_link("pages/6_Venue.py", label="Venue", icon="🗺️")
