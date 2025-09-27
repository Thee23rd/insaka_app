# pages/Admin_Announcements.py
import streamlit as st
import json
from datetime import datetime
from lib.ui import apply_brand

st.set_page_config(page_title="Admin - Announcements — Insaka", page_icon="📢", layout="wide")

apply_brand()

# Zambian-themed header
st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

st.markdown("# 📢 Admin - Conference Announcements")
st.markdown("Post and manage conference announcements")

st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

# Functions to manage announcements
def load_announcements():
    """Load announcements from JSON file"""
    try:
        with open("data/announcements.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_announcements(announcements):
    """Save announcements to JSON file"""
    try:
        with open("data/announcements.json", "w", encoding="utf-8") as f:
            json.dump(announcements, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"Error saving announcements: {e}")
        return False

def add_announcement(title, content, priority="Normal"):
    """Add a new announcement"""
    announcements = load_announcements()
    
    new_announcement = {
        "id": len(announcements) + 1,
        "title": title,
        "content": content,
        "priority": priority,
        "created_at": datetime.now().isoformat(),
        "created_by": "Admin"
    }
    
    announcements.append(new_announcement)
    return save_announcements(announcements)

def delete_announcement(announcement_id):
    """Delete an announcement by ID"""
    announcements = load_announcements()
    announcements = [a for a in announcements if a["id"] != announcement_id]
    return save_announcements(announcements)

# Navigation
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("← Back to Admin", type="secondary"):
        st.switch_page("pages/0_Admin.py")

with col2:
    if st.button("📰 News & Updates", type="secondary"):
        st.switch_page("pages/Admin_News.py")

with col3:
    if st.button("🌐 View Public Page", type="secondary"):
        st.switch_page("pages/9_External_Content.py")

st.markdown("---")

# Add new announcement form
st.subheader("📝 Add New Announcement")

with st.form("add_announcement", clear_on_submit=True):
    col1, col2 = st.columns([3, 1])
    
    with col1:
        title = st.text_input("Announcement Title", placeholder="Title...")
    
    with col2:
        priority = st.selectbox("Priority", ["Low", "Normal", "High", "Urgent"])
    
    content = st.text_area(
        "Announcement Content", 
        placeholder="Content...",
        height=150
    )
    
    submitted = st.form_submit_button("📢 Post Announcement", type="primary", use_container_width=True)
    
    if submitted:
        if title.strip() and content.strip():
            if add_announcement(title.strip(), content.strip(), priority):
                st.success("✅ Announcement posted successfully!")
                st.rerun()
            else:
                st.error("❌ Failed to save announcement")
        else:
            st.error("❌ Please fill in both title and content")

st.markdown("---")

# Display existing announcements
st.subheader("📋 Current Announcements")

announcements = load_announcements()

if announcements:
    # Sort by priority and date
    priority_order = {"Urgent": 4, "High": 3, "Normal": 2, "Low": 1}
    announcements.sort(key=lambda x: (priority_order.get(x.get("priority", "Normal"), 2), x.get("created_at", "")), reverse=True)
    
    for announcement in announcements:
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])
            
            with col1:
                # Priority badge
                priority = announcement.get("priority", "Normal")
                priority_colors = {
                    "Urgent": "🔴",
                    "High": "🟠", 
                    "Normal": "🟡",
                    "Low": "🟢"
                }
                st.markdown(f"**{priority_colors.get(priority, '🟡')} {announcement['title']}**")
                
                # Content
                st.markdown(announcement['content'])
                
                # Metadata
                created_at = datetime.fromisoformat(announcement['created_at']).strftime("%Y-%m-%d %H:%M")
                st.caption(f"Posted by {announcement.get('created_by', 'Admin')} on {created_at}")
            
            with col2:
                if st.button("🗑️ Delete", key=f"delete_{announcement['id']}", type="secondary"):
                    if delete_announcement(announcement['id']):
                        st.success("✅ Announcement deleted!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to delete announcement")

else:
    st.info("No announcements posted yet. Add your first announcement above!")

st.markdown("---")

# Statistics
st.subheader("📊 Announcements Statistics")
announcements = load_announcements()
if announcements:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Announcements", len(announcements))
    
    with col2:
        urgent_count = len([a for a in announcements if a.get("priority") == "Urgent"])
        st.metric("Urgent", urgent_count)
    
    with col3:
        high_count = len([a for a in announcements if a.get("priority") == "High"])
        st.metric("High Priority", high_count)
    
    with col4:
        recent_count = len([a for a in announcements 
                          if (datetime.now() - datetime.fromisoformat(a.get("created_at", "1970-01-01"))).days <= 7])
        st.metric("This Week", recent_count)

# Footer
st.markdown("---")
st.caption("Announcements will appear on the public Conference Showcase & News page for delegates to view.")
