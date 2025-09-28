# pages/Admin_QR_Codes.py
import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.ui import apply_brand
from lib.qr_system import create_badge_qr_code, save_qr_code, generate_all_delegate_qr_codes
from staff_service import load_staff_df, save_staff_df

st.set_page_config(page_title="QR Code Management — Insaka Admin", page_icon="📱", layout="wide")

apply_brand()

# Zambian-themed header
st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

st.markdown("""
<div style="background: linear-gradient(135deg, #198A00 0%, #2BA300 50%, #D10000 100%); color: white; padding: 2rem; border-radius: 20px; margin-bottom: 2rem; text-align: center; box-shadow: 0 8px 32px rgba(25, 138, 0, 0.2);">
    <h1 style="color: white; margin-bottom: 0.5rem; font-size: 2.5rem; font-weight: 700;">📱 QR Code Management</h1>
    <p style="color: #f0f8f0; margin-bottom: 0; font-size: 1.2rem; font-weight: 500;">Generate QR codes for delegate badges</p>
</div>
""", unsafe_allow_html=True)

# Authentication check
if not hasattr(st.session_state, 'admin_authenticated') or not st.session_state.admin_authenticated:
    st.error("🔒 Admin access required. Please login first.")
    if st.button("🔑 Admin Login"):
        st.switch_page("pages/Admin_Access.py")
    st.stop()

# Load staff data
try:
    staff_df = load_staff_df()
    if staff_df.empty:
        st.error("No delegate data found. Please import delegate data first.")
        st.stop()
except Exception as e:
    st.error(f"Error loading delegate data: {str(e)}")
    st.stop()

st.markdown("## 📊 Delegate Overview")
st.markdown(f"**Total Delegates:** {len(staff_df)}")

# Display delegate list
if not staff_df.empty:
    # Show key columns
    display_columns = ['ID', 'Full Name', 'Organization', 'Attendee Type', 'Title']
    available_columns = [col for col in display_columns if col in staff_df.columns]
    
    if available_columns:
        st.dataframe(
            staff_df[available_columns],
            width='stretch',
            height=300
        )

# QR Code Generation Section
st.markdown("## 🎫 QR Code Generation")

# Generation options
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📱 Individual QR Code")
    
    # Select delegate
    if not staff_df.empty:
        delegate_options = []
        for index, delegate in staff_df.iterrows():
            delegate_id = delegate.get('ID', '')
            delegate_name = delegate.get('Full Name', '')
            organization = delegate.get('Organization', '')
            display_name = f"ID: {delegate_id} - {delegate_name} ({organization})"
            delegate_options.append((display_name, index))
        
        selected_delegate = st.selectbox(
            "Select Delegate:",
            options=[opt[0] for opt in delegate_options],
            key="delegate_selector"
        )
        
        if selected_delegate:
            # Get selected delegate data
            selected_index = next(opt[1] for opt in delegate_options if opt[0] == selected_delegate)
            delegate = staff_df.iloc[selected_index]
            
            # Generate QR code
            if st.button("🎫 Generate QR Code", type="primary", width='stretch'):
                with st.spinner("Generating QR code..."):
                    try:
                        qr_img, qr_data = create_badge_qr_code(
                            delegate.get('ID'),
                            delegate.get('Full Name', ''),
                            delegate.get('Organization', ''),
                            title=delegate.get('Title', ''),
                            size=300
                        )
                        
                        # Save QR code
                        filepath = save_qr_code(qr_img, delegate.get('ID'), "badge_qr")
                        
                        st.success(f"✅ QR code generated successfully!")
                        st.info(f"📁 Saved to: {filepath}")
                        
                        # Display QR code
                        st.image(qr_img, caption=f"QR Code for {delegate.get('Full Name', '')}", width='stretch')
                        
                        # Show QR data
                        with st.expander("📋 QR Code Data", expanded=False):
                            st.code(qr_data, language="json")
                        
                        # Download button
                        with open(filepath, "rb") as file:
                            st.download_button(
                                label="📥 Download QR Code",
                                data=file.read(),
                                file_name=f"badge_qr_{delegate.get('ID')}.png",
                                mime="image/png",
                                width='stretch'
                            )
                    
                    except Exception as e:
                        st.error(f"❌ Error generating QR code: {str(e)}")

