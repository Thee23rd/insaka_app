import json, streamlit as st
from lib.ui import apply_brand, top_nav

st.set_page_config(page_title="Exhibitors — Insaka", page_icon="🏢", layout="wide")
apply_brand(); top_nav()
st.title("Exhibitors")

try:
    exhibitors = json.load(open("data/exhibitors.json","r",encoding="utf-8"))
except Exception:
    exhibitors = [
        {"name":"AgriTech Co.", "stand":"A12", "logo":"assets/logos/agritech.png", "url":"https://example.com"},
        {"name":"ZedFin", "stand":"B03", "logo":"assets/logos/zedfin.png", "url":"https://example.com"},
    ]

cols = st.columns(3)
for i, ex in enumerate(exhibitors):
    with cols[i % 3]:
        with st.container(border=True):
            if ex.get("logo"): st.image(ex["logo"], use_container_width=True)
            st.markdown(f"**{ex['name']}**  \nStand **{ex.get('stand','TBA')}**")
            if ex.get("url"):
                st.link_button("Visit website", ex["url"])
