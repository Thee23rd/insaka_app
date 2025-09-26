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

# Clean Zambian-themed banner without logo
st.markdown("""
<div style="background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 50%, #4CAF50 100%); color: white; padding: 3rem 2rem; border-radius: 15px; margin-bottom: 2rem; position: relative; overflow: hidden; text-align: center;">
    <h1 style="color: white; font-size: 2.5rem; margin-bottom: 1rem; font-weight: bold; line-height: 1.2;">ZAMBIA MINING AND INVESTMENT INSAKA CONFERENCE 2025</h1>
    <p style="color: #E8F5E8; font-size: 1.3rem; margin-bottom: 1.5rem; font-weight: 500;">Collaborate • Innovate • Thrive</p>
    <p style="color: #C8E6C9; font-size: 1.1rem; margin-bottom: 1rem;">October 6-8, 2025</p>
    <div style="position: absolute; top: -20px; right: -20px; width: 80px; height: 80px; background: rgba(255,107,53,0.1); border-radius: 50%;"></div>
    <div style="position: absolute; bottom: -30px; left: -30px; width: 60px; height: 60px; background: rgba(255,107,53,0.1); border-radius: 50%;"></div>
</div>
""", unsafe_allow_html=True)

# Clean Delegate Access Section
st.markdown("### 👤 Delegate Access")
st.markdown("Access conference information, update your details, and manage your participation in Insaka Conference 2025")

# Simple centered button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 Enter as Delegate", use_container_width=True, type="primary", key="delegate_btn"):
        st.switch_page("pages/7_Delegate_Self_Service.py")

# Zambian-themed Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%); color: white; padding: 2rem; border-radius: 15px; margin-top: 2rem;">
    <p style="color: #E8F5E8; font-size: 1rem; margin-bottom: 0.5rem; font-weight: 500;">ZM Insaka Conference 2025</p>
    <p style="color: #C8E6C9; font-size: 0.9rem; margin: 0;">Need help? Contact the conference organizers</p>
    <div style="display: flex; justify-content: center; align-items: center; margin-top: 1rem;">
        <div style="width: 8px; height: 8px; background: #FF6B35; border-radius: 50%; margin: 0 3px;"></div>
        <div style="width: 8px; height: 8px; background: #1B5E20; border-radius: 50%; margin: 0 3px;"></div>
        <div style="width: 8px; height: 8px; background: #FF6B35; border-radius: 50%; margin: 0 3px;"></div>
    </div>
</div>
""", unsafe_allow_html=True)
