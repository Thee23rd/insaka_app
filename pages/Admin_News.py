# pages/Admin_News.py
import streamlit as st
import json
from datetime import datetime
from lib.ui import apply_brand
from utils_assets import save_upload

st.set_page_config(page_title="Admin - News & Updates — Insaka", page_icon="📰", layout="wide")

apply_brand()

# Zambian-themed header
st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

st.markdown("# 📰 Admin - News & Updates")
st.markdown("Post and manage conference news and updates with images")

st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

# Functions to manage news
def load_news():
    """Load news from JSON file"""
    try:
        with open("data/news.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_news(news_list):
    """Save news to JSON file"""
    try:
        with open("data/news.json", "w", encoding="utf-8") as f:
            json.dump(news_list, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"Error saving news: {e}")
        return False

def add_news(title, content, image_path=None, category="General"):
    """Add a new news item"""
    news_list = load_news()
    
    new_news = {
        "id": len(news_list) + 1,
        "title": title,
        "content": content,
        "image": image_path,
        "category": category,
        "created_at": datetime.now().isoformat(),
        "created_by": "Admin"
    }
    
    news_list.append(new_news)
    return save_news(news_list)

def delete_news(news_id):
    """Delete a news item by ID"""
    news_list = load_news()
    news_list = [n for n in news_list if n["id"] != news_id]
    return save_news(news_list)

# Navigation
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("← Back to Admin", type="secondary"):
        st.switch_page("pages/0_Admin.py")

with col2:
    if st.button("📢 Announcements", type="secondary"):
        st.switch_page("pages/Admin_Announcements.py")

with col3:
    if st.button("🌐 View Public Page", type="secondary"):
        st.switch_page("pages/9_External_Content.py")

st.markdown("---")

# Add new news form
st.subheader("📝 Add New News/Update")

with st.form("add_news", clear_on_submit=True):
    col1, col2 = st.columns([3, 1])
    
    with col1:
        title = st.text_input("News Title", placeholder="Title...")
    
    with col2:
        category = st.selectbox("Category", ["General", "Conference Updates", "Industry News", "Speaker Updates", "Exhibitor News", "Schedule Changes"])
    
    content = st.text_area(
        "News Content", 
        placeholder="Content...",
        height=150
    )
    
    # Image upload
    st.write("**📸 Add Image (Optional)**")
    uploaded_image = st.file_uploader(
        "Upload an image for this news item", 
        type=["jpg", "jpeg", "png", "webp", "gif"],
        help="Upload an image to make your news more engaging"
    )
    
    submitted = st.form_submit_button("📰 Post News", type="primary", width='stretch')
    
    if submitted:
        if title.strip() and content.strip():
            image_path = None
            
            # Handle image upload
            if uploaded_image:
                try:
                    image_path = save_upload(uploaded_image, kind="news", name_hint=title)
                    st.success(f"✅ Image uploaded: {image_path}")
                except Exception as e:
                    st.error(f"❌ Image upload failed: {e}")
                    image_path = None
            
            if add_news(title.strip(), content.strip(), image_path, category):
                st.success("✅ News posted successfully!")
                st.rerun()
            else:
                st.error("❌ Failed to save news")
        else:
            st.error("❌ Please fill in both title and content")

st.markdown("---")

# Display existing news
st.subheader("📋 Current News & Updates")

news_list = load_news()

if news_list:
    # Sort by date (newest first)
    news_list.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    
    for news_item in news_list:
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])
            
            with col1:
                # Category badge
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
                        st.image(news_item['image'], width=400, caption=f"Image for: {news_item['title']}")
                    except:
                        st.write("📷 Image not found")
                
                # Content
                st.markdown(news_item['content'])
                
                # Metadata
                created_at = datetime.fromisoformat(news_item['created_at']).strftime("%Y-%m-%d %H:%M")
                st.caption(f"Posted by {news_item.get('created_by', 'Admin')} on {created_at} | Category: {category}")
            
            with col2:
                if st.button("🗑️ Delete", key=f"delete_{news_item['id']}", type="secondary"):
                    if delete_news(news_item['id']):
                        st.success("✅ News item deleted!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to delete news item")

else:
    st.info("No news posted yet. Add your first news item above!")

st.markdown("---")

# Statistics
st.subheader("📊 News Statistics")
news_list = load_news()
if news_list:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total News Items", len(news_list))
    
    with col2:
        with_images = len([n for n in news_list if n.get("image")])
        st.metric("With Images", with_images)
    
    with col3:
        recent_count = len([n for n in news_list 
                          if (datetime.now() - datetime.fromisoformat(n.get("created_at", "1970-01-01"))).days <= 7])
        st.metric("This Week", recent_count)
    
    with col4:
        categories = {}
        for news in news_list:
            cat = news.get("category", "General")
            categories[cat] = categories.get(cat, 0) + 1
        most_common = max(categories.items(), key=lambda x: x[1])[0] if categories else "None"
        st.metric("Top Category", most_common)

# Category breakdown
if news_list:
    st.subheader("📈 Category Breakdown")
    categories = {}
    for news in news_list:
        cat = news.get("category", "General")
        categories[cat] = categories.get(cat, 0) + 1
    
    for category, count in categories.items():
        col1, col2 = st.columns([1, 3])
        with col1:
            st.write(f"**{category}:**")
        with col2:
            st.progress(count / len(news_list))
            st.caption(f"{count} items")

# Footer
st.markdown("---")
st.caption("News and updates will appear on the public Conference Showcase & News page for delegates to view.")
