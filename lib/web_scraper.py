# lib/web_scraper.py
import requests
from bs4 import BeautifulSoup
import streamlit as st
from datetime import datetime, timedelta
import json

def fetch_web_content(url, cache_duration_minutes=30):
    """
    Fetch content from a website with caching to avoid repeated requests
    
    Args:
        url: The website URL to fetch content from
        cache_duration_minutes: How long to cache the content (default: 30 minutes)
    
    Returns:
        dict: Contains 'success', 'title', 'content', 'timestamp', 'error'
    """
    
    # Check cache first
    cache_key = f"web_content_{hash(url)}"
    if cache_key in st.session_state:
        cached_data = st.session_state[cache_key]
        cache_time = datetime.fromisoformat(cached_data['timestamp'])
        
        # Check if cache is still valid
        if datetime.now() - cache_time < timedelta(minutes=cache_duration_minutes):
            return cached_data
    
    try:
        # Make request with proper headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Try with SSL verification first, then without if it fails
        ssl_fallback_used = False
        try:
            response = requests.get(url, headers=headers, timeout=10, verify=True)
        except requests.exceptions.SSLError:
            # Fallback to unverified SSL for problematic certificates
            ssl_fallback_used = True
            response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()
        
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "No Title Found"
        
        # Extract main content (you can customize this based on the website structure)
        content_selectors = [
            'main', 'article', '.content', '.post-content', 
            '.entry-content', '.main-content', '#content'
        ]
        
        main_content = None
        for selector in content_selectors:
            main_content = soup.select_one(selector)
            if main_content:
                break
        
        if not main_content:
            main_content = soup.find('body')
        
        # Extract images and content
        images_html = ""
        content_text = ""
        
        if main_content:
            # Extract images first
            images = main_content.find_all('img')
            for img in images:
                src = img.get('src')
                if src:
                    # Handle relative URLs
                    if src.startswith('//'):
                        src = 'https:' + src
                    elif src.startswith('/'):
                        from urllib.parse import urljoin
                        src = urljoin(url, src)
                    elif not src.startswith('http'):
                        from urllib.parse import urljoin
                        src = urljoin(url, src)
                    
                    # Add image to HTML
                    alt_text = img.get('alt', 'Image')
                    images_html += f'<img src="{src}" alt="{alt_text}" style="max-width: 100%; height: auto; margin: 10px 0; border-radius: 8px;" /><br/>'
            
            # Remove scripts and styles but keep images
            for script in main_content(["script", "style", "nav", "header", "footer"]):
                script.decompose()
            
            # Get text content
            content_text = main_content.get_text()
            # Clean up whitespace
            content_text = ' '.join(content_text.split())
            
            # Limit content length
            if len(content_text) > 5000:
                content_text = content_text[:5000] + "..."
        else:
            content_text = "No main content found"
        
        # Prepare result
        result = {
            'success': True,
            'title': title_text,
            'content': content_text,
            'images_html': images_html,
            'timestamp': datetime.now().isoformat(),
            'error': None,
            'ssl_fallback_used': ssl_fallback_used
        }
        
        # Cache the result
        st.session_state[cache_key] = result
        
        return result
        
    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        # Provide more user-friendly error messages for SSL issues
        if "SSL" in error_msg or "certificate" in error_msg:
            error_msg = "SSL certificate verification failed. The website may have certificate issues."
        return {
            'success': False,
            'title': None,
            'content': None,
            'timestamp': datetime.now().isoformat(),
            'error': f"Network error: {error_msg}"
        }
    except Exception as e:
        return {
            'success': False,
            'title': None,
            'content': None,
            'timestamp': datetime.now().isoformat(),
            'error': f"Parsing error: {str(e)}"
        }

