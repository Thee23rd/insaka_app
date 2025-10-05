import json, streamlit as st
from lib.ui import apply_brand
from pathlib import Path
from datetime import datetime, timedelta
import re

st.set_page_config(page_title="Event Schedule — Insaka", page_icon="🗓️", layout="wide")

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
    
    /* Modern Calendar Styling */
    .modern-calendar {
        display: flex;
        gap: 1.5rem;
        margin: 2rem 0;
        overflow-x: auto;
        padding-bottom: 1rem;
    }
    
    .day-column {
        flex: 1;
        min-width: 280px;
        background: linear-gradient(145deg, rgba(26, 26, 26, 0.9) 0%, rgba(42, 42, 42, 0.8) 100%);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(25, 138, 0, 0.2);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .day-column:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(25, 138, 0, 0.3);
        border-color: rgba(25, 138, 0, 0.4);
    }
    
    .day-header {
        background: linear-gradient(135deg, #198A00 0%, #2BA300 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 15px;
        text-align: center;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(25, 138, 0, 0.4);
        letter-spacing: 0.5px;
    }
    
    .day-subheader {
        color: #FFD700;
        font-size: 0.85rem;
        margin-top: 0.25rem;
        opacity: 0.9;
    }
    
    .event-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);
        border-radius: 15px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        border-left: 5px solid;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .event-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, transparent 0%, rgba(255, 255, 255, 0.1) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .event-card:hover::before {
        opacity: 1;
    }
    
    .event-card:hover {
        transform: translateX(8px) scale(1.02);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
    }
    
    .event-type-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        color: white;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        margin-bottom: 0.75rem;
    }
    
    .event-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #F3F4F6;
        margin: 0.75rem 0 0.5rem 0;
        line-height: 1.4;
    }
    
    .event-time {
        display: inline-flex;
        align-items: center;
        font-size: 0.85rem;
        color: #FFD700;
        font-weight: 600;
        margin-bottom: 0.5rem;
        padding: 0.3rem 0.8rem;
        background: rgba(255, 215, 0, 0.1);
        border-radius: 8px;
        margin-right: 0.5rem;
    }
    
    .event-room {
        display: inline-flex;
        align-items: center;
        font-size: 0.85rem;
        color: #2BA300;
        font-weight: 600;
        padding: 0.3rem 0.8rem;
        background: rgba(43, 163, 0, 0.1);
        border-radius: 8px;
    }
    
    .event-description {
        color: rgba(243, 244, 246, 0.7);
        font-size: 0.85rem;
        margin: 0.75rem 0;
        line-height: 1.5;
    }
    
    .speaker-list {
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .speaker-mini {
        display: inline-flex;
        align-items: center;
        background: linear-gradient(135deg, rgba(25, 138, 0, 0.15) 0%, rgba(43, 163, 0, 0.1) 100%);
        padding: 0.5rem 1rem;
        border-radius: 25px;
        margin: 0.25rem;
        border: 1px solid rgba(25, 138, 0, 0.3);
        transition: all 0.2s ease;
        cursor: pointer;
        font-size: 0.85rem;
    }
    
    .speaker-mini:hover {
        background: linear-gradient(135deg, rgba(25, 138, 0, 0.3) 0%, rgba(43, 163, 0, 0.2) 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(25, 138, 0, 0.3);
    }
    
    .speaker-mini img {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        margin-right: 0.5rem;
        border: 2px solid rgba(25, 138, 0, 0.5);
        object-fit: cover;
    }
    
    .empty-slot {
        text-align: center;
        padding: 2rem;
        color: rgba(243, 244, 246, 0.3);
        font-style: italic;
    }
    
    /* Timeline view */
    .timeline-container {
        position: relative;
        padding: 2rem 0;
    }
    
    .timeline-item {
        display: flex;
        gap: 2rem;
        margin-bottom: 2rem;
        position: relative;
    }
    
    .timeline-time {
        min-width: 120px;
        text-align: right;
        font-weight: 700;
        font-size: 1.2rem;
        color: #2BA300;
        padding-top: 1rem;
    }
    
    .timeline-dot {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        border: 4px solid;
        background: #0A0A0A;
        position: relative;
        margin-top: 1.5rem;
        z-index: 2;
    }
    
    .timeline-line {
        position: absolute;
        left: 130px;
        top: 0;
        bottom: -2rem;
        width: 3px;
        background: linear-gradient(180deg, rgba(25, 138, 0, 0.5) 0%, rgba(25, 138, 0, 0.1) 100%);
    }
    
    .timeline-content {
        flex: 1;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .modern-calendar {
            flex-direction: column;
        }
        
        .day-column {
            min-width: 100%;
        }
    }
</style>
""", unsafe_allow_html=True)

apply_brand()

# Zambian-themed header
st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

# Back button
if st.button("← Back to Dashboard", type="secondary"):
    st.switch_page("pages/1_Delegate_Dashboard.py")

st.markdown("# 📅 Event Schedule")

st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

# Segment type colors
SEGMENT_COLORS = {
    "keynote": "#D10000",        # Zambian red
    "presentation": "#198A00",   # Zambian green
    "panel": "#FF9500",          # Orange
    "break": "#FFD700",          # Gold
    "networking": "#2BA300",     # Light green
    "workshop": "#8B4513",       # Brown
    "closing": "#D10000",        # Red
    "other": "#666666"           # Gray
}

# Load agenda
try:
    agenda = json.load(open("data/agenda.json", "r", encoding="utf-8"))
except Exception:
    agenda = []

# Load speakers for bio popup
try:
    all_speakers = json.load(open("data/speakers.json", "r", encoding="utf-8"))
except Exception:
    all_speakers = []

# Create speaker lookup dict
speakers_dict = {sp.get("name", ""): sp for sp in all_speakers}

# Speaker bio popup using dialog
@st.dialog("🎙️ Speaker Biography", width="large")
def show_speaker_bio(speaker_name):
    speaker = speakers_dict.get(speaker_name)
    if speaker:
        col1, col2 = st.columns([1, 2])
        with col1:
            if speaker.get("photo"):
                st.image(speaker["photo"], use_container_width=True)
            else:
                st.markdown("### 👤")
        with col2:
            st.markdown(f"### {speaker.get('name', '')}")
            
            # Helper function to check if value is valid
            def is_valid(value):
                if not value:
                    return False
                if isinstance(value, str) and value.strip().lower() in ['nan', 'n/a', 'none', '']:
                    return False
                return True
            
            # Show position and organization only if valid
            position = speaker.get("position")
            organization = speaker.get("organization")
            
            if is_valid(position) and is_valid(organization):
                st.caption(f"{position} at {organization}")
            elif is_valid(position):
                st.caption(position)
            elif is_valid(organization):
                st.caption(organization)
            
            # Show talk/presentation topic only if valid
            talk = speaker.get('talk')
            if is_valid(talk):
                st.markdown(f"**Presenting on:** {talk}")
            
            # Show bio only if valid
            bio = speaker.get("bio")
            if is_valid(bio):
                st.markdown("---")
                st.markdown(bio)
            
            # Show slides download only if valid
            slides = speaker.get("slides")
            if is_valid(slides):
                st.markdown("---")
                try:
                    st.download_button(
                        "📄 Download Slides",
                        data=open(slides, "rb").read(),
                        file_name=slides.split("/")[-1],
                        use_container_width=True
                    )
                except Exception:
                    st.caption(f"Slides: {slides}")
    else:
        st.warning(f"Speaker '{speaker_name}' not found in database.")

# Parse time to hour (for sorting)
def parse_time_to_hour(time_str):
    """Convert time string to hour (24-hour format) in minutes from midnight"""
    try:
        time_str = str(time_str).strip().upper()
        
        # Skip invalid times
        if time_str in ['NAN', 'N/A', '', 'TBA']:
            return 540  # Default to 9 AM
        
        time_str = re.sub(r'\s+', ' ', time_str)
        
        # Handle time ranges (e.g., "07:00 - 13:00") - extract start time
        if '-' in time_str or '–' in time_str:
            time_str = time_str.split('-')[0].split('–')[0].strip()
        
        # Handle "TO" in time ranges
        if 'TO' in time_str:
            time_str = time_str.split('TO')[0].strip()
        
        # Parse different time formats
        if 'AM' in time_str or 'PM' in time_str:
            # 12-hour format with AM/PM
            time_str_clean = time_str.replace('AM', ' AM').replace('PM', ' PM')
            time_str_clean = re.sub(r'\s+', ' ', time_str_clean)
            time_obj = datetime.strptime(time_str_clean.strip(), "%I:%M %p")
        else:
            # 24-hour format
            # Extract just the time part (HH:MM)
            time_match = re.search(r'(\d{1,2}):(\d{2})', time_str)
            if time_match:
                time_obj = datetime.strptime(time_match.group(0), "%H:%M")
            else:
                return 540  # Default to 9 AM
        
        return time_obj.hour * 60 + time_obj.minute
    except Exception as e:
        return 540  # Default to 9 AM if parsing fails

# Get unique days and sort them
days = sorted(set([item.get("day", "TBA") for item in agenda]))

if not days:
    st.info("No events scheduled yet. Check back soon!")
else:
    # View toggle
    view_mode = st.radio("View Mode:", ["🎨 Modern Calendar", "⏱️ Timeline View"], horizontal=True, key="view_toggle")
    
    if view_mode == "🎨 Modern Calendar":
        # Date tabs for navigation
        st.markdown("### 📅 Select Date")
        selected_day = st.radio(
            "Choose a day:",
            options=days,
            horizontal=True,
            label_visibility="collapsed",
            key="day_selector"
        )
        
        st.markdown("---")
        
        # Show only selected day
        day = selected_day
        day_items = sorted(
            [a for a in agenda if a.get("day") == day],
            key=lambda x: parse_time_to_hour(x.get("time", "09:00"))
        )
        
        # Count events
        event_count = len(day_items)
        
        # Single column for selected day
        st.markdown(f"""
        <div style="max-width: 800px; margin: 0 auto;">
            <div class="day-column">
                <div class="day-header">
                    {day}
                    <div class="day-subheader">{event_count} Event{'s' if event_count != 1 else ''}</div>
                </div>
        """, unsafe_allow_html=True)
        
        if not day_items:
            st.markdown('<div class="empty-slot">No events scheduled</div>', unsafe_allow_html=True)
        else:
            for event_idx, event in enumerate(day_items):
                segment_type = event.get("segment_type", "other")
                color = SEGMENT_COLORS.get(segment_type, SEGMENT_COLORS["other"])
                
                speakers_list = event.get("speakers", [])
                speakers_list = [s.strip().lstrip(',').strip() for s in speakers_list if s.strip().lstrip(',').strip()]
                
                st.markdown(f"""
                <div class="event-card" style="border-left-color: {color};">
                    <div class="event-type-badge" style="background: {color};">{segment_type}</div>
                    <div class="event-title">{event.get('title', 'Untitled')}</div>
                    <div>
                        <span class="event-time">⏰ {event.get('time', 'TBA')}</span>
                        <span class="event-room">📍 {event.get('room', 'TBA')}</span>
                    </div>
                """, unsafe_allow_html=True)
                
                if event.get("description"):
                    st.markdown(f'<div class="event-description">{event["description"]}</div>', unsafe_allow_html=True)
                
                if speakers_list:
                    st.markdown('<div class="speaker-list">', unsafe_allow_html=True)
                    
                    for speaker_idx, speaker_name in enumerate(speakers_list):
                        speaker = speakers_dict.get(speaker_name)
                        col1, col2 = st.columns([1, 5])
                        
                        with col1:
                            if speaker and speaker.get("photo"):
                                st.image(speaker["photo"], width=40)
                            else:
                                st.markdown("👤")
                        
                        with col2:
                            # Create unique key using day, event index, speaker index, and speaker name
                            unique_key = f"speaker_{day}_{event_idx}_{speaker_idx}_{speaker_name.replace(' ', '_').replace('.', '_')}"
                            if st.button(
                                speaker_name,
                                key=unique_key,
                                use_container_width=True
                            ):
                                show_speaker_bio(speaker_name)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div></div>', unsafe_allow_html=True)
        
        # Legend
        st.markdown("---")
        st.markdown("### 🎨 Event Types")
        cols = st.columns(4)
        legend_items = [
            ("keynote", "🔴 Keynote"),
            ("presentation", "🟢 Presentation"),
            ("panel", "🟠 Panel"),
            ("break", "🟡 Break"),
            ("networking", "🟢 Networking"),
            ("workshop", "🟤 Workshop"),
            ("closing", "🔴 Closing"),
            ("other", "⚫ Other")
        ]
        for idx, (seg_type, label) in enumerate(legend_items):
            with cols[idx % 4]:
                color = SEGMENT_COLORS.get(seg_type, "#666666")
                st.markdown(f'<span style="color: {color}; font-weight: bold;">{label}</span>', unsafe_allow_html=True)
    
    else:  # Timeline View
        # Date tabs for navigation
        st.markdown("### 📅 Select Date")
        selected_day_timeline = st.radio(
            "Choose a day:",
            options=days,
            horizontal=True,
            label_visibility="collapsed",
            key="day_selector_timeline"
        )
        
        st.markdown("---")
        st.markdown("### Daily Timeline")
        
        # Show only selected day
        day = selected_day_timeline
        st.markdown(f"## 📆 {day}")
        
        day_items = sorted(
            [a for a in agenda if a.get("day") == day],
            key=lambda x: parse_time_to_hour(x.get("time", "09:00"))
        )
        
        st.markdown('<div class="timeline-container"><div class="timeline-line"></div>', unsafe_allow_html=True)
        
        for idx, item in enumerate(day_items):
            segment_type = item.get("segment_type", "other")
            color = SEGMENT_COLORS.get(segment_type, SEGMENT_COLORS["other"])
            
            st.markdown(f"""
            <div class="timeline-item">
                <div class="timeline-time">{item.get('time', 'TBA')}</div>
                <div class="timeline-dot" style="border-color: {color};"></div>
                <div class="timeline-content">
            """, unsafe_allow_html=True)
            
            with st.container():
                st.markdown(f"""
                <div class="event-card" style="border-left-color: {color};">
                    <div class="event-type-badge" style="background: {color};">{segment_type}</div>
                    <div class="event-title">{item.get('title', 'Untitled')}</div>
                    <div class="event-room">📍 {item.get('room', 'TBA')}</div>
                """, unsafe_allow_html=True)
                
                if item.get("description"):
                    st.markdown(f'<div class="event-description">{item["description"]}</div>', unsafe_allow_html=True)
                
                speakers = item.get("speakers", [])
                speakers = [s.strip().lstrip(',').strip() for s in speakers if s.strip().lstrip(',').strip()]
                
                if speakers:
                    st.markdown("**🎙️ Speakers:**")
                    cols = st.columns(min(len(speakers), 3))
                    for idx2, speaker_name in enumerate(speakers):
                        with cols[idx2 % 3]:
                            speaker = speakers_dict.get(speaker_name)
                            if speaker:
                                col_img, col_btn = st.columns([1, 4])
                                with col_img:
                                    if speaker.get("photo"):
                                        st.image(speaker["photo"], width=40)
                                    else:
                                        st.markdown("👤")
                                with col_btn:
                                    if st.button(
                                        speaker_name,
                                        key=f"timeline_speaker_{day}_{item.get('time')}_{speaker_name}",
                                        use_container_width=True
                                    ):
                                        show_speaker_bio(speaker_name)
                            else:
                                st.caption(f"👤 {speaker_name}")
                
                facilitators = item.get("facilitators", [])
                if facilitators:
                    st.markdown("**👥 Facilitators:**")
                    st.caption(" · ".join(facilitators))
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div></div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Footer with logout button
st.markdown("---")
col_footer1, col_footer2, col_footer3 = st.columns([2, 1, 2])
with col_footer1:
    st.caption("Need help? Contact the conference organizers or visit the registration desk.")
with col_footer2:
    if hasattr(st.session_state, 'delegate_authenticated') and st.session_state.delegate_authenticated:
        if st.button("🚪 Logout", width='stretch', key="agenda_logout"):
            # Clear all session state
            for key in list(st.session_state.keys()):
                if key.startswith('delegate_'):
                    del st.session_state[key]
            st.success("✅ Logged out successfully!")
            st.switch_page("pages/0_Landing.py")