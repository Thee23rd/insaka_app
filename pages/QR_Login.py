# pages/QR_Login.py
import streamlit as st
import json
import sys
import os
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
    
    # Use the improved scanner HTML with components.html
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
    (function() {
      let stream = null;
      let scanning = false;
      let rafId = null;

      const video = document.getElementById('qr-video');
      const canvas = document.getElementById('qr-canvas');
      const ctx = canvas.getContext('2d');
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
          if (location.protocol !== 'https:' && location.hostname !== 'localhost') {
            statusEl.textContent = '❌ Camera blocked: use HTTPS or run on localhost.';
          } else {
            statusEl.textContent = '❌ Camera access denied. Allow permissions in your browser.';
          }
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
              const parsed = JSON.parse(code.data);
              if (parsed && parsed.type === 'delegate_login') {
                const url = new URL(window.location.href);
                url.searchParams.set('qr_data', code.data);
                window.location.href = url.toString();
              } else {
                statusEl.textContent = '❌ Invalid QR code type';
                setTimeout(() => { scanning = true; scanLoop(); }, 1500);
              }
            } catch (err) {
              console.error('QR parse error:', err);
              statusEl.textContent = '❌ Invalid QR code format';
              setTimeout(() => { scanning = true; scanLoop(); }, 1500);
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
    
    # Use components.html for better JavaScript execution
    components.html(scanner_html, height=520)
    
    col1, col2 = st.columns([1, 1])
    
    with col2:
        st.markdown("**Instructions:**")
        st.markdown("""
        1. Click "Start Camera" button above
        2. Allow camera access when prompted
        3. Point camera at QR code on badge
        4. Wait for automatic detection
        """)
    
    # Handle QR code data from scanner
    if 'qr_data' in st.query_params:
        qr_data_input = st.query_params['qr_data']
        st.success("QR Code detected! Processing...")
        
        with st.spinner("Authenticating..."):
            success, message, delegate = authenticate_with_qr_code(qr_data_input, staff_df)
            
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
                
                # Redirect to dashboard
                st.markdown("### 🎉 Login Successful!")
                st.markdown(f"**Welcome, {delegate.get('Full Name', '')}!**")
                st.markdown(f"**Organization:** {delegate.get('Organization', '')}")
                st.markdown(f"**Category:** {delegate.get('Attendee Type', '')}")
                
                if st.button("🏠 Go to Dashboard", type="primary", width='stretch'):
                    st.switch_page("pages/1_Delegate_Dashboard.py")
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
                    
                    # Redirect to dashboard
                    st.markdown("### 🎉 Login Successful!")
                    st.markdown(f"**Welcome, {delegate.get('Full Name', '')}!**")
                    st.markdown(f"**Organization:** {delegate.get('Organization', '')}")
                    st.markdown(f"**Category:** {delegate.get('Attendee Type', '')}")
                    
                    if st.button("🏠 Go to Dashboard", type="primary", width='stretch'):
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
