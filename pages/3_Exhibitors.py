import json, streamlit as st
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

st.markdown("# 🏢 Exhibitors")

st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

try:
    exhibitors = json.load(open("data/exhibitors.json","r",encoding="utf-8"))
except Exception:
    exhibitors = [
        {"name":"AgriTech Co.", "stand":"A12", "logo":"assets/logos/agritech.png", "url":"https://example.com"},
        {"name":"ZedFin", "stand":"B03", "logo":"assets/logos/zedfin.png", "url":"https://example.com"},
    ]

cols = st.columns(3)
for i, ex in enumerate(exhibitors):
    with cols[i % 3]:
        with st.container(border=True):
            if ex.get("logo"): st.image(ex["logo"], width='stretch')
            st.markdown(f"**{ex['name']}**  \nStand **{ex.get('stand','TBA')}**")
            if ex.get("url"):
                st.link_button("Visit website", ex["url"])

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
