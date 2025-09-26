import streamlit as st
from lib.ui import apply_brand

st.set_page_config(page_title="Venue — Insaka", page_icon="🗺️", layout="wide")

# Hide sidebar and navigation for delegates
st.markdown("""
<style>
    .stApp > header {
        display: none;
    }
    .stApp > div[data-testid="stToolbar"] {
        display: none;
    }
    .stSidebar {
        display: none;
    }
    .stApp > div[data-testid="stSidebar"] {
        display: none;
    }
    .stApp > div[data-testid="stSidebar"] > div {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

apply_brand()

# Zambian-themed header
st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

# Back button
if st.button("← Back to Dashboard", type="secondary"):
    st.switch_page("pages/1_Delegate_Dashboard.py")

st.markdown("# 🏢 Venue & Exhibition Map")

st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

left, right = st.columns([2,1])
with left:
    # Replace with your map image or embed
    st.image("assets/venue/floorplan.png", caption="Exhibition & Rooms", use_container_width=True)
with right:
    st.markdown("**Legend**")
    st.markdown("- A-Hall: Exhibitors A1–A20\n- B-Hall: Exhibitors B1–B16\n- Main Hall: Keynotes")
