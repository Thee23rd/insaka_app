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

# Quick Login Option (if delegate has ID)
if hasattr(st.session_state, 'delegate_id_displayed') and st.session_state.delegate_id_displayed:
    st.markdown("### 🔑 Quick Login")
    st.info("You have a delegate ID. Enter it below for quick access, or use the main button for first-time setup.")
    
    with st.form("landing_quick_login"):
        delegate_id = st.text_input("Your Delegate ID:", placeholder="Enter your delegate ID", help="Use the ID you received after your first search")
        
        col_quick1, col_quick2 = st.columns([1, 1])
        with col_quick1:
            if st.form_submit_button("🚀 Quick Access", use_container_width=True, type="primary"):
                if delegate_id.strip():
                    # Verify delegate exists and authenticate
                    try:
                        from staff_service import load_staff_df
                        df = load_staff_df()
                        mask = df["ID"].astype(str) == str(delegate_id.strip())
                        
                        if mask.any():
                            delegate_record = df[mask].iloc[0]
                            
                            # Set authentication and session data
                            st.session_state.delegate_authenticated = True
                            st.session_state.delegate_id = str(delegate_record['ID'])
                            st.session_state.delegate_name = delegate_record.get('Name', '')
                            st.session_state.delegate_organization = delegate_record.get('Organization', '')
                            st.session_state.delegate_category = delegate_record.get('Category', '')
                            st.session_state.delegate_title = delegate_record.get('RoleTitle', '')
                            
                            st.success(f"✅ Welcome back, {delegate_record.get('Name', '')}!")
                            st.switch_page("pages/1_Delegate_Dashboard.py")
                        else:
                            st.error("❌ Invalid delegate ID. Please check your ID and try again.")
                    except Exception as e:
                        st.error("❌ Error verifying delegate ID. Please try again.")
                else:
                    st.error("❌ Please enter your delegate ID.")
        
        with col_quick2:
            if st.form_submit_button("🔍 Search Again", use_container_width=True):
                st.switch_page("pages/7_Delegate_Self_Service.py")
    
    st.markdown("---")

# Main delegate button with enhanced styling
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 Enter as Delegate", use_container_width=True, type="primary", key="delegate_btn"):
        st.switch_page("pages/7_Delegate_Self_Service.py")

# Zambian-themed Footer
st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

# Footer content
st.markdown("###### Insaka Conference 2025")
st.markdown("**Need help?** Contact the conference organizers")

# Logout button (if user is authenticated)
if hasattr(st.session_state, 'delegate_authenticated') and st.session_state.delegate_authenticated:
    st.markdown("---")
    col_logout1, col_logout2, col_logout3 = st.columns([1, 1, 1])
    with col_logout2:
        if st.button("🚪 Logout", use_container_width=True, key="landing_logout"):
            # Clear all session state
            for key in list(st.session_state.keys()):
                if key.startswith('delegate_'):
                    del st.session_state[key]
            st.success("✅ Logged out successfully!")
            st.rerun()

# Zambian flag colors decoration
st.markdown("🟠 🟢 🔴 🟠")  # Orange, Green, Red, Orange

st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)
