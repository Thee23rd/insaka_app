# streamlit_app.py
from __future__ import annotations
import streamlit as st
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import required functions
from lib.qr_system import authenticate_with_qr_code, _normalize_qr_payload
from staff_service import load_staff_df

# Add PWA meta tags and service worker registration
st.markdown("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Insaka Conference 2025</title>
    
    <!-- PWA Meta Tags -->
    <meta name="application-name" content="Insaka Conference">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="apple-mobile-web-app-title" content="Insaka">
    <meta name="description" content="Zambian Mining and Investment Conference - Delegate Portal">
    <meta name="format-detection" content="telephone=no">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="msapplication-TileColor" content="#198A00">
    <meta name="msapplication-tap-highlight" content="no">
    <meta name="theme-color" content="#198A00">
    
    <!-- Apple Touch Icons -->
    <link rel="apple-touch-icon" href="/assets/pwa/icon-152x152.png">
    <link rel="apple-touch-icon" sizes="152x152" href="/assets/pwa/icon-152x152.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/pwa/icon-180x180.png">
    <link rel="apple-touch-icon" sizes="167x167" href="/assets/pwa/icon-167x167.png">
    
    <!-- Standard Icons -->
    <link rel="icon" type="image/png" sizes="32x32" href="/assets/pwa/icon-72x72.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/assets/pwa/icon-48x48.png">
    <link rel="shortcut icon" href="/assets/pwa/icon-96x96.png">
    
    <!-- PWA Manifest -->
    <link rel="manifest" href="/manifest.json">
    
    <style>
        /* Force dark theme and hide theme switcher */
        [data-testid="stHeader"] button[kind="header"] {
            display: none !important;
        }
        
        /* Hide theme toggle in settings menu */
        section[data-testid="stSidebar"] button[aria-label*="theme"],
        section[data-testid="stSidebar"] button[aria-label*="Theme"] {
            display: none !important;
        }
        
        /* PWA-specific styles */
        body {
            -webkit-user-select: none;
            -webkit-touch-callout: none;
            -webkit-tap-highlight-color: transparent;
        }
        
        /* Hide address bar on mobile */
        @media screen and (max-width: 768px) {
            body {
                padding-top: env(safe-area-inset-top);
                padding-bottom: env(safe-area-inset-bottom);
            }
        }
    </style>
</head>
<body>
    <script>
        // PWA Service Worker Registration
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', function() {
                navigator.serviceWorker.register('/sw.js')
                    .then(function(registration) {
                        console.log('✅ Insaka PWA: Service Worker registered successfully:', registration.scope);
                    })
                    .catch(function(error) {
                        console.log('❌ Insaka PWA: Service Worker registration failed:', error);
                    });
            });
        }
        
        // PWA Install Prompt
        let deferredPrompt;
        window.addEventListener('beforeinstallprompt', (e) => {
            console.log('📱 Insaka PWA: Install prompt triggered');
            e.preventDefault();
            deferredPrompt = e;
            
            // Show custom install button
            const installBtn = document.createElement('button');
            installBtn.innerHTML = '📱 Install Insaka App';
            installBtn.style.cssText = `
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: linear-gradient(135deg, #198A00, #2BA300);
                color: white;
                border: none;
                border-radius: 25px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: 600;
                cursor: pointer;
                box-shadow: 0 4px 12px rgba(25, 138, 0, 0.3);
                z-index: 1000;
                transition: all 0.3s ease;
            `;
            
            installBtn.addEventListener('click', async () => {
                if (deferredPrompt) {
                    deferredPrompt.prompt();
                    const { outcome } = await deferredPrompt.userChoice;
                    console.log(`📱 Insaka PWA: Install prompt outcome: ${outcome}`);
                    deferredPrompt = null;
                    installBtn.remove();
                }
            });
            
            document.body.appendChild(installBtn);
        });
        
        // Handle successful PWA installation
        window.addEventListener('appinstalled', (evt) => {
            console.log('✅ Insaka PWA: App installed successfully');
        });
        
        // Request notification permissions
        if ('Notification' in window && 'serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                setTimeout(() => {
                    if (Notification.permission === 'default') {
                        Notification.requestPermission().then(permission => {
                            console.log('🔔 Notification permission:', permission);
                            if (permission === 'granted') {
                                console.log('✅ Notification permission granted!');
                            }
                        });
                    }
                }, 3000); // Request after 3 seconds to avoid interrupting user
            });
        }
        
        // Notification sound playback function
        window.playNotificationSound = function() {
            try {
                const audio = new Audio('/app/static/assets/notification.wav');
                audio.volume = 1.0;
                audio.play().then(() => {
                    console.log('🔊 Notification sound played');
                }).catch(err => {
                    console.log('🔇 Sound play failed (needs user interaction):', err);
                });
            } catch (error) {
                console.error('❌ Sound playback error:', error);
            }
        };
        
        // Test notification function (for debugging)
        window.testNotification = function() {
            if (!('Notification' in window)) {
                console.error('❌ This browser does not support notifications');
                return;
            }
            
            if (Notification.permission === 'granted') {
                // Play sound first
                window.playNotificationSound();
                
                // Show notification
                const notification = new Notification('Insaka Conference', {
                    body: 'Test notification - This is a test message!',
                    icon: '/app/static/assets/pwa/icon-192x192.png',
                    badge: '/app/static/assets/pwa/icon-96x96.png',
                    vibrate: [200, 100, 200, 100, 200],
                    tag: 'test-notification'
                });
                
                notification.onclick = function() {
                    window.focus();
                    notification.close();
                };
                
                console.log('🔔 Test notification sent!');
            } else if (Notification.permission === 'default') {
                Notification.requestPermission().then(permission => {
                    if (permission === 'granted') {
                        window.testNotification();
                    }
                });
            } else {
                console.error('❌ Notification permission denied');
                alert('Please enable notifications in your browser settings to receive conference updates!');
            }
        };
        
        // Auto-play sound on any notification (for PWA)
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.addEventListener('message', event => {
                if (event.data && event.data.type === 'notification') {
                    window.playNotificationSound();
                }
            });
        }
    </script>
</body>
</html>
""", unsafe_allow_html=True)

# Check for QR data in URL parameters first
raw_param = st.query_params.get("qr_data")
if raw_param:
    qr_data_from_url = raw_param[0] if isinstance(raw_param, list) else raw_param
    if isinstance(qr_data_from_url, str) and qr_data_from_url.strip():
        st.success(f"🎉 QR Code detected! Processing...")
        
        # Load staff data
        try:
            staff_df = load_staff_df()
            if staff_df.empty:
                st.error("No delegate data found. Please contact administrator.")
                st.stop()
        except Exception as e:
            st.error(f"Error loading delegate data: {str(e)}")
            st.stop()
        
        # Normalize / parse (your helper)
        norm_text, payload = _normalize_qr_payload(qr_data_from_url)

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
                # Stage delegate for user-confirmed redirect on QR_Login page
                st.session_state.pending_delegate = delegate
                # Clear URL param to avoid re-auth on refresh
                try:
                    st.query_params.clear()
                except Exception:
                    pass
                # Navigate to QR Login to show confirmation card + big button
                try:
                    st.switch_page("pages/QR_Login.py")
                except Exception:
                    st.switch_page("QR_Login.py")
                st.stop()
            else:
                st.error(f"❌ {message}")
                # Clear the failed QR parameter and continue to landing page
                st.query_params.clear()
                st.rerun()

# Redirect to landing page
st.switch_page("pages/0_Landing.py")
