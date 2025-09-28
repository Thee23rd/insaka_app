import json, streamlit as st
from lib.ui import apply_brand, top_nav

st.set_page_config(page_title="Sponsors — Insaka", page_icon="🤝", layout="wide")

# Hide sidebar and navigation
st.markdown("""
<style>
    .stApp > div:first-child {
        display: none;
    }
    .stApp > div:nth-child(2) {
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

st.markdown("# 🤝 Sponsors")

st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

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
                if sp.get("logo"): st.image(sp["logo"], width='stretch')
                st.markdown(f"**{sp['name']}**")
