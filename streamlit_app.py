# streamlit_app.py
from __future__ import annotations
import streamlit as st
from lib.hide_streamlit_ui import apply_hide_streamlit_ui, apply_pwa_meta_tags

# Hide Streamlit UI elements for clean PWA experience
apply_hide_streamlit_ui()

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
    </script>
</body>
</html>
""", unsafe_allow_html=True)

# Redirect to landing page
st.switch_page("pages/0_Landing.py")
