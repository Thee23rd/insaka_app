# staff_service.py
from __future__ import annotations
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Tuple, List
import pandas as pd
import datetime as dt

DATA_DIR = Path("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)
STAFF_CSV = DATA_DIR / "complimentary_passes.csv"

COLUMNS = [
    "Nationality", "ID", "Name", "Category", "Organization", "RoleTitle",
    "Email", "Phone", "BadgePhoto", "Notes", "CheckedIn", "Day1_CheckIn", "Day2_CheckIn", "Day3_CheckIn", "Day4_CheckIn", "Day5_CheckIn", "CreatedAt"
]

def _ensure_schema(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for c in COLUMNS:
        if c not in df.columns:
            if c == "CheckedIn":
                df[c] = False
            else:
                df[c] = ""
    # types
    df["CheckedIn"] = df["CheckedIn"].astype(bool)
    # ID numeric or string ok; keep as str for safety
    df["ID"] = df["ID"].astype(str)
    
    # Fix phone numbers: convert floats to integers, remove .0 suffix, preserve country codes
    if "Phone" in df.columns:
        def format_phone(val):
            if pd.isna(val) or val == "" or val == "nan":
                return ""
            try:
                val_str = str(val).strip()
                # If it starts with +, preserve the country code
                if val_str.startswith("+"):
                    return val_str
                # Otherwise, try to remove .0 suffix by converting to int
                num_val = float(val)
                if num_val == num_val:  # Check if not NaN
                    return str(int(num_val))
                return ""
            except (ValueError, TypeError):
                return str(val).strip()
        df["Phone"] = df["Phone"].apply(format_phone)
    
    return df[COLUMNS]

def load_staff_df() -> pd.DataFrame:
    if STAFF_CSV.exists():
        df = pd.read_csv(STAFF_CSV)
    else:
        df = pd.DataFrame(columns=COLUMNS)
    return _ensure_schema(df)

def save_staff_df(df: pd.DataFrame) -> None:
    df = _ensure_schema(df)
    df.to_csv(STAFF_CSV, index=False)

# --- keep your imports and constants as-is ---

def _norm_str(s: pd.Series) -> pd.Series:
    return s.astype(str).str.strip().str.lower()

def _dedupe_key(name: str, org: str) -> str:
    return f"{(name or '').strip().lower()}|{(org or '').strip().lower()}"

def _next_id(df: pd.DataFrame) -> str:
    """
    Generate the next unique ID as a string.
    IDs are numeric and incremented from the max existing ID, or start at 1.
    """
    if df.empty or "ID" not in df.columns:
        return "1"
    try:
        ids = pd.to_numeric(df["ID"], errors="coerce")
        max_id = ids[~ids.isna()].max()
        if pd.isna(max_id):
            return "1"
        return str(int(max_id) + 1)
    except Exception:
        return str(len(df) + 1)

def register_staff(
    name: str,
    category: str,
    organization: str,
    role_title: str = "",
    email: str = "",
    phone: str = "",
    badge_photo_path: str = "",
    notes: str = "",
    nationality: str = ""
) -> tuple[bool, str]:
    if not name.strip():
        return False, "Name is required."
    if not category.strip():
        return False, "Category is required."

    df = load_staff_df()

    # Build vectorized key column (no apply)
    if len(df):
        df_keys = _norm_str(df["Name"]) + "|" + _norm_str(df["Organization"])
        key = _dedupe_key(name, organization)
        if (df_keys == key).any():
            return False, "This person already exists for that organization."

    # Next ID
    new_id = _next_id(df)

    row = {
        "ID": new_id,
        "Name": name.strip(),
        "Category": category.strip(),
        "Organization": (organization or "").strip(),
        "RoleTitle": (role_title or "").strip(),
        "Email": (email or "").strip(),
        "Phone": (phone or "").strip(),
        "BadgePhoto": (badge_photo_path or ""),
        "Notes": (notes or "").strip(),
        "Nationality": (nationality or "").strip(),
        "CheckedIn": False,
        "CreatedAt": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    save_staff_df(df)
    return True, f"Saved: {new_id}"


def set_checked_in(ids: List[str], checked: bool = True) -> Tuple[int, int]:
    """Mark a list of IDs as checked-in/out. Returns (updated, not_found)."""
    df = load_staff_df()
    updated = 0
    not_found = 0
    for i in ids:
        mask = df["ID"].astype(str) == str(i)
        if not mask.any():
            not_found += 1
            continue
        df.loc[mask, "CheckedIn"] = bool(checked)
        updated += 1
    if updated:
        save_staff_df(df)
    return updated, not_found

def set_daily_checkin(delegate_id: str, day: int, checked: bool = True) -> Tuple[bool, str]:
    """Mark a delegate as checked in for a specific day. Day: 1, 2, 3, 4, or 5."""
    if day not in [1, 2, 3, 4, 5]:
        return False, "Invalid day. Must be 1, 2, 3, 4, or 5."
    
    df = load_staff_df()
    mask = df["ID"].astype(str) == str(delegate_id)
    
    if not mask.any():
        return False, "Delegate not found."
    
    day_column = f"Day{day}_CheckIn"
    df.loc[mask, day_column] = bool(checked)
    save_staff_df(df)
    
    return True, f"Check-in updated for Day {day}"

def get_daily_checkin_status(delegate_id: str) -> dict:
    """Get check-in status for all days for a delegate."""
    df = load_staff_df()
    mask = df["ID"].astype(str) == str(delegate_id)
    
    if not mask.any():
        return {"error": "Delegate not found"}
    
    delegate = df[mask].iloc[0]
    return {
        "Day1": bool(delegate.get("Day1_CheckIn", False)),
        "Day2": bool(delegate.get("Day2_CheckIn", False)),
        "Day3": bool(delegate.get("Day3_CheckIn", False)),
        "Day4": bool(delegate.get("Day4_CheckIn", False)),
        "Day5": bool(delegate.get("Day5_CheckIn", False))
    }

def import_staff_excel(file_bytes: bytes) -> tuple[int, int]:
    incoming = pd.read_excel(BytesIO(file_bytes))
    incoming.columns = [c.strip() for c in incoming.columns]
    
    # Map new format columns to existing schema
    column_mapping = {
        "Full Name": "Name",
        "Attendee Type": "Category", 
        "Title": "RoleTitle",
        "Role": "RoleTitle",
        "Role Title": "RoleTitle"
    }
    incoming = incoming.rename(columns=column_mapping)

    # Ensure columns exist
    for c in ["Name","Category","Organization","RoleTitle","Email","Phone","Notes","Nationality"]:
        if c not in incoming.columns:
            incoming[c] = ""

    # Keep valid rows
    incoming["Name"] = incoming["Name"].astype(str)
    incoming = incoming[incoming["Name"].str.strip() != ""].copy()

    # Build keys vectorized
    incoming["__key__"] = _norm_str(incoming["Name"]) + "|" + _norm_str(incoming["Organization"])

    # Internal dedupe within the file
    incoming = incoming.drop_duplicates(subset="__key__", keep="first")

    existing = load_staff_df()
    if len(existing):
        existing_keys = (_norm_str(existing["Name"]) + "|" + _norm_str(existing["Organization"])).tolist()
    else:
        existing_keys = []

    to_add = incoming[~incoming["__key__"].isin(existing_keys)].copy()
    skipped = int(len(incoming) - len(to_add))

    if to_add.empty:
        return 0, skipped

    # Assign IDs & defaults
    out_rows = []
    df_cur = existing.copy()
    for _, r in to_add.iterrows():
        nid = _next_id(df_cur)
        out_rows.append({
            "ID": nid,
            "Name": str(r.get("Name","")).strip(),
            "Category": str(r.get("Category","")).strip(),
            "Organization": str(r.get("Organization","")).strip(),
            "RoleTitle": str(r.get("RoleTitle","")).strip(),
            "Email": str(r.get("Email","")).strip(),
            "Phone": str(r.get("Phone","")).strip(),
            "BadgePhoto": "",
            "Notes": str(r.get("Notes","")).strip(),
            "Nationality": str(r.get("Nationality","")).strip(),
            "CheckedIn": False,
            "CreatedAt": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
        df_cur = pd.concat([df_cur, pd.DataFrame([out_rows[-1]])], ignore_index=True)

    final = pd.concat([existing, pd.DataFrame(out_rows)], ignore_index=True)
    save_staff_df(final)
    return len(out_rows), skipped


def export_staff_excel() -> Tuple[bytes, str]:
    df = load_staff_df()
    out = BytesIO()
    with pd.ExcelWriter(out, engine="openpyxl") as w:
        df.to_excel(w, sheet_name="Complimentary Passes", index=False)
        # quick pivots
        by_cat = df.groupby("Category", dropna=False).agg(Count=("ID","count")).reset_index()
        by_org = df.groupby("Organization", dropna=False).agg(Count=("ID","count")).reset_index()
        by_nationality = df.groupby("Nationality", dropna=False).agg(Count=("ID","count")).reset_index()
        by_cat.to_excel(w, sheet_name="By Category", index=False)
        by_org.to_excel(w, sheet_name="By Organization", index=False)
        by_nationality.to_excel(w, sheet_name="By Nationality", index=False)
    out.seek(0)
    fname = f"complimentary_passes_{dt.datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    return out.read(), fname
