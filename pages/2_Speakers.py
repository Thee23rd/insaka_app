import json, streamlit as st
from lib.ui import apply_brand, top_nav

st.set_page_config(page_title="Speakers — Insaka", page_icon="🎤", layout="wide")
apply_brand()
top_nav()

st.title("Speakers")
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
