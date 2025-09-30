# pages/0_Admin.py
import os, json, io, pathlib
import streamlit as st
from lib.ui import apply_brand, top_nav 
from staff_service import (
    load_staff_df, save_staff_df, register_staff,
    import_staff_excel, export_staff_excel, set_checked_in
)
from utils_assets import save_upload

st.set_page_config(page_title="Admin — Insaka", page_icon="🔐", layout="wide")
apply_brand()
top_nav()

# Zambian-themed header
st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

st.markdown("# 🎫 Admin Panel")
st.markdown("**Organizers / Services / VIP Management**")

st.markdown('<div class="zambia-accent"></div>', unsafe_allow_html=True)

# Navigation to other admin pages
st.markdown("### 🔗 Admin Navigation")
nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns(5)

with nav_col1:
    if st.button("📢 Manage Announcements", use_container_width=True):
        st.switch_page("pages/Admin_Announcements.py")

with nav_col2:
    if st.button("📰 Manage News & Updates", use_container_width=True):
        st.switch_page("pages/Admin_News.py")

with nav_col3:
    if st.button("📸 PR & Social Media", use_container_width=True):
        st.switch_page("pages/Admin_PR.py")

with nav_col4:
    if st.button("📱 QR Code Management", use_container_width=True):
        st.switch_page("pages/Admin_QR_Codes.py")

