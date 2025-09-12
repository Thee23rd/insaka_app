import os, streamlit as st
from lib.ui import apply_brand, top_nav

st.set_page_config(page_title="Materials — Insaka", page_icon="📁", layout="wide")
apply_brand(); top_nav()
st.title("Conference Materials")

# Read ./assets/materials
materials_dir = "assets/materials"
if os.path.isdir(materials_dir):
    for fname in sorted(os.listdir(materials_dir)):
        fpath = os.path.join(materials_dir, fname)
        if os.path.isfile(fpath):
            with open(fpath, "rb") as f:
                st.download_button(label=f"Download {fname}", data=f.read(), file_name=fname)
else:
    st.info("Materials will appear here.")
