# pages/7_Delegate_Self_Service.py
import streamlit as st
import pandas as pd
from lib.ui import apply_brand
from staff_service import load_staff_df, save_staff_df

st.set_page_config(page_title="Delegate Self-Service — Insaka", page_icon="👤", layout="wide")

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

st.markdown("# 👤 Delegate Self-Service")
st.markdown("Check and update your conference details")

st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

# Authentication system
if not hasattr(st.session_state, 'delegate_authenticated') or not st.session_state.delegate_authenticated:
    
    # Check if user has their ID (for returning users)
    if hasattr(st.session_state, 'delegate_id_displayed') and st.session_state.delegate_id_displayed:
        st.subheader("🔐 Quick Login")
        st.info("Use your delegate ID to quickly access your account.")
        
        with st.form("quick_auth_form"):
            delegate_id = st.text_input("Your Delegate ID:", placeholder="Enter your delegate ID", help="Use the ID shown after your first search")
            
            if st.form_submit_button("🔑 Quick Login", width='stretch'):
                if delegate_id.strip():
                    # Verify delegate exists
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
                        st.rerun()
                    else:
                        st.error("❌ Invalid delegate ID. Please check your ID and try again.")
                else:
                    st.error("❌ Please enter your delegate ID.")
        
        st.markdown("---")
        st.info("💡 **Don't have your ID?** Search for your name below to get your delegate ID.")
    
    # Search for delegate (first-time or forgot ID)
    st.subheader("🔍 Find Your Record")
    st.info("Search for your name to get your delegate ID for future logins.")
    
    search_method = st.radio("Search by:", ["Name", "Email"], horizontal=True)
    search_term = st.text_input(f"Enter your {search_method.lower()}:", placeholder="Type your name or email here...")
    
    # Add search button for mobile-friendly experience
    search_clicked = st.button("🔍 Search My Record", width='stretch', type="primary")
    
    # Process search when button is clicked OR when text is entered
    if (search_clicked or search_term) and search_term:
        df = load_staff_df()
        results = pd.DataFrame()
        speaker_results = []
        
        if search_method == "Name":
            # Search delegates by name
            mask = df["Name"].str.contains(search_term, case=False, na=False)
            results = df[mask]
            
            # Also search speakers
            try:
                import json
                with open("data/speakers.json", "r", encoding="utf-8") as f:
                    speakers = json.load(f)
                
                for speaker in speakers:
                    if speaker.get("name") and search_term.lower() in speaker.get("name", "").lower():
                        speaker_results.append(speaker)
            except:
                pass
        else:
            # Search by email (only delegates have emails)
            mask = df["Email"].str.contains(search_term, case=False, na=False)
            
        if len(results) == 0 and len(speaker_results) == 0:
            st.warning("No records found. Please check your spelling or contact the organizers.")
        
        elif len(speaker_results) == 1 and len(results) == 0:
            # Speaker found
            st.success("✅ Speaker record found!")
            speaker_record = speaker_results[0]
            
            # Show speaker information
            st.markdown("### 🎙️ Your Speaker Profile")
            
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**Name:** {speaker_record.get('name', '')}")
                st.info(f"**Position:** {speaker_record.get('position', 'Not specified')}")
                st.info(f"**Organization:** {speaker_record.get('organization', 'Not specified')}")
            
            with col2:
                st.info(f"**Presenting on:** {speaker_record.get('talk', 'TBA')}")
                st.info(f"**Category:** Speaker")
                if speaker_record.get('photo'):
                    st.image(speaker_record['photo'], width=150)
            
            # Authentication button for speakers
            if st.button("🚀 Continue to Dashboard", width='stretch', type="primary", key="speaker_auth"):
                # Set authentication and session data
                speaker_id = f"SPEAKER_{speaker_record.get('name', '').replace(' ', '_')}"
                st.session_state.delegate_authenticated = True
                st.session_state.delegate_id = speaker_id
                st.session_state.delegate_name = speaker_record.get('name', '')
                st.session_state.delegate_organization = speaker_record.get('organization', '')
                st.session_state.delegate_category = 'Speaker'
                st.session_state.delegate_title = speaker_record.get('position', '')
                st.session_state.delegate_nationality = ''
                st.session_state.delegate_phone = ''
                
                st.success(f"✅ Welcome, {speaker_record.get('name', '')}!")
                st.switch_page("pages/1_Delegate_Dashboard.py")
        
        elif len(results) == 1:
            st.success("✅ Record found!")
            delegate_record = results.iloc[0]
            
            # Show delegate information and their ID
            st.markdown("### 📋 Your Delegate Information")
            
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**Name:** {delegate_record['Name']}")
                st.info(f"**Category:** {delegate_record['Category']}")
                st.info(f"**Organization:** {delegate_record['Organization']}")
            
            with col2:
                st.info(f"**Title:** {delegate_record['RoleTitle']}")
                st.info(f"**Email:** {delegate_record['Email']}")
                st.info(f"**Nationality:** {delegate_record.get('Nationality', 'Not specified')}")
            
            # Show ID prominently
            st.markdown("---")
            st.markdown("### 🔑 Your Delegate ID")
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #198A00 0%, #2BA300 50%, #D10000 100%); color: white; padding: 2rem; border-radius: 15px; text-align: center; margin: 1rem 0;">
                <h2 style="color: white; margin-bottom: 0.5rem;">Your Delegate ID</h2>
                <h1 style="color: white; font-size: 3rem; margin: 0; font-weight: bold;">{delegate_record['ID']}</h1>
                <p style="color: #f0f8f0; margin-bottom: 0;">Use this ID for future logins</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Store ID for future quick login
            st.session_state.delegate_id_displayed = True
            st.session_state.delegate_id = str(delegate_record['ID'])
            
            # Authentication button
            if st.button("🚀 Continue to Dashboard", width='stretch', type="primary"):
                # Set authentication and session data
                st.session_state.delegate_authenticated = True
                st.session_state.delegate_name = delegate_record.get('Name', '')
                st.session_state.delegate_organization = delegate_record.get('Organization', '')
                st.session_state.delegate_category = delegate_record.get('Category', '')
                st.session_state.delegate_title = delegate_record.get('RoleTitle', '')
                
                st.success(f"✅ Welcome, {delegate_record.get('Name', '')}!")
                st.rerun()
            
        else:
            total_found = len(results) + len(speaker_results)
            st.warning(f"Multiple records found ({total_found}). Please be more specific with your search.")
            
            if len(results) > 0:
                st.markdown("#### Delegates:")
                st.dataframe(results[["ID", "Name", "Category", "Organization", "Email"]], width='stretch')
            
            if len(speaker_results) > 0:
                st.markdown("#### Speakers:")
                speaker_df = pd.DataFrame([
                    {
                        "Name": sp.get("name", ""),
                        "Position": sp.get("position", ""),
                        "Organization": sp.get("organization", ""),
                        "Presenting on": sp.get("talk", "")
                    } for sp in speaker_results
                ])
                st.dataframe(speaker_df, width='stretch')
    
    else:
        st.info("👆 Please enter your name or email to search for your record.")
    
    st.stop()

