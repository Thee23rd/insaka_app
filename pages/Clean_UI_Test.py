# pages/Clean_UI_Test.py
import streamlit as st
from lib.hide_streamlit_ui import apply_hide_streamlit_ui, apply_pwa_meta_tags
from lib.ui import apply_brand

st.set_page_config(
    page_title="Clean UI Test — Insaka", 
    page_icon="🧪", 
    layout="wide"
)

# Apply clean UI (hides Streamlit elements)
apply_hide_streamlit_ui()

# Apply Zambian branding
apply_brand()

st.markdown("# 🧪 Clean UI Test")
st.markdown("This page tests the clean UI without Streamlit elements")

st.markdown("## ✅ What Should Be Hidden:")
st.markdown("""
- ❌ Streamlit header/toolbar
- ❌ Streamlit sidebar  
- ❌ Streamlit footer
- ❌ Streamlit branding
- ❌ Streamlit status bar
- ❌ Streamlit menu button
""")

st.markdown("## 🎯 What Should Be Visible:")
st.markdown("""
- ✅ Your app content only
- ✅ Zambian color scheme
- ✅ Clean, minimal interface
- ✅ Full-width layout
""")

# Test various Streamlit components
st.markdown("## 🧪 Component Tests")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📝 Text Input")
    st.text_input("Test input", placeholder="Type something...")
    
    st.markdown("### 🔘 Button")
    if st.button("Test Button", type="primary"):
        st.success("Button clicked!")
    
    st.markdown("### 📊 Selectbox")
    option = st.selectbox("Choose an option", ["Option 1", "Option 2", "Option 3"])
    st.write(f"You selected: {option}")

with col2:
    st.markdown("### 📅 Date Input")
    date = st.date_input("Pick a date")
    st.write(f"Selected date: {date}")
    
    st.markdown("### 🎨 Color Picker")
    color = st.color_picker("Pick a color", "#198A00")
    st.write(f"Selected color: {color}")
    
    st.markdown("### 📁 File Uploader")
    uploaded_file = st.file_uploader("Upload a file")
    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")

# Test expander
with st.expander("🔽 Expandable Section"):
    st.markdown("This is inside an expandable section.")
    st.markdown("The expander should work normally.")
    st.markdown("Only Streamlit UI elements should be hidden.")

# Test tabs
tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])

with tab1:
    st.markdown("### 📋 Tab 1 Content")
    st.markdown("This is the first tab.")

with tab2:
    st.markdown("### 📋 Tab 2 Content")
    st.markdown("This is the second tab.")

with tab3:
    st.markdown("### 📋 Tab 3 Content")
    st.markdown("This is the third tab.")

# Test metrics
st.markdown("## 📊 Metrics Test")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Users", "1,234", "123")
with col2:
    st.metric("Revenue", "$12,345", "-$123")
with col3:
    st.metric("Growth", "45%", "5%")
with col4:
    st.metric("Active", "89", "12")

# Test chart
st.markdown("## 📈 Chart Test")
import pandas as pd
import numpy as np

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['A', 'B', 'C']
)

st.line_chart(chart_data)

# Test alerts
st.markdown("## 🚨 Alert Test")
st.success("This is a success message!")
st.info("This is an info message!")
st.warning("This is a warning message!")
st.error("This is an error message!")

# Test progress
st.markdown("## ⏳ Progress Test")
progress = st.progress(0.7)
st.write("70% complete")

# Test spinner
if st.button("Test Spinner"):
    with st.spinner("Loading..."):
        import time
        time.sleep(2)
    st.success("Done!")

# Footer
st.markdown("---")
st.markdown("### 🎯 Clean UI Test Complete")
st.markdown("""
**If you can see this page without any Streamlit UI elements:**
- ✅ Header/toolbar is hidden
- ✅ Sidebar is hidden  
- ✅ Footer is hidden
- ✅ Only your app content is visible

**Your clean UI is working perfectly! 🎉**
""")

if st.button("🏠 Back to Dashboard", type="primary", use_container_width=True):
    st.switch_page("pages/1_Delegate_Dashboard.py")
