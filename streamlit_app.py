# streamlit_app.py
from __future__ import annotations
import streamlit as st
from lib.ui import apply_brand, top_nav

st.set_page_config(page_title="Insaka Conference", page_icon="🪘", layout="wide")
apply_brand()

top_nav()

st.markdown(
    """
    <div class="card">
      <img src="assets/logos/insaka.jpg" alt="Insaka Conference" style="width:100%;border-radius:12px;object-fit:cover;aspect-ratio:4/3">
      <section class="hero">
        <h1>Insaka Conference</h1>
        <p class="subtle">Collaborate • Innovate • Thrive — 6–8 Oct</p>
      </section>
      <p>Install this app:
        <span class="subtle pill">Android/Chrome: ⋮ → Install App</span>
        <span class="subtle pill">iOS Safari: Share → Add to Home Screen</span>
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("Open Agenda", use_container_width=True):
        st.switch_page("pages/1_Agenda.py")
with c2:
    if st.button("Speakers", use_container_width=True):
        st.switch_page("pages/2_Speakers.py")
with c3:
    if st.button("Venue Map", use_container_width=True):
        st.switch_page("pages/6_Venue.py")

st.write("---")
st.subheader("Welcome")
st.write(
    "Explore sessions, speakers, exhibition stands, and download conference materials. "
    "Enable notifications to get nudges when key sessions begin."
)
