import json, streamlit as st
from lib.ui import apply_brand, top_nav

st.set_page_config(page_title="Agenda — Insaka", page_icon="🗓️", layout="wide")
apply_brand()
top_nav()

st.title("Agenda")
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