# If authenticated, show delegate information and networking
col_header, col_logout = st.columns([3, 1])
with col_header:
    st.subheader("👤 Your Delegate Information")
    st.success(f"✅ Authenticated as: **{st.session_state.delegate_name}** (ID: {st.session_state.delegate_id})")
# with col_logout:
#     if st.button("🚪 Logout", width='stretch'):
#         # Clear all session state
#         for key in list(st.session_state.keys()):
#             if key.startswith('delegate_'):
#                 del st.session_state[key]
        # st.rerun()

# Show current user's record
df = load_staff_df()
mask = df["ID"].astype(str) == str(st.session_state.delegate_id)
delegate_record = df[mask].iloc[0]

st.success("✅ Your record found!")

# QUICK THUMBS UP - DISAPPEAR AFTER ANIMATION
st.markdown("""
        <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 9998;">
            <div style="position: absolute; top: 20%; left: 20%; animation: quickthumbsup 2s ease-out forwards; font-size: 3rem;">👍</div>
            <div style="position: absolute; top: 30%; left: 40%; animation: quickthumbsup 2s ease-out 0.2s forwards; font-size: 2.5rem;">👍</div>
            <div style="position: absolute; top: 40%; left: 60%; animation: quickthumbsup 2s ease-out 0.4s forwards; font-size: 4rem;">👍</div>
            <div style="position: absolute; top: 50%; left: 80%; animation: quickthumbsup 2s ease-out 0.6s forwards; font-size: 3.5rem;">👍</div>
            <div style="position: absolute; top: 60%; left: 10%; animation: quickthumbsup 2s ease-out 0.8s forwards; font-size: 2.8rem;">👍</div>
        </div>
        
        <style>
        @keyframes quickthumbsup {
            0% { transform: translateY(100vh) scale(0.5); opacity: 0; }
            20% { opacity: 1; transform: scale(1.2); }
            60% { opacity: 1; transform: scale(1); }
            100% { transform: translateY(-100px) scale(0.3); opacity: 0; }
        }
        </style>
        """, unsafe_allow_html=True)
        
# Session state already set during authentication

# Display current information
st.subheader("📋 Your Current Information")

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    st.info(f"**Nationality:** {delegate_record.get('Nationality', 'Not specified')}")
    st.info(f"**Name:** {delegate_record['Name']}")
    st.info(f"**Category:** {delegate_record['Category']}")
    st.info(f"**Organization:** {delegate_record['Organization']}")

