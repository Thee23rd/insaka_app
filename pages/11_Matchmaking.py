# pages/11_Matchmaking.py
import streamlit as st
import json
import random
from datetime import datetime
from lib.ui import apply_brand

st.set_page_config(page_title="Matchmaking Portal — Insaka", page_icon="🤝", layout="wide")

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

# Get current user info
current_user_id = st.session_state.get('delegate_id', 'anonymous')
current_user_name = st.session_state.get('delegate_name', 'Anonymous User')

# Import notification system
try:
    from lib.notifications import (
        get_notification_badge, 
        get_user_notifications, 
        get_notification_count,
        get_priority_color,
        create_connection_notification,
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
    
    def get_notification_count(user_id, unread_only=True):
        return 0
    
    def get_user_notifications(user_id, unread_only=False):
        return []
    
    def get_priority_color(priority):
        return "🟡"
    
    def create_connection_notification(from_user_id, to_user_id, action):
        return True
    
    def mark_notification_read(notification_id):
        return True
    
    NOTIFICATION_SYSTEM_AVAILABLE = False

# Calculate matchmaking notifications
def get_matchmaking_notifications():
    """Calculate total matchmaking notifications"""
    try:
        with open("data/matchmaking.json", "r", encoding="utf-8") as f:
            interactions = json.load(f)
        
        current_user_id = st.session_state.get('delegate_id', 'anonymous')
        
        # Count pending connection requests and new messages
        pending_requests = len([i for i in interactions if 
                               i.get('to_user_id') == current_user_id and 
                               i.get('type') == 'connection_request' and 
                               i.get('status') == 'pending'])
        
        new_messages = len([i for i in interactions if 
                           i.get('to_user_id') == current_user_id and 
                           i.get('type') == 'chat_message' and 
                           i.get('status') == 'sent'])
        
        return pending_requests + new_messages
    except:
        return 0

matchmaking_notifications = get_matchmaking_notifications()
if matchmaking_notifications > 0:
    badge_html = get_notification_badge(matchmaking_notifications)
    st.markdown(f"# 🤝 Conference Matchmaking Portal {badge_html}", unsafe_allow_html=True)
else:
    st.markdown("# 🤝 Conference Matchmaking Portal")

st.markdown("Connect with fellow delegates and expand your network")

# Add sound notification script for PWA
if NOTIFICATION_SYSTEM_AVAILABLE:
    try:
        from lib.notifications import get_sound_notification_script
        st.markdown(get_sound_notification_script(), unsafe_allow_html=True)
    except:
        pass

# Quick sound test for matchmaking
# if NOTIFICATION_SYSTEM_AVAILABLE:
#     st.markdown("### 🔊 Sound Test")
#     if st.button("🔊🔊🔊 TEST LOUD NOTIFICATION 🔊🔊🔊", width='stretch', type="primary"):
#         st.markdown("""
#         <script>
#         console.log('🔊 MATCHMAKING SOUND TEST...');
#         if (window.triggerNotificationFeedback) {
#             window.triggerNotificationFeedback();
#         }
#         </script>
#         """, unsafe_allow_html=True)
#         st.success("🔊 LOUD NOTIFICATION TEST TRIGGERED!")
#         st.balloons()

st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

# Authentication check
if not hasattr(st.session_state, 'delegate_authenticated') or not st.session_state.delegate_authenticated:
    st.error("🔒 Authentication Required")
    st.info("Please authenticate first by visiting the Delegate Self-Service page.")
    
    if st.button("🔑 Go to Authentication", width='stretch'):
        st.switch_page("pages/7_Delegate_Self_Service.py")
    
    st.stop()

# Show authenticated user info
col_header, col_logout = st.columns([3, 1])
with col_header:
    st.success(f"✅ Authenticated as: **{st.session_state.delegate_name}** (ID: {st.session_state.delegate_id})")
with col_logout:
    if st.button("🚪 Logout", width='stretch'):
        # Clear all session state
        for key in list(st.session_state.keys()):
            if key.startswith('delegate_'):
                del st.session_state[key]
        st.rerun()

# Helper functions
def load_delegates():
    """Load delegates list"""
    try:
        from staff_service import load_staff_df
        df = load_staff_df()
        return df[["ID", "Name", "Organization", "Category", "RoleTitle", "Email", "Phone"]].to_dict('records')
    except Exception:
        return []

def load_matchmaking_data():
    """Load matchmaking interactions"""
    try:
        with open("data/matchmaking.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_matchmaking_data(data):
    """Save matchmaking interactions"""
    with open("data/matchmaking.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_relative_time(iso_timestamp):
    """Convert ISO timestamp to relative time"""
    try:
        created_time = datetime.fromisoformat(iso_timestamp)
        now = datetime.now()
        diff = now - created_time
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        else:
            hours = diff.seconds // 3600
            if hours > 0:
                return f"{hours} hour{'s' if hours > 1 else ''} ago"
            else:
                minutes = diff.seconds // 60
                return f"{minutes} minute{'s' if minutes > 1 else ''} ago" if minutes > 0 else "just now"
    except:
        return "recently"

def get_user_interactions(user_id):
    """Get all interactions for a user"""
    interactions = load_matchmaking_data()
    return [i for i in interactions if i.get('from_user_id') == user_id or i.get('to_user_id') == user_id]

def get_connection_status(user1_id, user2_id):
    """Get connection status between two users"""
    interactions = load_matchmaking_data()
    
    # Check for any existing interactions
    for interaction in interactions:
        if ((interaction.get('from_user_id') == user1_id and interaction.get('to_user_id') == user2_id) or
            (interaction.get('from_user_id') == user2_id and interaction.get('to_user_id') == user1_id)):
            return interaction.get('status', 'pending')
    
    return 'none'

# Get current user info
current_user_id = st.session_state.get('delegate_id', 'anonymous')
current_user_name = st.session_state.get('delegate_name', 'Anonymous User')
current_user_org = st.session_state.get('delegate_organization', 'Unknown Organization')

# Back to dashboard button
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("🏠 Back to Dashboard", width='stretch'):
        st.switch_page("pages/1_Delegate_Dashboard.py")

with col2:
    st.markdown("### 🤝 Connect with Fellow Delegates")
    st.markdown(f"**👤 {current_user_name}** • {current_user_org}")

with col3:
    st.markdown("### 💡 Networking Tips")
    st.caption("💼 Be professional\n📱 Share contact info\n🤝 Schedule meetings\n🌐 Build your network")

st.markdown("---")

# Load delegates
delegates = load_delegates()

if not delegates:
    st.error("No delegates found. Please check back later.")
    st.stop()

# Filter out current user
other_delegates = [d for d in delegates if str(d.get('ID')) != str(current_user_id)]

if not other_delegates:
    st.info("You're the only delegate in the system!")
    st.stop()

# Tabs for different matchmaking features
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🔍 Browse Delegates", "📩 Connection Requests", "💬 My Conversations", "📞 Contact Sharing", "📅 Meeting Requests", "🎯 Recommended Matches"])

with tab1:
    st.markdown("### 👥 All Delegates")
    
    # Search and filter options
    col_search, col_filter = st.columns([2, 1])
    
    with col_search:
        search_term = st.text_input("🔍 Search delegates", placeholder="Name, organization, or role...")
    
    with col_filter:
        category_filter = st.selectbox("📋 Filter by Category", ["All"] + list(set([d.get('Category', '') for d in other_delegates])))
    
    # Filter delegates
    filtered_delegates = other_delegates
    
    if search_term:
        filtered_delegates = [d for d in filtered_delegates if 
                            search_term.lower() in d.get('Name', '').lower() or
                            search_term.lower() in d.get('Organization', '').lower() or
                            search_term.lower() in d.get('RoleTitle', '').lower()]
    
    if category_filter != "All":
        filtered_delegates = [d for d in filtered_delegates if d.get('Category') == category_filter]
    
    # Display delegates in a grid
    if filtered_delegates:
        # Display in rows of 3
        for i in range(0, len(filtered_delegates), 3):
            cols = st.columns(3)
            
            for j, col in enumerate(cols):
                if i + j < len(filtered_delegates):
                    delegate = filtered_delegates[i + j]
                    
                    with col:
                        with st.container(border=True):
                            # Delegate info
                            st.markdown(f"**👤 {delegate.get('Name', 'Unknown')}**")
                            st.write(f"🏢 {delegate.get('Organization', 'Unknown')}")
                            st.write(f"📋 {delegate.get('Category', 'Unknown')}")
                            
                            if delegate.get('RoleTitle'):
                                st.write(f"💼 {delegate.get('RoleTitle')}")
                            
                            # Connection status
                            connection_status = get_connection_status(current_user_id, delegate.get('ID'))
                            
                            if connection_status == 'none':
                                if st.button(f"🤝 Connect", key=f"connect_{delegate.get('ID')}", width='stretch'):
                                    # Send connection request
                                    interactions = load_matchmaking_data()
                                    new_interaction = {
                                        "id": len(interactions) + 1,
                                        "from_user_id": current_user_id,
                                        "to_user_id": delegate.get('ID'),
                                        "from_user_name": current_user_name,
                                        "to_user_name": delegate.get('Name'),
                                        "type": "connection_request",
                                        "status": "pending",
                                        "message": f"{current_user_name} wants to connect with you",
                                        "created_at": datetime.now().isoformat()
                                    }
                                    interactions.append(new_interaction)
                                    save_matchmaking_data(interactions)
                                    
                                    # Create notification for the recipient
                                    if NOTIFICATION_SYSTEM_AVAILABLE:
                                        try:
                                            create_connection_notification(current_user_id, delegate.get('ID'), "request")
                                        except:
                                            pass
                                    
                                    st.success(f"✅ Connection request sent to {delegate.get('Name')}!")
                                    st.rerun()
                            
                            elif connection_status == 'pending':
                                st.info("⏳ Connection pending")
                            
                            elif connection_status == 'accepted':
                                col_chat, col_meet = st.columns(2)
                                
                                with col_chat:
                                    if st.button(f"💬 Chat", key=f"chat_{delegate.get('ID')}", width='stretch'):
                                        st.session_state.selected_chat_user = delegate
                                        st.session_state.selected_chat_user_id = delegate.get('ID')
                                        st.rerun()
                                
                                with col_meet:
                                    if st.button(f"📅 Meet", key=f"meet_{delegate.get('ID')}", width='stretch'):
                                        st.session_state.show_meeting_request = True
                                        st.session_state.meeting_target_user = delegate
                                        st.rerun()
                            
                            elif connection_status == 'declined':
                                st.warning("❌ Connection declined")
    else:
        st.info("No delegates found matching your criteria.")

with tab2:
    st.markdown("### 📩 Connection Requests")
    
    # Get pending connection requests
    user_interactions = get_user_interactions(current_user_id)
    pending_requests = [i for i in user_interactions if 
                       i.get('to_user_id') == current_user_id and 
                       i.get('type') == 'connection_request' and 
                       i.get('status') == 'pending']
    
    # Get sent requests
    sent_requests = [i for i in user_interactions if 
                    i.get('from_user_id') == current_user_id and 
                    i.get('type') == 'connection_request']
    
    if pending_requests:
        st.markdown("#### 📥 Incoming Requests")
        for request in pending_requests:
            with st.container(border=True):
                st.markdown(f"**👤 {request.get('from_user_name')}** wants to connect with you")
                st.write(f"💬 Message: {request.get('message', 'No message')}")
                st.caption(f"Requested {get_relative_time(request.get('created_at', ''))}")
                
                # Accept/Decline buttons
                col_accept, col_decline = st.columns(2)
                
                with col_accept:
                    if st.button("✅ Accept Connection", key=f"accept_conn_{request.get('id')}", width='stretch'):
                        # Update connection status
                        interactions = load_matchmaking_data()
                        for i in interactions:
                            if i.get('id') == request.get('id'):
                                i['status'] = 'accepted'
                                break
                        save_matchmaking_data(interactions)
                        
                        # Create notification for the sender
                        if NOTIFICATION_SYSTEM_AVAILABLE:
                            try:
                                create_connection_notification(current_user_id, request.get('from_user_id'), "accepted")
                            except:
                                pass
                        
                        st.success(f"✅ Connected with {request.get('from_user_name')}!")
                        st.balloons()
                        st.rerun()
                
                with col_decline:
                    if st.button("❌ Decline", key=f"decline_conn_{request.get('id')}", width='stretch'):
                        # Update connection status
                        interactions = load_matchmaking_data()
                        for i in interactions:
                            if i.get('id') == request.get('id'):
                                i['status'] = 'declined'
                                break
                        save_matchmaking_data(interactions)
                        st.info(f"❌ Declined connection from {request.get('from_user_name')}")
                        st.rerun()
        
        st.markdown("---")
    
    if sent_requests:
        st.markdown("#### 📤 Sent Requests")
        for request in sent_requests:
            with st.container(border=True):
                status = request.get('status', 'pending')
                status_emoji = {
                    'pending': '⏳',
                    'accepted': '✅',
                    'declined': '❌'
                }
                
                st.markdown(f"**👤 {request.get('to_user_name')}** {status_emoji.get(status, '❓')} {status.title()}")
                st.caption(f"Sent {get_relative_time(request.get('created_at', ''))}")
                
                if status == 'pending':
                    st.info("Waiting for response...")
                elif status == 'accepted':
                    st.success("Connection accepted! You can now chat and schedule meetings.")
                elif status == 'declined':
                    st.warning("Connection declined.")
    
    if not pending_requests and not sent_requests:
        st.info("No connection requests yet. Browse delegates to start connecting!")

with tab3:
    st.markdown("### 💬 My Conversations")
    
    # Get user's accepted connections
    connections = []
    
    # Find accepted connections
    for interaction in user_interactions:
        if interaction.get('status') == 'accepted':
            if interaction.get('from_user_id') == current_user_id:
                connections.append({
                    'user_id': interaction.get('to_user_id'),
                    'user_name': interaction.get('to_user_name'),
                    'last_interaction': interaction.get('created_at')
                })
            elif interaction.get('to_user_id') == current_user_id:
                connections.append({
                    'user_id': interaction.get('from_user_id'),
                    'user_name': interaction.get('from_user_name'),
                    'last_interaction': interaction.get('created_at')
                })
    
    if connections:
        # Remove duplicates
        unique_connections = []
        seen_ids = set()
        for conn in connections:
            if conn['user_id'] not in seen_ids:
                unique_connections.append(conn)
                seen_ids.add(conn['user_id'])
        
        # Check for new messages
        new_messages_count = 0
        for conn in unique_connections:
            # Count unread messages from this connection
            unread_messages = [i for i in user_interactions if 
                             i.get('type') == 'chat_message' and 
                             i.get('from_user_id') == conn['user_id'] and 
                             i.get('to_user_id') == current_user_id and 
                             i.get('status') == 'sent']
            new_messages_count += len(unread_messages)
        
        if new_messages_count > 0:
            st.info(f"📩 You have {new_messages_count} new message{'s' if new_messages_count > 1 else ''}!")
        
        # Display conversations
        for conn in unique_connections:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**💬 {conn['user_name']}**")
                    last_time = get_relative_time(conn.get('last_interaction', ''))
                    st.caption(f"Last interaction: {last_time}")
                
                with col2:
                    col_chat, col_contact = st.columns(2)
                    
                    with col_chat:
                        if st.button("💬 Chat", key=f"conversation_{conn['user_id']}"):
                            st.session_state.selected_chat_user = {'Name': conn['user_name'], 'ID': conn['user_id']}
                            st.session_state.selected_chat_user_id = conn['user_id']
                            st.rerun()
                    
                    with col_contact:
                        if st.button("📞 Contact", key=f"contact_{conn['user_id']}"):
                            st.session_state.show_contact_form = True
                            st.session_state.contact_target_user = {'Name': conn['user_name'], 'ID': conn['user_id']}
                            st.rerun()
    else:
        st.info("No active conversations. Connect with delegates to start chatting!")
    
    # Chat interface
    if hasattr(st.session_state, 'selected_chat_user') and st.session_state.selected_chat_user:
        st.markdown("---")
        st.markdown(f"### 💬 Chat with {st.session_state.selected_chat_user.get('Name')}")
        
        # Show chat history
        chat_messages = [i for i in user_interactions if 
                        i.get('type') == 'chat_message' and 
                        ((i.get('from_user_id') == current_user_id and i.get('to_user_id') == st.session_state.selected_chat_user_id) or
                         (i.get('to_user_id') == current_user_id and i.get('from_user_id') == st.session_state.selected_chat_user_id))]
        
        # Mark messages as read when viewing chat
        if chat_messages:
            # Mark unread messages as read
            interactions = load_matchmaking_data()
            for msg in chat_messages:
                if msg.get('to_user_id') == current_user_id and msg.get('status') == 'sent':
                    for i in interactions:
                        if i.get('id') == msg.get('id'):
                            i['status'] = 'read'
                            break
            save_matchmaking_data(interactions)
            
            st.markdown("**Chat History:**")
            for msg in sorted(chat_messages, key=lambda x: x.get('created_at', '')):
                is_from_me = msg.get('from_user_id') == current_user_id
                if is_from_me:
                    st.markdown(f"**You:** {msg.get('message')}")
                else:
                    st.markdown(f"**{msg.get('from_user_name')}:** {msg.get('message')}")
                st.caption(f"Sent {get_relative_time(msg.get('created_at', ''))}")
                st.markdown("---")
        
        # Simple chat interface (in a real app, this would be more sophisticated)
        with st.form("chat_form"):
            message = st.text_area("Type your message:", placeholder="Message...")
            
            col_send, col_close = st.columns([1, 1])
            
            with col_send:
                    if st.form_submit_button("📤 Send Message", width='stretch'):
                        if message.strip():
                            # Save chat message to matchmaking data
                            interactions = load_matchmaking_data()
                            new_message = {
                                "id": len(interactions) + 1,
                                "from_user_id": current_user_id,
                                "to_user_id": st.session_state.selected_chat_user_id,
                                "from_user_name": current_user_name,
                                "to_user_name": st.session_state.selected_chat_user.get('Name'),
                                "type": "chat_message",
                                "status": "sent",
                                "message": message.strip(),
                                "created_at": datetime.now().isoformat()
                            }
                            interactions.append(new_message)
                            save_matchmaking_data(interactions)
                            st.success(f"✅ Message sent to {st.session_state.selected_chat_user.get('Name')}!")
                            st.rerun()
            
            with col_close:
                if st.form_submit_button("❌ Close Chat", width='stretch'):
                    st.session_state.selected_chat_user = None
                    st.session_state.selected_chat_user_id = None
                    st.rerun()
    
    # Quick contact sharing form
    if hasattr(st.session_state, 'show_contact_form') and st.session_state.show_contact_form:
        st.markdown("---")
        st.markdown(f"### 📞 Send Contact Info to {st.session_state.contact_target_user.get('Name')}")
        
        with st.form("quick_contact_form"):
            # Get current user's contact info
            current_user_delegate = None
            for d in delegates:
                if str(d.get('ID')) == str(current_user_id):
                    current_user_delegate = d
                    break
            
            if current_user_delegate:
                st.info("📋 Your contact information is pulled from your registration data.")
                
                email_available = bool(str(current_user_delegate.get('Email', '')).strip())
                phone_value = current_user_delegate.get('Phone', '')
                phone_available = bool(str(phone_value).strip()) if phone_value is not None and str(phone_value) != 'nan' else False
                
                col1, col2 = st.columns(2)
                
                with col1:
                    email = st.text_input("Email", value=current_user_delegate.get('Email', ''), disabled=True)
                
                with col2:
                    phone_display = str(current_user_delegate.get('Phone', '')) if current_user_delegate.get('Phone') is not None and str(current_user_delegate.get('Phone')) != 'nan' else ''
                    phone = st.text_input("Phone Number", value=phone_display, disabled=True)
                
                personal_message = st.text_area("Message", placeholder="Hi! Here are my contact details...")
                
                # Share options
                share_email = st.checkbox("📧 Share Email", value=email_available, disabled=not email_available)
                share_phone = st.checkbox("📱 Share Phone", value=phone_available, disabled=not phone_available)
                
                col_send, col_cancel = st.columns(2)
                
                with col_send:
                    if st.form_submit_button("📤 Send Contact Info", width='stretch'):
                        if not (share_email or share_phone):
                            st.error("Please select at least one contact method!")
                        elif share_phone and not phone_display.strip():
                            st.error("Phone number is not available in your registration data!")
                        else:
                            # Create contact sharing
                            contact_info = []
                            if share_email and email:
                                contact_info.append(f"📧 Email: {email}")
                            if share_phone and phone_display:
                                contact_info.append(f"📱 Phone: {phone_display}")
                            
                            contact_message = f"{personal_message}\n\n**My Contact Information:**\n" + "\n".join(contact_info) if personal_message else f"**My Contact Information:**\n" + "\n".join(contact_info)
                            
                            # Save to matchmaking data
                            interactions = load_matchmaking_data()
                            new_interaction = {
                                "id": len(interactions) + 1,
                                "from_user_id": current_user_id,
                                "to_user_id": st.session_state.contact_target_user.get('ID'),
                                "from_user_name": current_user_name,
                                "to_user_name": st.session_state.contact_target_user.get('Name'),
                                "type": "contact_sharing",
                                "status": "sent",
                                "message": contact_message,
                                "contact_info": {
                                    "email": email if share_email else None,
                                    "phone": phone_display if share_phone else None
                                },
                                "created_at": datetime.now().isoformat()
                            }
                            interactions.append(new_interaction)
                            save_matchmaking_data(interactions)
                            
                            st.success(f"✅ Contact info sent to {st.session_state.contact_target_user.get('Name')}!")
                            st.balloons()
                            st.session_state.show_contact_form = False
                            st.session_state.contact_target_user = None
                            st.rerun()
                
                with col_cancel:
                    if st.form_submit_button("❌ Cancel", width='stretch'):
                        st.session_state.show_contact_form = False
                        st.session_state.contact_target_user = None
                        st.rerun()

with tab4:
    st.markdown("### 📞 Contact Sharing")
    
    # Get user's accepted connections for contact sharing
    user_interactions = get_user_interactions(current_user_id)
    accepted_connections = []
    
    for interaction in user_interactions:
        if interaction.get('status') == 'accepted':
            if interaction.get('from_user_id') == current_user_id:
                accepted_connections.append({
                    'user_id': interaction.get('to_user_id'),
                    'user_name': interaction.get('to_user_name')
                })
            elif interaction.get('to_user_id') == current_user_id:
                accepted_connections.append({
                    'user_id': interaction.get('from_user_id'),
                    'user_name': interaction.get('from_user_name')
                })
    
    # Remove duplicates
    unique_connections = []
    seen_ids = set()
    for conn in accepted_connections:
        if conn['user_id'] not in seen_ids:
            unique_connections.append(conn)
            seen_ids.add(conn['user_id'])
    
    if unique_connections:
        st.markdown("**📋 Share your contact information with connected delegates:**")
        
        # Show available contact information
        current_user_delegate = None
        for d in delegates:
            if str(d.get('ID')) == str(current_user_id):
                current_user_delegate = d
                break
        
        if current_user_delegate:
            with st.container(border=True):
                st.markdown("**📞 Your Available Contact Information:**")
                col1, col2 = st.columns(2)
                
                with col1:
                    email_available = bool(str(current_user_delegate.get('Email', '')).strip())
                    phone_value = current_user_delegate.get('Phone', '')
                    phone_available = bool(str(phone_value).strip()) if phone_value is not None and str(phone_value) != 'nan' else False
                    
                    if email_available:
                        st.success(f"📧 Email: {current_user_delegate.get('Email')}")
                    else:
                        st.warning("📧 Email: Not provided")
                
                with col2:
                    if phone_available:
                        phone_display = str(current_user_delegate.get('Phone', '')) if current_user_delegate.get('Phone') is not None and str(current_user_delegate.get('Phone')) != 'nan' else ''
                        st.success(f"📱 Phone: {phone_display}")
                    else:
                        st.warning("📱 Phone: Not provided")
        
        # Contact sharing form
        with st.form("contact_sharing_form"):
            # Select recipient
            recipient_options = {f"{conn['user_name']} (ID: {conn['user_id']})": conn['user_id'] for conn in unique_connections}
            selected_recipient = st.selectbox("Select delegate to share contact with:", list(recipient_options.keys()))
            
            # Get current user's contact info
            current_user_delegate = None
            for d in delegates:
                if str(d.get('ID')) == str(current_user_id):
                    current_user_delegate = d
                    break
            
            if current_user_delegate:
                st.markdown("**Your Contact Information:**")
                st.info("📋 Your email and phone number are automatically pulled from your registration data. You can add additional contact details below.")
                col1, col2 = st.columns(2)
                
                with col1:
                    email = st.text_input("Email", value=current_user_delegate.get('Email', ''), disabled=True)
                
                with col2:
                    phone_display = str(current_user_delegate.get('Phone', '')) if current_user_delegate.get('Phone') is not None and str(current_user_delegate.get('Phone')) != 'nan' else ''
                    phone = st.text_input("Phone Number", value=phone_display, disabled=True)
                
                # Additional contact options
                st.markdown("**Additional Information:**")
                linkedin = st.text_input("LinkedIn Profile", placeholder="https://linkedin.com/in/yourprofile")
                company_website = st.text_input("Company Website", placeholder="https://yourcompany.com")
                
                # Personal message
                personal_message = st.text_area("Personal Message", placeholder="Hi! I'd love to connect with you. Here are my contact details...")
                
                # Share options
                st.markdown("**What to share:**")
                share_email = st.checkbox("📧 Email Address", value=email_available, disabled=not email_available)
                share_phone = st.checkbox("📱 Phone Number", value=phone_available, disabled=not phone_available)
                share_linkedin = st.checkbox("💼 LinkedIn Profile", value=False)
                share_website = st.checkbox("🌐 Company Website", value=False)
                
                col_send, col_cancel = st.columns(2)
                
                with col_send:
                    if st.form_submit_button("📤 Send Contact Information", width='stretch'):
                        if not (share_email or share_phone or share_linkedin or share_website):
                            st.error("Please select at least one contact method to share!")
                        elif share_phone and not phone_display.strip():
                            st.error("Phone number is not available in your registration data!")
                        else:
                            # Create contact sharing request
                            recipient_id = recipient_options[selected_recipient]
                            recipient_name = selected_recipient.split(" (ID:")[0]
                            
                            contact_info = []
                            if share_email and email:
                                contact_info.append(f"📧 Email: {email}")
                            if share_phone and phone_display:
                                contact_info.append(f"📱 Phone: {phone_display}")
                            if share_linkedin and linkedin:
                                contact_info.append(f"💼 LinkedIn: {linkedin}")
                            if share_website and company_website:
                                contact_info.append(f"🌐 Website: {company_website}")
                            
                            # Create the contact sharing message
                            contact_message = f"{personal_message}\n\n**My Contact Information:**\n" + "\n".join(contact_info) if personal_message else f"**My Contact Information:**\n" + "\n".join(contact_info)
                            
                            # Save contact sharing interaction
                            interactions = load_matchmaking_data()
                            new_interaction = {
                                "id": len(interactions) + 1,
                                "from_user_id": current_user_id,
                                "to_user_id": recipient_id,
                                "from_user_name": current_user_name,
                                "to_user_name": recipient_name,
                                "type": "contact_sharing",
                                "status": "sent",
                                "message": contact_message,
                                "contact_info": {
                                    "email": email if share_email else None,
                                    "phone": phone_display if share_phone else None,
                                    "linkedin": linkedin if share_linkedin else None,
                                    "website": company_website if share_website else None
                                },
                                "created_at": datetime.now().isoformat()
                            }
                            interactions.append(new_interaction)
                            save_matchmaking_data(interactions)
                            
                            st.success(f"✅ Contact information sent to {recipient_name}!")
                            st.balloons()
                            st.rerun()
                
                with col_cancel:
                    if st.form_submit_button("❌ Cancel", width='stretch'):
                        st.rerun()
    else:
        st.info("No connected delegates yet. Connect with delegates first to share contact information!")
    
    # Show received contact information
    st.markdown("---")
    st.markdown("### 📥 Received Contact Information")
    
    # Get received contact sharing
    received_contacts = [i for i in user_interactions if 
                        i.get('to_user_id') == current_user_id and 
                        i.get('type') == 'contact_sharing']
    
    if received_contacts:
        for contact in received_contacts:
            with st.container(border=True):
                st.markdown(f"**📞 From: {contact.get('from_user_name')}**")
                st.caption(f"Received {get_relative_time(contact.get('created_at', ''))}")
                
                # Display contact information
                contact_info = contact.get('contact_info', {})
                if contact_info:
                    st.markdown("**Contact Details:**")
                    
                    if contact_info.get('email'):
                        st.write(f"📧 **Email:** {contact_info['email']}")
                    
                    if contact_info.get('phone'):
                        st.write(f"📱 **Phone:** {contact_info['phone']}")
                    
                    if contact_info.get('linkedin'):
                        st.write(f"💼 **LinkedIn:** {contact_info['linkedin']}")
                    
                    if contact_info.get('website'):
                        st.write(f"🌐 **Website:** {contact_info['website']}")
                
                # Display personal message
                if contact.get('message'):
                    st.markdown("**Message:**")
                    st.write(contact.get('message'))
                
                # Action buttons
                col_copy, col_save = st.columns(2)
                
                with col_copy:
                    if st.button("📋 Copy All", key=f"copy_contact_{contact.get('id')}"):
                        # Create copyable text
                        copy_text = f"Contact Information from {contact.get('from_user_name')}:\n"
                        if contact_info.get('email'):
                            copy_text += f"Email: {contact_info['email']}\n"
                        if contact_info.get('phone'):
                            copy_text += f"Phone: {contact_info['phone']}\n"
                        if contact_info.get('linkedin'):
                            copy_text += f"LinkedIn: {contact_info['linkedin']}\n"
                        if contact_info.get('website'):
                            copy_text += f"Website: {contact_info['website']}\n"
                        
                        st.code(copy_text, language="text")
                        st.success("Contact information copied!")
                
                with col_save:
                    if st.button("💾 Save to Contacts", key=f"save_contact_{contact.get('id')}"):
                        st.info("💡 Tip: Copy the contact information above and save it to your phone's contacts app!")
    else:
        st.info("No contact information received yet.")

with tab5:
    st.markdown("### 📅 Meeting Requests")
    
    # Get meeting requests
    user_interactions = get_user_interactions(current_user_id)
    meeting_requests = [i for i in user_interactions if i.get('type') == 'meeting_request']
    
    if meeting_requests:
        for request in meeting_requests:
            with st.container(border=True):
                if request.get('from_user_id') == current_user_id:
                    # Sent requests
                    st.markdown(f"**📤 Sent to: {request.get('to_user_name')}**")
                    st.write(f"📅 Meeting: {request.get('meeting_type', 'General meeting')}")
                    st.write(f"💬 Message: {request.get('message', 'No message')}")
                    status = request.get('status', 'pending')
                    
                    if status == 'pending':
                        st.info("⏳ Awaiting response")
                    elif status == 'accepted':
                        st.success("✅ Meeting accepted!")
                    elif status == 'declined':
                        st.warning("❌ Meeting declined")
                
                else:
                    # Received requests
                    st.markdown(f"**📥 From: {request.get('from_user_name')}**")
                    st.write(f"📅 Meeting: {request.get('meeting_type', 'General meeting')}")
                    st.write(f"💬 Message: {request.get('message', 'No message')}")
                    
                    if request.get('status') == 'pending':
                        col_accept, col_decline = st.columns(2)
                        
                        with col_accept:
                            if st.button("✅ Accept", key=f"accept_meeting_{request.get('id')}"):
                                # Update meeting status
                                interactions = load_matchmaking_data()
                                for i in interactions:
                                    if i.get('id') == request.get('id'):
                                        i['status'] = 'accepted'
                                        break
                                save_matchmaking_data(interactions)
                                st.success("Meeting accepted!")
                                st.rerun()
                        
                        with col_decline:
                            if st.button("❌ Decline", key=f"decline_meeting_{request.get('id')}"):
                                # Update meeting status
                                interactions = load_matchmaking_data()
                                for i in interactions:
                                    if i.get('id') == request.get('id'):
                                        i['status'] = 'declined'
                                        break
                                save_matchmaking_data(interactions)
                                st.success("Meeting declined.")
                                st.rerun()
                    
                    elif request.get('status') == 'accepted':
                        st.success("✅ You accepted this meeting")
                    elif request.get('status') == 'declined':
                        st.warning("❌ You declined this meeting")
                
                st.caption(f"Requested {get_relative_time(request.get('created_at', ''))}")
    else:
        st.info("No meeting requests yet. Connect with delegates to start scheduling meetings!")
    
    # Meeting request form
    if hasattr(st.session_state, 'show_meeting_request') and st.session_state.show_meeting_request:
        st.markdown("---")
        st.markdown(f"### 📅 Request Meeting with {st.session_state.meeting_target_user.get('Name')}")
        
        with st.form("meeting_request_form"):
            meeting_type = st.selectbox("Meeting Type", [
                "Coffee Chat", "Business Discussion", "Networking", 
                "Collaboration", "General Meeting", "Quick Chat"
            ])
            
            message = st.text_area("Message (Optional)", placeholder="Hi! I'd like to meet with you to discuss...")
            
            col_send, col_cancel = st.columns(2)
            
            with col_send:
                if st.form_submit_button("📤 Send Request", width='stretch'):
                    # Create meeting request
                    interactions = load_matchmaking_data()
                    new_request = {
                        "id": len(interactions) + 1,
                        "from_user_id": current_user_id,
                        "to_user_id": st.session_state.meeting_target_user.get('ID'),
                        "from_user_name": current_user_name,
                        "to_user_name": st.session_state.meeting_target_user.get('Name'),
                        "type": "meeting_request",
                        "status": "pending",
                        "meeting_type": meeting_type,
                        "message": message.strip() if message.strip() else f"Would like to schedule a {meeting_type.lower()}",
                        "created_at": datetime.now().isoformat()
                    }
                    interactions.append(new_request)
                    save_matchmaking_data(interactions)
                    
                    st.success(f"Meeting request sent to {st.session_state.meeting_target_user.get('Name')}!")
                    st.session_state.show_meeting_request = False
                    st.session_state.meeting_target_user = None
                    st.rerun()
            
            with col_cancel:
                if st.form_submit_button("❌ Cancel", width='stretch'):
                    st.session_state.show_meeting_request = False
                    st.session_state.meeting_target_user = None
                    st.rerun()

with tab6:
    st.markdown("### 🎯 Recommended Matches")
    
    # Simple recommendation algorithm
    current_user_delegate = None
    for d in delegates:
        if str(d.get('ID')) == str(current_user_id):
            current_user_delegate = d
            break
    
    if current_user_delegate:
        # Find delegates with similar characteristics
        recommendations = []
        
        for delegate in other_delegates:
            score = 0
            
            # Same organization (higher weight)
            if delegate.get('Organization') == current_user_delegate.get('Organization'):
                score += 10
            
            # Same category
            if delegate.get('Category') == current_user_delegate.get('Category'):
                score += 5
            
            # Similar roles
            if (delegate.get('RoleTitle') and current_user_delegate.get('RoleTitle') and
                any(word in delegate.get('RoleTitle', '').lower() for word in current_user_delegate.get('RoleTitle', '').lower().split())):
                score += 3
            
            if score > 0:
                recommendations.append((delegate, score))
        
        # Sort by score
        recommendations.sort(key=lambda x: x[1], reverse=True)
        
        if recommendations:
            st.markdown("**💡 Based on your profile, we recommend these connections:**")
            
            for delegate, score in recommendations[:5]:  # Show top 5
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**👤 {delegate.get('Name')}**")
                        st.write(f"🏢 {delegate.get('Organization')}")
                        st.write(f"📋 {delegate.get('Category')}")
                        if delegate.get('RoleTitle'):
                            st.write(f"💼 {delegate.get('RoleTitle')}")
                        
                        # Show why recommended
                        reasons = []
                        if delegate.get('Organization') == current_user_delegate.get('Organization'):
                            reasons.append("Same organization")
                        if delegate.get('Category') == current_user_delegate.get('Category'):
                            reasons.append("Same category")
                        if reasons:
                            st.caption(f"💡 Recommended: {', '.join(reasons)}")
                    
                    with col2:
                        connection_status = get_connection_status(current_user_id, delegate.get('ID'))
                        
                        if connection_status == 'none':
                            if st.button(f"🤝 Connect", key=f"rec_connect_{delegate.get('ID')}", width='stretch'):
                                # Send connection request
                                interactions = load_matchmaking_data()
                                new_interaction = {
                                    "id": len(interactions) + 1,
                                    "from_user_id": current_user_id,
                                    "to_user_id": delegate.get('ID'),
                                    "from_user_name": current_user_name,
                                    "to_user_name": delegate.get('Name'),
                                    "type": "connection_request",
                                    "status": "pending",
                                    "message": f"{current_user_name} wants to connect with you",
                                    "created_at": datetime.now().isoformat()
                                }
                                interactions.append(new_interaction)
                                save_matchmaking_data(interactions)
                                
                                # Create notification for the recipient
                                if NOTIFICATION_SYSTEM_AVAILABLE:
                                    try:
                                        create_connection_notification(current_user_id, delegate.get('ID'), "request")
                                    except:
                                        pass
                                
                                st.success(f"✅ Connection request sent to {delegate.get('Name')}!")
                                st.rerun()
                        
                        elif connection_status == 'pending':
                            st.info("⏳ Pending")
                        
                        elif connection_status == 'accepted':
                            if st.button(f"💬 Chat", key=f"rec_chat_{delegate.get('ID')}", width='stretch'):
                                st.session_state.selected_chat_user = delegate
                                st.session_state.selected_chat_user_id = delegate.get('ID')
                                st.rerun()
        else:
            st.info("No specific recommendations available. Browse all delegates to find interesting connections!")
    else:
        st.info("Unable to generate recommendations. Please check your profile information.")

# Footer with logout button
st.markdown("---")
col_footer1, col_footer2, col_footer3 = st.columns([2, 1, 2])
with col_footer1:
    st.caption("💡 Tip: Be professional, respectful, and genuine in your networking interactions!")
with col_footer2:
    if st.button("🚪 Logout", width='stretch', key="matchmaking_logout"):
        # Clear all session state
        for key in list(st.session_state.keys()):
            if key.startswith('delegate_'):
                del st.session_state[key]
        st.success("✅ Logged out successfully!")
        st.switch_page("pages/0_Landing.py")
