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
            console.log('QR Code detected:', code.data);
            scanning = false;
            statusEl.textContent = '✅ QR Code detected! Processing...';
            try {
              const parsed = JSON.parse(code.data);
              console.log('Parsed QR data:', parsed);
              if (parsed && parsed.type === 'delegate_login') {
                statusEl.textContent = '🔄 Redirecting to dashboard...';
                // Redirect parent window (not the iframe)
                const url = new URL(window.top.location.href);
                url.searchParams.set('qr_data', code.data);
                console.log('Redirecting to:', url.toString());
                window.top.location.href = url.toString();
              } else {
                console.log('Invalid QR code type:', parsed?.type);
                statusEl.textContent = '❌ Invalid QR code type';
                setTimeout(() => { scanning = true; scanLoop(); }, 1500);
              }
            } catch (err) {
              console.error('QR parse error:', err);
              console.log('Raw QR data:', code.data);
              console.log('QR data type:', typeof code.data);
              console.log('QR data length:', code.data ? code.data.length : 'null');
              
              // Show the raw data to the user for debugging
              statusEl.innerHTML = `❌ Invalid QR code format<br><small>Raw data: "${code.data}"</small>`;
              
              // Try to handle non-JSON QR codes (like simple delegate IDs)
              if (code.data && code.data.trim()) {
                // If it's just a number (delegate ID), create a simple QR data
                if (/^[0-9]+$/.test(code.data.trim())) {
                  const simpleQrData = JSON.stringify({
                    type: 'delegate_login',
                    delegate_id: code.data.trim(),
                    delegate_name: 'Unknown',
                    organization: 'Unknown',
                    timestamp: new Date().toISOString(),
                    conference: 'Insaka Conference 2025'
                  });
                  
                  statusEl.textContent = '🔄 Processing delegate ID...';
                  const url = new URL(window.top.location.href);
                  url.searchParams.set('qr_data', simpleQrData);
                  console.log('Redirecting with delegate ID:', url.toString());
                  window.top.location.href = url.toString();
                  return;
                }
                
                // Try to handle any text that might be a delegate ID or name
                const trimmedData = code.data.trim();
                if (trimmedData.length > 0 && trimmedData.length < 100) {
                  // Create a generic QR data structure
                  const genericQrData = JSON.stringify({
                    type: 'delegate_login',
                    delegate_id: trimmedData,
                    delegate_name: 'Unknown',
                    organization: 'Unknown',
                    timestamp: new Date().toISOString(),
                    conference: 'Insaka Conference 2025'
                  });
                  
                  statusEl.textContent = '🔄 Processing generic data...';
                  const url = new URL(window.top.location.href);
                  url.searchParams.set('qr_data', genericQrData);
                  console.log('Redirecting with generic data:', url.toString());
                  window.top.location.href = url.toString();
                  return;
                }
              }
              
              setTimeout(() => { 
                scanning = true; 
                statusEl.textContent = '📷 Scanning... Point camera at QR code';
                scanLoop(); 
              }, 3000);
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
        
        # Test QR code generator
        st.markdown("---")
        st.markdown("**🧪 Test QR Code:**")
        if st.button("Generate Test QR Code", width='stretch'):
            # Generate a test QR code for testing
            test_qr_data = {
                "type": "delegate_login",
                "delegate_id": "123",
                "delegate_name": "Test User",
                "organization": "Test Organization",
                "timestamp": "2025-09-28T12:00:00",
                "conference": "Insaka Conference 2025"
            }
            
            # Try to generate an actual QR code image
            try:
                from lib.qr_system import create_qr_code
                qr_img, qr_data = create_qr_code(
                    "123", "Test User", "Test Organization", size=200
                )
                
                if qr_img is not None:
                    st.image(qr_img, caption="Test QR Code - Scan this with the camera scanner", width=200)
                    st.success("✅ Test QR code generated! Scan it with the camera scanner above.")
                else:
                    st.warning("QR code generation failed, showing data only.")
            except Exception as e:
                st.warning(f"Could not generate QR code: {e}")
            
            # Display the test QR data
            st.json(test_qr_data)
            st.info("This is the data that will be processed when you scan the QR code above.")
            
            # Also show as a clickable link for testing
            encoded_data = urllib.parse.quote(json.dumps(test_qr_data))
            test_url = f"http://localhost:8524/pages/QR_Login.py?qr_data={encoded_data}"
            st.markdown(f"**Test URL:** [Click to test authentication]({test_url})")
            
            # Direct test button
            if st.button("🚀 Test Authentication Directly", width='stretch'):
                # Simulate the QR data processing directly
                st.success("Testing authentication with test data...")
                
                with st.spinner("Authenticating..."):
                    # Create a fake delegate for testing
                    fake_delegate = {
                        'ID': 123,
                        'Full Name': 'Test User',
                        'Organization': 'Test Organization',
                        'Attendee Type': 'Delegate',
                        'Title': 'Test Title',
                        'Nationality': 'Zambian',
                        'Phone': '1234567890'
                    }
                    
                    # Set session state for authenticated delegate
                    st.session_state.delegate_authenticated = True
                    st.session_state.delegate_id = fake_delegate.get('ID')
                    st.session_state.delegate_name = fake_delegate.get('Full Name', '')
                    st.session_state.delegate_organization = fake_delegate.get('Organization', '')
                    st.session_state.delegate_category = fake_delegate.get('Attendee Type', '')
                    st.session_state.delegate_title = fake_delegate.get('Title', '')
                    st.session_state.delegate_nationality = fake_delegate.get('Nationality', '')
                    st.session_state.delegate_phone = fake_delegate.get('Phone', '')
                    
                    st.balloons()
                    
                    # Show success message and redirect
                    st.markdown("### 🎉 Login Successful!")
                    st.markdown(f"**Welcome, {fake_delegate.get('Full Name', '')}!**")
                    st.markdown(f"**Organization:** {fake_delegate.get('Organization', '')}")
                    st.markdown(f"**Category:** {fake_delegate.get('Attendee Type', '')}")
                    st.markdown("🔄 Redirecting to your dashboard...")
                    
                    # Try multiple redirect methods
                    try:
                        st.switch_page("pages/1_Delegate_Dashboard.py")
                    except Exception:
                        try:
                            st.switch_page("1_Delegate_Dashboard.py")
                        except Exception:
                            st.markdown("""
                                <script>
                                window.top.location.href = '/pages/1_Delegate_Dashboard.py';
                                </script>
                            """, unsafe_allow_html=True)
                    st.stop()
    
    # Handle QR code data from scanner
    if 'qr_data' in st.query_params:
        raw = st.query_params['qr_data']
        qr_data_input = raw[0] if isinstance(raw, list) else raw

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

                # Clear QR from URL so refreshes don’t re-trigger auth
                try:
                    st.query_params.clear()
                except Exception:
                    pass

                # Try both common switch_page targets, then stop
                try:
                    st.switch_page("pages/1_Delegate_Dashboard.py")
                except Exception:
                    try:
                        st.switch_page("1_Delegate_Dashboard.py")  # some setups want no "pages/"
                    except Exception:
                        # As a last resort, client-side redirect (works everywhere)
                        st.markdown("""
                            <script>
                            // Navigate parent (not the iframe)
                            window.top.location.href = window.top.location.href.split('?')[0]
                            + '?page=1_Delegate_Dashboard.py';
                            </script>
                        """, unsafe_allow_html=True)
                st.stop()
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
