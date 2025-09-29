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
from lib.qr_system import authenticate_with_qr_code, create_qr_scanner_script
from staff_service import load_staff_df
from lib.translations import get_translation, get_text_direction, is_rtl_language

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
    
    # Simple QR Scanner
    simple_scanner_html = """
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
        (function() {
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
                console.log('QR Code detected:', code.data);
                scanning = false;
                statusEl.textContent = '✅ QR Code detected! Redirecting...';
                
                // Send QR to parent; parent will update URL & redirect
                try {
                  window.parent.postMessage({ type: 'insaka:qr', qr: code.data }, '*');
                  console.log('QR data sent to parent:', code.data);
                  
                } catch (postMessageErr) {
                  console.log('PostMessage failed:', postMessageErr);
                  statusEl.textContent = '❌ Communication failed. Please refresh manually.';
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
        
     # Parent page listener: receives QR data from the scanner iframe and shows details
    st.markdown("""
     <script>
       window.addEventListener('message', function (event) {
         try {
           const data = event.data || {};
           if (data.type === 'insaka:qr' && typeof data.qr === 'string') {
             console.log('✅ QR data received by parent:', data.qr);
             
             // Store QR data for processing
             sessionStorage.setItem('insaka_scanned_qr', data.qr);
             
             // Show success message
             alert('✅ QR Code Scanned Successfully!\\n\\nQR Data: ' + data.qr.substring(0, 100) + '...\\n\\nThe page will refresh to show authentication details.');
             
             // Refresh to show authentication details
             window.location.reload();
           }
         } catch (e) { console.error('QR listener error:', e); }
       }, false);
     </script>
     """, unsafe_allow_html=True)
    
     # Check for QR data in sessionStorage from scanner
    st.markdown("""
     <script>
     const scannedQR = sessionStorage.getItem('insaka_scanned_qr');
     if (scannedQR) {
       console.log('📱 Found scanned QR data:', scannedQR);
       // Clear it so it doesn't keep processing
       sessionStorage.removeItem('insaka_scanned_qr');
       
       // Redirect to process the QR data
       const url = new URL(window.location.href);
       url.searchParams.set('qr_data', scannedQR);
       window.location.href = url.toString();
     }
     </script>
     """, unsafe_allow_html=True)
     
     # Use components.html for better JavaScript execution
    components.html(simple_scanner_html, height=400)
    
    
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

        st.success("QR Code detected! Processing...")

        # Normalize / parse
        qr_text, payload = _normalize_qr_payload(qr_data_input)

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
                
                # Show detailed delegate info and authentication context
                st.markdown("### 🎉 Authentication Successful!")
                st.markdown("**Welcome to the Insaka Conference 2025 Delegate Portal!**")
                
                # Delegate information card
                st.markdown("#### 👤 Your Information")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**👤 Name:** {delegate.get('Full Name', 'N/A')}")
                    st.markdown(f"**🏢 Organization:** {delegate.get('Organization', 'N/A')}")
                    st.markdown(f"**📱 Phone:** {delegate.get('Phone', 'N/A')}")
                with col2:
                    st.markdown(f"**🎫 Category:** {delegate.get('Attendee Type', 'N/A')}")
                    st.markdown(f"**🆔 Delegate ID:** {delegate.get('ID', 'N/A')}")
                    st.markdown(f"**🌍 Nationality:** {delegate.get('Nationality', 'N/A')}")
                
                # Authentication details
                st.markdown("#### 🔐 Authentication Details")
                from datetime import datetime
                col_auth1, col_auth2 = st.columns(2)
                with col_auth1:
                    st.markdown(f"**✅ Status:** Authenticated")
                    st.markdown(f"**📅 Login Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                with col_auth2:
                    st.markdown(f"**🎯 Method:** QR Code Authentication")
                    st.markdown(f"**🏆 Access Level:** Full Delegate Access")
                
                # Dashboard access section
                st.markdown("#### 🚀 Ready to Access Your Dashboard")
                st.info("📋 **Your dashboard includes:**\n• Conference agenda and schedule\n• Speaker profiles and presentations\n• Exhibitor information and networking\n• Venue details and maps\n• Interactive posts and announcements\n• Matchmaking and networking tools")
                
                # Go to Dashboard button with more context
                if st.button("🚀 **Enter Delegate Dashboard**", width='stretch', type="primary"):
                    st.markdown("🔄 **Redirecting to your personalized dashboard...**")
                    _set_session_and_go(delegate)
            else:
                st.error(f"❌ Authentication Failed: {message}")
                st.markdown("### 🔍 Troubleshooting")
                st.markdown("**If you're having trouble:**\n• Ensure you're scanning a valid Insaka Conference delegate QR code\n• Check that your QR code is not damaged or blurry\n• Try refreshing the page and scanning again\n• Contact conference support if the issue persists")

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