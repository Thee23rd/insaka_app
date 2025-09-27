# pages/1_Delegate_Dashboard.py
import streamlit as st
import json
from datetime import datetime
from lib.ui import apply_brand
from lib.translations import get_translation, create_language_switcher, get_text_direction, is_rtl_language

# Initialize notification system availability
NOTIFICATION_SYSTEM_AVAILABLE = False

st.set_page_config(page_title="Delegate Dashboard — Insaka", page_icon="👤", layout="wide")

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

# Authentication check
if not hasattr(st.session_state, 'delegate_authenticated') or not st.session_state.delegate_authenticated:
    st.error("🔒 Authentication Required")
    st.info("Please authenticate first by visiting the Delegate Self-Service page.")
    
    if st.button("🔑 Go to Authentication", use_container_width=True):
        st.switch_page("pages/7_Delegate_Self_Service.py")
    
    st.stop()

# Get current user info
current_user_id = st.session_state.get('delegate_id', 'anonymous')
current_user_name = st.session_state.get('delegate_name', 'Anonymous User')

# Language dropdown selector with styling
st.markdown("""
<style>
.language-selector {
    background: linear-gradient(135deg, #198A00, #2BA300);
    color: white;
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 20px;
    box-shadow: 0 4px 12px rgba(25, 138, 0, 0.3);
}
</style>
""", unsafe_allow_html=True)

from lib.translations import get_available_languages

# Get current language
current_language = st.session_state.get('language', 'en-us')

# Create language options for dropdown
languages = get_available_languages()
language_options = {f"{lang['flag']} {lang['name']}": lang['code'] for lang in languages}

