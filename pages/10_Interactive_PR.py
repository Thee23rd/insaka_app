# pages/10_Interactive_PR.py
import streamlit as st
import json
from datetime import datetime
from lib.ui import apply_brand

st.set_page_config(page_title="Interactive PR Posts — Insaka", page_icon="📸", layout="wide")

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

# Notification Helper Function
def get_notification_badge(count, max_show=99):
    """Generate notification badge text (no HTML)"""
    if count > 0:
        if count > max_show:
            return f" ({max_show}+)"
        else:
            return f" ({count})"
    return ""

# Calculate total engagement notifications
def get_engagement_notifications():
    """Calculate total engagement notifications"""
    try:
        with open("data/pr_posts.json", "r", encoding="utf-8") as f:
            posts = json.load(f)
        
        total_engagement = 0
        for post in posts:
            engagement = post.get('engagement', {})
            total_engagement += engagement.get('likes', 0) + engagement.get('shares', 0) + engagement.get('views', 0)
        
        return total_engagement
    except:
        return 0

engagement_notifications = get_engagement_notifications()
if engagement_notifications > 0:
    badge_html = get_notification_badge(engagement_notifications)
    st.markdown(f"# 📸 Interactive Conference Posts {badge_html}", unsafe_allow_html=True)
else:
    st.markdown("# 📸 Interactive Conference Posts")

st.markdown("Engage with trending conference content")

st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

