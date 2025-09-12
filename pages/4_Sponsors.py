import json, streamlit as st
from lib.ui import apply_brand, top_nav

st.set_page_config(page_title="Sponsors — Insaka", page_icon="🤝", layout="wide")
apply_brand(); top_nav()
st.title("Sponsors")

try:
    sponsors = json.load(open("data/sponsors.json","r",encoding="utf-8"))
except Exception:
    sponsors = {
        "Platinum":[{"name":"ZNBC","logo":"assets/logos/znbc.png"}],
        "Gold":[{"name":"ZESCO","logo":"assets/logos/zesco.png"}],
        "Silver":[{"name":"BoZ","logo":"assets/logos/boz.png"}]
    }

for tier, items in sponsors.items():
    st.subheader(tier)
    row = st.columns(4)
    for i, sp in enumerate(items):
        with row[i % 4]:
            with st.container(border=True):
                if sp.get("logo"): st.image(sp["logo"], use_container_width=True)
                st.markdown(f"**{sp['name']}**")
