import json, streamlit as st
from lib.ui import apply_brand

st.set_page_config(page_title="Agenda — Insaka", page_icon="🗓️", layout="wide")

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

# Back button
if st.button("← Back to Dashboard", type="secondary"):
    st.switch_page("pages/1_Delegate_Dashboard.py")

st.markdown("# 📅 Agenda")

st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)
# Example: load from data/agenda.json if present
try:
    agenda = json.load(open("data/agenda.json", "r", encoding="utf-8"))
except Exception:
    agenda = [
        {"day":"Sun 6 Oct", "time":"09:00", "title":"Opening & Keynote", "room":"Main Hall"},
        {"day":"Sun 6 Oct", "time":"11:00", "title":"Panel: Innovation", "room":"Auditorium A"},
    ]

days = sorted(set([a["day"] for a in agenda]))
for d in days:
    st.subheader(d)
    for item in [a for a in agenda if a["day"] == d]:
        st.write(f"**{item['time']}** — {item['title']}  ·  _{item.get('room','TBA')}_")
