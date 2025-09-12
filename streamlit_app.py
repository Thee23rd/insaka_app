import streamlit as st
from datetime import datetime
import pandas as pd
from dateutil import parser
from backend import get_sessions, get_speakers, get_exhibitors, get_sponsors, get_materials, get_venue

st.set_page_config(page_title="Insaka Conference", page_icon="🟢", layout="wide")

# Hide Streamlit chrome for a kiosk feel
st.markdown("""
<style>
#MainMenu{visibility:hidden} header{visibility:hidden} footer{visibility:hidden}
[data-testid="stToolbar"]{display:none!important}
.card{background:#101827;border:1px solid #1f2937;border-radius:16px;padding:18px}
.hero h1{margin:0;font-size:2rem}
.subtle{opacity:.8;margin-top:.25rem}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px}
.logo-tile{background:#0b1220;border:1px solid #1f2937;border-radius:14px;padding:12px;text-align:center}
.logo-tile img{max-width:100%;max-height:80px;object-fit:contain}
.sesh{border:1px solid #1f2937;border-radius:12px;padding:12px;margin-bottom:10px;background:#0b1220}
.btn{background:#22c55e;border:none;color:#081016;padding:8px 12px;border-radius:10px;cursor:pointer;font-weight:700}
.btn:disabled{opacity:.5;cursor:not-allowed}
</style>
""", unsafe_allow_html=True)

# tiny helper
def hms(ts):
    try:
        dt = parser.isoparse(ts)
        return dt.strftime("%a %d %b, %H:%M")
    except Exception:
        return ts or "TBA"

# --- NAV ---
tabs = st.tabs(["🏠 Home","🗓️ Agenda","🎤 Speakers","🏬 Exhibitors","🏅 Sponsors","📎 Materials","🗺️ Venue"])

# --- HOME ---
with tabs[0]:
    st.markdown("""
    <div class="card">
      <img src="https://picsum.photos/1200/400?blur=1" alt="Insaka" style="width:100%;border-radius:12px;object-fit:cover;aspect-ratio:3/1">
      <section class="hero">
        <h1>Insaka Conference</h1>
        <p class="subtle">Collaborate • Innovate • Thrive — 6–8 Oct</p>
      </section>
      <p>Install this app for quick access:
        <span class="subtle">Android/Chrome: tap “⋮” → Install App • iOS Safari: Share → Add to Home Screen</span>
      </p>
    </div>
    """, unsafe_allow_html=True)

    # Quick links
    c1,c2,c3 = st.columns(3)
    with c1: st.page_link("pages/1_Agenda.py", label="Open Agenda", icon="🗓️")
    with c2: st.page_link("pages/2_Speakers.py", label="Speakers", icon="🎤")
    with c3: st.page_link("pages/3_Venue.py", label="Venue Map", icon="🗺️")

# --- AGENDA ---
with tabs[1]:
    st.subheader("Agenda")
    st.caption("Tap “Remind me” to get a local notification at start time (requires permission; page must be open).")
    # JS helper for local notification
    st.markdown("""
    <script>
    async function remindAt(ts, title){
      try{
        const ok = (await Notification.requestPermission()) === 'granted';
        if(!ok){ alert('Notifications blocked'); return; }
        const when = new Date(ts).getTime() - Date.now();
        if (when<=0){ alert('This session has started or passed'); return; }
        setTimeout(()=> new Notification('Session reminder', {body: title}), when);
        alert('Reminder set for ' + new Date(ts).toLocaleString());
      }catch(e){ alert('Failed: '+e.message); }
    }
    </script>
    """, unsafe_allow_html=True)

    sessions = get_sessions()
    if not sessions:
        st.info("Agenda coming soon.")
    else:
        # group by day
        df = pd.DataFrame(sessions)
        df["day"] = pd.to_datetime(df["start_time"], errors="coerce").dt.date.astype(str)
        for day, group in df.sort_values("start_time").groupby("day"):
            st.markdown(f"### {day}")
            for row in group.to_dict("records"):
                st.markdown(f"""
                <div class="sesh">
                  <div><strong>{row.get("title")}</strong></div>
                  <div>{hms(row.get("start_time"))} → {hms(row.get("end_time"))} • {row.get("room","")}</div>
                  <div style="margin-top:6px">
                    <button class="btn" onclick="remindAt('{row.get("start_time","")}', `{row.get("title","")}`)">Remind me</button>
                    {'<a class="btn" style="margin-left:8px" href="'+row.get("materials_url")+'" target="_blank">Materials</a>' if row.get("materials_url") else ''}
                  </div>
                </div>
                """, unsafe_allow_html=True)

