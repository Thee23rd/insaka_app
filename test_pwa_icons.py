#!/usr/bin/env python3
"""
Test PWA Icons Accessibility
This script tests if the PWA icons are properly accessible and displays them
"""

import streamlit as st
import os
from PIL import Image

st.set_page_config(
    page_title="PWA Icons Test — Insaka", 
    page_icon="🧪", 
    layout="wide"
)

st.markdown("# 🧪 PWA Icons Test")
st.markdown("Testing if your PWA icons are properly generated and accessible")

# Check if PWA icons exist
pwa_dir = "assets/pwa"
icon_sizes = [48, 72, 96, 144, 152, 167, 180, 192, 512]

st.markdown("## 📁 File Check")
if os.path.exists(pwa_dir):
    st.success(f"✅ PWA directory exists: {pwa_dir}")
    
    # List all files in PWA directory
    files = os.listdir(pwa_dir)
    st.markdown(f"**Files found:** {len(files)}")
    
    for file in sorted(files):
        file_path = os.path.join(pwa_dir, file)
        file_size = os.path.getsize(file_path)
        st.markdown(f"- `{file}` ({file_size:,} bytes)")
        
    # Check for missing icons
    missing_icons = []
    for size in icon_sizes:
        icon_file = f"icon-{size}x{size}.png"
        if icon_file not in files:
            missing_icons.append(icon_file)
    
    if missing_icons:
        st.error(f"❌ Missing icons: {', '.join(missing_icons)}")
    else:
        st.success("✅ All required PWA icons are present!")
        
else:
    st.error(f"❌ PWA directory not found: {pwa_dir}")
    st.markdown("Run `python generate_pwa_logos.py` to create the icons.")

# Display the icons
st.markdown("## 🎨 Icon Preview")
st.markdown("Here's how your PWA icons look:")

# Create columns for displaying icons
cols = st.columns(3)

for i, size in enumerate(icon_sizes):
    icon_file = f"icon-{size}x{size}.png"
    icon_path = os.path.join(pwa_dir, icon_file)
    
    with cols[i % 3]:
        if os.path.exists(icon_path):
            try:
                st.image(icon_path, width=100, caption=f"{size}x{size}")
                
                # Get image info
                with Image.open(icon_path) as img:
                    width, height = img.size
                    mode = img.mode
                    st.caption(f"Size: {width}x{height}, Mode: {mode}")
                    
            except Exception as e:
                st.error(f"❌ Error loading {icon_file}: {e}")
        else:
            st.error(f"❌ Missing: {icon_file}")

# Test manifest.json
st.markdown("## 📋 Manifest.json Check")

manifest_path = "manifest.json"
if os.path.exists(manifest_path):
    st.success("✅ manifest.json exists")
    
    try:
        import json
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        st.markdown("**Manifest content:**")
        st.json(manifest)
        
        # Check if manifest references correct icon paths
        icons = manifest.get('icons', [])
        st.markdown(f"**Icons in manifest:** {len(icons)}")
        
        for icon in icons:
            icon_src = icon.get('src', '')
            icon_size = icon.get('sizes', '')
            icon_type = icon.get('type', '')
            st.markdown(f"- `{icon_src}` ({icon_size}, {icon_type})")
            
            # Check if icon file exists
            if icon_src.startswith('assets/pwa/'):
                if os.path.exists(icon_src):
                    st.success(f"✅ {icon_src} exists")
                else:
                    st.error(f"❌ {icon_src} missing")
            else:
                st.warning(f"⚠️ {icon_src} not in PWA directory")
                
    except Exception as e:
        st.error(f"❌ Error reading manifest.json: {e}")
else:
    st.error("❌ manifest.json not found")

# Browser cache clearing instructions
st.markdown("## 🔄 Browser Cache Issues")
st.markdown("""
If the PWA logo isn't updating, try these steps:

### For Desktop Browsers:
1. **Chrome/Edge**: Press `Ctrl+Shift+R` (hard refresh)
2. **Open DevTools** (F12) → Application tab → Storage → Clear storage
3. **Service Workers** → Unregister all workers
4. **Reload** the page

### For Mobile:
1. **Uninstall** the PWA app from home screen
2. **Clear browser cache** in settings
3. **Revisit** the website
4. **Reinstall** the PWA

### Force Update:
1. Open `force_pwa_update.html` in your browser
2. Click "Clear All Caches"
3. Click "Unregister Service Worker"
4. Reload the app
""")

# Regenerate icons button
st.markdown("## 🔧 Regenerate Icons")
if st.button("🔄 Regenerate PWA Icons", type="primary"):
    try:
        import subprocess
        result = subprocess.run(['python', 'generate_pwa_logos.py'], 
                              capture_output=True, text=True, cwd='.')
        
        if result.returncode == 0:
            st.success("✅ Icons regenerated successfully!")
            st.code(result.stdout)
            st.rerun()
        else:
            st.error(f"❌ Error regenerating icons: {result.stderr}")
            
    except Exception as e:
        st.error(f"❌ Error running generator: {e}")

# Footer
st.markdown("---")
st.markdown("### 📱 Next Steps:")
st.markdown("""
1. **Verify all icons** are displayed correctly above
2. **Clear browser cache** if needed
3. **Deploy to Streamlit Cloud** for testing
4. **Test on mobile device** for PWA installation
""")

if st.button("🏠 Back to Dashboard"):
    st.switch_page("pages/1_Delegate_Dashboard.py")