with nav_col5:
    if st.button("🌐 View Public Page", use_container_width=True):
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
    st.dataframe(df, use_container_width=True, height=420)

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
    st.subheader("Event Schedule Manager")
    
    # Load speakers for dropdown
    speakers_data = load_json(DATA_DIR / "speakers.json", [])
    speaker_names = [sp.get("name", "") for sp in speakers_data if sp.get("name")]
    
    default_agenda = [
        {
            "day":"Sun 6 Oct",
            "time":"09:00",
            "title":"Opening & Keynote",
            "room":"Main Hall",
            "segment_type":"keynote",
            "description":"",
            "speakers":[],
            "facilitators":[]
        }
    ]
    agenda = load_json(DATA_DIR / "agenda.json", default_agenda)
    
    # Data editor with enhanced columns
    edited = st.data_editor(
        agenda,
        num_rows="dynamic",
        width='stretch',
        column_config={
            "day": st.column_config.TextColumn("Day", help="e.g., Sun 6 Oct"),
            "time": st.column_config.TextColumn("Time", help="e.g., 09:00 AM"),
            "title": st.column_config.TextColumn("Title"),
            "room": st.column_config.TextColumn("Room/Venue"),
            "segment_type": st.column_config.SelectboxColumn(
                "Segment Type",
                options=["keynote", "presentation", "panel", "break", "networking", "workshop", "closing", "other"],
                help="Color-coded segment type"
            ),
            "description": st.column_config.TextColumn("Description"),
            "speakers": st.column_config.ListColumn("Speakers (comma-separated names)"),
            "facilitators": st.column_config.ListColumn("Facilitators/Moderators"),
        },
        key="ed_agenda",
    )
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("💾 Save Schedule"):
            save_json(DATA_DIR / "agenda.json", edited)
    
    with c2:
        st.markdown("**Segment Colors:**")
        st.caption("🔴 Keynote · 🟢 Presentation · 🟠 Panel · 🟡 Break · 🟢 Networking · 🟤 Workshop · 🔴 Closing")
    
    st.markdown("---")
    colA, colB = st.columns(2)
    
    # Quick add single schedule item
    with colA:
        st.markdown("#### ➕ Add Schedule Item")
        with st.form("add_schedule_item", clear_on_submit=True):
            sch_day = st.text_input("Day*", placeholder="e.g., Sun 6 Oct")
            sch_time = st.text_input("Time*", placeholder="e.g., 09:00 AM")
            sch_title = st.text_input("Title*")
            sch_room = st.text_input("Room/Venue")
            sch_type = st.selectbox("Segment Type", ["keynote", "presentation", "panel", "break", "networking", "workshop", "closing", "other"])
            sch_desc = st.text_area("Description")
            sch_speakers = st.multiselect("Speakers", options=speaker_names)
            sch_facilitators = st.text_input("Facilitators (comma-separated)")
            submitted_sch = st.form_submit_button("Add to Schedule")
        
        if submitted_sch:
            new_item = {
                "day": sch_day.strip(),
                "time": sch_time.strip(),
                "title": sch_title.strip(),
                "room": sch_room.strip(),
                "segment_type": sch_type,
                "description": sch_desc.strip(),
                "speakers": sch_speakers,
                "facilitators": [f.strip() for f in sch_facilitators.split(",") if f.strip()]
            }
            current = load_json(DATA_DIR / "agenda.json", default_agenda)
            current.append(new_item)
            save_json(DATA_DIR / "agenda.json", current)
    
    # Bulk import
    with colB:
        st.markdown("#### 📥 Bulk Import Schedule (CSV/XLSX)")
        st.caption("Expected columns: day, time, title, room, segment_type, description, speakers, facilitators")
        
        # Download template
        try:
            template_path = DATA_DIR / "schedule_template.csv"
            if template_path.exists():
                st.download_button(
                    "📥 Download CSV Template",
                    data=template_path.read_bytes(),
                    file_name="schedule_template.csv",
                    mime="text/csv"
                )
        except Exception:
            pass
        
        replace_agenda = st.checkbox("Replace existing schedule", key="agenda_replace")
        up_agenda = st.file_uploader("Upload file", type=["csv", "xlsx"], key="agenda_bulk")
        
        if up_agenda is not None:
            import pandas as pd
            try:
                if up_agenda.name.lower().endswith(".csv"):
                    df = pd.read_csv(up_agenda)
                else:
                    df = pd.read_excel(up_agenda)
                
                df.columns = [str(c).strip().lower() for c in df.columns]
                rows = []
                for _, r in df.iterrows():
                    # Parse speakers and facilitators (comma-separated)
                    speakers_str = str(r.get("speakers", ""))
                    speakers_list = [s.strip() for s in speakers_str.split(",") if s.strip()] if not pd.isna(r.get("speakers")) else []
                    
                    facilitators_str = str(r.get("facilitators", ""))
                    facilitators_list = [f.strip() for f in facilitators_str.split(",") if f.strip()] if not pd.isna(r.get("facilitators")) else []
                    
                    rows.append({
                        "day": str(r.get("day", "")).strip(),
                        "time": str(r.get("time", "")).strip(),
                        "title": str(r.get("title", "")).strip(),
                        "room": str(r.get("room", "")).strip(),
                        "segment_type": str(r.get("segment_type", "other")).strip(),
                        "description": str(r.get("description", "")).strip() if not pd.isna(r.get("description")) else "",
                        "speakers": speakers_list,
                        "facilitators": facilitators_list,
                    })
                
                if replace_agenda:
                    save_json(DATA_DIR / "agenda.json", rows)
                else:
                    existing = load_json(DATA_DIR / "agenda.json", default_agenda)
                    existing.extend(rows)
                    save_json(DATA_DIR / "agenda.json", existing)
                    
            except Exception as e:
                st.warning(f"Import failed: {e}")

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

    st.markdown("---")
    colA, colB = st.columns(2)

    # Add single speaker with direct photo upload (jpg/jpeg)
    with colA:
        st.markdown("#### ➕ Add Single Speaker")
        with st.form("add_speaker_form", clear_on_submit=True):
            s_name = st.text_input("Name*")
            s_talk = st.text_input("Talk Title*")
            s_bio = st.text_area("Bio")
            s_photo = st.file_uploader("Photo (JPG/JPEG)", type=["jpg","jpeg"]) 
            submitted_add = st.form_submit_button("Add Speaker")
        if submitted_add:
            photo_path = ""
            if s_photo is not None:
                (AS_PHOTOS / s_photo.name).write_bytes(s_photo.read())
                photo_path = (AS_PHOTOS / s_photo.name).as_posix()
            new_rec = {
                "name": s_name.strip(),
                "talk": s_talk.strip(),
                "bio": s_bio.strip(),
                "photo": photo_path,
                "slides": "",
            }
            all_speakers = load_json(DATA_DIR / "speakers.json", default_speakers)
            all_speakers.append(new_rec)
            save_json(DATA_DIR / "speakers.json", all_speakers)

        # Quick photo replace for an existing speaker
        st.markdown("#### 🖼️ Update Speaker Photo")
        if len(edited) > 0:
            try:
                names = [r.get("name", "") for r in edited]
            except Exception:
                names = []
            target_name = st.selectbox("Select speaker", options=names)
            up_one = st.file_uploader("Upload new photo (JPG/JPEG)", type=["jpg","jpeg"], key="sp_one_photo")
            if up_one is not None and target_name:
                (AS_PHOTOS / up_one.name).write_bytes(up_one.read())
                path = (AS_PHOTOS / up_one.name).as_posix()
                # update and save
                for rec in speakers:
                    if rec.get("name") == target_name:
                        rec["photo"] = path
                        break
                save_json(DATA_DIR / "speakers.json", speakers)

    # Bulk import and bulk link photos
    with colB:
        st.markdown("#### 📥 Bulk Import Speakers (CSV/XLSX)")
        replace = st.checkbox("Replace existing list (otherwise merge by Name)")
        up_table = st.file_uploader("Upload file", type=["csv", "xlsx"], key="sp_bulk")
        if up_table is not None:
            import pandas as pd
            try:
                if up_table.name.lower().endswith(".csv"):
                    df = pd.read_csv(up_table)
                else:
                    df = pd.read_excel(up_table)
                # normalize expected columns
                cols_map = {
                    "name": "name",
                    "talk": "talk",
                    "bio": "bio",
                    "photo": "photo",
                    "slides": "slides",
                }
                df.columns = [str(c).strip().lower() for c in df.columns]
                rows = []
                for _, r in df.iterrows():
                    rows.append({
                        "name": str(r.get("name", "")).strip(),
                        "talk": str(r.get("talk", "")).strip(),
                        "bio": str(r.get("bio", "")).strip(),
                        "photo": str(r.get("photo", "")).strip() if not pd.isna(r.get("photo", "")) else "",
                        "slides": str(r.get("slides", "")).strip() if not pd.isna(r.get("slides", "")) else "",
                    })
                if replace:
                    save_json(DATA_DIR / "speakers.json", rows)
                else:
                    existing = load_json(DATA_DIR / "speakers.json", default_speakers)
                    by_name = {rec.get("name", ""): rec for rec in existing}
                    for rec in rows:
                        nm = rec.get("name", "")
                        if nm in by_name:
                            by_name[nm].update({k: v for k, v in rec.items() if v})
                        else:
                            by_name[nm] = rec
                    merged = list(by_name.values())
                    save_json(DATA_DIR / "speakers.json", merged)
            except Exception as e:
                st.warning(f"Import failed: {e}")

        st.markdown("#### 🔗 Bulk Link Uploaded Photos")
        st.caption("Upload JPG/JPEG files; names will be matched to speaker names.")
        up_many = st.file_uploader("Upload photos", type=["jpg", "jpeg"], accept_multiple_files=True, key="sp_photos_bulk")
        if up_many:
            # Save photos and build a map by slugged basename
            import re
            def slug(s: str) -> str:
                s = re.sub(r"[^a-z0-9]+", "-", str(s).strip().lower())
                return re.sub(r"-+", "-", s).strip("-") or "file"
            saved = {}
            for f in up_many:
                (AS_PHOTOS / f.name).write_bytes(f.read())
                base = f.name.rsplit(".", 1)[0]
                saved[slug(base)] = (AS_PHOTOS / f.name).as_posix()
            # Load, match and update
            current = load_json(DATA_DIR / "speakers.json", default_speakers)
            updated = 0
            for rec in current:
                nm = rec.get("name", "")
                if not nm:
                    continue
                key = slug(nm)
                if key in saved:
                    rec["photo"] = saved[key]
                    updated += 1
            save_json(DATA_DIR / "speakers.json", current)
            st.success(f"Linked photos to {updated} speaker(s)")

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

    st.markdown("---")
    colA, colB = st.columns(2)

    # Single exhibitor add with direct logo upload
    with colA:
        st.markdown("#### ➕ Add Single Exhibitor")
        with st.form("add_exhibitor_form", clear_on_submit=True):
            ex_name = st.text_input("Name*")
            ex_stand = st.text_input("Stand*")
            ex_url = st.text_input("Website URL")
            ex_logo = st.file_uploader("Logo (JPG/JPEG/PNG/WebP)", type=["jpg","jpeg","png","webp"], key="ex_logo_one")
            submitted_ex_add = st.form_submit_button("Add Exhibitor")
        if submitted_ex_add:
            logo_path = ""
            if ex_logo is not None:
                (AS_LOGOS / ex_logo.name).write_bytes(ex_logo.read())
                logo_path = (AS_LOGOS / ex_logo.name).as_posix()
            new_ex = {"name": ex_name.strip(), "stand": ex_stand.strip(), "logo": logo_path, "url": ex_url.strip()}
            all_ex = load_json(DATA_DIR / "exhibitors.json", default_exh)
            all_ex.append(new_ex)
            save_json(DATA_DIR / "exhibitors.json", all_ex)

        st.markdown("#### 🖼️ Update Exhibitor Logo")
        try:
            ex_names = [r.get("name", "") for r in exhibitors]
        except Exception:
            ex_names = []
        target_ex = st.selectbox("Select exhibitor", options=ex_names, key="ex_sel_one")
        up_ex_logo = st.file_uploader("Upload new logo", type=["jpg","jpeg","png","webp"], key="ex_logo_replace")
        if up_ex_logo is not None and target_ex:
            (AS_LOGOS / up_ex_logo.name).write_bytes(up_ex_logo.read())
            path = (AS_LOGOS / up_ex_logo.name).as_posix()
            for rec in exhibitors:
                if rec.get("name") == target_ex:
                    rec["logo"] = path
                    break
            save_json(DATA_DIR / "exhibitors.json", exhibitors)

    with colB:
        st.markdown("#### 📥 Bulk Import Exhibitors (CSV/XLSX)")
        replace_ex = st.checkbox("Replace existing list (otherwise merge by Name)", key="ex_rep")
        up_ex = st.file_uploader("Upload file", type=["csv","xlsx"], key="ex_bulk")
        if up_ex is not None:
            import pandas as pd
            try:
                if up_ex.name.lower().endswith(".csv"):
                    df = pd.read_csv(up_ex)
                else:
                    df = pd.read_excel(up_ex)
                df.columns = [str(c).strip().lower() for c in df.columns]
                rows = []
                for _, r in df.iterrows():
                    rows.append({
                        "name": str(r.get("name", "")).strip(),
                        "stand": str(r.get("stand", "")).strip(),
                        "url": str(r.get("url", "")).strip(),
                        "logo": str(r.get("logo", "")).strip() if not pd.isna(r.get("logo", "")) else "",
                    })
                if replace_ex:
                    save_json(DATA_DIR / "exhibitors.json", rows)
                else:
                    existing = load_json(DATA_DIR / "exhibitors.json", default_exh)
                    by_name = {rec.get("name", ""): rec for rec in existing}
                    for rec in rows:
                        nm = rec.get("name", "")
                        if nm in by_name:
                            by_name[nm].update({k: v for k, v in rec.items() if v})
                        else:
                            by_name[nm] = rec
                    merged = list(by_name.values())
                    save_json(DATA_DIR / "exhibitors.json", merged)
            except Exception as e:
                st.warning(f"Import failed: {e}")

        st.markdown("#### 🔗 Bulk Link Uploaded Logos")
        st.caption("Match uploaded image filenames to exhibitor names (slug-based)")
        up_ex_many = st.file_uploader("Upload logos", type=["jpg","jpeg","png","webp"], accept_multiple_files=True, key="ex_logo_bulk")
        if up_ex_many:
            import re
            def slug(s: str) -> str:
                s = re.sub(r"[^a-z0-9]+", "-", str(s).strip().lower())
                return re.sub(r"-+", "-", s).strip("-") or "file"
            saved = {}
            for f in up_ex_many:
                (AS_LOGOS / f.name).write_bytes(f.read())
                base = f.name.rsplit(".", 1)[0]
                saved[slug(base)] = (AS_LOGOS / f.name).as_posix()
            current = load_json(DATA_DIR / "exhibitors.json", default_exh)
            updated = 0
            for rec in current:
                nm = rec.get("name", "")
                key = slug(nm)
                if key in saved:
                    rec["logo"] = saved[key]
                    updated += 1
            save_json(DATA_DIR / "exhibitors.json", current)
            st.success(f"Linked logos to {updated} exhibitor(s)")

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

        st.markdown("---")
        c1, c2 = st.columns(2)

        # Single sponsor add for selected tier
        with c1:
            st.markdown("#### ➕ Add Sponsor to Tier")
            with st.form(f"add_sponsor_form_{tier}", clear_on_submit=True):
                sp_name = st.text_input("Name*")
                sp_logo = st.file_uploader("Logo (JPG/JPEG/PNG/WebP)", type=["jpg","jpeg","png","webp"], key=f"sp_logo_one_{tier}")
                submitted_sp_add = st.form_submit_button("Add Sponsor")
            if submitted_sp_add:
                logo_path = ""
                if sp_logo is not None:
                    (AS_LOGOS / sp_logo.name).write_bytes(sp_logo.read())
                    logo_path = (AS_LOGOS / sp_logo.name).as_posix()
                rec = {"name": sp_name.strip(), "logo": logo_path}
                current = load_json(DATA_DIR / "sponsors.json", default_sponsors)
                tier_list = current.get(tier, [])
                tier_list.append(rec)
                current[tier] = tier_list
                save_json(DATA_DIR / "sponsors.json", current)

            st.markdown("#### 🖼️ Update Sponsor Logo")
            names = [r.get("name", "") for r in sponsors.get(tier, [])]
            target_sp = st.selectbox("Select sponsor", options=names, key=f"sp_sel_one_{tier}")
            up_sp_logo = st.file_uploader("Upload new logo", type=["jpg","jpeg","png","webp"], key=f"sp_logo_replace_{tier}")
            if up_sp_logo is not None and target_sp:
                (AS_LOGOS / up_sp_logo.name).write_bytes(up_sp_logo.read())
                path = (AS_LOGOS / up_sp_logo.name).as_posix()
                for rec in sponsors.get(tier, []):
                    if rec.get("name") == target_sp:
                        rec["logo"] = path
                        break
                save_json(DATA_DIR / "sponsors.json", sponsors)

        # Bulk import and bulk link for selected tier
        with c2:
            st.markdown("#### 📥 Bulk Import Sponsors (CSV/XLSX)")
            replace_sp = st.checkbox("Replace existing list (tier) — else merge by Name", key=f"sp_rep_{tier}")
            up_sp = st.file_uploader("Upload file", type=["csv","xlsx"], key=f"sp_bulk_{tier}")
            if up_sp is not None:
                import pandas as pd
                try:
                    if up_sp.name.lower().endswith(".csv"):
                        df = pd.read_csv(up_sp)
                    else:
                        df = pd.read_excel(up_sp)
                    df.columns = [str(c).strip().lower() for c in df.columns]
                    rows = []
                    for _, r in df.iterrows():
                        rows.append({
                            "name": str(r.get("name", "")).strip(),
                            "logo": str(r.get("logo", "")).strip(),
                        })
                    current = load_json(DATA_DIR / "sponsors.json", default_sponsors)
                    if replace_sp:
                        current[tier] = rows
                    else:
                        by_name = {rec.get("name", ""): rec for rec in current.get(tier, [])}
                        for rec in rows:
                            nm = rec.get("name", "")
                            if nm in by_name:
                                by_name[nm].update({k: v for k, v in rec.items() if v})
                            else:
                                by_name[nm] = rec
                        current[tier] = list(by_name.values())
                    save_json(DATA_DIR / "sponsors.json", current)
                except Exception as e:
                    st.warning(f"Import failed: {e}")

            st.markdown("#### 🔗 Bulk Link Uploaded Logos (Tier)")
            st.caption("Match uploaded image filenames to sponsor names in this tier")
            up_sp_many = st.file_uploader("Upload logos", type=["jpg","jpeg","png","webp"], accept_multiple_files=True, key=f"sp_logo_bulk_{tier}")
            if up_sp_many:
                import re
                def slug(s: str) -> str:
                    s = re.sub(r"[^a-z0-9]+", "-", str(s).strip().lower())
                    return re.sub(r"-+", "-", s).strip("-") or "file"
                saved = {}
                for f in up_sp_many:
                    (AS_LOGOS / f.name).write_bytes(f.read())
                    base = f.name.rsplit(".", 1)[0]
                    saved[slug(base)] = (AS_LOGOS / f.name).as_posix()
                current = load_json(DATA_DIR / "sponsors.json", default_sponsors)
                updated = 0
                for rec in current.get(tier, []):
                    nm = rec.get("name", "")
                    key = slug(nm)
                    if key in saved:
                        rec["logo"] = saved[key]
                        updated += 1
                save_json(DATA_DIR / "sponsors.json", current)
                st.success(f"Linked logos to {updated} sponsor(s) in {tier}")

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
