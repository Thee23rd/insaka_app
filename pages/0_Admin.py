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

st.header("Complimentary Passes (Organizers / Services / VIP)")
tab_new, tab_manage, tab_import, tab_export = st.tabs(
    ["➕ Add", "🗂 Manage", "⬆️ Import", "⬇️ Export"]
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
        use_container_width=True,
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
        use_container_width=True,
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
        use_container_width=True,
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
            use_container_width=True,
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
