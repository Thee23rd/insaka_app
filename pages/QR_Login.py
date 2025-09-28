# pages/QR_Login.py
import streamlit as st
import json
import sys
import os
import urllib.parse
import streamlit.components.v1 as components


# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.ui import apply_brand
from lib.qr_system import authenticate_with_qr_code, create_qr_scanner_script, _normalize_qr_payload
from staff_service import load_staff_df
from lib.translations import get_translation, get_text_direction, is_rtl_language

def _set_session_and_go(delegate):
    """Set session state and redirect to delegate dashboard"""
    # Set session state for authenticated delegate
    st.session_state.delegate_authenticated = True
    st.session_state.delegate_id = delegate.get('ID')
    st.session_state.delegate_name = delegate.get('Full Name', '')
    st.session_state.delegate_organization = delegate.get('Organization', '')
    st.session_state.delegate_category = delegate.get('Attendee Type', '')
    st.session_state.delegate_title = delegate.get('Title', '')
    st.session_state.delegate_nationality = delegate.get('Nationality', '')
    st.session_state.delegate_phone = delegate.get('Phone', '')
    
    st.balloons()
    
    # Show delegate info
    st.markdown("### 🎉 Login Successful!")
    st.markdown(f"**Welcome, {delegate.get('Full Name', '')}!**")
    st.markdown(f"**Organization:** {delegate.get('Organization', '')}")
    st.markdown(f"**Category:** {delegate.get('Attendee Type', '')}")
    
    st.markdown("🔄 Redirecting to your dashboard...")
    
    # Redirect to dashboard
    st.switch_page("pages/1_Delegate_Dashboard.py")
    st.stop()

st.set_page_config(page_title="QR Code Login — Insaka", page_icon="📱", layout="wide")

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

# Zambian-themed header
st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

# Get current language
current_language = st.session_state.get('language', 'en-us')

# RTL support
text_direction = get_text_direction(current_language)
rtl_style = "direction: rtl; text-align: right;" if is_rtl_language(current_language) else "direction: ltr; text-align: center;"

st.markdown(f"""
<div style="background: linear-gradient(135deg, #198A00 0%, #2BA300 50%, #D10000 100%); color: white; padding: 2rem; border-radius: 20px; margin-bottom: 2rem; {rtl_style} box-shadow: 0 8px 32px rgba(25, 138, 0, 0.2);">
    <h1 style="color: white; margin-bottom: 0.5rem; font-size: 2.5rem; font-weight: 700;">📱 {get_translation('qr_login', current_language)}</h1>
    <p style="color: #f0f8f0; margin-bottom: 0; font-size: 1.2rem; font-weight: 500;">{get_translation('qr_login_subtitle', current_language)}</p>
</div>
""", unsafe_allow_html=True)

# Load staff data
try:
    staff_df = load_staff_df()
    if staff_df.empty:
        st.error("No delegate data found. Please contact administrator.")
        st.stop()
except Exception as e:
    st.error(f"Error loading delegate data: {str(e)}")
    st.stop()

# QR Code Login Section
st.markdown("## 📱 QR Code Login")

# Method selection
login_method = st.radio(
    "Choose login method:",
    ["📱 Scan QR Code", "📝 Enter QR Code Data"],
    horizontal=True
)

