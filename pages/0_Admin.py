# pages/0_Admin.py
import os, json, io, pathlib
import streamlit as st
from lib.ui import apply_brand, top_nav 

import streamlit as st
from staff_service import (
    load_staff_df, save_staff_df, register_staff,
    import_staff_excel, export_staff_excel, set_checked_in
)
from utils_assets import save_upload

# Zambian-themed header
st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

st.markdown("# 🎫 Admin Panel")
st.markdown("**Organizers / Services / VIP Management**")

st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

            # Navigation to other admin pages
            st.markdown("### 🔗 Admin Navigation")
            nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns(5)

            with nav_col1:
                if st.button("📢 Manage Announcements", width='stretch'):
                    st.switch_page("pages/Admin_Announcements.py")

            with nav_col2:
                if st.button("📰 Manage News & Updates", width='stretch'):
                    st.switch_page("pages/Admin_News.py")

            with nav_col3:
                if st.button("📸 PR & Social Media", width='stretch'):
                    st.switch_page("pages/Admin_PR.py")

            with nav_col4:
                if st.button("📱 QR Code Management", width='stretch'):
                    st.switch_page("pages/Admin_QR_Codes.py")

            with nav_col5:
                if st.button("🌐 View Public Page", width='stretch'):
                    st.switch_page("pages/9_External_Content.py")

st.markdown("---")
st.markdown("### 🎫 Complimentary Passes Management")

tab_new, tab_manage, tab_stats, tab_import, tab_export = st.tabs(
    ["➕ Add", "🗂 Manage", "📊 Statistics", "⬆️ Import", "⬇️ Export"]
)

