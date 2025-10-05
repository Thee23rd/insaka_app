import json, streamlit as st
from lib.ui import apply_brand

st.set_page_config(page_title="Speakers — Insaka", page_icon="🎙️", layout="wide")

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
    
    /* Speaker tile styling */
    .speaker-tile {
        background: linear-gradient(145deg, rgba(26, 26, 26, 0.9) 0%, rgba(42, 42, 42, 0.8) 100%);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 2px solid rgba(25, 138, 0, 0.3);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .speaker-tile:hover {
        transform: translateY(-5px);
        border-color: rgba(25, 138, 0, 0.6);
        box-shadow: 0 8px 24px rgba(25, 138, 0, 0.4);
    }
</style>
""", unsafe_allow_html=True)

apply_brand()

# Zambian-themed header
st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

# Back button
if st.button("← Back to Dashboard", type="secondary"):
    st.switch_page("pages/1_Delegate_Dashboard.py")

# Welcome message
st.markdown("""
<div style="background: linear-gradient(135deg, #198A00 0%, #2BA300 50%, #D10000 100%); 
            color: white; padding: 2rem; border-radius: 20px; margin-bottom: 2rem; 
            text-align: center; box-shadow: 0 8px 32px rgba(25, 138, 0, 0.3);">
    <h1 style="color: white; margin-bottom: 0.5rem; font-size: 2.5rem; font-weight: 800;">
        🎙️ Conference Speakers
    </h1>
    <p style="color: #f0f8f0; margin: 0; font-size: 1.2rem; font-weight: 500;">
        Meet our distinguished speakers and industry experts
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

# Load speakers
try:
    speakers = json.load(open("data/speakers.json","r",encoding="utf-8"))
except Exception:
    speakers = []

# Search bar
st.markdown("### 🔍 Search Speakers")
search_term = st.text_input(
    "Search by name, organization, or topic",
    placeholder="Type to search...",
    label_visibility="collapsed"
)

# Filter speakers based on search
if search_term:
    filtered_speakers = [
        sp for sp in speakers 
        if (search_term.lower() in str(sp.get('name', '')).lower() or 
            search_term.lower() in str(sp.get('organization', '')).lower() or 
            search_term.lower() in str(sp.get('talk', '')).lower() or
            search_term.lower() in str(sp.get('position', '')).lower())
    ]
else:
    filtered_speakers = speakers

# Display count
st.caption(f"Showing {len(filtered_speakers)} speaker{'s' if len(filtered_speakers) != 1 else ''}")

st.markdown("---")

# Speaker bio popup
@st.dialog("Speaker Profile", width="large")
def show_speaker_details(speaker):
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if speaker.get("photo"):
            st.image(speaker["photo"], use_container_width=True)
        else:
            st.markdown("""
            <div style="background: #F3F4F6; border-radius: 10px; padding: 3rem; 
                       text-align: center; color: #666;">
                <span style="font-size: 5rem;">👤</span>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"### {speaker.get('name', '')}")
        
        if speaker.get('position'):
            st.markdown(f"**{speaker.get('position')}**")
        
        if speaker.get('organization'):
            st.markdown(f"💼 {speaker.get('organization')}")
        
        if speaker.get('talk'):
            st.markdown("---")
            st.markdown("**Presenting on:**")
            st.info(speaker.get('talk'))
        
        if speaker.get('bio'):
            st.markdown("---")
            st.markdown("**Biography:**")
            st.write(speaker.get('bio'))
        
        if speaker.get('slides'):
            st.markdown("---")
            try:
                st.download_button(
                    "📄 Download Presentation Slides",
                    data=open(speaker["slides"], "rb").read(),
                    file_name=speaker["slides"].split("/")[-1],
                    use_container_width=True
                )
            except:
                st.caption(f"Slides: {speaker['slides']}")

# Display speakers in grid
if filtered_speakers:
    # Create grid layout
    cols_per_row = 4
    
    for row_start in range(0, len(filtered_speakers), cols_per_row):
        row_speakers = filtered_speakers[row_start:row_start + cols_per_row]
        cols = st.columns(cols_per_row)
        
        for idx, speaker in enumerate(row_speakers):
            with cols[idx]:
                st.markdown('<div class="speaker-tile">', unsafe_allow_html=True)
                
                # Photo
                if speaker.get("photo"):
                    st.image(speaker["photo"], use_container_width=True)
                else:
                    st.markdown("""
                    <div style="background: #F3F4F6; border-radius: 10px; padding: 2rem; 
                               text-align: center; color: #666; min-height: 200px;
                               display: flex; align-items: center; justify-content: center;">
                        <span style="font-size: 4rem;">👤</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Name
                st.markdown(f"""
                <div style="color: #F3F4F6; font-size: 1.1rem; font-weight: 700; 
                           margin: 1rem 0 0.5rem 0;">
                    {speaker.get('name', 'Unknown')}
                </div>
                """, unsafe_allow_html=True)
                
                # Position
                if speaker.get('position'):
                    st.markdown(f"""
                    <div style="color: #F3F4F6; font-size: 0.9rem; font-weight: 500; margin: 0.5rem 0;">
                        {speaker.get('position')}
                    </div>
                    """, unsafe_allow_html=True)
                
                # Organization
                if speaker.get('organization'):
                    st.markdown(f"""
                    <div style="color: #2BA300; font-size: 0.85rem; font-weight: 600; margin-bottom: 1rem;">
                        💼 {speaker.get('organization')}
                    </div>
                    """, unsafe_allow_html=True)
                
                # View profile button
                if st.button("View Profile", key=f"speaker_{speaker.get('name', '')}_{row_start}_{idx}", use_container_width=True):
                    show_speaker_details(speaker)
                
                st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("No speakers found matching your search. Try different keywords.")

# Footer with logout button
st.markdown("---")
col_footer1, col_footer2, col_footer3 = st.columns([2, 1, 2])
with col_footer1:
    st.caption("Connect with our speakers at the conference")
with col_footer2:
    if hasattr(st.session_state, 'delegate_authenticated') and st.session_state.delegate_authenticated:
        if st.button("Logout", width='stretch', key="speakers_logout"):
            # Clear all session state
            for key in list(st.session_state.keys()):
                if key.startswith('delegate_'):
                    del st.session_state[key]
            st.success("Logged out successfully!")
            st.switch_page("pages/0_Landing.py")