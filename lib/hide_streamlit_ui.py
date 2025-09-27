"""
Hide Streamlit UI Elements for Clean PWA Experience
This module provides CSS to hide Streamlit's default UI elements
"""

def get_hide_streamlit_ui_css():
    """Return CSS to hide Streamlit UI elements"""
    return """
    <style>
    /* Hide Streamlit header */
    .stApp > header {
        display: none !important;
    }
    
    /* Hide Streamlit toolbar */
    .stApp > div[data-testid="stToolbar"] {
        display: none !important;
    }
    
    /* Hide Streamlit sidebar */
    .stSidebar {
        display: none !important;
    }
    
    .stApp > div[data-testid="stSidebar"] {
        display: none !important;
    }
    
    .stApp > div[data-testid="stSidebar"] > div {
        display: none !important;
    }
    
    /* Hide Streamlit footer */
    .stApp > footer {
        display: none !important;
    }
    
    .stApp > div[data-testid="stFooter"] {
        display: none !important;
    }
    
    /* Hide Streamlit branding */
    .stApp > div[data-testid="stDecoration"] {
        display: none !important;
    }
    
    /* Hide Streamlit status bar */
    .stApp > div[data-testid="stStatusWidget"] {
        display: none !important;
    }
    
    /* Hide Streamlit download button area */
    .stApp > div[data-testid="stDownloadButton"] {
        display: none !important;
    }
    
    /* Hide Streamlit menu button */
    .stApp > div[data-testid="stMenuButton"] {
        display: none !important;
    }
    
    /* Make main content full width */
    .stApp > div[data-testid="stMain"] {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
    
    /* Hide Streamlit report error button */
    .stApp > div[data-testid="stReportError"] {
        display: none !important;
    }
    
    /* Hide Streamlit rerun button */
    .stApp > div[data-testid="stRerun"] {
        display: none !important;
    }
    
    /* Hide Streamlit file uploader area */
    .stApp > div[data-testid="stFileUploader"] {
        display: none !important;
    }
    
    /* Hide Streamlit expander */
    .stApp > div[data-testid="stExpander"] {
        border: none !important;
    }
    
    /* Custom full-screen app styling */
    .stApp {
        background: #ffffff !important;
    }
    
    /* Remove margins and padding from main content */
    .main .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }
    
    /* Hide Streamlit's default styling */
    .stApp > div[data-testid="stAppViewContainer"] {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Custom scrollbar for cleaner look */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #198A00;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #2BA300;
    }
    
    /* Hide any remaining Streamlit elements */
    [data-testid="stHeader"] {
        display: none !important;
    }
    
    [data-testid="stToolbar"] {
        display: none !important;
    }
    
    /* Ensure full height */
    html, body, #root, .stApp {
        height: 100% !important;
        overflow-x: hidden !important;
    }
    
    /* PWA-specific styling */
    @media (display-mode: standalone) {
        .stApp {
            padding-top: env(safe-area-inset-top) !important;
            padding-bottom: env(safe-area-inset-bottom) !important;
        }
        
        /* Hide any browser UI elements in PWA mode */
        .stApp > div[data-testid="stHeader"] {
            display: none !important;
        }
    }
    
    /* Mobile-specific adjustments */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }
        
        /* Ensure no horizontal scroll */
        .stApp {
            overflow-x: hidden !important;
        }
    }
    
    /* Hide Streamlit's default button styling that might show */
    .stApp > div[data-testid="stButton"] {
        /* Keep buttons but ensure they don't have Streamlit styling */
    }
    
    /* Custom app container */
    .app-container {
        min-height: 100vh;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Hide any remaining Streamlit debug info */
    .stApp > div[data-testid="stDebugger"] {
        display: none !important;
    }
    
    /* Ensure clean mobile experience */
    @media (max-width: 768px) {
        .stApp {
            -webkit-overflow-scrolling: touch !important;
        }
        
        /* Remove any touch callouts */
        * {
            -webkit-touch-callout: none !important;
            -webkit-user-select: none !important;
            -khtml-user-select: none !important;
            -moz-user-select: none !important;
            -ms-user-select: none !important;
            user-select: none !important;
        }
        
        /* Allow text selection in input fields */
        input, textarea, [contenteditable] {
            -webkit-user-select: text !important;
            -khtml-user-select: text !important;
            -moz-user-select: text !important;
            -ms-user-select: text !important;
            user-select: text !important;
        }
    }
    </style>
    """

def apply_hide_streamlit_ui():
    """Apply CSS to hide Streamlit UI elements"""
    import streamlit as st
    st.markdown(get_hide_streamlit_ui_css(), unsafe_allow_html=True)

def get_pwa_meta_tags():
    """Return PWA meta tags for clean app experience"""
    return """
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Insaka Conference">
    <meta name="application-name" content="Insaka Conference">
    <meta name="msapplication-TileColor" content="#198A00">
    <meta name="theme-color" content="#198A00">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    """

def apply_pwa_meta_tags():
    """Apply PWA meta tags"""
    import streamlit as st
    st.markdown(f"""
    <head>
        {get_pwa_meta_tags()}
    </head>
    """, unsafe_allow_html=True)