# --- Add single ---
with tab_new:
    with st.form("comp_new", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name*", "")
            category = st.selectbox("Category*", [
                "Organizing Committee", "Speaker", "VIP", "Media",
                "Service Provider", "Sponsor/Exhibitor Staff", "Other"
            ])
            organization = st.text_input("Organization / Dept*", "")
            role_title = st.text_input("Role / Title", "")
        with col2:
            email = st.text_input("Email", "")
            phone = st.text_input("Phone", "")
            nationality = st.text_input("Nationality", "")
            notes = st.text_area("Notes", "")
            photo = st.file_uploader("Badge Photo (JPG/PNG/WebP)", type=["jpg","jpeg","png","webp"])

        submitted = st.form_submit_button("Save")
    if submitted:
        photo_path = ""
        if photo:
            # will become assets/uploads/badges/<slug>_timestamp.ext
            photo_path = save_upload(photo, kind="badges", name_hint=name)
        ok, msg = register_staff(
            name=name,
            category=category,
            organization=organization,
            role_title=role_title,
            email=email,
            phone=phone,
            badge_photo_path=photo_path,
            notes=notes,
            nationality=nationality,
        )
        st.success(msg) if ok else st.warning(msg)

# --- Manage list ---
with tab_manage:
    df = load_staff_df()
    st.caption(f"{len(df)} complimentary records")
    st.dataframe(df, width='stretch', height=420)

    st.subheader("Edit selected")
    ids = st.multiselect("Select ID(s)", options=df["ID"].tolist())
    if ids:
        # simple check-in toggle
        colA, colB = st.columns(2)
        with colA:
            if st.button("Mark as Checked-In"):
                upd, nf = set_checked_in(ids, True)
                st.success(f"Updated {upd}; Not found {nf}")
        with colB:
            if st.button("Mark as Not Checked-In"):
                upd, nf = set_checked_in(ids, False)
                st.success(f"Updated {upd}; Not found {nf}")

        # optional quick photo replace for one person
        if len(ids) == 1:
            up = st.file_uploader("Replace badge photo", type=["jpg","jpeg","png","webp"], key="rephoto")
            if up:
                df = load_staff_df()
                mask = df["ID"].astype(str) == ids[0]
                path = save_upload(up, kind="badges", name_hint=df.loc[mask, "Name"].values[0])
                df.loc[mask, "BadgePhoto"] = path
                save_staff_df(df)
                st.success(f"Photo saved → {path}")

# --- Statistics Dashboard ---
with tab_stats:
    df = load_staff_df()
    
    if len(df) == 0:
        st.info("No delegate records found. Add some records to see statistics.")
    else:
        # Overall statistics
        st.subheader("📊 Delegate Statistics Overview")
        
        # Key metrics in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                label="Total Delegates",
                value=len(df),
                help="Total number of delegates in the system"
            )
        
        with col2:
            checked_in_count = len(df[df.get('CheckedIn', False) == True])
            st.metric(
                label="Checked In",
                value=checked_in_count,
                delta=f"{checked_in_count/len(df)*100:.1f}%" if len(df) > 0 else "0%",
                help="Number and percentage of delegates who have checked in"
            )
        
        st.markdown("---")
        
        # Category breakdown
        st.subheader("👥 Delegates by Category")
        
        if 'Category' in df.columns:
            category_counts = df['Category'].value_counts()
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.bar_chart(category_counts)
            
            with col2:
                st.write("**Category Breakdown:**")
                for category, count in category_counts.items():
                    percentage = (count / len(df)) * 100
                    st.write(f"• **{category}**: {count} ({percentage:.1f}%)")
        
        st.markdown("---")
        
        # Organization breakdown
        st.subheader("🏢 Delegates by Organization")
        
        if 'Organization' in df.columns:
            org_counts = df['Organization'].value_counts().head(10)  # Top 10 organizations
            
            if len(org_counts) > 0:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.bar_chart(org_counts)
                
                with col2:
                    st.write("**Top Organizations:**")
                    for org, count in org_counts.items():
                        percentage = (count / len(df)) * 100
                        st.write(f"• **{org}**: {count} ({percentage:.1f}%)")
            else:
                st.info("No organization data available.")
        
        st.markdown("---")
        
        # Nationality breakdown
        st.subheader("🌍 Delegates by Nationality")
        
        if 'Nationality' in df.columns:
            nationality_counts = df['Nationality'].value_counts()
            
            # Filter out empty nationalities
            nationality_counts = nationality_counts[nationality_counts.index != '']
            
            if len(nationality_counts) > 0:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.bar_chart(nationality_counts)
                
                with col2:
                    st.write("**Nationality Breakdown:**")
                    for nationality, count in nationality_counts.items():
                        percentage = (count / len(df)) * 100
                        st.write(f"• **{nationality}**: {count} ({percentage:.1f}%)")
            else:
                st.info("No nationality data available.")
        
        st.markdown("---")
        
        # Daily check-in status
        st.subheader("✅ Daily Check-in Status")
        
        checkin_columns = [col for col in df.columns if col.startswith('Day') and col.endswith('_CheckIn')]
        
        if checkin_columns:
            checkin_stats = {}
            for col in checkin_columns:
                day_num = col.replace('Day', '').replace('_CheckIn', '')
                checked_count = len(df[df[col] == True])
                checkin_stats[f"Day {day_num}"] = checked_count
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.bar_chart(checkin_stats)
            
            with col2:
                st.write("**Daily Check-in:**")
                for day, count in checkin_stats.items():
                    percentage = (count / len(df)) * 100
                    st.write(f"• **{day}**: {count} ({percentage:.1f}%)")
        else:
            st.info("No daily check-in data available.")
        
        st.markdown("---")
        
        # Recent activity summary
        st.subheader("📈 Summary")
        
        summary_col1, summary_col2 = st.columns(2)
        
        with summary_col1:
            st.info(f"""
            **Total Delegates:** {len(df)}
            
            **Checked In:** {checked_in_count} ({checked_in_count/len(df)*100:.1f}%)
            
            **Categories:** {len(df['Category'].unique()) if 'Category' in df.columns else 0}
            
            **Organizations:** {len(df['Organization'].unique()) if 'Organization' in df.columns else 0}
            """)
        
        with summary_col2:
            if 'Category' in df.columns:
                top_category = df['Category'].value_counts().index[0] if len(df) > 0 else "N/A"
                top_category_count = df['Category'].value_counts().iloc[0] if len(df) > 0 else 0
                
                st.info(f"""
                **Top Category:** {top_category}
                
                **Count:** {top_category_count}
                
                **Percentage:** {top_category_count/len(df)*100:.1f}%
                
                **Last Updated:** {df.index.max() if len(df) > 0 else "N/A"}
                """)