with col2:
    st.info(f"**Title:** {delegate_record['RoleTitle']}")
    st.info(f"**Email:** {delegate_record['Email']}")
    st.info(f"**Phone:** {delegate_record['Phone']}")
    st.info(f"**Check-in Status:** {'✅ Checked In' if delegate_record['CheckedIn'] else '❌ Not Checked In'}")

with col3:
    st.markdown("**Your Photo:**")
    if delegate_record.get('BadgePhoto'):
        try:
            st.image(delegate_record['BadgePhoto'], caption="Current Badge Photo", use_container_width=True)
        except:
            st.caption("📷 Photo on file")
    else:
        st.markdown("""
        <div style="background: #F3F4F6; border-radius: 10px; padding: 2rem; 
                   text-align: center; color: #666; min-height: 150px; 
                   display: flex; align-items: center; justify-content: center;">
            <span style="font-size: 3rem;">👤</span>
        </div>
        """, unsafe_allow_html=True)
        st.caption("No photo uploaded")

# Dashboard access option
st.markdown("---")
if st.button("🚀 Go to Conference Dashboard", width='stretch', type="primary"):
    st.switch_page("pages/1_Delegate_Dashboard.py")

# Edit form
st.subheader("✏️ Update Your Information")
st.caption("Fill in the fields you want to update. Leave blank to keep current values.")