# --- SPEAKERS ---
with tabs[2]:
    st.subheader("Speakers")
    data = get_speakers()
    if not data:
        st.info("Speakers will be announced soon.")
    else:
        st.markdown('<div class="grid">', unsafe_allow_html=True)
        for s in data:
            img = s.get("headshot_url") or "https://via.placeholder.com/300x300?text=Speaker"
            title_line = " • ".join([t for t in [s.get("title"), s.get("org")] if t])
            st.markdown(f"""
            <div class="card" style="padding:12px">
              <img src="{img}" alt="{s.get('name','')}" style="width:100%;border-radius:12px;object-fit:cover;aspect-ratio:1/1">
              <h4 style="margin:.5rem 0 0">{s.get('name','')}</h4>
              <div class="subtle">{title_line}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- EXHIBITORS ---
with tabs[3]:
    st.subheader("Exhibitors")
    rows = get_exhibitors()
    if not rows:
        st.info("Exhibitors list coming soon.")
    else:
        st.markdown('<div class="grid">', unsafe_allow_html=True)
        for ex in rows:
            logo = ex.get("logo_url") or "https://via.placeholder.com/300x120?text=Logo"
            href = ex.get("website") or "#"
            st.markdown(f"""
            <a class="logo-tile" href="{href}" target="_blank">
              <img src="{logo}" alt="{ex.get('name','')}">
              <div style="margin-top:8px;font-weight:700">{ex.get('name','')}</div>
              <div class="subtle">{ex.get('booth','')}</div>
            </a>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- SPONSORS ---
with tabs[4]:
    st.subheader("Sponsors")
    rows = get_sponsors()
    if not rows:
        st.info("Sponsors will be announced soon.")
    else:
        tiers = ["Platinum","Gold","Silver","Bronze"]
        for tier in tiers:
            tier_rows = [r for r in rows if (r.get("tier") or "Bronze")==tier]
            if not tier_rows: continue
            st.markdown(f"### {tier}")
            st.markdown('<div class="grid">', unsafe_allow_html=True)
            for sp in tier_rows:
                logo = sp.get("logo_url") or "https://via.placeholder.com/300x120?text=Logo"
                href = sp.get("website") or "#"
                st.markdown(f"""
                <a class="logo-tile" href="{href}" target="_blank">
                  <img src="{logo}" alt="{sp.get('name','')}">
                  <div style="margin-top:8px;font-weight:700">{sp.get('name','')}</div>
                </a>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# --- MATERIALS ---
with tabs[5]:
    st.subheader("Conference Materials")
    mats = get_materials()
    if not mats:
        st.info("Materials will appear here as they’re uploaded.")
    else:
        for m in mats:
            st.markdown(f"- [{m.get('title','Untitled')}]({m.get('url','#')})  \n  <span class='subtle'>{m.get('description','')}</span>", unsafe_allow_html=True)

# --- VENUE ---
with tabs[6]:
    st.subheader("Venue Map")
    v = get_venue()
    if not v or not v.get("map_image_url"):
        st.info("Venue map will be posted soon.")
    else:
        st.image(v["map_image_url"], use_container_width=True, caption=v.get("name",""))
        if v.get("geo"):
            st.caption("Hotspots:")
            for pt in v["geo"]:
                st.markdown(f"- **{pt.get('label','Point')}** (x={pt.get('x')}, y={pt.get('y')})")
