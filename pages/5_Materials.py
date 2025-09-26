import os, streamlit as st
from lib.ui import apply_brand

st.set_page_config(page_title="Materials — Insaka", page_icon="📁", layout="wide")

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

st.markdown("# 📄 Conference Materials")

st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

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
