# pages/PWA_Debug.py - PWA Debugging & Testing Page
import streamlit as st
from lib.ui import apply_brand

st.set_page_config(page_title="PWA Debug — Insaka", page_icon="🔧", layout="wide")

apply_brand()

st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

st.title("🔧 PWA Debugging & Testing")
st.markdown("Test all PWA features: Icons, Notifications, Sound, Service Worker")

st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

# Status Checks
st.markdown("## 📊 System Status")

col_status1, col_status2, col_status3 = st.columns(3)

with col_status1:
    st.markdown("""
    <div style="background: #1A1A1A; border: 2px solid #198A00; border-radius: 12px; padding: 1rem;">
        <h4 style="color: #198A00;">Service Worker</h4>
        <div id="sw-status">Checking...</div>
    </div>
    """, unsafe_allow_html=True)

with col_status2:
    st.markdown("""
    <div style="background: #1A1A1A; border: 2px solid #198A00; border-radius: 12px; padding: 1rem;">
        <h4 style="color: #198A00;">Notifications</h4>
        <div id="notif-status">Checking...</div>
    </div>
    """, unsafe_allow_html=True)

with col_status3:
    st.markdown("""
    <div style="background: #1A1A1A; border: 2px solid #198A00; border-radius: 12px; padding: 1rem;">
        <h4 style="color: #198A00;">PWA Installed</h4>
        <div id="pwa-status">Checking...</div>
    </div>
    """, unsafe_allow_html=True)

# JavaScript Status Check
st.markdown("""
<script>
// Check Service Worker
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.getRegistration().then(reg => {
        const swStatus = document.getElementById('sw-status');
        if (reg) {
            swStatus.innerHTML = '✅ Active';
            swStatus.style.color = '#2BA300';
        } else {
            swStatus.innerHTML = '❌ Not Registered';
            swStatus.style.color = '#D10000';
        }
    });
} else {
    document.getElementById('sw-status').innerHTML = '❌ Not Supported';
    document.getElementById('sw-status').style.color = '#D10000';
}

// Check Notifications
const notifStatus = document.getElementById('notif-status');
if ('Notification' in window) {
    if (Notification.permission === 'granted') {
        notifStatus.innerHTML = '✅ Granted';
        notifStatus.style.color = '#2BA300';
    } else if (Notification.permission === 'denied') {
        notifStatus.innerHTML = '❌ Denied';
        notifStatus.style.color = '#D10000';
    } else {
        notifStatus.innerHTML = '⚠️ Not Requested';
        notifStatus.style.color = '#FF9500';
    }
} else {
    notifStatus.innerHTML = '❌ Not Supported';
    notifStatus.style.color = '#D10000';
}

// Check PWA Installation
const pwaStatus = document.getElementById('pwa-status');
if (window.matchMedia('(display-mode: standalone)').matches) {
    pwaStatus.innerHTML = '✅ Installed';
    pwaStatus.style.color = '#2BA300';
} else {
    pwaStatus.innerHTML = '⚠️ Not Installed (Browser Mode)';
    pwaStatus.style.color = '#FF9500';
}
</script>
""", unsafe_allow_html=True)

# Test Buttons
st.markdown("---")
st.markdown("## 🧪 Feature Tests")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🔔 Notification Test")
    if st.button("Request Permission", use_container_width=True):
        st.markdown("""
        <script>
        if ('Notification' in window) {
            Notification.requestPermission().then(permission => {
                if (permission === 'granted') {
                    alert('✅ Permission granted! You can now receive notifications.');
                    location.reload();
                } else {
                    alert('❌ Permission denied. Please enable notifications in browser settings.');
                }
            });
        }
        </script>
        """, unsafe_allow_html=True)
    
    if st.button("Test Notification", use_container_width=True):
        st.markdown("""
        <script>
        if (typeof window.testNotification === 'function') {
            window.testNotification();
        } else {
            // Manual test
            if (Notification.permission === 'granted') {
                new Notification('Insaka Test', {
                    body: 'Test notification from debug page!',
                    icon: './assets/pwa/icon-192x192.png',
                    vibrate: [200, 100, 200]
                });
            } else {
                alert('Please request notification permission first!');
            }
        }
        </script>
        """, unsafe_allow_html=True)
        st.success("Notification triggered!")

