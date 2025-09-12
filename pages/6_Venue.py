import streamlit as st
from lib.ui import apply_brand, top_nav

st.set_page_config(page_title="Venue — Insaka", page_icon="🗺️", layout="wide")
apply_brand(); top_nav()
st.title("Venue & Exhibition Map")

left, right = st.columns([2,1])
with left:
    # Replace with your map image or embed
    st.image("assets/venue/floorplan.png", caption="Exhibition & Rooms", use_container_width=True)
with right:
    st.markdown("**Legend**")
    st.markdown("- A-Hall: Exhibitors A1–A20\n- B-Hall: Exhibitors B1–B16\n- Main Hall: Keynotes")
