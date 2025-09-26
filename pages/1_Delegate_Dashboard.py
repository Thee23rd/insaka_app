# pages/1_Delegate_Dashboard.py
import streamlit as st
from lib.ui import apply_brand

st.set_page_config(page_title="Delegate Dashboard — Insaka", page_icon="👤", layout="wide")

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

# Personalized greeting
if hasattr(st.session_state, 'delegate_name') and st.session_state.delegate_name:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #2E8B57 0%, #3CB371 100%); color: white; padding: 2rem; border-radius: 12px; margin-bottom: 2rem; text-align: center;">
        <h1 style="color: white; margin-bottom: 0.5rem;">👋 Hello, {st.session_state.delegate_name}!</h1>
        <p style="color: #f0f8f0; margin-bottom: 0; font-size: 1.1rem;">Welcome to Insaka Conference 2025</p>
        <p style="color: #e8f5e8; margin-bottom: 0; font-size: 0.9rem;">{st.session_state.delegate_organization} • {st.session_state.delegate_category}</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.title("👤 Delegate Dashboard")
    st.markdown("Welcome to your conference dashboard")

# Personal section - Check-in first
st.subheader("👤 My Information")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("✏️ Update My Details", use_container_width=True):
        st.switch_page("pages/7_Delegate_Self_Service.py")

with col2:
    if st.button("📱 Download Materials", use_container_width=True):
        st.switch_page("pages/5_Materials.py")

with col3:
    if st.button("✅ Daily Check-In", use_container_width=True):
        st.switch_page("pages/8_Check_In.py")

st.write("")

# Quick access buttons
st.subheader("🚀 Quick Access")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📅 Agenda", use_container_width=True):
        st.switch_page("pages/1_Agenda.py")

with col2:
    if st.button("👥 Speakers", use_container_width=True):
        st.switch_page("pages/2_Speakers.py")

with col3:
    if st.button("🏢 Exhibitors", use_container_width=True):
        st.switch_page("pages/3_Exhibitors.py")

with col4:
    if st.button("🏛️ Venue", use_container_width=True):
        st.switch_page("pages/6_Venue.py")

# Conference info
st.subheader("📋 Conference Information")
st.info("""
**Conference Dates:** October 6-8, 2025  
**Location:** [Venue details will be shown here]  
**Theme:** Collaborate • Innovate • Thrive

**Key Sessions:**
- Opening & Keynote: Sunday 6 Oct, 09:00
- [Additional sessions will be loaded from agenda]

**Important Notes:**
- Please ensure your details are up to date
- Check the agenda regularly for updates
- Download conference materials from the Materials section
""")

# Quick stats or announcements
st.subheader("📢 Announcements")
st.success("✅ Welcome to Insaka Conference 2025! Make sure to check the agenda for the latest updates.")

# Simple footer
st.markdown("---")
st.caption("Need help? Contact the conference organizers or visit the registration desk.")
