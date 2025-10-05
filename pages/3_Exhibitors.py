import json, streamlit as st
import pandas as pd
from lib.ui import apply_brand

st.set_page_config(page_title="Exhibitors — Insaka", page_icon="🏢", layout="wide")

# Hide sidebar and navigation for delegates
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

# Back button
if st.button("← Back to Dashboard", type="secondary"):
    st.switch_page("pages/1_Delegate_Dashboard.py")

st.markdown("# 🏢 Conference Exhibitors")
st.markdown("### Explore Our Exhibition Booths")

st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

# Add custom CSS for exhibitor styling
st.markdown("""
<style>
    /* Style for Streamlit containers in exhibitor section */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
        border-radius: 15px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    /* Hover effect for containers */
    div[data-testid="stVerticalBlock"]:hover > div[data-testid="stVerticalBlock"] {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(25, 138, 0, 0.15);
    }
    
    /* Style for exhibitor images */
    div[data-testid="stImage"] img {
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        max-height: 120px !important;
        object-fit: contain !important;
    }
    
    /* Center align content in exhibitor cards */
    div[data-testid="stMarkdownContainer"] {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

try:
    exhibitors = json.load(open("data/exhibitors.json","r",encoding="utf-8"))
except Exception:
    exhibitors = [
        {"name":"AgriTech Co.", "stand":"A12", "logo":"assets/logos/agritech.png"},
        {"name":"ZedFin", "stand":"B03", "logo":"assets/logos/zedfin.png"},
    ]

# Filter out exhibitors with empty names or invalid data
valid_exhibitors = []
for ex in exhibitors:
    if ex.get("name") and str(ex.get("name")).strip() and str(ex.get("name")).lower() not in ['nan', 'none', '']:
        valid_exhibitors.append(ex)

if valid_exhibitors:
    
    # Create grid layout
    cols = st.columns(3)
    for i, ex in enumerate(valid_exhibitors):
        with cols[i % 3]:
            # Clean up stand information
            stand = ex.get('stand', 'TBA')
            if pd.isna(stand) or str(stand).lower() in ['nan', 'none', '', 'tba']:
                stand = 'TBA'
                stand_class = 'tba'
            else:
                stand_class = ''
            
            # Clean up logo path
            logo_path = ex.get('logo', '')
            has_logo = logo_path and str(logo_path).lower() not in ['nan', 'none', ''] and logo_path.strip()
            
            # Create exhibitor card using Streamlit container
            with st.container(border=True):
                # Logo section
                if has_logo:
                    try:
                        st.image(logo_path, use_container_width=True)
                    except Exception:
                        st.markdown("""
                        <div style="height: 120px; display: flex; align-items: center; justify-content: center; 
                                    background: #f0f0f0; border-radius: 10px; color: #666; font-size: 3rem;">
                            🏢
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="height: 120px; display: flex; align-items: center; justify-content: center; 
                                background: #f0f0f0; border-radius: 10px; color: #666; font-size: 3rem;">
                        🏢
                    </div>
                    """, unsafe_allow_html=True)
                
                # Company name
                st.markdown(f"**{ex['name']}**")
                
                # Stand information
                if stand == 'TBA':
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #666666 0%, #888888 100%); 
                                color: white; padding: 0.5rem 1rem; border-radius: 20px; 
                                font-weight: 600; font-size: 0.9rem; text-align: center; margin-top: 1rem;">
                        Stand {stand}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #198A00 0%, #2BA300 100%); 
                                color: white; padding: 0.5rem 1rem; border-radius: 20px; 
                                font-weight: 600; font-size: 0.9rem; text-align: center; margin-top: 1rem;">
                        Stand {stand}
                    </div>
                    """, unsafe_allow_html=True)
else:
    st.info("📋 Exhibitor information will be available soon. Check back for updates on our exhibition partners!")


# Footer with logout button
st.markdown("---")
col_footer1, col_footer2, col_footer3 = st.columns([2, 1, 2])
with col_footer1:
    st.caption("Need help? Contact the conference organizers or visit the registration desk.")
with col_footer2:
    if hasattr(st.session_state, 'delegate_authenticated') and st.session_state.delegate_authenticated:
        if st.button("🚪 Logout", width='stretch', key="exhibitors_logout"):
            # Clear all session state
            for key in list(st.session_state.keys()):
                if key.startswith('delegate_'):
                    del st.session_state[key]
            st.success("✅ Logged out successfully!")
            st.switch_page("pages/0_Landing.py")
