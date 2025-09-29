# pages/PWA_Fix.py
import streamlit as st
import os
import json
from datetime import datetime

st.set_page_config(
    page_title="PWA Logo Fix — Insaka", 
    page_icon="🔧", 
    layout="wide"
)

st.markdown("# 🔧 PWA Logo Fix Tool")
st.markdown("This tool will help you fix the PWA logo issue")

# Check current status
st.markdown("## 📊 Current Status")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📁 PWA Icons")
    pwa_dir = "assets/pwa"
    if os.path.exists(pwa_dir):
        files = os.listdir(pwa_dir)
        st.success(f"✅ {len(files)} icons found")
        for file in sorted(files):
            st.write(f"• {file}")
    else:
        st.error("❌ PWA directory not found")

with col2:
    st.markdown("### 📋 Manifest")
    if os.path.exists("manifest.json"):
        st.success("✅ manifest.json exists")
        try:
            with open("manifest.json", 'r') as f:
                manifest = json.load(f)
            icons = manifest.get('icons', [])
            st.write(f"• {len(icons)} icons in manifest")
        except:
            st.error("❌ Error reading manifest")
    else:
        st.error("❌ manifest.json missing")

with col3:
    st.markdown("### 🔄 Service Worker")
    if os.path.exists("sw.js"):
        st.success("✅ Service worker exists")
        # Check cache version
        try:
            with open("sw.js", 'r') as f:
                content = f.read()
                if "CACHE_NAME" in content:
                    st.write("• Cache versioning active")
        except:
            st.error("❌ Error reading service worker")
    else:
        st.error("❌ Service worker missing")

# Force update options
st.markdown("## 🔄 Force Update Options")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🗑️ Clear Browser Cache")
    st.markdown("""
    **For Desktop:**
    1. Press `Ctrl+Shift+R` (hard refresh)
    2. Open DevTools (F12)
    3. Go to Application tab
    4. Click "Clear storage"
    5. Click "Clear site data"
    """)
    
    st.markdown("""
    **For Mobile:**
    1. Go to browser settings
    2. Clear browsing data
    3. Clear cache and cookies
    4. Restart browser
    """)

with col2:
    st.markdown("### 🔄 Service Worker Reset")
    st.markdown("""
    **Manual Reset:**
    1. Open DevTools (F12)
    2. Go to Application tab
    3. Click "Service Workers"
    4. Click "Unregister"
    5. Reload page
    """)
    
    st.markdown("""
    **PWA Reinstall:**
    1. Uninstall PWA from home screen
    2. Clear browser cache
    3. Revisit website
    4. Reinstall PWA
    """)

# Regenerate icons
st.markdown("## 🎨 Regenerate Icons")

if st.button("🔄 Regenerate PWA Icons", type="primary", use_container_width=True):
    try:
        import subprocess
        result = subprocess.run(['python', 'generate_pwa_logos.py'], 
                              capture_output=True, text=True, cwd='.')
        
        if result.returncode == 0:
            st.success("✅ Icons regenerated successfully!")
            st.code(result.stdout)
            st.rerun()
        else:
            st.error(f"❌ Error: {result.stderr}")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# Test icon display
st.markdown("## 🖼️ Test Icon Display")

st.markdown("**Your PWA icons should look like this:**")

# Display icons in a grid
icon_sizes = [48, 72, 96, 144, 152, 167, 180, 192, 512]
cols = st.columns(3)

for i, size in enumerate(icon_sizes):
    with cols[i % 3]:
        icon_path = f"assets/pwa/icon-{size}x{size}.png"
        if os.path.exists(icon_path):
            try:
                st.image(icon_path, width=80, caption=f"{size}x{size}")
            except:
                st.error(f"❌ {size}x{size}")
        else:
            st.error(f"❌ Missing {size}x{size}")

# Cache busting instructions
st.markdown("## 💡 Cache Busting Solutions")

with st.expander("🔧 Advanced Cache Busting", expanded=False):
    st.markdown("""
    ### Method 1: Service Worker Update
    The service worker has been updated with a timestamp-based cache name.
    This forces a complete cache refresh.
    
    ### Method 2: Manifest Versioning
    Add a version parameter to your manifest.json:
    ```json
    {
      "name": "Insaka Conference 2025",
      "version": "1.0.2"
    }
    ```
    
    ### Method 3: Icon Timestamping
    Add query parameters to icon URLs in manifest.json:
    ```json
    {
      "src": "assets/pwa/icon-192x192.png?v=20250927",
      "sizes": "192x192"
    }
    ```
    """)

# Quick fixes
st.markdown("## ⚡ Quick Fixes")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔄 Hard Refresh", use_container_width=True):
        st.markdown("""
        <script>
        window.location.reload(true);
        </script>
        """, unsafe_allow_html=True)
        st.success("Page refreshed!")

with col2:
    if st.button("🗑️ Clear Cache", use_container_width=True):
        st.markdown("""
        <script>
        if ('caches' in window) {
            caches.keys().then(function(names) {
                for (let name of names) {
                    caches.delete(name);
                }
                alert('Cache cleared!');
            });
        } else {
            alert('Cache API not supported');
        }
        </script>
        """, unsafe_allow_html=True)

with col3:
    if st.button("🔄 Unregister SW", use_container_width=True):
        st.markdown("""
        <script>
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.getRegistrations().then(function(registrations) {
                for(let registration of registrations) {
                    registration.unregister();
                }
                alert('Service workers unregistered!');
                window.location.reload();
            });
        } else {
            alert('Service Worker not supported');
        }
        </script>
        """, unsafe_allow_html=True)

# Deployment instructions
st.markdown("## 🚀 Deployment Instructions")

st.markdown("""
### For Streamlit Cloud:
1. **Commit all changes** to your repository
2. **Deploy to Streamlit Cloud**
3. **Wait 2-3 minutes** for deployment to complete
4. **Test on mobile device** with fresh browser session

### For Local Testing:
1. **Stop the current server** (Ctrl+C)
2. **Clear browser cache** completely
3. **Restart the server**: `streamlit run streamlit_app.py`
4. **Open in incognito/private mode**
5. **Test PWA installation**

### Mobile Testing:
1. **Use a different mobile device** or clear all data
2. **Open in Chrome/Edge** mobile browser
3. **Look for install prompt** or "Add to Home Screen"
4. **Install and check** if logo appears correctly
""")

# Debug information
st.markdown("## 🔍 Debug Information")

with st.expander("📊 Technical Details", expanded=False):
    st.markdown(f"**Current timestamp:** {datetime.now().isoformat()}")
    st.markdown(f"**Working directory:** {os.getcwd()}")
    
    # Check file sizes
    st.markdown("**Icon file sizes:**")
    for size in [48, 96, 192, 512]:
        icon_path = f"assets/pwa/icon-{size}x{size}.png"
        if os.path.exists(icon_path):
            file_size = os.path.getsize(icon_path)
            st.write(f"• {size}x{size}: {file_size:,} bytes")
        else:
            st.write(f"• {size}x{size}: Missing")

# Footer
st.markdown("---")
st.markdown("### 🎯 Next Steps:")
st.markdown("""
1. **Regenerate icons** if needed
2. **Clear browser cache** completely
3. **Test on mobile device**
4. **Deploy to Streamlit Cloud**
5. **Verify PWA installation**
""")

if st.button("🏠 Back to Dashboard", use_container_width=True):
    st.switch_page("pages/1_Delegate_Dashboard.py")

