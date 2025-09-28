# pages/Admin_PR.py
import streamlit as st
import json
import os
from datetime import datetime
from lib.ui import apply_brand

st.set_page_config(page_title="PR Management — Insaka Admin", page_icon="📸", layout="wide")

apply_brand()

# Zambian-themed header
st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

st.markdown("# 📸 PR & Social Media Management")
st.markdown("Post trending conference news, images, and hashtags")

st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

# Helper functions
def load_pr_posts():
    """Load PR posts from JSON file"""
    try:
        with open("data/pr_posts.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_pr_posts(posts):
    """Save PR posts to JSON file"""
    with open("data/pr_posts.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)

def display_pr_posts(posts):
    """Display existing PR posts"""
    if not posts:
        st.info("No PR posts yet. Create your first post below!")
        return
    
    st.markdown("### 📱 Current PR Posts")
    
    # Sort by date (newest first)
    posts.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    
    for i, post in enumerate(posts):
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Post content
                st.markdown(f"**📸 {post['title']}**")
                
                # Display image if available
                if post.get('image'):
                    try:
                        st.image(post['image'], width=300)
                    except:
                        st.write("📷 Image not found")
                
                # Content
                st.write(post['content'])
                
                # Hashtags
                if post.get('hashtags'):
                    hashtag_text = " ".join([f"#{tag}" for tag in post['hashtags']])
                    st.markdown(f"**Tags:** {hashtag_text}")
                
                # Engagement metrics
                engagement = post.get('engagement', {})
                if engagement:
                    col_views, col_likes, col_shares = st.columns(3)
                    with col_views:
                        st.metric("Views", engagement.get('views', 0))
                    with col_likes:
                        st.metric("Likes", engagement.get('likes', 0))
                    with col_shares:
                        st.metric("Shares", engagement.get('shares', 0))
                
                # Timestamp
                created_at = datetime.fromisoformat(post['created_at']).strftime("%Y-%m-%d %H:%M")
                st.caption(f"Posted on {created_at}")
            
            with col2:
                # Action buttons
                if st.button("🗑️ Delete", key=f"delete_{i}", type="secondary"):
                    posts.pop(i)
                    save_pr_posts(posts)
                    st.rerun()
                
                # Edit button (placeholder for future functionality)
                if st.button("✏️ Edit", key=f"edit_{i}"):
                    st.info("Edit functionality coming soon!")

# Load existing posts
pr_posts = load_pr_posts()

# Add new PR post form
st.markdown("### ✨ Create New PR Post")

with st.form("pr_post_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        post_title = st.text_input("📸 Post Title", placeholder="Title...")
        post_content = st.text_area("📝 Content", placeholder="Content...", height=100)
        
        # Hashtags
        hashtags_input = st.text_input("🏷️ Hashtags (comma-separated)", placeholder="e.g., Insaka2025, MiningZambia, Conference")
        hashtags = [tag.strip() for tag in hashtags_input.split(",") if tag.strip()] if hashtags_input else []
    
    with col2:
        # Image upload
        uploaded_image = st.file_uploader("📷 Upload Image", type=["jpg", "jpeg", "png", "webp"], help="Upload a trending conference image")
        
        # Post type
        post_type = st.selectbox("📋 Post Type", ["Trending News", "Event Highlights", "Speaker Spotlight", "Exhibitor Showcase", "Behind the Scenes", "Networking Moments"])
        
        # Priority level
        priority = st.selectbox("⭐ Priority", ["High", "Medium", "Low"])
    
    # Engagement metrics (can be set manually for testing)
    st.markdown("#### 📊 Engagement Metrics (Optional)")
    col_views, col_likes, col_shares = st.columns(3)
    
    with col_views:
        views = st.number_input("👀 Views", min_value=0, value=0)
    with col_likes:
        likes = st.number_input("❤️ Likes", min_value=0, value=0)
    with col_shares:
        shares = st.number_input("🔄 Shares", min_value=0, value=0)
    
    submitted = st.form_submit_button("🚀 Publish PR Post", width='stretch', type="primary")
    
    if submitted:
        if not post_title.strip():
            st.error("Please enter a post title.")
        elif not post_content.strip():
            st.error("Please enter post content.")
        else:
            # Handle image upload
            image_path = None
            if uploaded_image:
                try:
                    from utils_assets import save_upload
                    image_path = save_upload(uploaded_image, kind="pr_posts", name_hint=post_title)
                    st.success(f"Image uploaded: {image_path}")
                except Exception as e:
                    st.error(f"Error uploading image: {e}")
                    image_path = None
            
            # Create new post
            new_post = {
                "id": len(pr_posts) + 1,
                "title": post_title.strip(),
                "content": post_content.strip(),
                "hashtags": hashtags,
                "type": post_type,
                "priority": priority,
                "image": image_path,
                "engagement": {
                    "views": views,
                    "likes": likes,
                    "shares": shares
                },
                "created_at": datetime.now().isoformat(),
                "created_by": "PR Team"
            }
            
            # Add to posts
            pr_posts.append(new_post)
            save_pr_posts(pr_posts)
            
            st.success("🎉 PR post published successfully!")
            st.balloons()
            st.rerun()

# Display existing posts
st.markdown("---")
display_pr_posts(pr_posts)

# Navigation
st.markdown("---")
st.markdown("### 🔗 Navigation")
nav_col1, nav_col2, nav_col3 = st.columns(3)

with nav_col1:
    if st.button("🏠 Back to Admin Panel", width='stretch'):
        st.switch_page("pages/0_Admin.py")

with nav_col2:
    if st.button("📢 Manage Announcements", width='stretch'):
        st.switch_page("pages/Admin_Announcements.py")

with nav_col3:
    if st.button("🌐 View Public Page", width='stretch'):
        st.switch_page("pages/9_External_Content.py")

# Footer
st.markdown("---")
st.caption("💡 Tip: Use trending hashtags and engaging images to maximize conference visibility!")