if login_method == "📱 Scan QR Code":
    st.markdown("### 📷 Camera Scanner")
    st.markdown("Use your device camera to scan the QR code from your conference badge.")
    
     # QR scanner via components.html that RETURNS the QR payload
    scanner_html = """
     <div id="qr-scanner-container" style="max-width: 720px; margin: 0 auto;">
       <video id="qr-video" style="width: 100%; height: 300px; border: 3px solid #198A00; border-radius: 15px; display: none;" playsinline></video>
       <canvas id="qr-canvas" style="display: none;"></canvas>
       <div id="qr-status" style="text-align: center; padding: 10px; background: #f0f8f0; border-radius: 10px; margin: 10px 0; font-weight: bold; color: #198A00;">
         📷 Camera scanner ready — click start to begin
       </div>
       <div style="text-align:center;">
         <button id="start-btn" style="background:#198A00;color:white;border:none;padding:12px 24px;border-radius:25px;cursor:pointer;font-weight:bold;margin:5px;">
           📷 Start Camera
         </button>
         <button id="stop-btn" style="background:#D10000;color:white;border:none;padding:12px 24px;border-radius:25px;cursor:pointer;font-weight:bold;margin:5px;display:none;">
           🛑 Stop Camera
         </button>
       </div>
     </div>

     <script src="https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.js"></script>
     <script>
     (function () {
       let stream = null;
       let scanning = false;
       let rafId = null;

       const video = document.getElementById('qr-video');
       const canvas = document.getElementById('qr-canvas');
       const ctx = canvas.getContext('2d', { willReadFrequently: true });
       const statusEl = document.getElementById('qr-status');
       const startBtn = document.getElementById('start-btn');
       const stopBtn = document.getElementById('stop-btn');

       async function startCamera() {
         try {
           statusEl.textContent = '📷 Requesting camera access...';
           const constraints = {
             video: { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } },
             audio: false
           };
           stream = await navigator.mediaDevices.getUserMedia(constraints);
           video.srcObject = stream;
           video.style.display = 'block';
           startBtn.style.display = 'none';
           stopBtn.style.display = 'inline-block';
           await video.play();
           scanning = true;
           statusEl.textContent = '📷 Camera active! Point at QR code';
           scanLoop();
         } catch (e) {
           console.error('Camera error:', e);
           statusEl.textContent = '❌ Camera access denied. Please allow camera permissions.';
         }
       }

       function stopCamera() {
         scanning = false;
         if (rafId) cancelAnimationFrame(rafId);
         if (stream) { stream.getTracks().forEach(t => t.stop()); stream = null; }
         video.pause(); video.removeAttribute('src'); video.load();
         video.style.display = 'none';
         startBtn.style.display = 'inline-block';
         stopBtn.style.display = 'none';
         statusEl.textContent = '📷 Camera stopped';
       }

       function scanLoop() {
         if (!scanning) return;
         if (video.readyState === video.HAVE_ENOUGH_DATA) {
           canvas.width = video.videoWidth;
           canvas.height = video.videoHeight;
           ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
           const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
           const code = jsQR(imageData.data, imageData.width, imageData.height);

           if (code && code.data) {
             scanning = false;
             statusEl.textContent = '✅ QR Code detected! Processing...';
             try {
               // Clean string a bit
               let cleanData = (code.data || '').trim().replace(/^\uFEFF/, '').replace(/[\\u200B-\\u200D\\uFEFF]/g, '');
               // Return QR payload to Python via Streamlit components API
               if (window.Streamlit && typeof window.Streamlit.setComponentValue === 'function') {
                 window.Streamlit.setComponentValue(cleanData);
               } else {
                 // Fallback: show payload visibly
                 statusEl.textContent = '✅ Detected (but cannot return to Streamlit).';
                 console.log('QR payload:', cleanData);
               }
             } catch (err) {
               console.error('QR processing error:', err);
               statusEl.textContent = '❌ Invalid QR code data';
             }
             return;
           } else {
             statusEl.textContent = '📷 Scanning... Point camera at QR code';
           }
         }
         rafId = requestAnimationFrame(scanLoop);
       }

       startBtn.addEventListener('click', startCamera);
       stopBtn.addEventListener('click', stopCamera);
       window.addEventListener('beforeunload', stopCamera);
     })();
     </script>
     """
        
    
     # Render the component and CAPTURE its return value (the scanned QR payload)
    try:
         qr_scanned_value = components.html(scanner_html, height=520)
    except Exception as e:
         st.error(f"Component error: {str(e)}")
         st.markdown("**Fallback:** Camera scanner unavailable. Please use manual entry below.")
         qr_scanned_value = None
         
         # Show fallback camera option
         st.markdown("### 📷 Alternative Camera Method")
         st.markdown("If the camera scanner above doesn't work, you can still scan QR codes manually:")
         
         # Simple file upload for QR code images
         uploaded_file = st.file_uploader("Upload QR Code Image", type=['png', 'jpg', 'jpeg'])
         if uploaded_file is not None:
             st.success("QR code image uploaded! Please use manual entry method below to enter the QR data.")
     
     # Debug: Show what we received from the component  
    st.markdown(f"**Debug - Component returned:** `{qr_scanned_value}`")
     
     # If the component returned a QR payload, process it (no URL tricks needed)
    if qr_scanned_value:
         qr_text = qr_scanned_value  # raw string from the QR
         st.success(f"🎉 QR Code detected! Processing: `{qr_text}`")

         # Normalize / parse (your helper)
         norm_text, payload = _normalize_qr_payload(qr_text)

         with st.spinner("Authenticating..."):
             success, message, delegate = authenticate_with_qr_code(norm_text, staff_df)

             # Fallback: direct lookup by ID
             if not success and isinstance(payload, dict) and payload.get("delegate_id"):
                 norm_id = str(payload["delegate_id"])
                 try:
                     match_df = staff_df[staff_df["ID"].astype(str) == norm_id]
                     if not match_df.empty:
                         row = match_df.iloc[0].to_dict()
                         delegate = {
                             'ID': row.get('ID'),
                             'Full Name': row.get('Full Name') or row.get('Name') or '',
                             'Organization': row.get('Organization') or row.get('Company') or '',
                             'Attendee Type': row.get('Attendee Type') or row.get('Category') or '',
                             'Title': row.get('Title') or '',
                             'Nationality': row.get('Nationality') or '',
                             'Phone': row.get('Phone') or row.get('Contact') or '',
                         }
                         success, message = True, "Authenticated by ID lookup"
                 except Exception as e:
                     st.info(f"Debug: ID lookup failed ({e})")

             if success:
                 st.success(f"✅ {message}")
                 _set_session_and_go(delegate)  # this calls st.switch_page(...) and st.stop()
             else:
                 st.error(f"❌ {message}")
    else:
         st.info("📷 No QR data received from scanner yet. Try scanning a QR code.")
    
    # Manual test with the detected QR data
    st.markdown("---")
    st.markdown("### 🧪 Manual Test (Use the QR data from console)")
    
    test_qr_data = st.text_area(
        "QR Data from Console:",
        value='{"type": "delegate_login", "delegate_id": "6", "delegate_name": "Annie Mwape", "organization": "MMMD", "timestamp": "2025-09-28T21:48:48.116331", "conference": "Insaka Conference 2025"}',
        height=100
    )
    
    if st.button("🔍 Test with This QR Data", width='stretch'):
        if test_qr_data:
            st.success(f"🎉 Testing with QR data: `{test_qr_data}`")
            
            # Normalize / parse (your helper)
            norm_text, payload = _normalize_qr_payload(test_qr_data)

            with st.spinner("Authenticating..."):
                success, message, delegate = authenticate_with_qr_code(norm_text, staff_df)

                # Fallback: direct lookup by ID
                if not success and isinstance(payload, dict) and payload.get("delegate_id"):
                    norm_id = str(payload["delegate_id"])
                    try:
                        match_df = staff_df[staff_df["ID"].astype(str) == norm_id]
                        if not match_df.empty:
                            row = match_df.iloc[0].to_dict()
                            delegate = {
                                'ID': row.get('ID'),
                                'Full Name': row.get('Full Name') or row.get('Name') or '',
                                'Organization': row.get('Organization') or row.get('Company') or '',
                                'Attendee Type': row.get('Attendee Type') or row.get('Category') or '',
                                'Title': row.get('Title') or '',
                                'Nationality': row.get('Nationality') or '',
                                'Phone': row.get('Phone') or row.get('Contact') or '',
                            }
                            success, message = True, "Authenticated by ID lookup"
                    except Exception as e:
                        st.info(f"Debug: ID lookup failed ({e})")

                if success:
                    st.success(f"✅ {message}")
                    _set_session_and_go(delegate)  # this calls st.switch_page(...) and st.stop()
                else:
                    st.error(f"❌ {message}")
    
    # Manual redirect button as backup
    st.markdown("---")
    st.markdown("### 🔄 If QR scanning doesn't redirect automatically:")
    
    col_manual1, col_manual2 = st.columns(2)
    
    with col_manual1:
        if st.button("🚀 Go to Delegate Dashboard", width='stretch'):
            st.switch_page("pages/1_Delegate_Dashboard.py")
    
    with col_manual2:
        if st.button("🔍 Go to Self-Service", width='stretch'):
            st.switch_page("pages/7_Delegate_Self_Service.py")
    
    col1, col2 = st.columns([1, 1])
    
    with col2:
        st.markdown("**Instructions:**")
        st.markdown("""
        1. Click "Start Camera" button above
        2. Allow camera access when prompted
        3. Point camera at QR code on badge
        4. Wait for automatic detection
        """)
        
    
    # --- Handle QR code data from scanner (robust) ---
    def _normalize_qr_payload(qr_text: str):
        # 1) URL-decode and strip common wrappers
        try:
            qr_text = urllib.parse.unquote_plus(qr_text or "")
        except Exception:
            pass
        qr_text = qr_text.strip()
        # Remove accidental leading/trailing quotes
        if (qr_text.startswith('"') and qr_text.endswith('"')) or (qr_text.startswith("'") and qr_text.endswith("'")):
            qr_text = qr_text[1:-1].strip()

        # 2) Try parse JSON
        payload = {}
        try:
            payload = json.loads(qr_text)
        except Exception:
            # allow non-JSON simple IDs (e.g., "6")
            if qr_text.isdigit():
                payload = {"type": "delegate_login", "delegate_id": qr_text}

        # 3) Normalize keys and types
        if isinstance(payload, dict):
            delegate_id = payload.get("delegate_id") or payload.get("ID") or payload.get("id")
            if delegate_id is not None:
                # cast to string for comparison
                payload["delegate_id"] = str(delegate_id).strip()
            payload["type"] = payload.get("type") or "delegate_login"
        return qr_text, payload

    def _set_session_and_go(delegate: dict):
        st.session_state.delegate_authenticated = True
        st.session_state.delegate_id = delegate.get('ID')
        st.session_state.delegate_name = delegate.get('Full Name', '')
        st.session_state.delegate_organization = delegate.get('Organization', '')
        st.session_state.delegate_category = delegate.get('Attendee Type', '')
        st.session_state.delegate_title = delegate.get('Title', '')
        st.session_state.delegate_nationality = delegate.get('Nationality', '')
        st.session_state.delegate_phone = delegate.get('Phone', '')

        # Clear param so refresh doesn't re-trigger
        try:
            st.query_params.clear()
        except Exception:
            pass

        # Navigate (try both)
        try:
            st.switch_page("pages/1_Delegate_Dashboard.py")
        except Exception:
            try:
                st.switch_page("1_Delegate_Dashboard.py")
            except Exception:
                st.markdown("""
                    <script>
                    window.top.location.href = window.top.location.href.split('?')[0]
                      + '?page=1_Delegate_Dashboard.py';
                    </script>
                """, unsafe_allow_html=True)
        st.stop()

    if 'qr_data' in st.query_params:
        raw = st.query_params['qr_data']
        qr_data_input = raw[0] if isinstance(raw, list) else raw

        st.success("🎉 QR Code detected! Processing...")
        st.markdown(f"**Raw QR Data:** `{qr_data_input}`")

        # Normalize / parse
        qr_text, payload = _normalize_qr_payload(qr_data_input)
        
        st.markdown(f"**Normalized QR Data:** `{qr_text}`")
        st.json(payload)

        with st.spinner("Authenticating..."):
            # 1) Try your existing validator first (pass original text)
            success, message, delegate = authenticate_with_qr_code(qr_text, staff_df)

            # 2) If that fails, fall back to a direct lookup by normalized ID
            if not success and isinstance(payload, dict) and payload.get("type") == "delegate_login" and payload.get("delegate_id"):
                norm_id = payload["delegate_id"]
                # accept either numeric or string id; compare as strings
                try:
                    # Convert staff_df ID to str for comparison
                    match_df = staff_df[staff_df["ID"].astype(str) == str(norm_id)]
                    if not match_df.empty:
                        row = match_df.iloc[0].to_dict()
                        delegate = {
                            'ID': row.get('ID'),
                            'Full Name': row.get('Full Name') or row.get('Name') or row.get('Full_Name') or '',
                            'Organization': row.get('Organization') or row.get('Company') or '',
                            'Attendee Type': row.get('Attendee Type') or row.get('Category') or '',
                            'Title': row.get('Title') or '',
                            'Nationality': row.get('Nationality') or '',
                            'Phone': row.get('Phone') or row.get('Contact') or '',
                        }
                        success, message = True, "Authenticated by ID lookup"
                except Exception as e:
                    st.info(f"Debug: ID lookup failed ({e})")

            if success:
                st.success(f"✅ {message}")
                
                # Show delegate info before redirect
                st.markdown("### 🎉 Login Successful!")
                st.markdown(f"**Welcome, {delegate.get('Full Name', 'Unknown')}!**")
                st.markdown(f"**Organization:** {delegate.get('Organization', 'Unknown')}")
                st.markdown(f"**Category:** {delegate.get('Attendee Type', 'Unknown')}")
                st.markdown(f"**Delegate ID:** {delegate.get('ID', 'Unknown')}")
                
                st.markdown("🔄 Redirecting to your dashboard...")
                st.markdown("If redirect doesn't work, use the manual redirect buttons below.")
                
                # Try redirect with delay
                import time
                time.sleep(2)
                _set_session_and_go(delegate)
            else:
                st.error(f"❌ {message}")
                st.markdown("Please try scanning the QR code again.")

