# lib/simple_web_fetcher.py
import requests
import streamlit as st
from datetime import datetime, timedelta
import json

def fetch_web_text(url, cache_duration_minutes=30):
    """
    Simple web content fetcher without HTML parsing
    
    Args:
        url: The website URL to fetch content from
        cache_duration_minutes: How long to cache the content (default: 30 minutes)
    
    Returns:
        dict: Contains 'success', 'content', 'timestamp', 'error'
    """
    
    # Check cache first
    cache_key = f"web_text_{hash(url)}"
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
        
        # Extract images and content
        import re
        from urllib.parse import urljoin
        
        # Extract images first
        images_html = ""
        img_pattern = r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>'
        img_matches = re.findall(img_pattern, response.text, re.IGNORECASE)
        
        for img_src in img_matches:
            # Handle relative URLs
            if img_src.startswith('//'):
                full_img_src = 'https:' + img_src
            elif img_src.startswith('/'):
                full_img_src = urljoin(url, img_src)
            elif not img_src.startswith('http'):
                full_img_src = urljoin(url, img_src)
            else:
                full_img_src = img_src
            
            # Add image to HTML
            images_html += f'<img src="{full_img_src}" alt="Image" style="max-width: 100%; height: auto; margin: 10px 0; border-radius: 8px;" /><br/>'
        
        # Get text content
        content_text = response.text
        
        # Simple cleanup - remove HTML tags manually
        # Remove script and style elements
        content_text = re.sub(r'<script[^>]*>.*?</script>', '', content_text, flags=re.DOTALL | re.IGNORECASE)
        content_text = re.sub(r'<style[^>]*>.*?</style>', '', content_text, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove HTML tags
        content_text = re.sub(r'<[^>]+>', ' ', content_text)
        
        # Clean up whitespace
        content_text = ' '.join(content_text.split())
        
        # Limit content length
        if len(content_text) > 5000:
            content_text = content_text[:5000] + "..."
        
        # Prepare result
        result = {
            'success': True,
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
        return {
            'success': False,
            'content': None,
            'timestamp': datetime.now().isoformat(),
            'error': f"Network error: {str(e)}"
        }
    except Exception as e:
        return {
            'success': False,
            'content': None,
            'timestamp': datetime.now().isoformat(),
            'error': f"Error: {str(e)}"
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

def display_simple_content(content_data, show_timestamp=True):
    """
    Display simple web content in Streamlit with proper formatting
    
    Args:
        content_data: The result from fetch_web_text()
        show_timestamp: Whether to show when content was fetched
    """
    
    if not content_data['success']:
        st.error(f"❌ Error fetching content: {content_data['error']}")
        return
    
    # Display SSL fallback warning if applicable
    if content_data.get('ssl_fallback_used', False):
        st.warning("⚠️ SSL certificate verification was bypassed for this website. Content was fetched successfully but with reduced security.")
    
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
