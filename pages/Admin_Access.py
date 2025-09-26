# pages/Admin_Access.py
import streamlit as st
import os
from lib.ui import apply_brand

st.set_page_config(page_title="Admin Access — Insaka", page_icon="🔐", layout="wide")

# Hide sidebar and navigation
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

# Admin access form
st.markdown("""
<div style="text-align: center; padding: 3rem 0;">
    <h1 style="color: #8B4513; font-size: 2.5rem; margin-bottom: 1rem;">🔐 Admin Access</h1>
    <p style="color: #666; font-size: 1.2rem; margin-bottom: 2rem;">Insaka Conference Management</p>
</div>
""", unsafe_allow_html=True)

# Password form
with st.form("admin_login", clear_on_submit=False):
    st.markdown("### Enter Admin Credentials")
    
    # Get admin PIN from environment or secrets
    ADMIN_PIN = os.environ.get("ADMIN_PIN", "") or st.secrets.get("ADMIN_PIN", "1234")
    
    admin_pin = st.text_input("Admin PIN", type="password", placeholder="Enter your admin PIN")
    
    col1, col2 = st.columns(2)
    with col1:
        submitted = st.form_submit_button("🔓 Access Admin Panel", use_container_width=True, type="primary")
    with col2:
        if st.form_submit_button("🏠 Back to Main", use_container_width=True, type="secondary"):
            st.switch_page("pages/0_Landing.py")
    
    if submitted:
        if admin_pin == ADMIN_PIN:
            st.success("✅ Access granted! Redirecting to admin panel...")
            st.switch_page("pages/0_Admin.py")
        else:
            st.error("❌ Invalid PIN. Access denied.")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #999; font-size: 0.9rem; padding: 2rem 0;">
    <p>Authorized personnel only</p>
</div>
""", unsafe_allow_html=True)