else:
    st.markdown("### 📝 Manual QR Code Entry")
    st.markdown("If you have the QR code data, enter it below:")
    
    # Manual QR code data entry
    qr_data_input = st.text_area(
        "QR Code Data:",
        placeholder="Paste the QR code data here...",
        height=100
    )
    
    if st.button("🔐 Login with QR Code", type="primary", width='stretch'):
        if qr_data_input.strip():
            with st.spinner("Authenticating..."):
                success, message, delegate = authenticate_with_qr_code(qr_data_input.strip(), staff_df)
                
                if success:
                    st.success(f"✅ {message}")
                    
                    # Set session state for authenticated delegate
                    st.session_state.delegate_authenticated = True
                    st.session_state.delegate_id = delegate.get('ID')
                    st.session_state.delegate_name = delegate.get('Full Name', '')
                    st.session_state.delegate_organization = delegate.get('Organization', '')
                    st.session_state.delegate_category = delegate.get('Attendee Type', '')
                    st.session_state.delegate_title = delegate.get('Title', '')
                    st.session_state.delegate_nationality = delegate.get('Nationality', '')
                    st.session_state.delegate_phone = delegate.get('Phone', '')
                    
                    st.balloons()
                    
                    # Auto-redirect to dashboard
                    st.markdown("### 🎉 Login Successful!")
                    st.markdown(f"**Welcome, {delegate.get('Full Name', '')}!**")
                    st.markdown(f"**Organization:** {delegate.get('Organization', '')}")
                    st.markdown(f"**Category:** {delegate.get('Attendee Type', '')}")
                    
                    st.markdown("🔄 Redirecting to your dashboard...")
                    
                    # Immediate redirect
                    st.switch_page("pages/1_Delegate_Dashboard.py")
                else:
                    st.error(f"❌ {message}")
        else:
            st.warning("Please enter QR code data")