with col2:
    st.markdown("### 🔊 Sound Test")
    if st.button("Play Sound (Relative)", use_container_width=True):
        st.markdown("""
        <script>
        const audio = new Audio('./assets/notification.wav');
        audio.volume = 1.0;
        audio.play().then(() => {
            console.log('✅ Sound played successfully!');
        }).catch(err => {
            console.error('❌ Sound failed:', err);
            alert('Sound failed! Error: ' + err.message);
        });
        </script>
        """, unsafe_allow_html=True)
        st.success("Playing sound...")
    
    if st.button("Play Sound (Absolute)", use_container_width=True):
        st.markdown("""
        <script>
        const audio = new Audio('assets/notification.wav');
        audio.volume = 1.0;
        audio.play().then(() => {
            console.log('✅ Sound played successfully!');
        }).catch(err => {
            console.error('❌ Sound failed:', err);
            alert('Sound failed! Error: ' + err.message);
        });
        </script>
        """, unsafe_allow_html=True)
        st.success("Playing sound...")

with col3:
    st.markdown("### 🖼️ Icon Test")
    st.markdown("**Check these paths:**")
    st.code("./assets/pwa/icon-192x192.png")
    
    # Show icon preview
    try:
        st.image("assets/pwa/icon-192x192.png", width=100, caption="PWA Icon")
        st.success("✅ Icon loaded!")
    except:
        st.error("❌ Icon failed to load!")

# Console Output
st.markdown("---")
st.markdown("## 📋 Console Output")
st.info("Open browser console (F12) to see detailed logs and errors")

# Detailed Diagnostics
st.markdown("---")
st.markdown("## 🔍 Detailed Diagnostics")

if st.button("Run Full Diagnostic", use_container_width=True):
    st.markdown("""
    <script>
    console.clear();
    console.log('═══════════════════════════════════════');
    console.log('🔧 INSAKA PWA DIAGNOSTIC REPORT');
    console.log('═══════════════════════════════════════');
    
    // Browser Info
    console.log('\\n📱 BROWSER INFO:');
    console.log('- User Agent:', navigator.userAgent);
    console.log('- Platform:', navigator.platform);
    console.log('- Online:', navigator.onLine);
    
    // Service Worker
    console.log('\\n🔧 SERVICE WORKER:');
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.getRegistrations().then(regs => {
            console.log('- Registrations:', regs.length);
            regs.forEach((reg, idx) => {
                console.log(`  Registration ${idx}:`, reg);
                console.log('  - Scope:', reg.scope);
                console.log('  - Active:', reg.active ? 'Yes' : 'No');
            });
        });
    } else {
        console.log('- Status: ❌ NOT SUPPORTED');
    }
    
    // Notifications
    console.log('\\n🔔 NOTIFICATIONS:');
    if ('Notification' in window) {
        console.log('- Supported: ✅ YES');
        console.log('- Permission:', Notification.permission);
        console.log('- Max Actions:', Notification.maxActions || 'Unknown');
    } else {
        console.log('- Supported: ❌ NO');
    }
    
    // PWA Features
    console.log('\\n📱 PWA FEATURES:');
    console.log('- Standalone Mode:', window.matchMedia('(display-mode: standalone)').matches);
    console.log('- Installed:', window.matchMedia('(display-mode: standalone)').matches);
    
    // Audio Support
    console.log('\\n🔊 AUDIO:');
    console.log('- Audio API:', typeof Audio !== 'undefined' ? '✅ Supported' : '❌ Not Supported');
    
    // Test Audio Paths
    console.log('\\n🎵 TESTING AUDIO PATHS:');
    const paths = [
        './assets/notification.wav',
        'assets/notification.wav',
        '/assets/notification.wav'
    ];
    
    paths.forEach(path => {
        const audio = new Audio(path);
        audio.addEventListener('canplaythrough', () => {
            console.log(`✅ Path works: ${path}`);
        });
        audio.addEventListener('error', (e) => {
            console.log(`❌ Path failed: ${path}`, e);
        });
    });
    
    // Test Icon Paths
    console.log('\\n🖼️ TESTING ICON PATHS:');
    const iconPaths = [
        './assets/pwa/icon-192x192.png',
        'assets/pwa/icon-192x192.png',
        '/assets/pwa/icon-192x192.png'
    ];
    
    iconPaths.forEach(path => {
        const img = new Image();
        img.onload = () => console.log(`✅ Icon loads: ${path}`);
        img.onerror = () => console.log(`❌ Icon fails: ${path}`);
        img.src = path;
    });
    
    // Manifest
    console.log('\\n📄 MANIFEST:');
    fetch('./manifest.json')
        .then(r => r.json())
        .then(manifest => {
            console.log('- Name:', manifest.name);
            console.log('- Icons:', manifest.icons.length);
            console.log('- First Icon Path:', manifest.icons[0].src);
        })
        .catch(e => console.log('❌ Manifest load failed:', e));
    
    console.log('\\n═══════════════════════════════════════');
    console.log('✅ DIAGNOSTIC COMPLETE - Check logs above');
    console.log('═══════════════════════════════════════');
    
    alert('✅ Diagnostic complete! Check browser console (F12) for full report.');
    </script>
    """, unsafe_allow_html=True)
    st.success("✅ Diagnostic running! Check console (F12)")