# --- Import ---
with tab_import:
    st.caption("Excel expected columns: Name, Category, Organization, RoleTitle, Email, Phone, Notes")
    up = st.file_uploader("Upload Excel (.xlsx)", type=["xlsx"])
    if up:
        added, skipped = import_staff_excel(up.read())
        st.success(f"Added {added} • Skipped duplicates {skipped}")

# --- Export ---
with tab_export:
    data, fname = export_staff_excel()
    st.download_button("Download Excel", data=data, file_name=fname,
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

st.set_page_config(page_title="Admin — Insaka", page_icon="🔐", layout="wide")
apply_brand()
top_nav()

ADMIN_PIN = os.environ.get("ADMIN_PIN", "") or st.secrets.get("ADMIN_PIN", "")
st.title("Admin Console")

# --- Auth ---
pin = st.text_input("Enter Admin PIN", type="password")
if not (ADMIN_PIN and pin.strip() == ADMIN_PIN):
    st.warning("Enter the admin PIN to manage data and files.")
    st.stop()

st.success("Authenticated.")

# --- Helpers ---
DATA_DIR = pathlib.Path("data")
ASSETS = pathlib.Path("assets")
AS_MATERIALS = ASSETS / "materials"
AS_LOGOS = ASSETS / "logos"
AS_PHOTOS = ASSETS / "photos"
for p in [DATA_DIR, AS_MATERIALS, AS_LOGOS, AS_PHOTOS]:
    p.mkdir(parents=True, exist_ok=True)

def load_json(path: pathlib.Path, default):
    try:
        return json.loads(path.read_text("utf-8"))
    except Exception:
        return default

def save_json(path: pathlib.Path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    st.success(f"Saved → {path}")

# --- Tabs ---
tab_agenda, tab_speakers, tab_exhibitors, tab_sponsors, tab_materials = st.tabs(
    ["Agenda", "Speakers", "Exhibitors", "Sponsors", "Materials"]
)

# ===== Agenda =====
with tab_agenda:
    st.subheader("Agenda (edit rows and save)")
    default_agenda = [{"day":"Sun 6 Oct", "time":"09:00", "title":"Opening & Keynote", "room":"Main Hall"}]
    agenda = load_json(DATA_DIR / "agenda.json", default_agenda)
    edited = st.data_editor(
        agenda,
        num_rows="dynamic",
        width='stretch',
        column_config={
            "day": "Day",
            "time": "Time",
            "title": "Title",
            "room": "Room",
        },
        key="ed_agenda",
    )
    if st.button("Save Agenda"):
        save_json(DATA_DIR / "agenda.json", edited)

# ===== Speakers =====
with tab_speakers:
    st.subheader("Speakers")
    default_speakers = [{"name":"Dr. Chileshe Banda","talk":"Digital Agriculture","bio":"","photo":"","slides":""}]
    speakers = load_json(DATA_DIR / "speakers.json", default_speakers)
    edited = st.data_editor(
        speakers,
        num_rows="dynamic",
        width='stretch',
        column_config={
            "name": "Name",
            "talk": "Talk Title",
            "bio": "Bio",
            "photo": "Photo (path or URL)",
            "slides": "Slides (path or URL)",
        },
        key="ed_speakers",
    )
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Save Speakers"):
            save_json(DATA_DIR / "speakers.json", edited)
    with c2:
        up_photo = st.file_uploader("Upload speaker photo(s)", type=["png","jpg","jpeg"], accept_multiple_files=True)
        if up_photo:
            for f in up_photo:
                (AS_PHOTOS / f.name).write_bytes(f.read())
            st.success("Uploaded to assets/photos/")
        up_slides = st.file_uploader("Upload slides (PDF)", type=["pdf"], accept_multiple_files=True)
        if up_slides:
            for f in up_slides:
                (AS_MATERIALS / f.name).write_bytes(f.read())
            st.success("Uploaded to assets/materials/")

# ===== Exhibitors =====
with tab_exhibitors:
    st.subheader("Exhibitors")
    default_exh = [{"name":"AgriTech Co.","stand":"A12","logo":"assets/logos/agritech.png","url":"https://example.com"}]
    exhibitors = load_json(DATA_DIR / "exhibitors.json", default_exh)
    edited = st.data_editor(
        exhibitors,
        num_rows="dynamic",
        width='stretch',
        column_config={
            "name":"Name",
            "stand":"Stand",
            "logo":"Logo (path or URL)",
            "url":"Website",
        },
        key="ed_exhibitors",
    )
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Save Exhibitors"):
            save_json(DATA_DIR / "exhibitors.json", edited)
    with c2:
        up_logos = st.file_uploader("Upload exhibitor logo(s)", type=["png","jpg","jpeg","webp"], accept_multiple_files=True)
        if up_logos:
            for f in up_logos:
                (AS_LOGOS / f.name).write_bytes(f.read())
            st.success("Uploaded to assets/logos/")

# ===== Sponsors =====
with tab_sponsors:
    st.subheader("Sponsors (by tiers)")
    default_sponsors = {
        "Platinum":[{"name":"ZNBC","logo":"assets/logos/znbc.png"}],
        "Gold":[{"name":"ZESCO","logo":"assets/logos/zesco.png"}],
        "Silver":[{"name":"BoZ","logo":"assets/logos/boz.png"}]
    }
    sponsors = load_json(DATA_DIR / "sponsors.json", default_sponsors)

    tiers = list(sponsors.keys())
    tier = st.selectbox("Tier", options=tiers + ["+ Add new tier"])
    if tier == "+ Add new tier":
        new_tier = st.text_input("New tier name")
        if st.button("Create tier") and new_tier:
            sponsors[new_tier] = []
            save_json(DATA_DIR / "sponsors.json", sponsors)

    else:
        st.caption(f"Editing tier: {tier}")
        edited = st.data_editor(
            sponsors.get(tier, []),
            num_rows="dynamic",
            width='stretch',
            column_config={"name":"Name", "logo":"Logo (path or URL)"},
            key=f"ed_sponsors_{tier}"
        )
        colA, colB = st.columns(2)
        with colA:
            if st.button("Save sponsors tier"):
                sponsors[tier] = edited
                save_json(DATA_DIR / "sponsors.json", sponsors)
        with colB:
            up_logos = st.file_uploader("Upload sponsor logo(s)", type=["png","jpg","jpeg","webp"], accept_multiple_files=True)
            if up_logos:
                for f in up_logos:
                    (AS_LOGOS / f.name).write_bytes(f.read())
                st.success("Uploaded to assets/logos/")

# ===== Materials =====
with tab_materials:
    st.subheader("Conference Materials (files)")
    up_files = st.file_uploader("Upload files (PDF, images, etc.)", type=None, accept_multiple_files=True)
    if up_files:
        for f in up_files:
            (AS_MATERIALS / f.name).write_bytes(f.read())
        st.success("Uploaded to assets/materials/")

    st.caption("Files present in assets/materials/:")
    for f in sorted(AS_MATERIALS.glob("*")):
        st.write("•", f.name)