# Helper functions
def load_pr_posts():
    """Load PR posts from JSON file"""
    try:
        with open("data/pr_posts.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def load_delegate_interactions():
    """Load delegate interactions from JSON file"""
    try:
        with open("data/delegate_interactions.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_delegate_interactions(interactions):
    """Save delegate interactions to JSON file"""
    with open("data/delegate_interactions.json", "w", encoding="utf-8") as f:
        json.dump(interactions, f, indent=2, ensure_ascii=False)

def load_delegates():
    """Load delegates list for mentions"""
    try:
        from staff_service import load_staff_df
        df = load_staff_df()
        return df[["Name", "Organization", "ID"]].to_dict('records')
    except Exception:
        return []

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

def get_user_interactions(post_id, user_id):
    """Get user's interactions with a specific post"""
    interactions = load_delegate_interactions()
    user_interactions = [i for i in interactions if i.get('post_id') == post_id and i.get('user_id') == user_id]
    
    result = {
        'liked': False,
        'shared': False,
        'comments': []
    }
    
    for interaction in user_interactions:
        if interaction.get('type') == 'like':
            result['liked'] = True
        elif interaction.get('type') == 'share':
            result['shared'] = True
        elif interaction.get('type') == 'comment':
            result['comments'].append(interaction)
    
    return result

def update_post_engagement(post_id, action_type, increment=True):
    """Update post engagement metrics"""
    posts = load_pr_posts()
    for post in posts:
        if post.get('id') == post_id:
            if action_type == 'like':
                current_likes = post.get('engagement', {}).get('likes', 0)
                post['engagement']['likes'] = current_likes + (1 if increment else -1)
            elif action_type == 'share':
                current_shares = post.get('engagement', {}).get('shares', 0)
                post['engagement']['shares'] = current_shares + (1 if increment else -1)
            elif action_type == 'view':
                current_views = post.get('engagement', {}).get('views', 0)
                post['engagement']['views'] = current_views + 1
            
            # Save updated posts
            with open("data/pr_posts.json", "w", encoding="utf-8") as f:
                json.dump(posts, f, indent=2, ensure_ascii=False)
            break

def add_interaction(post_id, user_id, user_name, interaction_type, content=None, mentions=None):
    """Add a new interaction"""
    interactions = load_delegate_interactions()
    
    new_interaction = {
        "id": len(interactions) + 1,
        "post_id": post_id,
        "user_id": user_id,
        "user_name": user_name,
        "type": interaction_type,
        "content": content,
        "mentions": mentions or [],
        "created_at": datetime.now().isoformat()
    }
    
    interactions.append(new_interaction)
    save_delegate_interactions(interactions)
    
    # Update post engagement
    if interaction_type in ['like', 'share']:
        update_post_engagement(post_id, interaction_type, increment=True)
    
    # Create notification for the interaction
    try:
        from lib.notifications import create_interaction_notification
        
        # Get post owner (simplified - would need to track post owners)
        # For now, create notification for all users
        post_owner_id = "all"  # This would be the actual post owner
        
        if post_owner_id != user_id:  # Don't notify self
            create_interaction_notification(
                from_user_id=user_id,
                to_user_id=post_owner_id,
                interaction_type=interaction_type,
                content=content or ""
            )
    except ImportError:
        pass  # Continue if notification system not available

def remove_interaction(post_id, user_id, interaction_type):
    """Remove an interaction"""
    interactions = load_delegate_interactions()
    interactions = [i for i in interactions if not (
        i.get('post_id') == post_id and 
        i.get('user_id') == user_id and 
        i.get('type') == interaction_type
    )]
    save_delegate_interactions(interactions)
    
    # Update post engagement
    if interaction_type in ['like', 'share']:
        update_post_engagement(post_id, interaction_type, increment=False)

def get_post_comments(post_id):
    """Get all comments for a post"""
    interactions = load_delegate_interactions()
    comments = [i for i in interactions if i.get('post_id') == post_id and i.get('type') == 'comment']
    comments.sort(key=lambda x: x.get('created_at', ''))
    return comments

# Get current user info
current_user_id = st.session_state.get('delegate_id', 'anonymous')
current_user_name = st.session_state.get('delegate_name', 'Anonymous User')

# Back to dashboard button
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("🏠 Back to Dashboard", width='stretch'):
        st.switch_page("pages/1_Delegate_Dashboard.py")

with col2:
    st.markdown("### 📸 Interactive Conference Posts")
    st.markdown("Like, share, comment, and mention fellow delegates!")

with col3:
    st.markdown(f"**👤 {current_user_name}**")

st.markdown("---")

# Load and display PR posts
pr_posts = load_pr_posts()

# Check for specific post ID in URL parameters
post_id_param = st.query_params.get("post")
if post_id_param:
    try:
        post_id_param = int(post_id_param)
        # Find the specific post and increment view count
        for post in pr_posts:
            if post.get('id') == post_id_param:
                update_post_engagement(post_id_param, 'view', increment=True)
                st.success(f"📖 Viewing post: {post['title']}")
                break
    except ValueError:
        st.warning("Invalid post ID in URL")

if not pr_posts:
    st.info("No posts available yet. Check back later for exciting conference content!")
else:
    # Sort by engagement and date (trending posts first)
    pr_posts.sort(key=lambda x: (
        x.get('engagement', {}).get('likes', 0) + 
        x.get('engagement', {}).get('shares', 0) * 2,
        x.get('created_at', "")
    ), reverse=True)
    
    for post in pr_posts:
        with st.container(border=True):
            # Track view for this post (only if not already tracked via URL parameter)
            post_id = post.get('id')
            if not post_id_param or post_id != post_id_param:
                update_post_engagement(post_id, 'view', increment=True)
            
            # Post header
            post_type = post.get("type", "General")
            priority = post.get("priority", "Medium")
            type_colors = {
                "Trending News": "🔥",
                "Event Highlights": "⭐",
                "Speaker Spotlight": "🎤",
                "Exhibitor Showcase": "🏢",
                "Behind the Scenes": "🎬",
                "Networking Moments": "🤝"
            }
            priority_colors = {
                "High": "🔴",
                "Medium": "🟡", 
                "Low": "🟢"
            }
            
            st.markdown(f"**{type_colors.get(post_type, '📸')} {post['title']}** {priority_colors.get(priority, '🟡')}")
            
            # Display image if available
            if post.get('image'):
                try:
                    st.image(post['image'], width=600)
                except:
                    st.write("📷 Image not found")
            
            # Content
            st.write(post['content'])
            
            # Hashtags
            if post.get('hashtags'):
                hashtag_text = " ".join([f"#{tag}" for tag in post['hashtags']])
                st.markdown(f"**🏷️ {hashtag_text}**")
            
            # Engagement metrics and buttons
            engagement = post.get('engagement', {})
            post_id = post.get('id')
            
            # Get user's current interactions
            user_interactions = get_user_interactions(post_id, current_user_id)
            
            # Engagement buttons row
            col_like, col_share, col_comment, col_views = st.columns([1, 1, 1, 1])
            
            with col_like:
                like_count = engagement.get('likes', 0)
                if user_interactions['liked']:
                    if st.button(f"❤️ {like_count}", key=f"unlike_{post_id}"):
                        remove_interaction(post_id, current_user_id, 'like')
                        st.rerun()
                else:
                    if st.button(f"🤍 {like_count}", key=f"like_{post_id}"):
                        add_interaction(post_id, current_user_id, current_user_name, 'like')
                        st.rerun()
            
            with col_share:
                share_count = engagement.get('shares', 0)
                if user_interactions['shared']:
                    if st.button(f"🔄 {share_count}", key=f"unshare_{post_id}"):
                        remove_interaction(post_id, current_user_id, 'share')
                        st.rerun()
                else:
                    if st.button(f"📤 {share_count}", key=f"share_{post_id}"):
                        # Show share options
                        st.session_state[f'show_share_options_{post_id}'] = True
                        st.rerun()
            
            with col_comment:
                comments = get_post_comments(post_id)
                comment_count = len(comments)
                st.button(f"💬 {comment_count}", key=f"comment_btn_{post_id}", disabled=True)
            
            with col_views:
                views_count = engagement.get('views', 0)
                st.metric("👀 Views", views_count)
            
            # Share options modal
            if st.session_state.get(f'show_share_options_{post_id}', False):
                with st.container(border=True):
                    st.markdown("#### 📤 Share Post")
                    
                    # Generate share URLs
                    post_url = f"https://insaka-conference.streamlit.app/pages/10_Interactive_PR.py?post={post_id}"
                    post_text = f"Check out this post from Insaka Conference 2025: {post['title']}"
                    
                    # Social media share buttons
                    col_whatsapp, col_twitter, col_linkedin, col_copy = st.columns(4)
                    
                    with col_whatsapp:
                        whatsapp_url = f"https://wa.me/?text={post_text}%20{post_url}"
                        if st.button("📱 WhatsApp", key=f"whatsapp_{post_id}", width='stretch'):
                            st.markdown(f'<script>window.open("{whatsapp_url}", "_blank")</script>', unsafe_allow_html=True)
                    
                    with col_twitter:
                        twitter_url = f"https://twitter.com/intent/tweet?text={post_text}&url={post_url}"
                        if st.button("🐦 Twitter", key=f"twitter_{post_id}", width='stretch'):
                            st.markdown(f'<script>window.open("{twitter_url}", "_blank")</script>', unsafe_allow_html=True)
                    
                    with col_linkedin:
                        linkedin_url = f"https://www.linkedin.com/sharing/share-offsite/?url={post_url}"
                        if st.button("💼 LinkedIn", key=f"linkedin_{post_id}", width='stretch'):
                            st.markdown(f'<script>window.open("{linkedin_url}", "_blank")</script>', unsafe_allow_html=True)
                    
                    with col_copy:
                        if st.button("📋 Copy Link", key=f"copy_{post_id}", width='stretch'):
                            # Use JavaScript to copy to clipboard
                            st.markdown(f"""
                            <script>
                            navigator.clipboard.writeText('{post_url}').then(function() {{
                                console.log('Link copied to clipboard');
                            }});
                            </script>
                            """, unsafe_allow_html=True)
                            st.session_state[f'copied_{post_id}'] = True
                    
                    # Show copied message and link
                    if st.session_state.get(f'copied_{post_id}', False):
                        st.success("✅ Link copied to clipboard!")
                        st.markdown(f"**Shareable Link:**")
                        st.code(post_url, language="text")
                        
                        # Also show as clickable link
                        st.markdown(f"🔗 [Open Post Link]({post_url})")
                        
                        st.session_state[f'copied_{post_id}'] = False
                    
                    # Action buttons
                    col_confirm, col_cancel = st.columns(2)
                    
                    with col_confirm:
                        if st.button("✅ Share & Count", key=f"confirm_share_{post_id}", width='stretch'):
                            add_interaction(post_id, current_user_id, current_user_name, 'share')
                            st.session_state[f'show_share_options_{post_id}'] = False
                            st.rerun()
                    
                    with col_cancel:
                        if st.button("❌ Cancel", key=f"cancel_share_{post_id}", width='stretch'):
                            st.session_state[f'show_share_options_{post_id}'] = False
                            st.rerun()
                    
                    st.markdown("---")
            
            # Comment section
            st.markdown("#### 💬 Comments")
            
            # Display existing comments
            comments = get_post_comments(post_id)
            if comments:
                for comment in comments:
                    with st.container(border=True):
                        col_comment_user, col_comment_time = st.columns([3, 1])
                        with col_comment_user:
                            st.markdown(f"**👤 {comment.get('user_name', 'Anonymous')}**")
                        with col_comment_time:
                            comment_time = get_relative_time(comment.get('created_at', ''))
                            st.caption(comment_time)
                        
                        st.write(comment.get('content', ''))
                        
                        # Show mentions in comment
                        if comment.get('mentions'):
                            mentions_text = " ".join([f"@{mention}" for mention in comment['mentions']])
                            st.caption(f"**Mentioned:** {mentions_text}")
            else:
                st.info("No comments yet. Be the first to comment!")
            
            # Add comment form
            with st.form(f"comment_form_{post_id}"):
                st.markdown("**Add a comment:**")
                
                # Load delegates for mentions
                delegates = load_delegates()
                delegate_names = [d['Name'] for d in delegates if d['Name'] != current_user_name]
                
                comment_text = st.text_area("Your comment:", placeholder="Comment...", height=80)
                
                # Mention people
                if delegate_names:
                    mentioned_people = st.multiselect(
                        "Mention people:", 
                        options=delegate_names,
                        placeholder="Select people to mention...",
                        key=f"mentions_{post_id}"
                    )
                else:
                    mentioned_people = []
                
                col_submit, col_cancel = st.columns([1, 1])
                
                with col_submit:
                    comment_submitted = st.form_submit_button("💬 Post Comment", width='stretch', type="primary")
                
                with col_cancel:
                    st.form_submit_button("❌ Cancel", width='stretch')
                
                if comment_submitted and comment_text.strip():
                    add_interaction(
                        post_id=post_id,
                        user_id=current_user_id,
                        user_name=current_user_name,
                        interaction_type='comment',
                        content=comment_text.strip(),
                        mentions=mentioned_people
                    )
                    st.success("💬 Comment posted!")
                    st.rerun()
                elif comment_submitted and not comment_text.strip():
                    st.error("Please enter a comment.")
            
            # Timestamp
            relative_time = get_relative_time(post['created_at'])
            st.caption(f"Posted {relative_time} • {post_type}")
            
            st.markdown("---")

# Footer with logout button
st.markdown("---")
col_footer1, col_footer2, col_footer3 = st.columns([2, 1, 2])
with col_footer1:
    st.caption("💡 Tip: Use mentions (@name) to tag fellow delegates in your comments!")
with col_footer2:
    if hasattr(st.session_state, 'delegate_authenticated') and st.session_state.delegate_authenticated:
        if st.button("🚪 Logout", width='stretch', key="interactive_pr_logout"):
            # Clear all session state
            for key in list(st.session_state.keys()):
                if key.startswith('delegate_'):
                    del st.session_state[key]
            st.success("✅ Logged out successfully!")
            st.switch_page("pages/0_Landing.py")
