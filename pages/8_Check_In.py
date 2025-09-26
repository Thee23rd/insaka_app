# pages/8_Check_In.py
import streamlit as st
from lib.ui import apply_brand
from staff_service import load_staff_df, set_daily_checkin, get_daily_checkin_status
import datetime

st.set_page_config(page_title="Daily Check-In — Insaka", page_icon="✅", layout="wide")

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

st.title("✅ Daily Check-In")
st.markdown("Check in for each day of the conference")

# Check if delegate is logged in
if not hasattr(st.session_state, 'delegate_name') or not st.session_state.delegate_name:
    st.warning("Please search for your record first to access check-in.")
    if st.button("🔍 Find My Record", use_container_width=True):
        st.switch_page("pages/7_Delegate_Self_Service.py")
    st.stop()

# Get delegate ID from session state
delegate_id = st.session_state.get('delegate_id')
if not delegate_id:
    st.error("Delegate ID not found. Please search for your record again.")
    if st.button("🔍 Search Again", use_container_width=True):
        st.switch_page("pages/7_Delegate_Self_Service.py")
    st.stop()

# Conference days configuration
conference_days = {
    1: {
        "date": "Sunday, October 6, 2025",
        "title": "Day 1 - Opening & Keynote",
        "description": "Opening ceremony, keynote speeches, and networking"
    },
    2: {
        "date": "Monday, October 7, 2025", 
        "title": "Day 2 - Technical Sessions",
        "description": "Mining technologies, big data, and industry insights"
    },
    3: {
        "date": "Tuesday, October 8, 2025",
        "title": "Day 3 - Closing & Awards",
        "description": "Final sessions, awards ceremony, and closing remarks"
    }
}

# Get current check-in status
checkin_status = get_daily_checkin_status(delegate_id)

# Display delegate info
st.markdown(f"""
<div style="background: linear-gradient(135deg, #2E8B57 0%, #3CB371 100%); color: white; padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem;">
    <h3 style="color: white; margin-bottom: 0.5rem;">👋 Hello, {st.session_state.delegate_name}!</h3>
    <p style="color: #f0f8f0; margin-bottom: 0;">{st.session_state.delegate_organization} • {st.session_state.delegate_category}</p>
</div>
""", unsafe_allow_html=True)

# Check-in status overview
st.subheader("📊 Your Check-In Status")
col1, col2, col3 = st.columns(3)

for day_num in [1, 2, 3]:
    day_info = conference_days[day_num]
    is_checked_in = checkin_status.get(f"Day{day_num}", False)
    
    with [col1, col2, col3][day_num-1]:
        if is_checked_in:
            st.success(f"✅ {day_info['title']}")
            st.caption("Checked In")
        else:
            st.info(f"⏳ {day_info['title']}")
            st.caption("Not Checked In")

# Daily check-in section
st.subheader("🎯 Daily Check-In")

# Get current date to determine which days are available
current_date = datetime.date.today()
conference_start = datetime.date(2025, 10, 6)  # October 6, 2025
conference_end = datetime.date(2025, 10, 8)    # October 8, 2025

# For testing purposes, allow check-in even before conference
# In production, remove this section and use the original logic below
st.info("🧪 **Testing Mode** - Check-in is available for testing purposes")

# Allow testing of all days
st.subheader("🎯 Test Check-In (All Days Available)")
col1, col2, col3 = st.columns(3)

for day_num in [1, 2, 3]:
    day_info = conference_days[day_num]
    is_checked_in = checkin_status.get(f"Day{day_num}", False)
    
    with [col1, col2, col3][day_num-1]:
        st.markdown(f"**{day_info['title']}**")
        st.caption(f"{day_info['date']}")
        st.caption(day_info['description'])
        
        if is_checked_in:
            st.success("✅ Checked In")
            if st.button(f"❌ Undo Day {day_num}", key=f"undo_{day_num}"):
                success, message = set_daily_checkin(delegate_id, day_num, False)
                if success:
                    st.success("Check-in undone!")
                    st.rerun()
                else:
                    st.error(f"Error: {message}")
        else:
            st.info("⏳ Not Checked In")
            if st.button(f"✅ Check In Day {day_num}", key=f"checkin_{day_num}"):
                success, message = set_daily_checkin(delegate_id, day_num, True)
                if success:
                    st.success("🎉 Check-in successful!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"Error: {message}")

st.markdown("---")

# Original production logic (commented out for testing)
# Uncomment this section when ready for production:
"""
# Check if we're in conference period
if current_date < conference_start:
    st.info("🕐 Conference check-in will be available starting October 6, 2025")
elif current_date > conference_end:
    st.info("🏁 Conference has ended. Check-in is no longer available.")
else:
    # Determine which day we're on
    if current_date == conference_start:
        current_day = 1
    elif current_date == datetime.date(2025, 10, 7):
        current_day = 2
    elif current_date == conference_end:
        current_day = 3
    else:
        current_day = None
    
    if current_day:
        day_info = conference_days[current_day]
        st.markdown(f"**Today:** {day_info['date']}")
        st.markdown(f"**Session:** {day_info['title']}")
        st.markdown(f"**Description:** {day_info['description']}")
        
        # Check-in button for current day
        is_checked_in_today = checkin_status.get(f"Day{current_day}", False)
        
        if is_checked_in_today:
            st.success("✅ You are checked in for today!")
            st.balloons()
        else:
            if st.button(f"✅ Check In for {day_info['title']}", use_container_width=True, type="primary"):
                success, message = set_daily_checkin(delegate_id, current_day, True)
                if success:
                    st.success("🎉 Check-in successful!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"Error: {message}")
    else:
        st.warning("Check-in is only available on conference days (October 6-8, 2025)")
"""

# Back to dashboard
st.markdown("---")
if st.button("🏠 Back to Dashboard", use_container_width=True):
    st.switch_page("pages/1_Delegate_Dashboard.py")

# Footer
st.markdown("---")
st.caption("Need help? Contact the conference organizers or visit the registration desk.")
