# pages/0_Landing.py
import streamlit as st
from lib.ui import apply_brand

st.set_page_config(page_title="Insaka Conference", page_icon="🪘", layout="wide")

# Hide the default navigation for this landing page
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

# Main Conference Banner
st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

# Conference title and details
st.markdown("# ZAMBIA MINING AND INVESTMENT INSAKA CONFERENCE 2025")
st.markdown("## Collaborate • Innovate • Thrive")
st.markdown("### October 6th-10th, 2025")


st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

# Enhanced Delegate Access Section
st.markdown("""
<div style="background: linear-gradient(145deg, #1A1A1A 0%, #2A2A2A 100%); border: 2px solid #198A00; border-radius: 20px; padding: 2rem; margin: 2rem 0; box-shadow: 0 8px 32px rgba(25, 138, 0, 0.2); text-align: center;">
    <h3 style="color: #198A00; font-size: 1.8rem; margin-bottom: 1rem; font-weight: 700;">👤 Delegate Access</h3>
    <p style="color: #F3F4F6; font-size: 1.1rem; margin-bottom: 1.5rem; line-height: 1.5;">Access conference information, update your details, and manage your participation in the 5-day Insaka Conference 2025</p>
</div>
""", unsafe_allow_html=True)

# Delegate button with enhanced styling
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 Enter as Delegate", use_container_width=True, type="primary", key="delegate_btn"):
        st.switch_page("pages/7_Delegate_Self_Service.py")

# Zambian-themed Footer
st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

# Footer content
st.markdown("###### Insaka Conference 2025")
st.markdown("**Need help?** Contact the conference organizers")

# Zambian flag colors decoration
st.markdown("🟠 🟢 🔴 🟠")  # Orange, Green, Red, Orange

st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)