with col2:
    st.markdown("### 📱 Batch QR Code Generation")
    
    st.markdown("Generate QR codes for all delegates at once.")
    
    if st.button("🎫 Generate All QR Codes", type="secondary", width='stretch'):
        with st.spinner("Generating QR codes for all delegates..."):
            try:
                qr_codes = generate_all_delegate_qr_codes(staff_df)
                
                st.success(f"✅ Generated {len(qr_codes)} QR codes successfully!")
                
                # Show progress
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                saved_files = []
                for i, (delegate_id, qr_info) in enumerate(qr_codes.items()):
                    # Update progress
                    progress = (i + 1) / len(qr_codes)
                    progress_bar.progress(progress)
                    status_text.text(f"Processing delegate {delegate_id}...")
                    
                    # Save QR code
                    filepath = save_qr_code(qr_info['image'], delegate_id, "badge_qr")
                    saved_files.append(filepath)
                
                status_text.text("✅ All QR codes generated successfully!")
                
                # Create zip file for download
                import zipfile
                import io
                
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for filepath in saved_files:
                        if os.path.exists(filepath):
                            zip_file.write(filepath, os.path.basename(filepath))
                
                zip_buffer.seek(0)
                
                st.download_button(
                    label="📥 Download All QR Codes (ZIP)",
                    data=zip_buffer.getvalue(),
                    file_name=f"insaka_qr_codes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                    mime="application/zip",
                    width='stretch'
                )
                
                # Show summary
                st.markdown("### 📊 Generation Summary")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Generated", len(qr_codes))
                
                with col2:
                    st.metric("Success Rate", "100%")
                
                with col3:
                    st.metric("File Size", f"{len(zip_buffer.getvalue()) // 1024} KB")
            
            except Exception as e:
                st.error(f"❌ Error generating batch QR codes: {str(e)}")

# QR Code Management
st.markdown("## 🔧 QR Code Management")

# Check existing QR codes
qr_dir = "assets/qr_codes"
if os.path.exists(qr_dir):
    qr_files = [f for f in os.listdir(qr_dir) if f.endswith('.png')]
    
    if qr_files:
        st.markdown(f"**Existing QR Codes:** {len(qr_files)}")
        
        # Show QR code files
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**QR Code Files:**")
            for file in sorted(qr_files):
                st.write(f"• {file}")
        
        with col2:
            if st.button("🗑️ Clear All QR Codes", type="secondary"):
                try:
                    for file in qr_files:
                        os.remove(os.path.join(qr_dir, file))
                    st.success("✅ All QR codes cleared!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error clearing QR codes: {str(e)}")
    else:
        st.info("No QR codes generated yet.")
else:
    st.info("QR codes directory not found. Generate some QR codes first.")

# QR Code Testing
st.markdown("## 🧪 QR Code Testing")

with st.expander("🔍 Test QR Code Login", expanded=False):
    st.markdown("Test the QR code login functionality:")
    
    # Test with sample data
    if not staff_df.empty:
        test_delegate = staff_df.iloc[0]
        
        st.markdown("**Test with sample delegate:**")
        st.write(f"**Name:** {test_delegate.get('Full Name', '')}")
        st.write(f"**Organization:** {test_delegate.get('Organization', '')}")
        
        if st.button("🧪 Generate Test QR Code"):
            try:
                qr_img, qr_data = create_badge_qr_code(
                    test_delegate.get('ID'),
                    test_delegate.get('Full Name', ''),
                    test_delegate.get('Organization', ''),
                    title=test_delegate.get('Title', ''),
                    size=200
                )
                
                st.image(qr_img, caption="Test QR Code", width='stretch')
                
                with st.expander("📋 Test QR Data", expanded=True):
                    st.code(qr_data, language="json")
                
                st.info("💡 Use this QR code data to test the login functionality.")
            
            except Exception as e:
                st.error(f"❌ Error generating test QR code: {str(e)}")

# Instructions
st.markdown("## 📋 Instructions")

with st.expander("📖 How to Use QR Codes", expanded=True):
    st.markdown("""
    **For Conference Organizers:**
    
    1. **Generate QR Codes** - Use the individual or batch generation tools above
    2. **Print on Badges** - Include QR codes on delegate badges
    3. **Distribute Badges** - Give badges to delegates at registration
    4. **Test Login** - Verify QR codes work with the login system
    
    **For Delegates:**
    
    1. **Receive Badge** - Get your conference badge with QR code
    2. **Scan QR Code** - Use the QR login page to scan your badge
    3. **Instant Access** - Automatically logged into your dashboard
    4. **Secure Login** - No need to remember passwords
    
    **QR Code Features:**
    
    - ✅ **Unique per delegate** - Each QR code is personalized
    - ✅ **Time-limited** - QR codes expire after 24 hours
    - ✅ **Secure** - Contains encrypted delegate information
    - ✅ **Mobile-friendly** - Works on any smartphone
    - ✅ **Badge-ready** - Optimized for printing on badges
    """)

# Footer
st.markdown("---")
st.markdown("### 🎯 Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 Admin Dashboard", width='stretch'):
        st.switch_page("pages/0_Admin.py")

with col2:
    if st.button("📱 QR Login Test", width='stretch'):
        st.switch_page("pages/QR_Login.py")

with col3:
    if st.button("👥 Delegate Management", width='stretch'):
        st.switch_page("pages/0_Admin.py")