# QR Code Information
st.markdown("## ℹ️ About QR Code Login")

with st.expander("📋 How QR Code Login Works", expanded=True):
    st.markdown("""
    **QR Code Login Benefits:**
    - 🚀 **Fast & Easy** - No need to remember passwords
    - 🔒 **Secure** - Each QR code is unique and time-limited
    - 📱 **Mobile-Friendly** - Works on any smartphone
    - 🎫 **Badge Integration** - QR code printed on your conference badge
    
    **How It Works:**
    1. **QR Code Generation** - Each delegate gets a unique QR code
    2. **Badge Printing** - QR code is printed on your conference badge
    3. **Quick Login** - Scan QR code to instantly access your dashboard
    4. **Secure Access** - QR codes expire after 24 hours for security
    """)

with st.expander("🔧 Troubleshooting", expanded=False):
    st.markdown("""
    **Common Issues:**
    
    **❌ "QR code has expired"**
    - QR codes are valid for 24 hours
    - Contact admin for a new QR code
    
    **❌ "Delegate not found"**
    - Verify you're using the correct QR code
    - Check if delegate data is properly loaded
    
    **❌ "Camera access denied"**
    - Allow camera permissions in browser
    - Try refreshing the page
    
    **❌ "Invalid QR code data"**
    - Ensure QR code is not damaged
    - Try manual entry method
    """)

# Alternative login methods
st.markdown("## 🔄 Alternative Login Methods")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔍 Search by Name")
    if st.button("Search for Your Name", width='stretch'):
        st.switch_page("pages/7_Delegate_Self_Service.py")

with col2:
    st.markdown("### 🔑 Quick Login")
    if st.button("Enter Delegate ID", width='stretch'):
        st.switch_page("pages/0_Landing.py")

# Footer
st.markdown("---")
st.markdown("### 🎯 Need Help?")
st.markdown("""
- **QR Code Issues:** Contact registration desk
- **Technical Support:** Ask conference staff
- **Alternative Login:** Use name search or delegate ID
""")

if st.button("🏠 Back to Landing Page", width='stretch'):
    st.switch_page("pages/0_Landing.py")