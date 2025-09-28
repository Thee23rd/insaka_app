import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.qr_system import authenticate_with_qr_code
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

# Handle QR code data from URL
if 'qr_data' in st.query_params:
    raw = st.query_params['qr_data']
    qr_data_input = raw[0] if isinstance(raw, list) else raw

    st.success("QR Code detected! Processing...")
    
    try:
        # Try to parse as JSON first
        qr_data = json.loads(qr_data_input)
        delegate_id = qr_data.get('delegate_id', '')
    except:
        # If not JSON, treat as simple ID
        delegate_id = str(qr_data_input).strip()
    
    if delegate_id:
        # Find delegate in staff data
        try:
            match_df = staff_df[staff_df["ID"].astype(str) == str(delegate_id)]
            if not match_df.empty:
                row = match_df.iloc[0].to_dict()
                
                # Set session state
                st.session_state.delegate_authenticated = True
                st.session_state.delegate_id = row.get('ID')
                st.session_state.delegate_name = row.get('Full Name', '')
                st.session_state.delegate_organization = row.get('Organization', '')
                st.session_state.delegate_category = row.get('Attendee Type', '')
                st.session_state.delegate_title = row.get('Title', '')
                st.session_state.delegate_nationality = row.get('Nationality', '')
                st.session_state.delegate_phone = row.get('Phone', '')

                st.success(f"Welcome, {row.get('Full Name', 'Unknown')}!")
                st.info("Redirecting to your dashboard...")
                
                # Clear URL parameters
                try:
                    st.query_params.clear()
                except:
                    pass
                
                # Redirect to dashboard
                st.switch_page("pages/1_Delegate_Dashboard.py")
            else:
                st.error(f"Delegate ID {delegate_id} not found in the system.")
        except Exception as e:
            st.error(f"Error processing delegate data: {str(e)}")
    else:
        st.error("Invalid QR code data received.")

# QR Code Scanner
st.markdown("### Camera Scanner")
st.markdown("Use your device camera to scan the QR code from your conference badge.")

# Simple scanner HTML
scanner_html = """
<div style="text-align: center; max-width: 600px; margin: 0 auto;">
    <video id="video" style="width: 100%; height: 300px; border: 2px solid #198A00; border-radius: 10px; display: none;"></video>
    <canvas id="canvas" style="display: none;"></canvas>
    <div id="status" style="padding: 10px; margin: 10px 0; background: #f0f8f0; border-radius: 5px; font-weight: bold;">
        Camera ready - click start to begin
    </div>
    <button id="start" style="background: #198A00; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin: 5px;">
        Start Camera
    </button>
    <button id="stop" style="background: #D10000; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin: 5px; display: none;">
        Stop Camera
    </button>
</div>

<script src="https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.js"></script>
<script>
let stream = null;
let scanning = false;

function startCamera() {
    const video = document.getElementById('video');
    const status = document.getElementById('status');
    const startBtn = document.getElementById('start');
    const stopBtn = document.getElementById('stop');
    
    navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
    .then(function(mediaStream) {
        stream = mediaStream;
        video.srcObject = mediaStream;
        video.style.display = 'block';
        startBtn.style.display = 'none';
        stopBtn.style.display = 'inline-block';
        video.play();
        scanning = true;
        status.textContent = 'Camera started - point at QR code';
        scanLoop();
    })
    .catch(function(err) {
        status.textContent = 'Camera access denied';
    });
}

function stopCamera() {
    scanning = false;
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
    const video = document.getElementById('video');
    const status = document.getElementById('status');
    const startBtn = document.getElementById('start');
    const stopBtn = document.getElementById('stop');
    video.style.display = 'none';
    startBtn.style.display = 'inline-block';
    stopBtn.style.display = 'none';
    status.textContent = 'Camera stopped';
}

function scanLoop() {
    if (!scanning) return;
    
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    const status = document.getElementById('status');
    
    if (video.readyState === video.HAVE_ENOUGH_DATA) {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const code = jsQR(imageData.data, imageData.width, imageData.height);

        if (code && code.data) {
            scanning = false;
            status.textContent = 'QR Code detected! Redirecting...';
            const url = new URL(window.location.href);
            url.searchParams.set('qr_data', code.data);
            window.location.href = url.toString();
            return;
        }
    }
    requestAnimationFrame(scanLoop);
}

document.getElementById('start').addEventListener('click', startCamera);
document.getElementById('stop').addEventListener('click', stopCamera);
window.addEventListener('beforeunload', stopCamera);
</script>
"""

st.markdown(scanner_html, unsafe_allow_html=True)

# Manual entry option
st.markdown("---")
st.markdown("### Manual Entry")
st.markdown("If you can't use the camera, enter your delegate ID manually:")

manual_id = st.text_input("Enter your delegate ID:", placeholder="e.g., 123")
if st.button("Login with ID"):
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

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("Back to Landing Page"):
        st.switch_page("pages/0_Landing.py")
with col2:
    if st.button("Go to Self-Service"):
        st.switch_page("pages/7_Delegate_Self_Service.py")
