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
    
    if st.button("🔑 Go to Authentication", width='stretch'):
        st.switch_page("pages/7_Delegate_Self_Service.py")
    
    st.stop()

# Get current user info
current_user_id = st.session_state.get('delegate_id', 'anonymous')
current_user_name = st.session_state.get('delegate_name', 'Anonymous User')

# Role switching feature for dual-role users
def check_and_show_role_switch():
    """Check if user has dual roles and show switch option"""
    try:
        from lib.qr_system import check_dual_role_user
        is_dual_role, speaker_info = check_dual_role_user(current_user_name)
        
        if is_dual_role and speaker_info:
            current_role = "Speaker" if st.session_state.get('delegate_category') == 'Speaker' else "Delegate"
            
            st.markdown("---")
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.info(f"🎭 **Current Role:** {current_role} | You have access to both Delegate and Speaker features")
            
            with col2:
                if current_role == "Delegate":
                    if st.button("🎤 Switch to Speaker", key="switch_to_speaker"):
                        # Switch to speaker role
                        speaker_id = f"SPEAKER_{speaker_info.get('name', '').replace(' ', '_')}"
                        st.session_state.delegate_id = speaker_id
                        st.session_state.delegate_name = speaker_info.get('name', '')
                        st.session_state.delegate_organization = speaker_info.get('organization', '')
                        st.session_state.delegate_category = 'Speaker'
                        st.session_state.delegate_title = speaker_info.get('position', '')
                        st.session_state.delegate_nationality = speaker_info.get('nationality', '')
                        st.session_state.delegate_phone = speaker_info.get('phone', '')
                        st.session_state.delegate_email = speaker_info.get('email', '')
                        st.rerun()
                else:
                    if st.button("👤 Switch to Delegate", key="switch_to_delegate"):
                        # Need to load delegate data - redirect to role selection
                        st.session_state.dual_role_user = True
                        # We'll need to get delegate record from the staff data
                        import pandas as pd
                        from staff_service import load_staff_df
                        df = load_staff_df()
                        delegate_record = df[df['Name'].str.lower().str.strip() == current_user_name.lower().strip()].iloc[0]
                        st.session_state.current_delegate_record = delegate_record
                        st.session_state.current_speaker_info = speaker_info
                        st.rerun()
            
            with col3:
                if st.button("🔄 Role Selection", key="full_role_selection"):
                    # Redirect to full role selection
                    st.session_state.dual_role_user = True
                    # Get delegate record
                    import pandas as pd
                    from staff_service import load_staff_df
                    df = load_staff_df()
                    delegate_record = df[df['Name'].str.lower().str.strip() == current_user_name.lower().strip()].iloc[0]
                    st.session_state.current_delegate_record = delegate_record
                    st.session_state.current_speaker_info = speaker_info
                    st.switch_page("pages/7_Delegate_Self_Service.py")
    
    except Exception as e:
        # Silently fail if there's an error
        pass

# Show role switching if applicable
check_and_show_role_switch()

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

/* Profile photo styling for dashboard */
.dashboard-profile-photo {
    border-radius: 50% !important;
    object-fit: cover !important;
    border: 2px solid #198A00 !important;
}

/* Force all Streamlit images to be rounded */
div[data-testid="stImage"] img {
    border-radius: 50% !important;
    object-fit: cover !important;
    border: 2px solid #198A00 !important;
}

