import streamlit as st
import streamlit.components.v1 as components
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.qr_system import authenticate_with_qr_code, create_qr_scanner_script
import pandas as pd
import urllib.parse
import json

st.set_page_config(
    page_title="QR Code Login - Insaka Conference 2025",
    page_icon="📱",
    layout="wide"
)

# Load staff data
@st.cache_data
def load_staff_data():
    try:
        return pd.read_csv("data/complimentary_passes.csv")
    except FileNotFoundError:
        st.error("Staff data file not found. Please ensure data/complimentary_passes.csv exists.")
        return pd.DataFrame()

staff_df = load_staff_data()

st.markdown("""
<div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #198A00, #2BA300); color: white; border-radius: 15px; margin-bottom: 30px;">
    <h1>📱 QR Code Login</h1>
    <p>Scan your conference badge QR code to access your delegate dashboard</p>
</div>
""", unsafe_allow_html=True)

# Login method selection
login_method = st.radio(
    "Choose your login method:",
    ["📱 Scan QR Code", "✍️ Manual Entry"],
    horizontal=True
)

if login_method == "📱 Scan QR Code":
    st.markdown("### 📷 Camera Scanner")
    st.markdown("Use your device camera to scan the QR code from your conference badge.")
    
    # Simple QR Scanner with proper syntax
    simple_scanner_html = """
        <div id="qr-scanner-container" style="max-width: 720px; margin: 0 auto;">
          <video id="qr-video" style="width: 100%; height: 300px; border: 3px solid #198A00; border-radius: 15px; display: none;" playsinline></video>
          <canvas id="qr-canvas" style="display: none;"></canvas>
          <div id="qr-status" style="text-align: center; padding: 10px; background: #f0f8f0; border-radius: 10px; margin: 10px 0; font-weight: bold; color: #198A00;">
            Camera scanner ready — click start to begin
          </div>
          <div style="text-align:center;">
            <button id="start-btn" style="background:#198A00;color:white;border:none;padding:12px 24px;border-radius:25px;cursor:pointer;font-weight:bold;margin:5px;">
              Start Camera
            </button>
            <button id="stop-btn" style="background:#D10000;color:white;border:none;padding:12px 24px;border-radius:25px;cursor:pointer;font-weight:bold;margin:5px;display:none;">
              Stop Camera
            </button>
          </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.js"></script>
        <script>
        let stream = null;
        let scanning = false;
        let rafId = null;

        function startCamera() {
          const video = document.getElementById('qr-video');
          const canvas = document.getElementById('qr-canvas');
          const ctx = canvas.getContext('2d');
          const statusEl = document.getElementById('qr-status');
          const startBtn = document.getElementById('start-btn');
          const stopBtn = document.getElementById('stop-btn');
          
          navigator.mediaDevices.getUserMedia({ 
            video: { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } } 
          }).then(function(mediaStream) {
            stream = mediaStream;
            video.srcObject = mediaStream;
            video.style.display = 'block';
            startBtn.style.display = 'none';
            stopBtn.style.display = 'inline-block';
            video.play();
            scanning = true;
            statusEl.textContent = 'Camera started. Point at QR code...';
            scanLoop();
          }).catch(function(err) {
            statusEl.textContent = 'Camera access denied';
          });
        }

        function stopCamera() {
          scanning = false;
          if (rafId) cancelAnimationFrame(rafId);
          if (stream) {
            stream.getTracks().forEach(track => track.stop());
            stream = null;
          }
          const video = document.getElementById('qr-video');
          const startBtn = document.getElementById('start-btn');
          const stopBtn = document.getElementById('stop-btn');
          const statusEl = document.getElementById('qr-status');
          video.style.display = 'none';
          startBtn.style.display = 'inline-block';
          stopBtn.style.display = 'none';
          statusEl.textContent = 'Camera stopped';
        }

        function scanLoop() {
          if (!scanning) return;
          const video = document.getElementById('qr-video');
          const canvas = document.getElementById('qr-canvas');
          const ctx = canvas.getContext('2d');
          const statusEl = document.getElementById('qr-status');
          
          if (video.readyState === video.HAVE_ENOUGH_DATA) {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            const code = jsQR(imageData.data, imageData.width, imageData.height);

            if (code && code.data) {
              scanning = false;
              statusEl.textContent = 'QR Code detected! Redirecting...';
              const url = new URL(window.location.href);
              url.searchParams.set('qr_data', code.data);
              window.location.href = url.toString();
              return;
            }
          }
          rafId = requestAnimationFrame(scanLoop);
        }

        document.getElementById('start-btn').addEventListener('click', startCamera);
        document.getElementById('stop-btn').addEventListener('click', stopCamera);
        window.addEventListener('beforeunload', stopCamera);
        </script>
        """
    
    # Use st.markdown for direct JavaScript execution
    st.markdown(simple_scanner_html, unsafe_allow_html=True)
    
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

elif login_method == "✍️ Manual Entry":
    st.markdown("### ✍️ Manual Login")
    st.markdown("Enter your delegate information manually.")
    
    col1, col2 = st.columns([1, 1])
    
    with col2:
        manual_id = st.text_input("Enter your delegate ID:", placeholder="e.g., 123")
        if st.button("Login with ID", width='stretch'):
            if manual_id:
                try:
                    match_df = staff_df[staff_df["ID"].astype(str) == str(manual_id)]
                    if not match_df.empty:
                        row = match_df.iloc[0].to_dict()
                        
                        st.session_state.delegate_authenticated = True
                        st.session_state.delegate_id = row.get('ID')
                        st.session_state.delegate_name = row.get('Full Name', '')
                        st.session_state.delegate_organization = row.get('Organization', '')
                        st.session_state.delegate_category = row.get('Attendee Type', '')
                        st.session_state.delegate_title = row.get('Title', '')
                        st.session_state.delegate_nationality = row.get('Nationality', '')
                        st.session_state.delegate_phone = row.get('Phone', '')

                        st.success(f"Welcome, {row.get('Full Name', 'Unknown')}!")
                        st.switch_page("pages/1_Delegate_Dashboard.py")
                    else:
                        st.error(f"Delegate ID {manual_id} not found.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.warning("Please enter a delegate ID.")

# Handle QR code data from URL
if 'qr_data' in st.query_params:
    raw = st.query_params['qr_data']
    qr_data_input = raw[0] if isinstance(raw, list) else raw

    st.success("🎉 QR Code detected! Processing...")
    st.markdown(f"**Raw QR Data:** `{qr_data_input}`")

    # Normalize / parse QR data
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

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("Back to Landing Page", width='stretch'):
        st.switch_page("pages/0_Landing.py")
with col2:
    if st.button("Go to Self-Service", width='stretch'):
        st.switch_page("pages/7_Delegate_Self_Service.py")
