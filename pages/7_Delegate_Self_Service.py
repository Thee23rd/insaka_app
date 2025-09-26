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

st.title("👤 Delegate Self-Service")
st.markdown("Check and update your conference details")

# Search for delegate
st.subheader("🔍 Find Your Record")
search_method = st.radio("Search by:", ["Name", "Email"], horizontal=True)

search_term = st.text_input(f"Enter your {search_method.lower()}:", placeholder="Type your name or email here...")

if search_term:
    df = load_staff_df()
    
    if search_method == "Name":
        # Search by name (case insensitive, partial match)
        mask = df["Name"].str.contains(search_term, case=False, na=False)
    else:
        # Search by email (case insensitive, partial match)
        mask = df["Email"].str.contains(search_term, case=False, na=False)
    
    results = df[mask]
    
    if len(results) == 0:
        st.warning("No records found. Please check your spelling or contact the organizers.")
    elif len(results) == 1:
        st.success("✅ Record found!")
        delegate_record = results.iloc[0]
        
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
        
        # Store delegate info in session state for personalized greeting
        st.session_state.delegate_name = delegate_record['Name']
        st.session_state.delegate_organization = delegate_record['Organization']
        st.session_state.delegate_category = delegate_record['Category']
        st.session_state.delegate_title = delegate_record.get('RoleTitle', '')
        st.session_state.delegate_id = delegate_record['ID']
        
        # Display current information
        st.subheader("📋 Your Current Information")
        
        col1, col2 = st.columns(2)
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
        
        # Dashboard access option
        st.markdown("---")
        if st.button("🚀 Go to Conference Dashboard", use_container_width=True, type="primary"):
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
                
                # Photo upload
                st.write("**Badge Photo**")
                if delegate_record['BadgePhoto']:
                    st.caption(f"Current photo: {delegate_record['BadgePhoto']}")
                new_photo = st.file_uploader("Upload new photo (JPG/PNG/WebP)", type=["jpg","jpeg","png","webp"], key="delegate_photo")
            
            submitted = st.form_submit_button("💾 Update My Information", use_container_width=True)
            
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
            if st.button("🚀 Go to Conference Dashboard", use_container_width=True, type="primary", key="dashboard_btn_after_update"):
                st.switch_page("pages/1_Delegate_Dashboard.py")
    
    else:
        st.warning(f"Multiple records found ({len(results)}). Please be more specific with your search.")
        st.dataframe(results[["ID", "Name", "Category", "Organization", "Email"]], use_container_width=True)

else:
    st.info("👆 Please enter your name or email to search for your record.")

# Footer
st.markdown("---")
st.caption("Need help? Contact the conference organizers or visit the registration desk.")