with st.form("update_delegate", clear_on_submit=False):
    col1, col2 = st.columns(2)
    
    with col1:
        new_name = st.text_input("Full Name", value=delegate_record['Name'])
        new_category = st.selectbox(
            "Category", 
            options=["Organizing Committee", "Speaker", "VIP", "Media", "Service Provider", "Sponsor/Exhibitor Staff", "Government Official", "Other"],
            index=["Organizing Committee", "Speaker", "VIP", "Media", "Service Provider", "Sponsor/Exhibitor Staff", "Government Official", "Other"].index(delegate_record['Category']) if delegate_record['Category'] in ["Organizing Committee", "Speaker", "VIP", "Media", "Service Provider", "Sponsor/Exhibitor Staff", "Government Official", "Other"] else 6
        )
        new_organization = st.text_input("Organization", value=delegate_record['Organization'])
        new_title = st.text_input("Title/Role", value=delegate_record['RoleTitle'])
    
    with col2:
        new_email = st.text_input("Email", value=delegate_record['Email'])
        new_phone = st.text_input("Phone", value=delegate_record['Phone'])
        new_nationality = st.text_input("Nationality", value=delegate_record.get('Nationality', ''))
        new_notes = st.text_area("Notes", value=delegate_record['Notes'])
    
    # Photo upload section - separate and prominent
    st.markdown("---")
    st.markdown("### 📸 Badge Photo")
    
    col_photo1, col_photo2 = st.columns([1, 2])
    
    with col_photo1:
        if delegate_record.get('BadgePhoto'):
            try:
                st.image(delegate_record['BadgePhoto'], caption="Current Badge Photo", use_container_width=True)
            except:
                st.markdown("""
                <div style="background: #F3F4F6; border-radius: 10px; padding: 2rem; 
                           text-align: center; color: #666; min-height: 180px; 
                           display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 4rem;">👤</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #F3F4F6; border-radius: 10px; padding: 2rem; 
                       text-align: center; color: #666; min-height: 180px; 
                       display: flex; align-items: center; justify-content: center;">
                <span style="font-size: 4rem;">👤</span>
            </div>
            """, unsafe_allow_html=True)
            st.caption("No photo yet")
    
    with col_photo2:
        st.markdown("**Upload New Photo:**")
        st.caption("📷 Photo will appear on your conference badge and networking profile")
        st.caption("✅ Recommended: Professional headshot, clear background")
        st.caption("📐 Recommended size: 400x400px or larger")
        
        new_photo = st.file_uploader(
            "Choose photo file",
            type=["jpg","jpeg","png","webp"],
            key="delegate_photo",
            help="Upload a professional photo for your badge"
        )
        
        if new_photo:
            st.success("✅ New photo selected! Click 'Update My Information' below to save.")

    submitted = st.form_submit_button("💾 Update My Information", width='stretch')
    
    if submitted:
        # Validate required fields
        if not new_name.strip():
            st.error("Name is required.")
        elif not new_category.strip():
            st.error("Category is required.")
        else:
            # Update the record
            df = load_staff_df()
            mask = df["ID"].astype(str) == str(delegate_record['ID'])
            
            # Update fields
            df.loc[mask, "Name"] = new_name.strip()
            df.loc[mask, "Category"] = new_category.strip()
            df.loc[mask, "Organization"] = new_organization.strip()
            df.loc[mask, "RoleTitle"] = new_title.strip()
            df.loc[mask, "Email"] = new_email.strip()
            df.loc[mask, "Phone"] = new_phone.strip()
            df.loc[mask, "Nationality"] = new_nationality.strip()
            df.loc[mask, "Notes"] = new_notes.strip()
            
            # Handle photo upload
            if new_photo:
                from utils_assets import save_upload
                photo_path = save_upload(new_photo, kind="badges", name_hint=new_name)
                df.loc[mask, "BadgePhoto"] = photo_path
                st.success(f"Photo uploaded: {photo_path}")
            
            # Save changes
            save_staff_df(df)
            st.success("✅ Your information has been updated successfully!")
            
            # BIG FLOATING BALLOONS ONLY
            st.markdown("""
<div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 9999;">
    <div style="position: absolute; top: 20%; left: 10%; animation: float 180s ease-in-out infinite; font-size: 3rem;">🎈</div>
    <div style="position: absolute; top: 30%; left: 20%; animation: float 210s ease-in-out infinite 10s; font-size: 3.5rem;">🎈</div>
    <div style="position: absolute; top: 40%; left: 30%; animation: float 195s ease-in-out infinite 20s; font-size: 2.8rem;">🎈</div>
    <div style="position: absolute; top: 25%; left: 40%; animation: float 225s ease-in-out infinite 5s; font-size: 4rem;">🎈</div>
    <div style="position: absolute; top: 35%; left: 50%; animation: float 165s ease-in-out infinite 15s; font-size: 3.2rem;">🎈</div>
    <div style="position: absolute; top: 45%; left: 60%; animation: float 240s ease-in-out infinite 25s; font-size: 2.9rem;">🎈</div>
    <div style="position: absolute; top: 30%; left: 70%; animation: float 200s ease-in-out infinite 30s; font-size: 3.8rem;">🎈</div>
    <div style="position: absolute; top: 40%; left: 80%; animation: float 215s ease-in-out infinite 8s; font-size: 3rem;">🎈</div>
    <div style="position: absolute; top: 50%; left: 90%; animation: float 175s ease-in-out infinite 18s; font-size: 3.6rem;">🎈</div>
    <div style="position: absolute; top: 60%; left: 15%; animation: float 220s ease-in-out infinite 28s; font-size: 2.7rem;">🎈</div>
    <div style="position: absolute; top: 70%; left: 25%; animation: float 205s ease-in-out infinite 35s; font-size: 4.2rem;">🎈</div>
    <div style="position: absolute; top: 80%; left: 35%; animation: float 185s ease-in-out infinite 3s; font-size: 2.6rem;">🎈</div>
    <div style="position: absolute; top: 75%; left: 45%; animation: float 230s ease-in-out infinite 12s; font-size: 4.5rem;">🎈</div>
    <div style="position: absolute; top: 65%; left: 55%; animation: float 160s ease-in-out infinite 28s; font-size: 2.8rem;">🎈</div>
    <div style="position: absolute; top: 55%; left: 65%; animation: float 245s ease-in-out infinite 7s; font-size: 3.4rem;">🎈</div>
    <div style="position: absolute; top: 85%; left: 75%; animation: float 250s ease-in-out infinite 22s; font-size: 2.9rem;">🎈</div>
    <div style="position: absolute; top: 90%; left: 85%; animation: float 155s ease-in-out infinite 32s; font-size: 4.8rem;">🎈</div>
</div>

<style>
@keyframes float {
    0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
    2% { opacity: 1; }
    98% { opacity: 1; }
    100% { transform: translateY(-100px) rotate(360deg); opacity: 0; }
}
</style>
""", unsafe_allow_html=True)
            st.session_state.show_dashboard_button = True
            
            # Refresh the page to show updated info
            st.rerun()

# Show dashboard button if update was successful
if hasattr(st.session_state, 'show_dashboard_button') and st.session_state.show_dashboard_button:
    st.markdown("---")
    if st.button("🚀 Go to Conference Dashboard", width='stretch', type="primary", key="dashboard_btn_after_update"):
        st.switch_page("pages/1_Delegate_Dashboard.py")

else:
    st.info("👆 Please enter your name or email to search for your record.")

# Footer with logout button (if authenticated)
st.markdown("---")
col_footer1, col_footer2, col_footer3 = st.columns([2, 1, 2])
with col_footer1:
    st.caption("Need help? Contact the conference organizers or visit the registration desk.")
with col_footer2:
    if hasattr(st.session_state, 'delegate_authenticated') and st.session_state.delegate_authenticated:
        if st.button("🚪 Logout", width='stretch', key="self_service_logout"):
            # Clear all session state
            for key in list(st.session_state.keys()):
                if key.startswith('delegate_'):
                    del st.session_state[key]
            st.success("✅ Logged out successfully!")
            st.switch_page("pages/0_Landing.py")