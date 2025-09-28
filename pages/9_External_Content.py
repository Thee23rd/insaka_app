# pages/9_External_Content.py
import streamlit as st
import json
from datetime import datetime
from lib.ui import apply_brand

# # Try to import the advanced web scraper, fallback to simple version
# try:
#     from lib.web_scraper import fetch_web_content, fetch_specific_content, display_web_content, fetch_exhibitor_logos
#     ADVANCED_SCRAPING = True
# except ImportError:
#     from lib.simple_web_fetcher import fetch_web_text as fetch_web_content, display_simple_content as display_web_content
#     ADVANCED_SCRAPING = False
#     st.warning("⚠️ Advanced web scraping features are not available. Using basic text extraction.")

st.set_page_config(page_title="External Content — Insaka", page_icon="🌐", layout="wide")

# Hide sidebar and navigation
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

# Functions to load local content
def load_local_speakers():
    """Load speakers from local JSON file"""
    try:
        with open("data/speakers.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def load_local_exhibitors():
    """Load exhibitors from local JSON file"""
    try:
        with open("data/exhibitors.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def display_local_speakers(speakers):
    """Display local speakers in a grid"""
    if not speakers:
        st.info("No speakers data available.")
        return
    
    st.markdown("### 🎤 Conference Speakers")
    
    # Create columns for speakers
    cols = st.columns(min(len(speakers), 3))
    
    for i, speaker in enumerate(speakers):
        with cols[i % 3]:
            with st.container(border=True):
                # Speaker photo
                if speaker.get('photo'):
                    try:
                        st.image(speaker['photo'], width=150)
                    except:
                        st.write("📷 Photo unavailable")
                
                # Speaker info
                st.markdown(f"**{speaker.get('name', 'Unknown')}**")
                if speaker.get('talk'):
                    st.markdown(f"*{speaker['talk']}*")
                if speaker.get('bio'):
                    st.markdown(speaker['bio'])

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

def display_announcements(announcements):
    """Display announcements"""
    if not announcements:
        st.info("No announcements available.")
        return
    
    st.markdown("### 📢 Conference Announcements")
    
    # Sort by priority and date
    priority_order = {"Urgent": 4, "High": 3, "Normal": 2, "Low": 1}
    announcements.sort(key=lambda x: (priority_order.get(x.get("priority", "Normal"), 2), x.get("created_at", "")), reverse=True)
    
    for announcement in announcements:
        with st.container(border=True):
            priority = announcement.get("priority", "Normal")
            priority_colors = {
                "Urgent": "🔴",
                "High": "🟠", 
                "Normal": "🟡",
                "Low": "🟢"
            }
            st.markdown(f"**{priority_colors.get(priority, '🟡')} {announcement['title']}**")
            st.markdown(announcement['content'])
            
            # Show relative time
            relative_time = get_relative_time(announcement['created_at'])
            st.caption(f"Posted {relative_time}")

def display_news(news_list):
    """Display news items"""
    if not news_list:
        st.info("No news available.")
        return
    
    st.markdown("### 📰 Latest News & Updates")
    
    # Sort by date (newest first)
    news_list.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    
    for news_item in news_list[:5]:  # Show only latest 5
        with st.container(border=True):
            category = news_item.get("category", "General")
            category_colors = {
                "General": "🔵",
                "Conference Updates": "🟢",
                "Industry News": "🟡",
                "Speaker Updates": "🟣",
                "Exhibitor News": "🟠",
                "Schedule Changes": "🔴"
            }
            st.markdown(f"**{category_colors.get(category, '🔵')} {news_item['title']}**")
            
            # Display image if available
            if news_item.get('image'):
                try:
                    st.image(news_item['image'], width=300)
                except:
                    st.write("📷 Image not found")
            
            st.markdown(news_item['content'])
            
            # Show relative time
            relative_time = get_relative_time(news_item['created_at'])
            st.caption(f"Posted {relative_time} | Category: {category}")

def display_pr_posts(pr_posts):
    """Display PR posts"""
    if not pr_posts:
        st.info("No PR posts available.")
        return
    
    st.markdown("### 📸 Trending Conference Posts")
    
    # Sort by engagement and date (trending posts first)
    pr_posts.sort(key=lambda x: (
        x.get('engagement', {}).get('likes', 0) + 
        x.get('engagement', {}).get('shares', 0) * 2,  # Shares weighted more
        x.get('created_at', "")
    ), reverse=True)
    
    for post in pr_posts:
        with st.container(border=True):
            # Post header with type and priority
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
                    st.image(post['image'], width=400)
                except:
                    st.write("📷 Image not found")
            
            # Content
            st.write(post['content'])
            
            # Hashtags
            if post.get('hashtags'):
                hashtag_text = " ".join([f"#{tag}" for tag in post['hashtags']])
                st.markdown(f"**🏷️ {hashtag_text}**")
            
            # Engagement metrics
            engagement = post.get('engagement', {})
            if engagement:
                col_views, col_likes, col_shares = st.columns(3)
                with col_views:
                    st.metric("👀 Views", engagement.get('views', 0))
                with col_likes:
                    st.metric("❤️ Likes", engagement.get('likes', 0))
                with col_shares:
                    st.metric("🔄 Shares", engagement.get('shares', 0))
            
            # Timestamp
            relative_time = get_relative_time(post['created_at'])
            st.caption(f"Posted {relative_time} • {post_type}")

def display_local_exhibitors(exhibitors):
    """Display local exhibitors in a grid"""
    if not exhibitors:
        st.info("No exhibitors data available.")
        return
    
    st.markdown("### 🏢 Conference Exhibitors")
    
    # Create columns for exhibitors
    cols = st.columns(min(len(exhibitors), 3))
    
    for i, exhibitor in enumerate(exhibitors):
        with cols[i % 3]:
            with st.container(border=True):
                # Exhibitor logo
                if exhibitor.get('logo'):
                    try:
                        st.image(exhibitor['logo'], width=150)
                    except:
                        st.write("🏢 Logo unavailable")
                
                # Exhibitor info
                st.markdown(f"**{exhibitor.get('name', 'Unknown')}**")
                if exhibitor.get('stand'):
                    st.markdown(f"📍 Stand: {exhibitor['stand']}")
                if exhibitor.get('url'):
                    st.markdown(f"🌐 {exhibitor['url']}")

# Zambian-themed header
st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

st.markdown("# 🏢 Conference Showcase & News")
st.markdown("View  speakers, exhibitors, and external conference content")

# # SSL Certificate Information
# st.info("🔒 **SSL Certificate Note**: Some government and organizational websites may have SSL certificate issues. The system automatically handles this by falling back to unverified SSL connections when needed.")

# # Image Display Information
# st.info("📸 **Image Display**: The system will automatically extract and display images from the website along with the text content.")

# Quick Access Section
st.markdown("### 🚀 Quick Access")
quick_col1, quick_col2, quick_col3, quick_col4, quick_col5 = st.columns(5)

with quick_col1:
    if st.button("🏢 Exhibitors", key="quick_local_exhibitors", width='stretch', type="primary"):
        st.session_state.quick_load_local_exhibitors = True
        st.rerun()

with quick_col2:
    if st.button("🎤 Speakers", key="quick_local_speakers", width='stretch'):
        st.session_state.quick_load_local_speakers = True
        st.rerun()

with quick_col3:
    if st.button("📢 Announcements", key="quick_announcements", width='stretch'):
        st.session_state.quick_load_announcements = True
        st.rerun()

with quick_col4:
    if st.button("📰 Updates & News", key="quick_updates_news", width='stretch'):
        st.session_state.quick_load_updates_news = True
        st.rerun()

with quick_col5:
    if st.button("📸 Interactive Posts", key="quick_pr_posts", width='stretch'):
        # Track view for all posts when accessing interactive page
        try:
            with open("data/pr_posts.json", "r", encoding="utf-8") as f:
                posts = json.load(f)
            
            # Increment view count for all posts when accessing the interactive page
            for post in posts:
                current_views = post.get('engagement', {}).get('views', 0)
                post['engagement']['views'] = current_views + 1
            
            with open("data/pr_posts.json", "w", encoding="utf-8") as f:
                json.dump(posts, f, indent=2, ensure_ascii=False)
        except Exception:
            pass  # Continue even if view tracking fails
        
        st.switch_page("pages/10_Interactive_PR.py")

# Handle quick access buttons
if hasattr(st.session_state, 'quick_load_local_exhibitors') and st.session_state.quick_load_local_exhibitors:
    st.session_state.quick_load_local_exhibitors = False
    exhibitors = load_local_exhibitors()
    display_local_exhibitors(exhibitors)

if hasattr(st.session_state, 'quick_load_local_speakers') and st.session_state.quick_load_local_speakers:
    st.session_state.quick_load_local_speakers = False
    speakers = load_local_speakers()
    display_local_speakers(speakers)

if hasattr(st.session_state, 'quick_load_announcements') and st.session_state.quick_load_announcements:
    st.session_state.quick_load_announcements = False
    # Load admin-posted announcements
    announcements = load_announcements()
    display_announcements(announcements)

if hasattr(st.session_state, 'quick_load_updates_news') and st.session_state.quick_load_updates_news:
    st.session_state.quick_load_updates_news = False
    # Load admin-posted news and updates
    news_list = load_news()
    display_news(news_list)

if hasattr(st.session_state, 'quick_load_pr_posts') and st.session_state.quick_load_pr_posts:
    st.session_state.quick_load_pr_posts = False
    # Load PR posts
    pr_posts = load_pr_posts()
    display_pr_posts(pr_posts)

# Handle navigation from dashboard
if hasattr(st.session_state, 'show_announcements') and st.session_state.show_announcements:
    st.session_state.show_announcements = False
    # Load admin-posted announcements
    announcements = load_announcements()
    display_announcements(announcements)

if hasattr(st.session_state, 'show_news') and st.session_state.show_news:
    st.session_state.show_news = False
    # Load admin-posted news and updates
    news_list = load_news()
    display_news(news_list)

if hasattr(st.session_state, 'show_pr_posts') and st.session_state.show_pr_posts:
    st.session_state.show_pr_posts = False
    # Load PR posts
    pr_posts = load_pr_posts()
    display_pr_posts(pr_posts)

st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

# Auto-load local content section
st.markdown("### 📋 Current Conference Information")
auto_col1, auto_col2 = st.columns(2)

with auto_col1:
    st.markdown("#### 🎤 Speakers")
    speakers = load_local_speakers()
    if speakers:
        for speaker in speakers[:2]:  # Show first 2 speakers
            with st.container(border=True):
                cols = st.columns([1, 2])
                with cols[0]:
                    if speaker.get('photo'):
                        try:
                            st.image(speaker['photo'], width=80)
                        except:
                            st.write("📷")
                with cols[1]:
                    st.markdown(f"**{speaker.get('name', 'Unknown')}**")
                    if speaker.get('talk'):
                        st.markdown(f"*{speaker['talk']}*")
    else:
        st.info("No speakers data available")

with auto_col2:
    st.markdown("#### 🏢 Exhibitors")
    exhibitors = load_local_exhibitors()
    if exhibitors:
        for exhibitor in exhibitors[:2]:  # Show first 2 exhibitors
            with st.container(border=True):
                cols = st.columns([1, 2])
                with cols[0]:
                    if exhibitor.get('logo'):
                        try:
                            st.image(exhibitor['logo'], width=80)
                        except:
                            st.write("🏢")
                with cols[1]:
                    st.markdown(f"**{exhibitor.get('name', 'Unknown')}**")
                    if exhibitor.get('stand'):
                        st.markdown(f"📍 Stand: {exhibitor['stand']}")
    else:
        st.info("No exhibitors data available")

st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

# Back button
if st.button("← Back to Dashboard", type="secondary"):
    st.switch_page("pages/1_Delegate_Dashboard.py")

st.markdown("---")

# # Configuration section
# st.subheader("⚙️ Content Configuration")

# # Example URLs for demonstration
# example_urls = {
#     "Exhibitors & Sponsors": "https://www.mmmd.gov.zm/insakasummit/?page_id=5228",
#     "Conference Updates": "https://www.mmmd.gov.zm/insakasummit/?page_id=5228",
#     "Industry News": "https://www.mmmd.gov.zm/insakasummit/?page_id=5228",
#     "Custom URL": "https://www.mmmd.gov.zm/insakasummit/?page_id=5228"
# }

# # URL input
# url_option = st.selectbox(
#     "Select a pre-configured URL or enter custom:",
#     options=list(example_urls.keys())
# )

# if url_option == "Custom URL":
#     website_url = st.text_input(
#         "Enter website URL:",
#         placeholder="https://www.mmmd.gov.zm/insakasummit/?page_id=5228",
#         help="Enter the full URL of the website you want to pull content from"
#     )
# else:
#     website_url = example_urls[url_option]
#     st.info(f"Selected URL: {website_url}")

# # Content selector (optional) - only show if advanced scraping is available
# if ADVANCED_SCRAPING:
#     st.subheader("🎯 Content Targeting")
#     use_selector = st.checkbox("Use specific content selector", help="Target specific parts of the page using CSS selectors")

#     content_selector = None
#     if use_selector:
#         # Quick selector options for common content types
#         quick_selectors = {
#             "Exhibitor Logos": ".exhibitor-logo, .sponsor-logo, .company-logo, .logo",
#             "All Images": "img",
#             "Main Content": ".main-content, .content, .post-content",
#             "Article Body": ".article-body, .entry-content",
#             "Custom Selector": ""
#         }
        
#         selector_choice = st.selectbox(
#             "Quick Selector Options:",
#             options=list(quick_selectors.keys()),
#             help="Choose a common selector or enter custom"
#         )
        
#         if selector_choice == "Custom Selector":
#             content_selector = st.text_input(
#                 "Custom CSS Selector:",
#                 placeholder=".exhibitor-logo, .sponsor-logo, .company-logo",
#                 help="Examples: .exhibitor-logo, .sponsor-logo, .company-logo, .logo, img"
#             )
#         else:
#             content_selector = quick_selectors[selector_choice]
#             st.info(f"Selected: `{content_selector}`")
# else:
#     use_selector = False
#     content_selector = None

# # Cache duration
# cache_duration = st.slider(
#     "Cache Duration (minutes):",
#     min_value=5,
#     max_value=120,
#     value=30,
#     help="How long to cache the content before fetching again"
# )

# # Fetch button
# if st.button("🔍 Fetch Content", type="primary", width='stretch'):
#     if website_url:
#         with st.spinner("Fetching content from website..."):
#             if ADVANCED_SCRAPING and use_selector and content_selector:
#                 # Fetch specific content using selector (advanced mode)
#                 result = fetch_specific_content(website_url, content_selector)
                
#                 if result['success']:
#                     st.success("✅ Content fetched successfully!")
                    
#                     # Display SSL fallback warning if applicable
#                     if result.get('ssl_fallback_used', False):
#                         st.warning("⚠️ SSL certificate verification was bypassed for this website. Content was fetched successfully but with reduced security.")
                    
#                     # Display images first
#                     if result.get('images_html'):
#                         st.markdown("### 📸 Images")
#                         st.markdown(result['images_html'], unsafe_allow_html=True)
#                         st.markdown("---")
                    
#                     # Display content
#                     st.markdown("### 📄 Fetched Content")
#                     st.markdown(result['content'])
#                 else:
#                     st.error(f"❌ Error: {result['error']}")
#             else:
#                 # Fetch general content (works in both modes)
#                 result = fetch_web_content(website_url, cache_duration)
#                 display_web_content(result, show_timestamp=True)
#     else:
#         st.warning("Please enter a valid URL")

# st.markdown("---")

# # Pre-configured content sections
# st.subheader("🏢 Conference Content")

# # Local and external content
# col1, col2 = st.columns(2)

# with col1:
#     st.markdown("#### 🏢 Conference Data")
    
#     # Local exhibitors
#     if st.button("🏢 Load Exhibitors", key="local_exhibitor_btn"):
#         exhibitors = load_local_exhibitors()
#         display_local_exhibitors(exhibitors)
    
#     # Local speakers
#     if st.button("🎤 Load Speakers", key="local_speaker_btn"):
#         speakers = load_local_speakers()
#         display_local_speakers(speakers)

# with col2:
#     st.markdown("#### 🌐 External Website Content")
    
#     # External exhibitor logos
#     if st.button("🌐 Load External Logos", key="external_exhibitor_btn"):
#         exhibitor_url = "https://www.mmmd.gov.zm/insakasummit/?page_id=5228"
#         if ADVANCED_SCRAPING:
#             result = fetch_exhibitor_logos(exhibitor_url)
#             if result['success']:
#                 st.success("✅ External logos loaded!")
#                 if result.get('logos_grid_html'):
#                     st.markdown("### 🌐 External Exhibitor Logos & Photos")
#                     st.markdown(result['logos_grid_html'], unsafe_allow_html=True)
#                 elif result.get('images_html'):
#                     st.markdown("### 🌐 External Exhibitor Logos & Photos")
#                     st.markdown(result['images_html'], unsafe_allow_html=True)
#                 else:
#                     st.info("No external logos found.")
#             else:
#                 st.error(f"❌ Error: {result['error']}")
#         else:
#             result = fetch_web_content(exhibitor_url, 30)
#             display_web_content(result, show_timestamp=True)
    
#     # External updates
#     if st.button("📰 Load External Updates", key="external_updates_btn"):
#         updates_url = "https://www.mmmd.gov.zm/insakasummit/?page_id=5228"
#         result = fetch_web_content(updates_url, 15)
#         display_web_content(result, show_timestamp=True)

# # All images from the site
# st.markdown("#### 📸 All Images from Site")
# if st.button("Load All Images", key="all_images_btn"):
#     all_images_url = "https://www.mmmd.gov.zm/insakasummit/?page_id=5228"
#     if ADVANCED_SCRAPING:
#         # Get all images
#         result = fetch_specific_content(all_images_url, "img", text_only=False)
        
#         if result['success']:
#             st.success("✅ All images loaded!")
            
#             # Display SSL warning if applicable
#             if result.get('ssl_fallback_used', False):
#                 st.warning("⚠️ SSL certificate verification was bypassed.")
            
#             # Display all images
#             if result.get('images_html'):
#                 st.markdown("### 📸 All Images from Website")
#                 st.markdown(result['images_html'], unsafe_allow_html=True)
#             else:
#                 st.info("No images found on the website.")
#         else:
#             st.error(f"❌ Error: {result['error']}")
#     else:
#         # Fallback to general content
#         result = fetch_web_content(all_images_url, 30)
#         display_web_content(result, show_timestamp=True)

# # Example: Schedule updates
# st.markdown("#### 📅 Schedule Updates")
# if st.button("Load Schedule Updates", key="schedule_btn"):
#     # Example schedule URL
#     schedule_url = "https://www.mmmd.gov.zm/insakasummit/?page_id=5228"  # Demo URL
#     result = fetch_web_content(schedule_url, 60)  # 1 hour cache
    
#     if result['success']:
#         st.markdown("**Latest Schedule Information:**")
#         display_web_content(result)
#     else:
#         st.error("Could not fetch schedule updates")

# st.markdown("---")

# # Instructions
# st.subheader("📖 Instructions")

# st.markdown("""
# ### How to Use External Content:

# 1. **Configure URL**: Enter the website URL you want to pull content from
# 2. **Target Content** (Optional): Use CSS selectors to target specific content areas
# 3. **Set Cache Duration**: Choose how long to cache content before refreshing
# 4. **Fetch Content**: Click the fetch button to load content

# ### CSS Selector Examples:
# - `.news-content` - Target elements with class "news-content"
# - `#article-body` - Target element with ID "article-body"
# - `.main-content` - Target elements with class "main-content"
# - `.post-content` - Target elements with class "post-content"

# ### Benefits:
# - ✅ **Real-time updates** from external websites
# - ✅ **Caching** to avoid excessive requests
# - ✅ **Content targeting** for specific sections
# - ✅ **Error handling** for failed requests
# - ✅ **Zambian branding** integrated seamlessly

# ### Use Cases:
# - 📰 Pull latest news from industry websites
# - 📢 Display conference announcements
# - 📅 Show schedule updates
# - 🏢 Display sponsor/exhibitor information
# - 📄 Show speaker updates
# """)

# Footer with logout button
st.markdown("---")
col_footer1, col_footer2, col_footer3 = st.columns([2, 1, 2])
with col_footer1:
    st.caption("Need help? Contact the conference organizers or visit the registration desks.")
with col_footer2:
    if hasattr(st.session_state, 'delegate_authenticated') and st.session_state.delegate_authenticated:
        if st.button("🚪 Logout", width='stretch', key="external_content_logout"):
            # Clear all session state
            for key in list(st.session_state.keys()):
                if key.startswith('delegate_'):
                    del st.session_state[key]
            st.success("✅ Logged out successfully!")
            st.switch_page("pages/0_Landing.py")