def fetch_specific_content(url, selector=None, text_only=True):
    """
    Fetch specific content from a website using CSS selectors
    
    Args:
        url: The website URL
        selector: CSS selector to target specific content (e.g., '.news-item', '#article-content')
        text_only: Whether to return only text or include HTML
    
    Returns:
        dict: Contains 'success', 'content', 'images_html', 'error'
    """
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Try with SSL verification first, then without if it fails
        ssl_fallback_used = False
        try:
            response = requests.get(url, headers=headers, timeout=10, verify=True)
        except requests.exceptions.SSLError:
            # Fallback to unverified SSL for problematic certificates
            ssl_fallback_used = True
            response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if selector:
            elements = soup.select(selector)
            if not elements:
                return {
                    'success': False,
                    'content': None,
                    'images_html': None,
                    'error': f"No content found for selector: {selector}"
                }
            
            # Extract images from selected elements
            images_html = ""
            for element in elements:
                images = element.find_all('img')
                for img in images:
                    src = img.get('src')
                    if src:
                        # Handle relative URLs
                        if src.startswith('//'):
                            src = 'https:' + src
                        elif src.startswith('/'):
                            from urllib.parse import urljoin
                            src = urljoin(url, src)
                        elif not src.startswith('http'):
                            from urllib.parse import urljoin
                            src = urljoin(url, src)
                        
                        # Add image to HTML
                        alt_text = img.get('alt', 'Image')
                        images_html += f'<img src="{src}" alt="{alt_text}" style="max-width: 100%; height: auto; margin: 10px 0; border-radius: 8px;" /><br/>'
            
            if text_only:
                content = ' '.join([elem.get_text().strip() for elem in elements])
            else:
                content = str(elements[0]) if elements else None
        else:
            # Get all content including images
            images = soup.find_all('img')
            images_html = ""
            for img in images:
                src = img.get('src')
                if src:
                    # Handle relative URLs
                    if src.startswith('//'):
                        src = 'https:' + src
                    elif src.startswith('/'):
                        from urllib.parse import urljoin
                        src = urljoin(url, src)
                    elif not src.startswith('http'):
                        from urllib.parse import urljoin
                        src = urljoin(url, src)
                    
                    # Add image to HTML
                    alt_text = img.get('alt', 'Image')
                    images_html += f'<img src="{src}" alt="{alt_text}" style="max-width: 100%; height: auto; margin: 10px 0; border-radius: 8px;" /><br/>'
            
            content = soup.get_text()
            content = ' '.join(content.split())  # Clean whitespace
        
        return {
            'success': True,
            'content': content,
            'images_html': images_html,
            'ssl_fallback_used': ssl_fallback_used,
            'error': None
        }
        
    except Exception as e:
        return {
            'success': False,
            'content': None,
            'images_html': None,
            'error': f"Error fetching content: {str(e)}"
        }

def fetch_json_api(url):
    """
    Fetch JSON data from an API endpoint
    
    Args:
        url: The API URL
    
    Returns:
        dict: Contains 'success', 'data', 'error'
    """
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        
        # Try with SSL verification first, then without if it fails
        try:
            response = requests.get(url, headers=headers, timeout=10, verify=True)
        except requests.exceptions.SSLError:
            # Fallback to unverified SSL for problematic certificates
            response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()
        
        data = response.json()
        
        return {
            'success': True,
            'data': data,
            'error': None
        }
        
    except Exception as e:
        return {
            'success': False,
            'data': None,
            'error': f"API error: {str(e)}"
        }

def display_web_content(content_data, show_timestamp=True):
    """
    Display web content in Streamlit with proper formatting
    
    Args:
        content_data: The result from fetch_web_content()
        show_timestamp: Whether to show when content was fetched
    """
    
    if not content_data['success']:
        st.error(f"❌ Error fetching content: {content_data['error']}")
        return
    
    # Display SSL fallback warning if applicable
    if content_data.get('ssl_fallback_used', False):
        st.warning("⚠️ SSL certificate verification was bypassed for this website. Content was fetched successfully but with reduced security.")
    
    # Display title
    if content_data['title']:
        st.markdown(f"### {content_data['title']}")
    
    # Display images first
    if content_data.get('images_html'):
        st.markdown("### 📸 Images")
        st.markdown(content_data['images_html'], unsafe_allow_html=True)
        st.markdown("---")
    
    # Display content
    if content_data['content']:
        st.markdown(content_data['content'])
    
    # Display timestamp
    if show_timestamp and content_data['timestamp']:
        timestamp = datetime.fromisoformat(content_data['timestamp'])
        st.caption(f"📅 Content fetched on {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Add refresh button
    if st.button("🔄 Refresh Content", key=f"refresh_{hash(content_data['timestamp'])}"):
        st.rerun()

# Example usage functions for different types of content
def fetch_news_content(news_url):
    """Example: Fetch news content from a news website"""
    return fetch_specific_content(news_url, '.news-content, .article-body, .post-content')

def fetch_announcements(announcement_url):
    """Example: Fetch announcements from a conference website"""
    return fetch_specific_content(announcement_url, '.announcement, .notice, .alert')

def fetch_schedule_data(schedule_url):
    """Example: Fetch schedule/agenda data"""
    return fetch_specific_content(schedule_url, '.schedule, .agenda, .timetable')

def fetch_exhibitor_logos(url):
    """
    Fetch exhibitor logos and photos specifically
    Returns organized display of logos in a grid format
    """
    result = fetch_specific_content(url, '.exhibitor-logo, .sponsor-logo, .company-logo, .logo, img', text_only=False)
    
    if result['success'] and result.get('images_html'):
        # Enhance the HTML for better logo display
        logos_html = result['images_html']
        # Add grid styling for better organization
        grid_html = f"""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0;">
            {logos_html.replace('<img src="', '<div style="text-align: center; padding: 15px; border: 2px solid #198A00; border-radius: 10px; background: linear-gradient(135deg, #1a1a1a, #2d2d2d);"><img src="').replace('" alt="Image" style="max-width: 100%; height: auto; margin: 10px 0; border-radius: 8px;" /><br/>', '" alt="Logo" style="max-width: 100%; max-height: 120px; height: auto; border-radius: 8px;" /></div>')}
        </div>
        """
        result['logos_grid_html'] = grid_html
    
    return result
