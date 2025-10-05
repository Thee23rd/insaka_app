import streamlit as st
from lib.ui import apply_brand

st.set_page_config(page_title="Venue — Insaka", page_icon="🗺️", layout="wide")

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

st.markdown("# 🗺️ Conference Venue & Navigation")
st.markdown("### 📍 Insaka Mining Conference - October 6-8, 2025")

st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

# Event-specific venue information
st.markdown("## 📍 Event Location")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    **Venue:** Mulungushi International Conference Center  
    **Address:** Independence Avenue, Lusaka, Zambia  
    **Event Dates:** October 6-8, 2025  
    **Registration:** 07:00 - 13:00 (Day 1)  
    
    **GPS Coordinates:** -15.3875, 28.3228  
    **Main Contact:** +260 211 254 442  
    """)

with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #198A00 0%, #2BA300 100%); 
                color: white; padding: 1.5rem; border-radius: 15px; text-align: center;">
        <h4>🎫 Event Badge Required</h4>
        <p>Please wear your conference badge at all times for venue access</p>
    </div>
    """, unsafe_allow_html=True)

# Conference Schedule Overview
st.markdown("---")
st.markdown("## 📅 Daily Schedule Overview")

schedule_col1, schedule_col2, schedule_col3 = st.columns(3)

with schedule_col1:
    st.markdown("""
    ### 📅 Monday, Oct 6
    **🌅 Registration Day**
    - **07:00-13:00** Registration & Accreditation
    - **08:00** CEO's Round Table
    - **09:30-12:30** Opening Sessions
    - **Afternoon** Panel Discussions
    """)

with schedule_col2:
    st.markdown("""
    ### 📅 Tuesday, Oct 7
    **🎯 Main Conference**
    - **08:30-09:00** Arrival & Networking
    - **09:00-12:30** Keynote Sessions
    - **14:00-17:30** Technical Sessions
    - **19:00-22:00** Networking Dinner
    """)

with schedule_col3:
    st.markdown("""
    ### 📅 Wednesday, Oct 8
    **🤝 Networking & Closing**
    - **09:30-12:45** Final Sessions
    - **14:00-16:30** Workshops
    - **15:00-16:30** Closing Ceremony
    - **Evening** Departure
    """)

# Event-Specific Services
st.markdown("---")
st.markdown("## 🎯 Conference Services")

services_col1, services_col2 = st.columns(2)

with services_col1:
    st.markdown("""
    ### 🎫 Registration & Check-in
    - **Location:** Main Entrance Lobby
    - **Hours:** 07:00 - 13:00 (Day 1)
    - **Required:** Valid ID and confirmation
    - **Badge Collection:** On-site printing available
    
    ### 📱 Conference App Support
    - **Help Desk:** Available throughout event
    - **WiFi:** Network details provided at registration
    - **Technical Support:** IT assistance available
    """)

with services_col2:
    st.markdown("""
    ### 🍽️ Catering & Refreshments
    - **Coffee Breaks:** 10:00 & 15:00 daily
    - **Lunch:** 12:30 - 14:00 daily
    - **Networking Dinner:** Tuesday evening
    - **Special Diets:** Pre-arranged only
    
    ### 🚗 Parking & Transportation
    - **Delegate Parking:** Complimentary
    - **Shuttle Service:** From major hotels
    - **Taxi Coordination:** Available at reception
    """)

# Room Assignments (Pending Confirmation)
st.markdown("---")
st.markdown("## 🏢 Room Assignments")

st.info("📋 **Room Assignments:** Final room allocations are being confirmed. This section will be updated with specific room details and navigation once available.")

# Temporary room structure
room_col1, room_col2 = st.columns(2)

with room_col1:
    st.markdown("""
    ### 🎪 Main Sessions
    **Main Conference Hall**
    - Opening Ceremony
    - Keynote Presentations
    - CEO's Round Table
    - Closing Ceremony
    
    **Exhibition Area**
    - Sponsor Booths
    - Networking Spaces
    - Coffee Break Areas
    """)