.stImage > div > img {
    border-radius: 50% !important;
    object-fit: cover !important;
    border: 2px solid #198A00 !important;
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

# # Language demo section
# with st.expander("🌍 Language Demo - Try Different Languages", expanded=False):
#     st.markdown("**Try switching languages to see the interface change!**")
    
#     # Show some sample translations
#     sample_keys = ['welcome', 'my_information', 'quick_access', 'agenda', 'speakers']
    
#     col_demo1, col_demo2, col_demo3 = st.columns(3)
    
#     with col_demo1:
#         st.markdown("**English (US) 🇺🇸**")
#         for key in sample_keys:
#             st.write(f"• {get_translation(key, 'en-us')}")
    
#     with col_demo2:
#         st.markdown("**Français 🇫🇷**")
#         for key in sample_keys:
#             st.write(f"• {get_translation(key, 'fr')}")
    
#     with col_demo3:
#         st.markdown("**العربية 🇸🇦**")
#         for key in sample_keys:
#             st.write(f"• {get_translation(key, 'ar')}")
    
#     st.markdown("---")
#     st.info("💡 **Tip:** Select different languages from the dropdown above to see the entire interface change to your chosen language!")

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

def format_count(count):
    """Format large numbers with k, M suffix (e.g., 1000 -> 1k, 1000000 -> 1M)"""
    try:
        count = int(count)
        if count >= 1_000_000:
            return f"{count / 1_000_000:.1f}M".rstrip('0').rstrip('.')
        elif count >= 1_000:
            return f"{count / 1_000:.1f}k".rstrip('0').rstrip('.')
        else:
            return str(count)
    except (ValueError, TypeError):
        return str(count)

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
#     if st.button("🔔 Create Test Notifications", width='stretch'):
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
#     if st.button("🗑️ Clear All Notifications", width='stretch'):
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
#     if st.button("🔄 Refresh Page", width='stretch'):
#         st.rerun()

# Sound and vibration test buttons
# if NOTIFICATION_SYSTEM_AVAILABLE:
#     st.markdown("---")
#     st.markdown("### 🔊 ATTENTION-GRABBING SOUND TEST")
#     st.warning("🔊 **Click the button below to test if sound works!** This will play a loud triple beep to get attention.")
    
#     # Big prominent test button
#     if st.button("🔊🔊🔊 TEST LOUD NOTIFICATION SOUND 🔊🔊🔊", width='stretch', type="primary"):
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
#         if st.button("🔊 Sound Only", width='stretch'):
#             st.markdown("""
#             <script>
#             if (window.playNotificationSound) {
#                 window.playNotificationSound();
#             }
#             </script>
#             """, unsafe_allow_html=True)
#             st.success("🔊 Sound test triggered!")
    
#     with col_vibrate:
#         if st.button("📳 Vibration Only", width='stretch'):
#             st.markdown("""
#             <script>
#             if (window.vibrateDevice) {
#                 window.vibrateDevice();
#             }
#             </script>
#             """, unsafe_allow_html=True)
#             st.success("📳 Vibration test triggered!")
    
#     with col_visual:
#         if st.button("👁️ Visual Alert", width='stretch'):
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
    # Get delegate photo
    try:
        from staff_service import load_staff_df
        df = load_staff_df()
        delegate_id = str(st.session_state.delegate_id)
        
        # Check if it's a speaker ID
        if delegate_id.startswith("SPEAKER_"):
            # Load from speakers
            import json
            with open("data/speakers.json", "r", encoding="utf-8") as f:
                speakers = json.load(f)
            
            delegate_photo = None
            for sp in speakers:
                if f"SPEAKER_{sp.get('name', '').replace(' ', '_')}" == delegate_id:
                    delegate_photo = sp.get('photo', '')
                    break
        else:
            # Load from delegates
            mask = df["ID"].astype(str) == delegate_id
            if mask.any():
                delegate_photo = df[mask].iloc[0].get('BadgePhoto', '')
            else:
                delegate_photo = ''
    except:
        delegate_photo = ''
    
    # Display greeting with photo
    col_photo, col_greeting = st.columns([1, 4])
    
    with col_photo:
        if delegate_photo:
            try:
                st.image(delegate_photo, use_container_width=True)
            except:
                st.markdown("""
                <div style="background: #F3F4F6; border-radius: 50%; width: 100px; height: 100px; 
                           display: flex; align-items: center; justify-content: center; margin: 0 auto;">
                    <span style="font-size: 3rem;">👤</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #F3F4F6; border-radius: 50%; width: 100px; height: 100px; 
                       display: flex; align-items: center; justify-content: center; margin: 0 auto;">
                <span style="font-size: 3rem;">👤</span>
            </div>
            """, unsafe_allow_html=True)
    
    with col_greeting:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #198A00 0%, #2BA300 50%, #D10000 100%); color: white; padding: 2rem; border-radius: 20px; {rtl_style} box-shadow: 0 8px 32px rgba(25, 138, 0, 0.2);">
            <h1 style="color: white; margin-bottom: 0.5rem; font-size: 2rem; font-weight: 700;">👋 {get_translation('hello', current_language)}, {st.session_state.delegate_name}!</h1>
            <p style="color: #f0f8f0; margin-bottom: 0; font-size: 1.1rem; font-weight: 500;">{get_translation('welcome', current_language)} to The Zambian Mining and Investment Insaka Conference 2025</p>
            <p style="color: #e8f5e8; margin-bottom: 0; font-size: 0.9rem;">{st.session_state.delegate_organization} • {st.session_state.delegate_category}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
else:
    st.markdown(f"# 👤 {get_translation('delegate_dashboard', current_language)}")
    st.markdown("Welcome to your conference dashboard")



st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

# Helper functions for agenda snippets
def load_agenda():
    """Load agenda from JSON file"""
    try:
        with open("data/agenda.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def parse_time_to_minutes(time_str):
    """Convert time string to minutes since midnight for comparison"""
    import re
    try:
        time_str = time_str.strip().upper()
        time_str = re.sub(r'\s+', ' ', time_str)
        
        if 'AM' in time_str or 'PM' in time_str:
            time_obj = datetime.strptime(time_str, "%I:%M %p")
        else:
            time_obj = datetime.strptime(time_str, "%H:%M")
        return time_obj.hour * 60 + time_obj.minute
    except:
        return 540  # Default to 9 AM

def get_current_and_upcoming_sessions():
    """Get current session and next 2 upcoming sessions"""
    agenda = load_agenda()
    if not agenda:
        return None, []
    
    # Get current time and day
    now = datetime.now()
    current_minutes = now.hour * 60 + now.minute
    
    # Simple day name mapping (you may need to adjust based on your day format)
    current_day_name = now.strftime("%a %d %b")  # e.g., "Sun 6 Oct"
    
    # Get today's events
    today_events = [e for e in agenda if current_day_name in e.get('day', '')]
    
    # If no events today, get all future events
    if not today_events:
        future_events = sorted(agenda, key=lambda x: parse_time_to_minutes(x.get('time', '09:00')))
        return None, future_events[:2]
    
    # Sort by time
    today_events.sort(key=lambda x: parse_time_to_minutes(x.get('time', '09:00')))
    
    # Find current and upcoming
    current_session = None
    upcoming = []
    
    for idx, event in enumerate(today_events):
        event_time = parse_time_to_minutes(event.get('time', '09:00'))
        
        # Assume each session lasts 60 minutes (you can adjust this)
        session_duration = 60
        
        if event_time <= current_minutes < event_time + session_duration:
            # This is the current session
            current_session = event
            # Get next 2 sessions
            upcoming = today_events[idx+1:idx+3]
            break
        elif event_time > current_minutes:
            # This is a future session
            upcoming = today_events[idx:idx+2]
            break
    
    return current_session, upcoming

# Segment type colors (matching agenda page)
SEGMENT_COLORS = {
    "keynote": "#D10000",
    "presentation": "#198A00",
    "panel": "#FF9500",
    "break": "#FFD700",
    "networking": "#2BA300",
    "workshop": "#8B4513",
    "closing": "#D10000",
    "other": "#666666"
}

# Personal section - Check-in first (as dropdown)
with st.expander(f"👤 {get_translation('my_information', current_language)}", expanded=True):
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(f"✏️ {get_translation('update_details', current_language)}", width='stretch'):
            st.switch_page("pages/7_Delegate_Self_Service.py")

    with col2:
        if st.button(f"📱 {get_translation('download_materials', current_language)}", width='stretch'):
            st.switch_page("pages/5_Materials.py")

    with col3:
        if st.button(f"✅ {get_translation('daily_checkin', current_language)}", width='stretch'):
            st.switch_page("pages/8_Check_In.py")

    # QR Code section - HIDDEN FOR NOW
    # st.markdown("---")
    # st.markdown("### 📱 Your QR Code")
    # (QR code functionality hidden but available in code)

st.write("")

# Quick access buttons (as dropdown)
with st.expander(f"▶️ {get_translation('quick_access', current_language)}", expanded=True):
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
        
        if st.button(get_translation('view_schedule', current_language), width='stretch', help="View conference schedule"):
            st.switch_page("pages/1_Agenda.py")

    with col2:
        # Check for speaker updates
        speakers_notifications = 0  # Could check for speaker updates
        
        if speakers_notifications > 0:
            badge_html = get_notification_badge(speakers_notifications)
            st.markdown(f"🎙️ **{get_translation('speakers', current_language)}** {badge_html}", unsafe_allow_html=True)
        else:
            st.markdown(f"🎙️ **{get_translation('speakers', current_language)}**")
        
        if st.button(get_translation('meet_speakers', current_language), width='stretch', help="Meet our speakers"):
            st.switch_page("pages/2_Speakers.py")

    with col3:
        # Check for exhibitor updates
        exhibitors_notifications = 0  # Could check for exhibitor updates
        
        if exhibitors_notifications > 0:
            badge_html = get_notification_badge(exhibitors_notifications)
            st.markdown(f"🏢 **{get_translation('exhibitors', current_language)}** {badge_html}", unsafe_allow_html=True)
        else:
            st.markdown(f"🏢 **{get_translation('exhibitors', current_language)}**")
        
        if st.button(get_translation('explore_booths', current_language), width='stretch', help="Explore exhibitor booths"):
            st.switch_page("pages/3_Exhibitors.py")

    with col4:
        # Sponsors button (NEW)
        st.markdown(f"🤝 **Sponsors**")
        if st.button("View Sponsors", width='stretch', help="View conference sponsors"):
            st.switch_page("pages/4_Sponsors.py")

    with col5:
        # Check for venue updates
        venue_notifications = 0  # Could check for venue updates
        
        if venue_notifications > 0:
            badge_html = get_notification_badge(venue_notifications)
            st.markdown(f"🏛️ **{get_translation('venue', current_language)}** {badge_html}", unsafe_allow_html=True)
        else:
            st.markdown(f"🏛️ **{get_translation('venue', current_language)}**")
        
        if st.button(get_translation('venue_info', current_language), width='stretch', help="Venue information"):
            st.switch_page("pages/6_Venue.py")

    with col6:
        # Check for news and announcements (COMBINED)
        announcements = load_announcements()
        news_list = load_news()
        updates_notifications = len(announcements) + len(news_list)
        
        if updates_notifications > 0:
            badge_html = get_notification_badge(updates_notifications)
            st.markdown(f"📰 **Updates & News** {badge_html}", unsafe_allow_html=True)
        else:
            st.markdown(f"📰 **Updates & News**")
        
        if st.button("Latest Updates", width='stretch', help="Latest news and announcements"):
            st.switch_page("pages/9_External_Content.py")

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
            st.markdown(f"💼 **{get_translation('matchmaking', current_language)}** {badge_html}", unsafe_allow_html=True)
        else:
            st.markdown(f"💼 **{get_translation('matchmaking', current_language)}**")
        
        if st.button(get_translation('network_now', current_language), width='stretch', help="Network with other delegates"):
            st.switch_page("pages/11_Matchmaking.py")

# Conference info
st.subheader(f"📋 {get_translation('conference_info', current_language)}")
st.info(f"""
**{get_translation('conference_dates', current_language)}:** October 6-8, 2025  
**{get_translation('location', current_language)}:** [Venue details will be shown here]  
**{get_translation('theme', current_language)}:** {get_translation('collaborate_innovate_thrive', current_language)}
""")

# What's Happening Now & Coming Up section
st.markdown("### 🎯 What's Happening Now & Coming Up")

current_session, upcoming_sessions = get_current_and_upcoming_sessions()

if current_session:
    # Current session - large featured card
    segment_type = current_session.get("segment_type", "other")
    color = SEGMENT_COLORS.get(segment_type, SEGMENT_COLORS["other"])
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {color}15 0%, {color}30 100%); 
                border-left: 6px solid {color}; 
                border-radius: 15px; 
                padding: 1.5rem; 
                margin-bottom: 1.5rem;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div>
                <span style="background: {color}; color: white; padding: 0.4rem 1rem; border-radius: 20px; 
                             font-size: 0.75rem; font-weight: 700; letter-spacing: 1px;">
                    ⚡ HAPPENING NOW
                </span>
            </div>
            <span style="background: rgba(255,255,255,0.1); color: #F3F4F6; padding: 0.3rem 0.8rem; 
                         border-radius: 15px; font-size: 0.75rem; font-weight: 600;">
                {segment_type.upper()}
            </span>
        </div>
        <h2 style="color: #F3F4F6; margin: 1rem 0 0.5rem 0; font-size: 1.5rem; font-weight: 700;">
            {current_session.get('title', 'Untitled')}
        </h2>
        <div style="color: #FFD700; font-size: 1rem; font-weight: 600; margin-bottom: 0.5rem;">
            ⏰ {current_session.get('time', 'TBA')} • 📍 {current_session.get('room', 'TBA')}
        </div>
    """, unsafe_allow_html=True)
    
    # Show speakers if available
    speakers = current_session.get("speakers", [])
    speakers = [s.strip().lstrip(',').strip() for s in speakers if s.strip().lstrip(',').strip()]
    if speakers:
        speaker_text = ", ".join(speakers)
        st.markdown(f"""
        <div style="color: #2BA300; font-size: 0.9rem; margin-top: 0.5rem;">
            🎙️ <strong>Speakers:</strong> {speaker_text}
        </div>
        """, unsafe_allow_html=True)
    
    if current_session.get("description"):
        st.markdown(f"""
        <p style="color: rgba(243, 244, 246, 0.8); margin-top: 0.75rem; line-height: 1.5;">
            {current_session.get("description")}
        </p>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("📅 No session currently in progress. Check upcoming sessions below!")

# Upcoming sessions - compact snippet cards
if upcoming_sessions:
    st.markdown("#### 📅 Coming Up Next")
    
    cols = st.columns(len(upcoming_sessions))
    
    for idx, session in enumerate(upcoming_sessions):
        with cols[idx]:
            segment_type = session.get("segment_type", "other")
            color = SEGMENT_COLORS.get(segment_type, SEGMENT_COLORS["other"])
            
            st.markdown(f"""
            <div style="background: linear-gradient(145deg, rgba(26, 26, 26, 0.9) 0%, rgba(42, 42, 42, 0.8) 100%); 
                        border-left: 4px solid {color}; 
                        border-radius: 12px; 
                        padding: 1rem; 
                        margin-bottom: 1rem;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                        transition: transform 0.2s;
                        cursor: pointer;">
                <div style="background: {color}; color: white; padding: 0.3rem 0.8rem; border-radius: 15px; 
                           font-size: 0.7rem; font-weight: 700; letter-spacing: 1px; margin-bottom: 0.75rem; display: inline-block;">
                    {segment_type.upper()}
                </div>
                <h4 style="color: #F3F4F6; margin: 0.5rem 0; font-size: 1rem; font-weight: 700; line-height: 1.3;">
                    {session.get('title', 'Untitled')[:50]}{"..." if len(session.get('title', '')) > 50 else ''}
                </h4>
                <div style="color: #FFD700; font-size: 0.85rem; font-weight: 600; margin: 0.5rem 0;">
                    ⏰ {session.get('time', 'TBA')}
                </div>
                <div style="color: #2BA300; font-size: 0.8rem; margin-top: 0.3rem;">
                    📍 {session.get('room', 'TBA')}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Show speakers if available
            speakers = session.get("speakers", [])
            speakers = [s.strip().lstrip(',').strip() for s in speakers if s.strip().lstrip(',').strip()]
            if speakers:
                st.caption(f"🎙️ {', '.join(speakers[:2])}")
    
    # Link to full schedule
    if st.button("📅 View Full Schedule", use_container_width=True, key="schedule_view_btn"):
        st.switch_page("pages/1_Agenda.py")
else:
    st.info("📋 No more sessions scheduled for today. Check the full agenda for other days!")
    if st.button("📅 View Full Schedule", use_container_width=True, key="schedule_view_btn_alt"):
        st.switch_page("pages/1_Agenda.py")

st.markdown("---")

# Updates, PR, and Networking sections
col1, col2, col3 = st.columns(3)

# Updates & News (Combined Announcements and News)
with col1:
    announcements = load_announcements()
    news_list = load_news()
    
    urgent_count = len([a for a in announcements if a.get('priority') == 'Urgent'])
    high_count = len([a for a in announcements if a.get('priority') == 'High'])
    total_updates = len(announcements) + len(news_list)
    
    # Add notification indicator to header
    if total_updates > 0:
        badge_html = get_notification_badge(total_updates)
        st.markdown(f"### 📰 Updates & News {badge_html}", unsafe_allow_html=True)
        if urgent_count > 0:
            st.error(f"🚨 {urgent_count} urgent update{'s' if urgent_count > 1 else ''} require immediate attention!")
        elif high_count > 0:
            st.warning(f"⚠️ {high_count} high priority update{'s' if high_count > 1 else ''}")
    else:
        st.subheader("📰 Updates & News")
    
    # Combine and sort all updates
    all_updates = []
    
    # Add announcements with priority
    for announcement in announcements:
        priority_order = {"Urgent": 4, "High": 3, "Normal": 2, "Low": 1}
        all_updates.append({
            'type': 'announcement',
            'data': announcement,
            'sort_key': (priority_order.get(announcement.get("priority", "Normal"), 2), announcement.get("created_at", ""))
        })
    
    # Add news
    for news_item in news_list:
        all_updates.append({
            'type': 'news',
            'data': news_item,
            'sort_key': (2, news_item.get("created_at", ""))  # Normal priority
        })
    
    # Sort by priority and date
    all_updates.sort(key=lambda x: x['sort_key'], reverse=True)
    
    if all_updates:
        # Show all updates chronologically (most recent first)
        for update_item in all_updates[:5]:  # Show latest 5
            item_type = update_item['type']
            item = update_item['data']
            
            if item_type == 'announcement':
                priority = item.get("priority", "Normal")
                priority_colors = {
                    "Urgent": "🔴",
                    "High": "🟠", 
                    "Normal": "🟡",
                    "Low": "🟢"
                }
                icon = priority_colors.get(priority, '🟡')
                badge = f"[Announcement]"
            else:  # news
                category = item.get("category", "General")
                category_colors = {
                    "General": "🔵",
                    "Conference Updates": "🟢",
                    "Industry News": "🟡",
                    "Speaker Updates": "🟣",
                    "Exhibitor News": "🟠",
                    "Schedule Changes": "🔴"
                }
                icon = category_colors.get(category, '🔵')
                badge = f"[{category}]"
            
            # Create snippet
            content_snippet = item['content'][:100] + "..." if len(item['content']) > 100 else item['content']
            relative_time = get_relative_time(item['created_at'])
            
            with st.container(border=True):
                st.markdown(f"**{icon} {item['title']}**")
                st.caption(badge)
                st.write(content_snippet)
                st.caption(f"Posted {relative_time}")
                
                if st.button(f"Read More", key=f"update_{item.get('id', 0)}_{item_type}", use_container_width=True):
                    if item_type == 'announcement':
                        st.session_state.show_announcements = True
                    else:
                        st.session_state.show_news = True
                    st.switch_page("pages/9_External_Content.py")
        
        # Show "View All" if more than 5
        if len(all_updates) > 5:
            st.markdown(f"""
            <div style="text-align: center; margin-top: 1rem;">
                <span style="color: #FF9500; font-weight: 600; font-size: 0.9rem;">
                    +{len(all_updates) - 5} more updates
                </span>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("📰 View All Updates", use_container_width=True, key="view_all_updates"):
                st.switch_page("pages/9_External_Content.py")
    else:
        st.info("No updates or news available.")

# Latest PR Posts
with col2:
    st.subheader(f"📰 {get_translation('trending_posts', current_language)}")
    pr_posts = load_pr_posts()
    
    if pr_posts:
        # Sort by time (most recent first)
        pr_posts.sort(key=lambda x: x.get('created_at', ""), reverse=True)
        
        type_colors = {
            "Trending News": "🔥",
            "Event Highlights": "🏆",
            "Speaker Spotlight": "🎙️",
            "Exhibitor Showcase": "🏢",
            "Behind the Scenes": "📹",
            "Networking Moments": "💼"
        }
        
        # Show each post individually
        for post in pr_posts[:3]:  # Show latest 3
            post_type = post.get("type", "General")
            content_snippet = post['content'][:100] + "..." if len(post['content']) > 100 else post['content']
            relative_time = get_relative_time(post['created_at'])
            
            with st.container(border=True):
                st.markdown(f"**{type_colors.get(post_type, '📰')} {post['title']}**")
                
                # Show image thumbnail if available
                if post.get('image'):
                    try:
                        st.image(post['image'], width=200)
                    except:
                        pass
                
                st.write(content_snippet)
                
                # Show hashtags
                if post.get('hashtags'):
                    hashtag_text = " ".join([f"#{tag}" for tag in post['hashtags'][:3]])
                    st.caption(f"🏷️ {hashtag_text}")
                
                # Show engagement
                engagement = post.get('engagement', {})
                if engagement:
                    likes = engagement.get('likes', 0)
                    shares = engagement.get('shares', 0)
                    st.caption(f"❤️ {format_count(likes)} • 🔄 {format_count(shares)}")
                
                st.caption(f"Posted {relative_time}")
                
                if st.button("View Post", key=f"view_pr_{post.get('id', 0)}", use_container_width=True):
                    st.switch_page("pages/10_Interactive_PR.py")
        
        # Show "View All" if more than 3
        if len(pr_posts) > 3:
            st.markdown(f"""
            <div style="text-align: center; margin-top: 1rem;">
                <span style="color: #FF9500; font-weight: 600; font-size: 0.9rem;">
                    +{len(pr_posts) - 3} more posts
                </span>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("📰 View All Posts", use_container_width=True, key="view_all_pr"):
                st.switch_page("pages/10_Interactive_PR.py")
    else:
        st.info(get_translation('no_trending_posts', current_language))

# Networking Overview
with col3:
    st.subheader(f"💼 {get_translation('networking', current_language)}")
    
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
        st.markdown(f"### 💼 {get_translation('networking', current_language)} {badge_html}", unsafe_allow_html=True)
    else:
        st.subheader(f"💼 {get_translation('networking', current_language)}")
    
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
        if st.button("🤝 Find Connections", width='stretch'):
            st.switch_page("pages/11_Matchmaking.py")
    else:
        st.success(f"🤝 You're connected with {connection_count} delegate{'s' if connection_count > 1 else ''}!")
        if st.button("🤝 Expand Network", width='stretch'):
            st.switch_page("pages/11_Matchmaking.py")

# Footer with logout button
st.markdown("---")
col_footer1, col_footer2, col_footer3 = st.columns([2, 1, 2])
with col_footer1:
    st.caption("Need help? Contact the conference organizers or visit the registration desks.")
with col_footer2:
    if st.button(f"🚪 {get_translation('logout', current_language)}", width='stretch', key="dashboard_logout"):
        # Clear all session state
        for key in list(st.session_state.keys()):
            if key.startswith('delegate_'):
                del st.session_state[key]
        st.success("✅ Logged out successfully!")
        st.switch_page("pages/0_Landing.py")
