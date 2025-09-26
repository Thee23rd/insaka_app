import json, streamlit as st
from lib.ui import apply_brand

st.set_page_config(page_title="Speakers — Insaka", page_icon="🎤", layout="wide")

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

st.markdown("# 🎤 Speakers")

st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)
try:
    speakers = json.load(open("data/speakers.json","r",encoding="utf-8"))
except Exception:
    speakers = [
      
        {"name":"Mukuka Mwape", "talk":"SME Financing", "bio":"...", "slides":"", "photo":""},
    ]

for sp in speakers:
    with st.container(border=True):
        cols = st.columns([1,3,1])
        with cols[0]:
            if sp.get("photo"):
                st.image(sp["photo"], use_container_width=True)
        with cols[1]:
            st.markdown(f"### {sp['name']}")
            st.caption(sp.get("talk","Talk"))
            st.write(sp.get("bio",""))
        with cols[2]:
            if sp.get("slides"):
                st.download_button("Download slides", data=open(sp["slides"],"rb").read(),
                                   file_name=sp["slides"].split("/")[-1])