with room_col2:
    st.markdown("""
    ### 🏢 Breakout Sessions
    **Room A** *(To be confirmed)*
    - Panel Discussions
    - Technical Sessions
    
    **Room B** *(To be confirmed)*
    - Workshops
    - Smaller Group Sessions
    
    **Meeting Rooms**
    - Private Meetings
    - Media Interviews
    """)

# Important Information for Delegates
st.markdown("---")
st.markdown("## ⚠️ Important Information")

important_col1, important_col2 = st.columns(2)

with important_col1:
    st.markdown("""
    ### 📋 What to Bring
    - **Valid Photo ID** (required for registration)
    - **Conference Confirmation** (email or printed)
    - **Business Cards** (for networking)
    - **Mobile Device** (for conference app)
    - **Notebook & Pen** (for sessions)
    
    ### 🎫 Badge & Access
    - **Wear badge at all times** within venue
    - **Different access levels** for different areas
    - **Lost badges** can be replaced at registration
    """)

with important_col2:
    st.markdown("""
    ### ⏰ Key Times
    - **Registration Opens:** 07:00 (Day 1)
    - **First Session:** 08:00 (CEO's Round Table)
    - **Coffee Breaks:** 10:00 & 15:00
    - **Lunch:** 12:30 - 14:00
    - **Networking Dinner:** 19:00 (Day 2)
    
    ### 📱 WiFi & Technology
    - **Network Name:** [To be provided at registration]
    - **Password:** [To be provided at registration]
    - **Charging Stations:** Available throughout venue
    """)

# Contact & Support
st.markdown("---")
st.markdown("## 📞 Conference Support")

contact_col1, contact_col2 = st.columns(2)

with contact_col1:
    st.markdown("""
    ### 🎯 Event Support
    **Registration Desk:** Main Lobby  
    **Hours:** 07:00 - 18:00 (All Days)  
    **Help with:** Badge issues, room directions, general inquiries  
    
    ### 📱 Technical Support
    **IT Help Desk:** [Location TBD]  
    **WiFi Issues:** On-site technical team  
    **App Support:** Available throughout event  
    """)

with contact_col2:
    st.markdown("""
    ### 🚨 Emergency Contacts
    **Police:** 999  
    **Ambulance:** 992  
    **Fire:** 993  
    **Venue Security:** [To be provided]  
    
    ### 🏥 Medical Support
    **First Aid Station:** Available on-site  
    **Nearest Hospital:** University Teaching Hospital (8km)  
    **Emergency:** +260 211 256 067  
    """)

# Floor Plan Coming Soon
st.markdown("---")
st.markdown("## 🗺️ Floor Plan & Navigation")

st.info("📋 **Coming Soon:** Detailed floor plan with room locations and navigation will be available once room assignments are confirmed.")

floor_plan_placeholder = st.container()
with floor_plan_placeholder:
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(25, 138, 0, 0.1) 0%, rgba(43, 163, 0, 0.1) 100%); 
                border: 2px dashed #198A00; padding: 2rem; border-radius: 15px; text-align: center; margin: 1rem 0;">
        <h4>🏗️ Interactive Floor Plan</h4>
        <p>Room locations, navigation paths, and facility markers will be displayed here</p>
        <small>📅 Available once room assignments are finalized</small>
    </div>
    """, unsafe_allow_html=True)

# What You Need to Provide
st.markdown("---")
st.markdown("## 📝 To Complete This Page")

st.markdown("""
**For a fully functional venue page, please provide:**

### 🏢 **Room Information:**
- Final room names and numbers
- Room capacities and layouts
- Session assignments to specific rooms
- Special equipment in each room

### 🗺️ **Navigation:**
- Floor plan image (high resolution)
- Room location markers
- Restroom and facility locations
- Emergency exit routes

### 📞 **Event Contacts:**
- Conference coordinator contact details
- Technical support contact
- Emergency contact for the event
- Registration desk phone number

### 📱 **Technology:**
- WiFi network name and password
- Charging station locations
- A/V equipment specifications per room
""")

st.success("✅ **Current Status:** Event-focused information is ready. Will be enhanced as room details are confirmed.")