# Quick Fixes
st.markdown("---")
st.markdown("## 🔧 Quick Fixes")

col_fix1, col_fix2, col_fix3 = st.columns(3)

with col_fix1:
    st.markdown("### Clear Service Worker")
    if st.button("Unregister SW", use_container_width=True):
        st.markdown("""
        <script>
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.getRegistrations().then(regs => {
                regs.forEach(reg => reg.unregister());
                alert('✅ Service Worker unregistered! Reload page to re-register.');
            });
        }
        </script>
        """, unsafe_allow_html=True)
        st.success("SW unregistered!")

with col_fix2:
    st.markdown("### Clear Cache")
    if st.button("Clear All Caches", use_container_width=True):
        st.markdown("""
        <script>
        if ('caches' in window) {
            caches.keys().then(names => {
                names.forEach(name => caches.delete(name));
                alert('✅ All caches cleared! Reload page.');
            });
        }
        </script>
        """, unsafe_allow_html=True)
        st.success("Caches cleared!")

with col_fix3:
    st.markdown("### Reload PWA")
    if st.button("Force Reload", use_container_width=True):
        st.markdown("""
        <script>
        location.reload(true);
        </script>
        """, unsafe_allow_html=True)

# Instructions
st.markdown("---")
st.markdown("## 📖 Instructions")

with st.expander("How to fix PWA issues", expanded=False):
    st.markdown("""
    ### If Icons Don't Show:
    1. Uninstall PWA from home screen
    2. Clear browser cache
    3. Reload page
    4. Reinstall PWA
    
    ### If Notifications Don't Work:
    1. Click "Request Permission" button above
    2. Allow notifications in browser
    3. Check device notification settings
    4. Make sure "Do Not Disturb" is OFF
    
    ### If Sound Doesn't Play:
    1. Check device volume
    2. Make sure sound is not muted
    3. Try clicking "Play Sound" buttons above
    4. Check console for errors
    
    ### For Mobile:
    1. Install app on home screen first
    2. Open as PWA (not in browser)
    3. Test features using buttons above
    4. Check browser console for errors
    """)

# Back button
st.markdown("---")
if st.button("← Back to Landing Page", use_container_width=True):
    st.switch_page("pages/0_Landing.py")
