import json, streamlit as st
from lib.ui import apply_brand

st.set_page_config(page_title="Sponsors — Insaka", page_icon="🤝", layout="wide")

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
    
    /* Remove extra padding from containers */
    .stContainer {
        padding: 0 !important;
    }
    
    /* Reduce spacing between columns */
    [data-testid="column"] {
        padding: 0.5rem !important;
    }
</style>
""", unsafe_allow_html=True)

apply_brand()

# Zambian-themed header
st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

# Back button
if st.button("← Back to Dashboard", type="secondary"):
    st.switch_page("pages/1_Delegate_Dashboard.py")

st.markdown("# Our Sponsors")

st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

# Load sponsors data
try:
    sponsors = json.load(open("data/sponsors.json","r",encoding="utf-8"))
except Exception:
    sponsors = {
        "Platinum":[{"name":"ZNBC","logo":"assets/logos/znbc.png"}],
        "Gold":[{"name":"ZESCO","logo":"assets/logos/zesco.png"}],
        "Silver":[{"name":"BoZ","logo":"assets/logos/boz.png"}]
    }

# Tier order for display
tier_order = ["Platinum", "Gold", "Silver", "Bronze"]

tier_colors = {
    "Platinum": "#E5E4E2",
    "Gold": "#FFD700",
    "Silver": "#C0C0C0",
    "Bronze": "#CD7F32"
}

# Display each tier
for tier in tier_order:
    if tier in sponsors and sponsors[tier]:
        items = sponsors[tier]
        tier_color = tier_colors.get(tier, "#CD7F32")
        
        # Tier header
        st.markdown(f"### {tier} Tier")
        st.markdown("---")
        
        # Create horizontal scrollable layout
        cols = st.columns(len(items) if len(items) <= 6 else 6)
        
        for idx, sponsor in enumerate(items):
            col_idx = idx % len(cols)
            with cols[col_idx]:
                # Sponsor name at top
                st.markdown(f"""
                <div style="color: #F3F4F6; font-size: 0.95rem; font-weight: 700; 
                           margin-bottom: 0.5rem; text-align: center;">
                    {sponsor.get("name", "")}
                </div>
                """, unsafe_allow_html=True)
                
                # Tier badge
                st.markdown(f"""
                <div style="background: {tier_color}; 
                           color: {'#1A1A1A' if tier in ['Platinum', 'Gold', 'Silver'] else 'white'}; 
                           padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.65rem; 
                           font-weight: 700; text-transform: uppercase; 
                           display: inline-block; margin-bottom: 0.75rem;">
                    {tier}
                </div>
                """, unsafe_allow_html=True)
                
                # Logo in white box - compact
                if sponsor.get("logo"):
                    try:
                        st.image(sponsor["logo"], use_container_width=True)
                    except Exception as e:
                        st.markdown(f"""
                        <div style="background: #F3F4F6; border-radius: 8px; padding: 1rem; 
                                   height: 120px; display: flex; align-items: center; 
                                   justify-content: center; color: #666; font-size: 0.9rem;">
                            {sponsor.get("name", "")}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: #F3F4F6; border-radius: 8px; padding: 1rem; 
                               height: 120px; display: flex; align-items: center; 
                               justify-content: center; color: #198A00; 
                               font-weight: 700; font-size: 1rem;">
                        {sponsor.get("name", "")}
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("")  # Just spacing

# Display other tiers
other_tiers = [tier for tier in sponsors.keys() if tier not in tier_order]
for tier in other_tiers:
    if sponsors[tier]:
        items = sponsors[tier]
        
        st.markdown(f"### {tier} Tier")
        st.markdown("---")
        
        cols = st.columns(len(items) if len(items) <= 6 else 6)
        
        for idx, sponsor in enumerate(items):
            col_idx = idx % len(cols)
            with cols[col_idx]:
                st.markdown(f"""
                <div style="color: #F3F4F6; font-size: 0.95rem; font-weight: 700; 
                           margin-bottom: 0.5rem; text-align: center;">
                    {sponsor.get("name", "")}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="background: #198A00; color: white; 
                           padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.65rem; 
                           font-weight: 700; text-transform: uppercase; 
                           display: inline-block; margin-bottom: 0.75rem;">
                    {tier}
                </div>
                """, unsafe_allow_html=True)
                
                if sponsor.get("logo"):
                    try:
                        st.image(sponsor["logo"], use_container_width=True)
                    except:
                        st.markdown(f"""
                        <div style="background: #F3F4F6; border-radius: 8px; padding: 1rem; 
                                   height: 120px; display: flex; align-items: center; 
                                   justify-content: center; color: #666; font-size: 0.9rem;">
                            {sponsor.get("name", "")}
                        </div>
                        """, unsafe_allow_html=True)
        
        st.markdown("")  # Just spacing

# Thank you message
st.markdown("---")
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(25, 138, 0, 0.15) 0%, rgba(209, 0, 0, 0.15) 100%); 
            border: 2px solid rgba(25, 138, 0, 0.4); border-radius: 20px; 
            padding: 3rem; text-align: center; margin: 2rem 0;
            box-shadow: 0 8px 24px rgba(25, 138, 0, 0.2);">
    <h2 style="color: #2BA300; font-size: 2rem; font-weight: 800; margin-bottom: 1.5rem;">
        Thank You to All Our Sponsors
    </h2>
    <p style="color: #F3F4F6; font-size: 1.15rem; line-height: 1.8; margin: 0; max-width: 800px; margin: 0 auto;">
        Your generous support and partnership make the Zambian Mining and Investment Insaka Conference 2025 possible. 
        Together, we are driving innovation, fostering collaboration, and shaping the future of Zambia's mining industry.
    </p>
</div>
""", unsafe_allow_html=True)

# Footer with logout button
st.markdown("---")
col_footer1, col_footer2, col_footer3 = st.columns([2, 1, 2])
with col_footer1:
    st.caption("Thank you to our valued sponsors")
with col_footer2:
    if hasattr(st.session_state, 'delegate_authenticated') and st.session_state.delegate_authenticated:
        if st.button("Logout", width='stretch', key="sponsors_logout"):
            # Clear all session state
            for key in list(st.session_state.keys()):
                if key.startswith('delegate_'):
                    del st.session_state[key]
            st.success("Logged out successfully!")
            st.switch_page("pages/0_Landing.py")