# Language selector with custom styling
with st.container():
    st.markdown('<div class="language-selector">', unsafe_allow_html=True)
    st.markdown("### 🌍 Language Selection")
    
    col_lang1, col_lang2 = st.columns([2, 1])
    
    with col_lang1:
        selected_lang_display = st.selectbox(
            "Choose your preferred language:",
            options=list(language_options.keys()),
            index=list(language_options.values()).index(current_language) if current_language in language_options.values() else 0,
            key="language_selector"
        )
        
        # Update language when selection changes
        new_language = language_options[selected_lang_display]
        if new_language != current_language:
            st.session_state.language = new_language
            current_language = new_language
            st.rerun()
    
    with col_lang2:
        current_lang_info = next((lang for lang in languages if lang['code'] == current_language), languages[0])
        st.markdown(f"**Current:** {current_lang_info['flag']} {current_lang_info['name']}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Language demo section
with st.expander("🌍 Language Demo - Try Different Languages", expanded=False):
    st.markdown("**Try switching languages to see the interface change!**")
    
    # Show some sample translations
    sample_keys = ['welcome', 'my_information', 'quick_access', 'agenda', 'speakers']
    
    col_demo1, col_demo2, col_demo3 = st.columns(3)
    
    with col_demo1:
        st.markdown("**English (US) 🇺🇸**")
        for key in sample_keys:
            st.write(f"• {get_translation(key, 'en-us')}")
    
    with col_demo2:
        st.markdown("**Français 🇫🇷**")
        for key in sample_keys:
            st.write(f"• {get_translation(key, 'fr')}")
    
    with col_demo3:
        st.markdown("**العربية 🇸🇦**")
        for key in sample_keys:
            st.write(f"• {get_translation(key, 'ar')}")
    
    st.markdown("---")
    st.info("💡 **Tip:** Select different languages from the dropdown above to see the entire interface change to your chosen language!")

# Import notification system
try:
    from lib.notifications import (
        get_notification_badge, 
        get_user_notifications, 
        get_notification_count,
        get_priority_color,
        create_test_notifications,
        clear_all_notifications,
        mark_notification_read,
        NOTIFICATION_TYPES
    )
    NOTIFICATION_SYSTEM_AVAILABLE = True
except ImportError:
    # Fallback function if notification system not available
    def get_notification_badge(count, max_show=99):
        """Generate notification badge HTML"""
        if count > 0:
            if count > max_show:
                return f'<span style="background: #ff4444; color: white; border-radius: 50%; padding: 2px 6px; font-size: 0.7rem; margin-left: 5px; font-weight: bold;">{max_show}+</span>'
            else:
                return f'<span style="background: #ff4444; color: white; border-radius: 50%; padding: 2px 6px; font-size: 0.7rem; margin-left: 5px; font-weight: bold;">{count}</span>'
        return ""
    
    def get_user_notifications(user_id, unread_only=False):
        return []
    
    def get_notification_count(user_id, unread_only=True):
        return 0
    
    def create_test_notifications(user_id, count=3):
        return False
    
    def clear_all_notifications(user_id):
        return False
    
    def mark_notification_read(notification_id):
        return False
    
    NOTIFICATION_SYSTEM_AVAILABLE = False

# Helper functions for news and announcements
def load_announcements():
    """Load announcements from JSON file"""
    try:
        with open("data/announcements.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def load_news():
    """Load news from JSON file"""
    try:
        with open("data/news.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def load_pr_posts():
    """Load PR posts from JSON file"""
    try:
        with open("data/pr_posts.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def load_matchmaking_data():
    """Load matchmaking interactions"""
    try:
        with open("data/matchmaking.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def get_user_connections(user_id):
    """Get user's connection count"""
    interactions = load_matchmaking_data()
    connections = 0
    
    for interaction in interactions:
        if interaction.get('status') == 'accepted':
            if interaction.get('from_user_id') == user_id or interaction.get('to_user_id') == user_id:
                connections += 1
    
    return connections

def get_relative_time(iso_timestamp):
    """Convert ISO timestamp to relative time like '2 hours ago'"""
    try:
        created_time = datetime.fromisoformat(iso_timestamp)
        now = datetime.now()
        diff = now - created_time
        
        if diff.days > 0:
            if diff.days == 1:
                return "1 day ago"
            elif diff.days < 7:
                return f"{diff.days} days ago"
            elif diff.days < 30:
                weeks = diff.days // 7
                if weeks == 1:
                    return "1 week ago"
                else:
                    return f"{weeks} weeks ago"
            else:
                months = diff.days // 30
                if months == 1:
                    return "1 month ago"
                else:
                    return f"{months} months ago"
        else:
            hours = diff.seconds // 3600
            if hours > 0:
                if hours == 1:
                    return "1 hour ago"
                else:
                    return f"{hours} hours ago"
            else:
                minutes = diff.seconds // 60
                if minutes <= 1:
                    return "just now"
                else:
                    return f"{minutes} minutes ago"
    except:
        return "recently"

# Zambian-themed header
st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

# Notification Summary
def get_total_notifications():
    """Calculate total notifications across all features"""
    # Use the notification system if available
    try:
        system_notifications = get_notification_count(current_user_id, unread_only=True)
    except:
        system_notifications = 0
    
    # Fallback to manual calculation for legacy data
    total = system_notifications
    
    # Check announcements
    announcements = load_announcements()
    urgent_count = len([a for a in announcements if a.get('priority') == 'Urgent'])
    high_count = len([a for a in announcements if a.get('priority') == 'High'])
    total += urgent_count + high_count
    
    # Check news
    news_list = load_news()
    total += len(news_list)
    
    # Check PR posts and interactions
    pr_posts = load_pr_posts()
    for post in pr_posts:
        engagement = post.get('engagement', {})
        total += engagement.get('likes', 0) + engagement.get('shares', 0)
    
    try:
        with open("data/delegate_interactions.json", "r", encoding="utf-8") as f:
            interactions = json.load(f)
        user_interactions = [i for i in interactions if i.get('user_id') == current_user_id]
        total += len(user_interactions)
    except:
        pass
    
    # Check matchmaking
    try:
        with open("data/matchmaking.json", "r", encoding="utf-8") as f:
            matchmaking_data = json.load(f)
        for interaction in matchmaking_data:
            if (interaction.get('to_user_id') == current_user_id and 
                interaction.get('status') == 'pending' and 
                interaction.get('type') in ['connection_request', 'chat_message']):
                total += 1
    except:
        pass
    
    return total

# Test notification controls (for demonstration)
# st.markdown("### 🧪 Notification Test Controls")
# test_col1, test_col2, test_col3 = st.columns(3)

# with test_col1:
#     if st.button("🔔 Create Test Notifications", use_container_width=True):
#         if NOTIFICATION_SYSTEM_AVAILABLE:
#             try:
#                 create_test_notifications(current_user_id, 3)
#                 st.success("✅ Created 3 test notifications!")
#                 st.rerun()
#             except Exception as e:
#                 st.error(f"❌ Error: {e}")
#         else:
#             st.error("❌ Notification system not available")

# with test_col2:
#     if st.button("🗑️ Clear All Notifications", use_container_width=True):
#         if NOTIFICATION_SYSTEM_AVAILABLE:
#             try:
#                 clear_all_notifications(current_user_id)
#                 st.success("✅ Cleared all notifications!")
#                 st.rerun()
#             except Exception as e:
#                 st.error(f"❌ Error: {e}")
#         else:
#             st.error("❌ Notification system not available")

# with test_col3:
#     if st.button("🔄 Refresh Page", use_container_width=True):
#         st.rerun()

# Sound and vibration test buttons
# if NOTIFICATION_SYSTEM_AVAILABLE:
#     st.markdown("---")
#     st.markdown("### 🔊 ATTENTION-GRABBING SOUND TEST")
#     st.warning("🔊 **Click the button below to test if sound works!** This will play a loud triple beep to get attention.")
    
#     # Big prominent test button
#     if st.button("🔊🔊🔊 TEST LOUD NOTIFICATION SOUND 🔊🔊🔊", use_container_width=True, type="primary"):
#         st.markdown("""
#         <script>
#         console.log('🔊 TESTING LOUD NOTIFICATION...');
        
#         // Try multiple approaches to ensure sound works
#         try {
#             // Method 1: Our custom sound
#             if (window.playNotificationSound) {
#                 window.playNotificationSound();
#                 console.log('✅ Custom sound function called');
#             }
            
#             // Method 2: Browser alert sound (fallback)
#             setTimeout(() => {
#                 try {
#                     const audio = new Audio();
#                     audio.src = 'data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmQbBzKO0fPTgjMGHm7A7+OZURE=';
#                     audio.volume = 1.0;
#                     audio.play().catch(e => console.log('Browser audio failed:', e));
#                 } catch (e) {
#                     console.log('Browser audio setup failed:', e);
#                 }
#             }, 500);
            
#             // Method 3: Browser beep (if available)
#             setTimeout(() => {
#                 try {
#                     // Some browsers support this
#                     if (typeof console !== 'undefined' && console.log) {
#                         console.log('\\a'); // Bell character
#                     }
#                 } catch (e) {
#                     console.log('Console beep failed:', e);
#                 }
#             }, 1000);
            
#         } catch (error) {
#             console.log('❌ All sound methods failed:', error);
#         }
#         </script>
#         """, unsafe_allow_html=True)
#         st.success("🔊 LOUD SOUND TEST TRIGGERED! Check your speakers/headphones!")
#         st.balloons()
        
#         # Also try a direct browser alert as ultimate fallback
#         st.markdown("""
#         <script>
#         setTimeout(() => {
#             alert('🔊 NOTIFICATION SOUND TEST - Did you hear any beeps?');
#         }, 2000);
#         </script>
#         """, unsafe_allow_html=True)
    
#     # Additional test options
#     col_sound, col_vibrate, col_visual = st.columns(3)
    
#     with col_sound:
#         if st.button("🔊 Sound Only", use_container_width=True):
#             st.markdown("""
#             <script>
#             if (window.playNotificationSound) {
#                 window.playNotificationSound();
#             }
#             </script>
#             """, unsafe_allow_html=True)
#             st.success("🔊 Sound test triggered!")
    
#     with col_vibrate:
#         if st.button("📳 Vibration Only", use_container_width=True):
#             st.markdown("""
#             <script>
#             if (window.vibrateDevice) {
#                 window.vibrateDevice();
#             }
#             </script>
#             """, unsafe_allow_html=True)
#             st.success("📳 Vibration test triggered!")
    
#     with col_visual:
#         if st.button("👁️ Visual Alert", use_container_width=True):
#             st.markdown("""
#             <script>
#             if (window.showVisualAlert) {
#                 window.showVisualAlert();
#             } else {
#                 // Fallback visual alert
#                 const flash = document.createElement('div');
#                 flash.style.cssText = 'position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: #ff0000; z-index: 99999; pointer-events: none; opacity: 0.8;';
#                 document.body.appendChild(flash);
#                 setTimeout(() => { if (document.body.contains(flash)) document.body.removeChild(flash); }, 500);
#             }
#             </script>
#             """, unsafe_allow_html=True)
#             st.success("👁️ Visual alert triggered!")
    
#     # Instructions
#     st.info("""
#     💡 **Instructions:**
#     1. **Click the big red button above** to test the main notification sound
#     2. **Make sure your device volume is up** and not muted
#     3. **Allow audio permissions** if your browser asks
#     4. **Check the browser console** (F12) to see if there are any errors
#     """)
    
#     # Debug info
#     st.markdown("""
#     <script>
#     console.log('🔊 Notification system debug info:');
#     console.log('- AudioContext supported:', typeof AudioContext !== 'undefined' || typeof webkitAudioContext !== 'undefined');
#     console.log('- Vibration supported:', 'vibrate' in navigator);
#     console.log('- playNotificationSound function:', typeof window.playNotificationSound);
#     </script>
#     """, unsafe_allow_html=True)

# # Show notification system status
# if NOTIFICATION_SYSTEM_AVAILABLE:
#     st.success("✅ Notification system is active")
#     # Add sound notification script for PWA
#     try:
#         from lib.notifications import get_sound_notification_script
#         st.markdown(get_sound_notification_script(), unsafe_allow_html=True)
#     except:
#         pass
# else:
#     st.warning("⚠️ Notification system not available - using fallback mode")

# # Show notification bell if there are notifications
# total_notifications = get_total_notifications()
# if total_notifications > 0:
#     st.markdown(f"""
#     <div style="background: linear-gradient(135deg, #ff4444 0%, #ff6666 100%); color: white; padding: 1rem; border-radius: 10px; margin-bottom: 1rem; text-align: center; box-shadow: 0 4px 16px rgba(255, 68, 68, 0.3);">
#         <h3 style="color: white; margin: 0; font-size: 1.2rem;">🔔 {total_notifications} New Notification{'s' if total_notifications > 1 else ''}</h3>
#         <p style="color: #fff; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Check the sections below for updates</p>
#     </div>
#     """, unsafe_allow_html=True)
    
#     # Show recent notifications if available
#     try:
#         recent_notifications = get_user_notifications(current_user_id, unread_only=True)[:5]
#         if recent_notifications:
#             st.markdown("### 📋 Recent Notifications")
#             for notification in recent_notifications:
#                 priority_color = get_priority_color(notification.get('priority', 'Normal'))
#                 with st.container(border=True):
#                     col_notif1, col_notif2 = st.columns([4, 1])
#                     with col_notif1:
#                         st.markdown(f"**{priority_color} {notification.get('title', 'Notification')}**")
#                         st.write(notification.get('message', ''))
#                         st.caption(f"Posted {get_relative_time(notification.get('created_at', ''))}")
#                     with col_notif2:
#                         if st.button("✓", key=f"mark_read_{notification.get('id')}", help="Mark as read"):
#                             try:
#                                 if NOTIFICATION_SYSTEM_AVAILABLE:
#                                     mark_notification_read(notification.get('id'))
#                                     st.success("✅ Marked as read!")
#                                     st.rerun()
#                                 else:
#                                     st.error("❌ Notification system not available")
#                             except Exception as e:
#                                 st.error(f"❌ Error: {e}")
#     except:
#         pass
# else:
#     st.info("ℹ️ No notifications at this time. Use the test controls above to create some!")

# Full-width personalized greeting with RTL support
text_direction = get_text_direction(current_language)
rtl_style = "direction: rtl; text-align: right;" if is_rtl_language(current_language) else "direction: ltr; text-align: center;"

if hasattr(st.session_state, 'delegate_name') and st.session_state.delegate_name:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #198A00 0%, #2BA300 50%, #D10000 100%); color: white; padding: 2rem; border-radius: 20px; margin-bottom: 2rem; {rtl_style} box-shadow: 0 8px 32px rgba(25, 138, 0, 0.2);">
        <h1 style="color: white; margin-bottom: 0.5rem; font-size: 2rem; font-weight: 700;">👋 {get_translation('hello', current_language)}, {st.session_state.delegate_name}!</h1>
        <p style="color: #f0f8f0; margin-bottom: 0; font-size: 1.1rem; font-weight: 500;">{get_translation('welcome', current_language)} to The Zambian Mining and Investment Insaka Conference 2025</p>
        <p style="color: #e8f5e8; margin-bottom: 0; font-size: 0.9rem;">{st.session_state.delegate_organization} • {st.session_state.delegate_category}</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"# 👤 {get_translation('delegate_dashboard', current_language)}")
    st.markdown("Welcome to your conference dashboard")



st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

# Personal section - Check-in first (as dropdown)
with st.expander(f"👤 {get_translation('my_information', current_language)}", expanded=True):
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(f"✏️ {get_translation('update_details', current_language)}", use_container_width=True):
            st.switch_page("pages/7_Delegate_Self_Service.py")

    with col2:
        if st.button(f"📱 {get_translation('download_materials', current_language)}", use_container_width=True):
            st.switch_page("pages/5_Materials.py")

    with col3:
        if st.button(f"✅ {get_translation('daily_checkin', current_language)}", use_container_width=True):
            st.switch_page("pages/8_Check_In.py")

st.write("")

# Quick access buttons (as dropdown)
with st.expander(f"🚀 {get_translation('quick_access', current_language)}", expanded=True):
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

    with col1:
        # Check for agenda updates
        agenda_notifications = 0  # Could check for agenda changes
        
        # Create notification badge with HTML
        if agenda_notifications > 0:
            badge_html = get_notification_badge(agenda_notifications)
            st.markdown(f"📅 **{get_translation('agenda', current_language)}** {badge_html}", unsafe_allow_html=True)
        else:
            st.markdown(f"📅 **{get_translation('agenda', current_language)}**")
        
        if st.button(get_translation('view_schedule', current_language), use_container_width=True, help="View conference schedule"):
            st.switch_page("pages/1_Agenda.py")

    with col2:
        # Check for speaker updates
        speakers_notifications = 0  # Could check for speaker updates
        
        if speakers_notifications > 0:
            badge_html = get_notification_badge(speakers_notifications)
            st.markdown(f"👥 **{get_translation('speakers', current_language)}** {badge_html}", unsafe_allow_html=True)
        else:
            st.markdown(f"👥 **{get_translation('speakers', current_language)}**")
        
        if st.button(get_translation('meet_speakers', current_language), use_container_width=True, help="Meet our speakers"):
            st.switch_page("pages/2_Speakers.py")

    with col3:
        # Check for exhibitor updates
        exhibitors_notifications = 0  # Could check for exhibitor updates
        
        if exhibitors_notifications > 0:
            badge_html = get_notification_badge(exhibitors_notifications)
            st.markdown(f"🏢 **{get_translation('exhibitors', current_language)}** {badge_html}", unsafe_allow_html=True)
        else:
            st.markdown(f"🏢 **{get_translation('exhibitors', current_language)}**")
        
        if st.button(get_translation('explore_booths', current_language), use_container_width=True, help="Explore exhibitor booths"):
            st.switch_page("pages/3_Exhibitors.py")

    with col4:
        # Check for venue updates
        venue_notifications = 0  # Could check for venue updates
        
        if venue_notifications > 0:
            badge_html = get_notification_badge(venue_notifications)
            st.markdown(f"🏛️ **{get_translation('venue', current_language)}** {badge_html}", unsafe_allow_html=True)
        else:
            st.markdown(f"🏛️ **{get_translation('venue', current_language)}**")
        
        if st.button(get_translation('venue_info', current_language), use_container_width=True, help="Venue information"):
            st.switch_page("pages/6_Venue.py")

    with col5:
        # Check for news and announcements
        announcements = load_announcements()
        news_list = load_news()
        showcase_notifications = len(announcements) + len(news_list)
        
        if showcase_notifications > 0:
            badge_html = get_notification_badge(showcase_notifications)
            st.markdown(f"🌐 **{get_translation('showcase_news', current_language)}** {badge_html}", unsafe_allow_html=True)
        else:
            st.markdown(f"🌐 **{get_translation('showcase_news', current_language)}**")
        
        if st.button(get_translation('latest_updates', current_language), use_container_width=True, help="Latest news and announcements"):
            st.switch_page("pages/9_External_Content.py")

    with col6:
        # Check for new PR posts and interactions
        pr_posts = load_pr_posts()
        pr_notifications = 0
        
        # Count total engagement
        for post in pr_posts:
            engagement = post.get('engagement', {})
            pr_notifications += engagement.get('likes', 0) + engagement.get('shares', 0)
        
        # Also check for delegate interactions
        try:
            with open("data/delegate_interactions.json", "r", encoding="utf-8") as f:
                interactions = json.load(f)
            
            # Count interactions involving this user
            user_interactions = [i for i in interactions if i.get('user_id') == current_user_id]
            pr_notifications += len(user_interactions)
        except:
            pass
        
        if pr_notifications > 0:
            badge_html = get_notification_badge(pr_notifications)
            st.markdown(f"📸 **{get_translation('interactive_posts', current_language)}** {badge_html}", unsafe_allow_html=True)
        else:
            st.markdown(f"📸 **{get_translation('interactive_posts', current_language)}**")
        
        if st.button(get_translation('engage_posts', current_language), use_container_width=True, help="Engage with conference posts"):
            st.switch_page("pages/10_Interactive_PR.py")

    with col7:
        # Check for matchmaking activity
        try:
            with open("data/matchmaking.json", "r", encoding="utf-8") as f:
                matchmaking_data = json.load(f)
            
            # Count pending connection requests and new messages
            matchmaking_notifications = 0
            for interaction in matchmaking_data:
                if (interaction.get('to_user_id') == current_user_id and 
                    interaction.get('status') == 'pending' and 
                    interaction.get('type') in ['connection_request', 'chat_message']):
                    matchmaking_notifications += 1
        except:
            matchmaking_notifications = 0
        
        if matchmaking_notifications > 0:
            badge_html = get_notification_badge(matchmaking_notifications)
            st.markdown(f"🤝 **{get_translation('matchmaking', current_language)}** {badge_html}", unsafe_allow_html=True)
        else:
            st.markdown(f"🤝 **{get_translation('matchmaking', current_language)}**")
        
        if st.button(get_translation('network_now', current_language), use_container_width=True, help="Network with other delegates"):
            st.switch_page("pages/11_Matchmaking.py")

# Conference info
st.subheader(f"📋 {get_translation('conference_info', current_language)}")
st.info(f"""
**{get_translation('conference_dates', current_language)}:** October 6-8, 2025  
**{get_translation('location', current_language)}:** [Venue details will be shown here]  
**{get_translation('theme', current_language)}:** {get_translation('collaborate_innovate_thrive', current_language)}

**{get_translation('key_sessions', current_language)}:**
- {get_translation('opening_keynote', current_language)}: Sunday 6 Oct, 09:00
- [Additional sessions will be loaded from agenda]

**{get_translation('important_notes', current_language)}:**
- {get_translation('ensure_details_updated', current_language)}
- {get_translation('check_agenda_regularly', current_language)}
- {get_translation('download_materials_section', current_language)}
""")

# News, Announcements, PR, and Networking sections
col1, col2, col3, col4 = st.columns(4)

# Latest Announcements
with col1:
    announcements = load_announcements()
    urgent_count = len([a for a in announcements if a.get('priority') == 'Urgent'])
    high_count = len([a for a in announcements if a.get('priority') == 'High'])
    total_notifications = urgent_count + high_count
    
    # Add notification indicator to header
    if total_notifications > 0:
        badge_html = get_notification_badge(total_notifications)
        st.markdown(f"### 📢 {get_translation('latest_announcements', current_language)} {badge_html}", unsafe_allow_html=True)
        if urgent_count > 0:
            st.error(f"🚨 {urgent_count} urgent announcement{'s' if urgent_count > 1 else ''} require immediate attention!")
        elif high_count > 0:
            st.warning(f"⚠️ {high_count} high priority announcement{'s' if high_count > 1 else ''}")
    else:
        st.subheader(f"📢 {get_translation('latest_announcements', current_language)}")
    
    if announcements:
        # Sort by priority and date, show only latest 3
        priority_order = {"Urgent": 4, "High": 3, "Normal": 2, "Low": 1}
        announcements.sort(key=lambda x: (priority_order.get(x.get("priority", "Normal"), 2), x.get("created_at", "")), reverse=True)
        
        for announcement in announcements[:3]:  # Show only latest 3
            priority = announcement.get("priority", "Normal")
            priority_colors = {
                "Urgent": "🔴",
                "High": "🟠", 
                "Normal": "🟡",
                "Low": "🟢"
            }
            
            # Create snippet (first 100 characters)
            content_snippet = announcement['content'][:100] + "..." if len(announcement['content']) > 100 else announcement['content']
            relative_time = get_relative_time(announcement['created_at'])
            
            with st.container(border=True):
                st.markdown(f"**{priority_colors.get(priority, '🟡')} {announcement['title']}**")
                st.write(content_snippet)
                st.caption(f"Posted {relative_time}")
                
                if st.button(f"Read More", key=f"announcement_{announcement.get('id', 0)}"):
                    st.session_state.show_announcements = True
                    st.switch_page("pages/9_External_Content.py")
    else:
        st.info(get_translation('no_announcements', current_language))

# Latest News
with col2:
    news_list = load_news()
    new_news_count = len(news_list)  # Could implement "new since last visit" logic
    
    # Add notification indicator to header
    if new_news_count > 0:
        badge_html = get_notification_badge(new_news_count)
        st.markdown(f"### 📰 {get_translation('latest_news', current_language)} {badge_html}", unsafe_allow_html=True)
    else:
        st.subheader(f"📰 {get_translation('latest_news', current_language)}")
    
    if news_list:
        # Sort by date, show only latest 3
        news_list.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        for news_item in news_list[:3]:  # Show only latest 3
            category = news_item.get("category", "General")
            category_colors = {
                "General": "🔵",
                "Conference Updates": "🟢",
                "Industry News": "🟡",
                "Speaker Updates": "🟣",
                "Exhibitor News": "🟠",
                "Schedule Changes": "🔴"
            }
            
            # Create snippet (first 100 characters)
            content_snippet = news_item['content'][:100] + "..." if len(news_item['content']) > 100 else news_item['content']
            relative_time = get_relative_time(news_item['created_at'])
            
            with st.container(border=True):
                st.markdown(f"**{category_colors.get(category, '🔵')} {news_item['title']}**")
                st.write(content_snippet)
                st.caption(f"Posted {relative_time} | {category}")
                
                if st.button(f"Read More", key=f"news_{news_item.get('id', 0)}"):
                    st.session_state.show_news = True
                    st.switch_page("pages/9_External_Content.py")
    else:
        st.info(get_translation('no_news', current_language))

# Latest PR Posts
with col3:
    st.subheader(f"📸 {get_translation('trending_posts', current_language)}")
    pr_posts = load_pr_posts()
    
    if pr_posts:
        # Sort by engagement and date, show only latest 2
        pr_posts.sort(key=lambda x: (
            x.get('engagement', {}).get('likes', 0) + 
            x.get('engagement', {}).get('shares', 0) * 2,
            x.get('created_at', "")
        ), reverse=True)
        
        for post in pr_posts[:2]:  # Show only latest 2
            post_type = post.get("type", "General")
            type_colors = {
                "Trending News": "🔥",
                "Event Highlights": "⭐",
                "Speaker Spotlight": "🎤",
                "Exhibitor Showcase": "🏢",
                "Behind the Scenes": "🎬",
                "Networking Moments": "🤝"
            }
            
            # Create snippet (first 80 characters)
            content_snippet = post['content'][:80] + "..." if len(post['content']) > 80 else post['content']
            relative_time = get_relative_time(post['created_at'])
            
            with st.container(border=True):
                st.markdown(f"**{type_colors.get(post_type, '📸')} {post['title']}**")
                
                # Show image thumbnail if available
                if post.get('image'):
                    try:
                        st.image(post['image'], width=150)
                    except:
                        st.write("📷")
                
                st.write(content_snippet)
                
                # Show hashtags
                if post.get('hashtags'):
                    hashtag_text = " ".join([f"#{tag}" for tag in post['hashtags'][:3]])  # Show first 3 hashtags
                    st.caption(f"🏷️ {hashtag_text}")
                
                # Show engagement
                engagement = post.get('engagement', {})
                if engagement:
                    likes = engagement.get('likes', 0)
                    shares = engagement.get('shares', 0)
                    st.caption(f"❤️ {likes} • 🔄 {shares}")
                
                st.caption(f"Posted {relative_time}")
                
                # Quick action buttons
                col_view, col_share = st.columns(2)
                
                with col_view:
                    if st.button(f"👀 View", key=f"view_pr_{post.get('id', 0)}"):
                        # Track view before navigating
                        from staff_service import load_staff_df
                        import json
                        
                        # Update view count
                        try:
                            with open("data/pr_posts.json", "r", encoding="utf-8") as f:
                                posts = json.load(f)
                            
                            for p in posts:
                                if p.get('id') == post.get('id'):
                                    current_views = p.get('engagement', {}).get('views', 0)
                                    p['engagement']['views'] = current_views + 1
                                    break
                            
                            with open("data/pr_posts.json", "w", encoding="utf-8") as f:
                                json.dump(posts, f, indent=2, ensure_ascii=False)
                        except Exception as e:
                            st.error(f"Error tracking view: {e}")
                        
                        st.switch_page("pages/10_Interactive_PR.py")
                
                with col_share:
                    if st.button(f"📤 Share", key=f"quick_share_{post.get('id', 0)}"):
                        # Generate share URL
                        post_url = f"https://insaka-conference.streamlit.app/pages/10_Interactive_PR.py?post={post.get('id', 0)}"
                        st.success("📋 Link copied to clipboard!")
                        st.code(post_url, language="text")
                        
                        # JavaScript copy to clipboard
                        st.markdown(f"""
                        <script>
                        navigator.clipboard.writeText('{post_url}');
                        </script>
                        """, unsafe_allow_html=True)
    else:
        st.info(get_translation('no_trending_posts', current_language))

# Networking Overview
with col4:
    # Get user's connection count
    connection_count = get_user_connections(current_user_id)
    
    # Get pending requests and new messages
    interactions = load_matchmaking_data()
    pending_requests = len([i for i in interactions if 
                           i.get('to_user_id') == current_user_id and 
                           i.get('type') == 'connection_request' and 
                           i.get('status') == 'pending'])
    
    # Count new messages (unread chat messages)
    new_messages = len([i for i in interactions if 
                       i.get('to_user_id') == current_user_id and 
                       i.get('type') == 'chat_message' and 
                       i.get('status') == 'sent'])  # 'sent' means unread
    
    total_networking_notifications = pending_requests + new_messages
    
    # Add notification indicator to header
    if total_networking_notifications > 0:
        badge_html = get_notification_badge(total_networking_notifications)
        st.markdown(f"### 🤝 {get_translation('networking', current_language)} {badge_html}", unsafe_allow_html=True)
    else:
        st.subheader(f"🤝 {get_translation('networking', current_language)}")
    
    st.metric(get_translation('connections', current_language), connection_count)
    
    if pending_requests > 0:
        st.metric(get_translation('pending_requests', current_language), pending_requests)
        st.error(f"🚨 {pending_requests} pending connection request{'s' if pending_requests > 1 else ''}!")
    elif new_messages > 0:
        st.metric("New Messages", new_messages)
        st.warning(f"💬 {new_messages} new message{'s' if new_messages > 1 else ''}!")
    
    # Meeting requests
    meeting_requests = len([i for i in interactions if 
                           (i.get('to_user_id') == current_user_id or i.get('from_user_id') == current_user_id) and 
                           i.get('type') == 'meeting_request' and 
                           i.get('status') == 'pending'])
    
    if meeting_requests > 0:
        st.metric("Meeting Requests", meeting_requests)
        st.info(f"📅 You have {meeting_requests} pending meeting request{'s' if meeting_requests > 1 else ''}!")
    
    # Quick networking stats
    if connection_count == 0:
        st.info("🌟 Start networking by connecting with fellow delegates!")
        if st.button("🤝 Find Connections", use_container_width=True):
            st.switch_page("pages/11_Matchmaking.py")
    else:
        st.success(f"🎉 You're connected with {connection_count} delegate{'s' if connection_count > 1 else ''}!")
        if st.button("🤝 Expand Network", use_container_width=True):
            st.switch_page("pages/11_Matchmaking.py")

# Footer with logout button
st.markdown("---")
col_footer1, col_footer2, col_footer3 = st.columns([2, 1, 2])
with col_footer1:
    st.caption("Need help? Contact the conference organizers or visit the registration desks.")
with col_footer2:
    if st.button(f"🚪 {get_translation('logout', current_language)}", use_container_width=True, key="dashboard_logout"):
        # Clear all session state
        for key in list(st.session_state.keys()):
            if key.startswith('delegate_'):
                del st.session_state[key]
        st.success("✅ Logged out successfully!")
        st.switch_page("pages/0_Landing.py")
