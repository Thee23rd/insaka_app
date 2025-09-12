# lib/ui.py
import streamlit as st

ZAMBIA = {
    "green":  "#198A00",
    "red":    "#D10000",
    "black":  "#000000",
    "orange": "#FF9500",
    "ink":    "#F3F4F6",
    "paper":  "#000000",
    "panel":  "#101827",
}

def apply_brand():
    p = ZAMBIA
    st.markdown(
        f"""
        <style>
        .stApp {{ background:{p["paper"]}; color:{p["ink"]}; }}
        section.main > div {{ padding-top:.5rem; }}
        .card {{
            background:{p["panel"]}; border-radius:12px; padding:16px; border:1px solid rgba(255,255,255,.08);
        }}
        .hero h1 {{ margin:.25rem 0 .25rem; font-size:2rem; }}
        .subtle {{ opacity:.8; font-size:.95rem; }}
        .stButton > button {{
            background:{p["green"]} !important; color:#fff !important; border-radius:10px !important; font-weight:600 !important;
        }}
        .pill {{ display:inline-block; padding:.25rem .6rem; border-radius:999px; border:1px solid rgba(255,255,255,.15); }}
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
