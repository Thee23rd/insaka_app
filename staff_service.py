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

def scan_excel_for_duplicates(file_bytes: bytes, existing_names: set, existing_emails: set) -> tuple[dict, list]:
    """
    Scan Excel file for duplicates before importing.
    Returns scan results and sheet information.
    """
    # Read all sheets from Excel file
    excel_file = BytesIO(file_bytes)
    
    # Get all sheet names
    try:
        sheet_names = pd.ExcelFile(excel_file).sheet_names
    except Exception:
        sheet_names = [0]
    
    all_delegates = []
    processed_sheets = []
    skipped_sheets = []
    
    # Process each sheet (similar to import but without saving)
    for sheet in sheet_names:
        try:
            # Skip metadata sheets
            if isinstance(sheet, str) and any(skip_word in sheet.lower() for skip_word in ['summary', 'stats', 'overview', 'total']):
                skipped_sheets.append(f"{sheet} (metadata/summary)")
                continue
                
            sheet_data = pd.read_excel(excel_file, sheet_name=sheet)
            
            if sheet_data.empty:
                skipped_sheets.append(f"{sheet} (empty)")
                continue
                
            sheet_data.columns = [c.strip() for c in sheet_data.columns]
            
            # Apply same column mapping and processing as import
            column_mapping = {
                "Full Name": "Name",
                "Attendee Type": "Category", 
                "Title": "RoleTitle",
                "Role": "RoleTitle",
                "Role Title": "RoleTitle",
                "Contact Number": "Phone",
                "Contact": "Phone",
                "Phone Number": "Phone",
                "Mobile": "Phone",
                "Mobile Number": "Phone",
                "Surname": "Last Name",
                "First Name": "First Name",
                "Email Address": "Email",
                "Email Adress": "Email",
                "Email": "Email"
            }
            sheet_data = sheet_data.rename(columns=column_mapping)
            
            # Process names (same logic as import)
            if "Name" not in sheet_data.columns:
                name_col = None
                first_name_col = None
                last_name_col = None
                
                for col in sheet_data.columns:
                    col_lower = col.lower()
                    if col_lower in ['name', 'full name', 'fullname', 'full_name', 'delegate name', 'attendee name']:
                        name_col = col
                        break
                    elif col_lower in ['first name', 'firstname', 'first_name', 'given name']:
                        first_name_col = col
                    elif col_lower in ['last name', 'lastname', 'last_name', 'surname', 'family name']:
                        last_name_col = col
                
                if name_col:
                    sheet_data["Name"] = sheet_data[name_col].astype(str).str.strip()
                elif first_name_col and last_name_col:
                    first_names = sheet_data[first_name_col].astype(str).str.strip()
                    last_names = sheet_data[last_name_col].astype(str).str.strip()
                    first_names = first_names.replace(['nan', 'None', 'null', ''], '')
                    last_names = last_names.replace(['nan', 'None', 'null', ''], '')
                    sheet_data["Name"] = (first_names + " " + last_names).str.strip()
                    sheet_data["Name"] = sheet_data["Name"].str.replace(r'\s+', ' ', regex=True)
                elif first_name_col:
                    sheet_data["Name"] = sheet_data[first_name_col].astype(str).str.strip()
                elif last_name_col:
                    sheet_data["Name"] = sheet_data[last_name_col].astype(str).str.strip()
                else:
                    for col in sheet_data.columns:
                        if col and not col.lower() in ['id', 'email', 'phone', 'contact', 'category', 'organization', 'notes']:
                            sample_data = sheet_data[col].astype(str).str.strip()
                            sample_data = sample_data.replace(['nan', 'None', 'null'], '')
                            if not sample_data.empty and len(sample_data.iloc[0]) > 2:
                                sheet_data["Name"] = sample_data
                                break
            
            # Clean up emails
            if "Email" in sheet_data.columns:
                sheet_data["Email"] = sheet_data["Email"].astype(str).str.strip().str.lower()
                sheet_data["Email"] = sheet_data["Email"].replace(['nan', 'None', 'null'], '')
            
            # Filter valid rows
            sheet_data["Name"] = sheet_data["Name"].astype(str)
            valid_rows = sheet_data[
                (sheet_data["Name"].str.strip() != "") & 
                (sheet_data["Name"].str.strip() != "nan") & 
                (sheet_data["Name"].str.strip() != "None") & 
                (sheet_data["Name"].str.strip() != "null")
            ].copy()
            
            if valid_rows.empty:
                skipped_sheets.append(f"{sheet} (no valid names found)")
                continue
            
            # Extract organization from sheet name
            sheet_name = sheet if isinstance(sheet, str) else f"Sheet_{sheet + 1}"
            clean_org_name = sheet_name.replace("_", " ").replace("-", " ").title()
            for suffix in ["Sheet", "Tab", "Data", "List"]:
                if clean_org_name.endswith(suffix):
                    clean_org_name = clean_org_name[:-len(suffix)].strip()
            
            if not clean_org_name or clean_org_name.strip() == "":
                clean_org_name = f"Organization_{sheet_name}"
            
            # Ensure columns exist
            for c in ["Name","Category","Organization","RoleTitle","Email","Phone","Notes","Nationality"]:
                if c not in valid_rows.columns:
                    valid_rows[c] = ""
            
            # Set organization
            if "Organization" not in valid_rows.columns or valid_rows["Organization"].isna().all() or (valid_rows["Organization"].str.strip() == "").all():
                valid_rows["Organization"] = clean_org_name
            else:
                mask = valid_rows["Organization"].isna() | (valid_rows["Organization"].astype(str).str.strip().isin(['nan', 'None', 'null', '']))
                valid_rows.loc[mask, "Organization"] = clean_org_name
            
            # Convert to delegate records
            for _, row in valid_rows.iterrows():
                delegate = {
                    "Name": str(row.get("Name","")).strip(),
                    "Category": str(row.get("Category","")).strip(),
                    "Organization": str(row.get("Organization","")).strip(),
                    "RoleTitle": str(row.get("RoleTitle","")).strip(),
                    "Email": str(row.get("Email","")).strip(),
                    "Phone": str(row.get("Phone","")).strip(),
                    "Notes": str(row.get("Notes","")).strip(),
                    "Nationality": str(row.get("Nationality","")).strip(),
                }
                all_delegates.append(delegate)
            
            processed_sheets.append(f"{sheet_name} ({len(valid_rows)} rows)")
            
        except Exception as e:
            skipped_sheets.append(f"{sheet} (error: {str(e)[:50]})")
            continue
    
    # Analyze for duplicates
    duplicate_names = {}
    duplicate_emails = {}
    new_delegates = []
    
    for delegate in all_delegates:
        name = delegate["Name"].lower().strip()
        email = delegate["Email"].lower().strip()
        
        # Check for name duplicates
        if name in existing_names:
            if name not in duplicate_names:
                duplicate_names[name] = 0
            duplicate_names[name] += 1
        
        # Check for email duplicates
        if email and email in existing_emails:
            if email not in duplicate_emails:
                duplicate_emails[email] = 0
            duplicate_emails[email] += 1
        
        # Check if this is a new delegate (not duplicate name or email)
        if name not in existing_names and (not email or email not in existing_emails):
            new_delegates.append(delegate)
    
    scan_results = {
        "total_found": len(all_delegates),
        "new_delegates": new_delegates,
        "duplicate_names": duplicate_names,
        "duplicate_emails": duplicate_emails,
    }
    
    sheet_info = {"processed": processed_sheets, "skipped": skipped_sheets}
    
    return scan_results, sheet_info

def import_staff_excel(file_bytes: bytes) -> tuple[int, int, list]:
    # Read all sheets from Excel file
    excel_file = BytesIO(file_bytes)
    
    # Get all sheet names
    try:
        sheet_names = pd.ExcelFile(excel_file).sheet_names
    except Exception:
        # Fallback to single sheet if there's an issue
        sheet_names = [0]
    
    all_incoming = []
    processed_sheets = []
    skipped_sheets = []
    
    # Process each sheet
    for sheet in sheet_names:
        try:
            # Skip sheets that might be metadata or summaries
            if isinstance(sheet, str) and any(skip_word in sheet.lower() for skip_word in ['summary', 'stats', 'overview', 'total']):
                skipped_sheets.append(f"{sheet} (metadata/summary)")
                continue
                
            sheet_data = pd.read_excel(excel_file, sheet_name=sheet)
            
            # Skip empty sheets
            if sheet_data.empty:
                skipped_sheets.append(f"{sheet} (empty)")
                continue
                
            sheet_data.columns = [c.strip() for c in sheet_data.columns]
            
            # Debug: Log what columns we found
            columns_found = list(sheet_data.columns)
            
            # Map new format columns to existing schema
            column_mapping = {
                "Full Name": "Name",
                "Attendee Type": "Category", 
                "Title": "RoleTitle",
                "Role": "RoleTitle",
                "Role Title": "RoleTitle",
                "Contact Number": "Phone",
                "Contact": "Phone",
                "Phone Number": "Phone",
                "Mobile": "Phone",
                "Mobile Number": "Phone",
                # Handle the specific format from the image
                "Surname": "Last Name",
                "First Name": "First Name",
                "Email Address": "Email",
                "Email Adress": "Email",  # Common typo
                "Email": "Email"
            }
            sheet_data = sheet_data.rename(columns=column_mapping)

            # Check if we already have a Name column, if not try to find/create one
            if "Name" not in sheet_data.columns:
                # Try to find name-related columns
                name_col = None
                first_name_col = None
                last_name_col = None
                
                # Look for existing name columns (case-insensitive)
                for col in sheet_data.columns:
                    col_lower = col.lower()
                    if col_lower in ['name', 'full name', 'fullname', 'full_name', 'delegate name', 'attendee name']:
                        name_col = col
                        break
                    elif col_lower in ['first name', 'firstname', 'first_name', 'given name']:
                        first_name_col = col
                    elif col_lower in ['last name', 'lastname', 'last_name', 'surname', 'family name']:
                        last_name_col = col
                
                # Use existing name column if found
                if name_col:
                    sheet_data["Name"] = sheet_data[name_col].astype(str).str.strip()
                # Combine first and last names if both exist
                elif first_name_col and last_name_col:
                    first_names = sheet_data[first_name_col].astype(str).str.strip()
                    last_names = sheet_data[last_name_col].astype(str).str.strip()
                    
                    # Handle empty or NaN values
                    first_names = first_names.replace(['nan', 'None', 'null', ''], '')
                    last_names = last_names.replace(['nan', 'None', 'null', ''], '')
                    
                    # Combine with proper spacing
                    sheet_data["Name"] = (first_names + " " + last_names).str.strip()
                    sheet_data["Name"] = sheet_data["Name"].str.replace(r'\s+', ' ', regex=True)
                # Use just first name if only that exists
                elif first_name_col:
                    sheet_data["Name"] = sheet_data[first_name_col].astype(str).str.strip()
                    sheet_data["Name"] = sheet_data["Name"].replace(['nan', 'None', 'null'], '')
                # Use just last name if only that exists
                elif last_name_col:
                    sheet_data["Name"] = sheet_data[last_name_col].astype(str).str.strip()
                    sheet_data["Name"] = sheet_data["Name"].replace(['nan', 'None', 'null'], '')
                else:
                    # No name column found - try to use first column that looks like names
                    for col in sheet_data.columns:
                        if col and not col.lower() in ['id', 'email', 'phone', 'contact', 'category', 'organization', 'notes']:
                            # Check if this column contains name-like data
                            sample_data = sheet_data[col].astype(str).str.strip()
                            sample_data = sample_data.replace(['nan', 'None', 'null'], '')
                            if not sample_data.empty and len(sample_data.iloc[0]) > 2:  # Names should be longer than 2 chars
                                sheet_data["Name"] = sample_data
                                break
            
            # Handle split name columns (First Name + Last Name/Surname)
            elif "First Name" in sheet_data.columns or "Last Name" in sheet_data.columns:
                first_name_col = None
                last_name_col = None
                
                # Find first name column (case-insensitive)
                for col in sheet_data.columns:
                    if col.lower() in ['first name', 'firstname', 'first_name', 'given name']:
                        first_name_col = col
                        break
                
                # Find last name column (case-insensitive)
                for col in sheet_data.columns:
                    if col.lower() in ['last name', 'lastname', 'last_name', 'surname', 'family name']:
                        last_name_col = col
                        break
                
                # Combine names if both columns exist
                if first_name_col and last_name_col:
                    # Clean up names and combine them
                    first_names = sheet_data[first_name_col].astype(str).str.strip()
                    last_names = sheet_data[last_name_col].astype(str).str.strip()
                    
                    # Handle empty or NaN values
                    first_names = first_names.replace(['nan', 'None', 'null', ''], '')
                    last_names = last_names.replace(['nan', 'None', 'null', ''], '')
                    
                    # Combine with proper spacing
                    sheet_data["Name"] = (first_names + " " + last_names).str.strip()
                    
                    # Clean up extra spaces
                    sheet_data["Name"] = sheet_data["Name"].str.replace(r'\s+', ' ', regex=True)
                    
                elif first_name_col:
                    sheet_data["Name"] = sheet_data[first_name_col].astype(str).str.strip()
                    sheet_data["Name"] = sheet_data["Name"].replace(['nan', 'None', 'null'], '')
                elif last_name_col:
                    sheet_data["Name"] = sheet_data[last_name_col].astype(str).str.strip()
                    sheet_data["Name"] = sheet_data["Name"].replace(['nan', 'None', 'null'], '')

            # Extract organization from sheet name if not in data
            sheet_name = sheet if isinstance(sheet, str) else f"Sheet_{sheet + 1}"
            
            # Clean sheet name to use as organization
            clean_org_name = sheet_name.replace("_", " ").replace("-", " ").title()
            # Remove common sheet suffixes
            for suffix in ["Sheet", "Tab", "Data", "List"]:
                if clean_org_name.endswith(suffix):
                    clean_org_name = clean_org_name[:-len(suffix)].strip()
            
            # Ensure we have a valid organization name
            if not clean_org_name or clean_org_name.strip() == "":
                clean_org_name = f"Organization_{sheet_name}"
            
            # Ensure columns exist - especially Name column
            for c in ["Name","Category","Organization","RoleTitle","Email","Phone","Notes","Nationality"]:
                if c not in sheet_data.columns:
                    sheet_data[c] = ""
            
            # Final fallback: if Name column is still empty, try to use any column that might contain names
            if "Name" not in sheet_data.columns or sheet_data["Name"].isna().all() or (sheet_data["Name"].str.strip() == "").all():
                for col in sheet_data.columns:
                    if col and col.lower() not in ['id', 'email', 'phone', 'contact', 'category', 'organization', 'notes', 'badgephoto', 'checkedin']:
                        sample_values = sheet_data[col].astype(str).str.strip()
                        sample_values = sample_values.replace(['nan', 'None', 'null'], '')
                        # Check if this column has meaningful data (not all empty)
                        if not sample_values.empty and not sample_values.isin(['', 'nan', 'None', 'null']).all():
                            sheet_data["Name"] = sample_values
                            break
            
            # Use sheet name as organization if Organization column is empty or doesn't exist
            if "Organization" not in sheet_data.columns:
                # No Organization column at all - use sheet name for all rows
                sheet_data["Organization"] = clean_org_name
            else:
                # Organization column exists - check if it has any valid data
                org_series = sheet_data["Organization"].astype(str).str.strip()
                has_valid_org = not org_series.isin(['nan', 'None', 'null', '']).all()
                
                if not has_valid_org:
                    # All organization values are empty/invalid - use sheet name
                    sheet_data["Organization"] = clean_org_name
                else:
                    # Some valid organizations exist - fill only empty ones with sheet name
                    mask = sheet_data["Organization"].isna() | (sheet_data["Organization"].astype(str).str.strip().isin(['nan', 'None', 'null', '']))
                    sheet_data.loc[mask, "Organization"] = clean_org_name
            
            # Clean up phone numbers (handle text-stored numbers)
            if "Phone" in sheet_data.columns:
                # Convert to string and clean up
                sheet_data["Phone"] = sheet_data["Phone"].astype(str)
                # Remove common prefixes and clean formatting
                sheet_data["Phone"] = sheet_data["Phone"].str.replace(r'^\+?260', '', regex=True)  # Remove Zambian country code if present
                sheet_data["Phone"] = sheet_data["Phone"].str.replace(r'[^\d]', '', regex=True)  # Keep only digits
                # Handle empty/NaN values
                sheet_data["Phone"] = sheet_data["Phone"].replace(['nan', 'None', 'null', ''], '')
            
            # Clean up email addresses - ensure they are properly imported
            if "Email" in sheet_data.columns:
                sheet_data["Email"] = sheet_data["Email"].astype(str).str.strip().str.lower()
                sheet_data["Email"] = sheet_data["Email"].replace(['nan', 'None', 'null'], '')
                # Remove any trailing dots or invalid characters
                sheet_data["Email"] = sheet_data["Email"].str.replace(r'\.$', '', regex=True)
            else:
                # Ensure Email column exists even if not in original data
                sheet_data["Email"] = ""

            # Keep valid rows - only require Name to be present
            sheet_data["Name"] = sheet_data["Name"].astype(str)
            
            # Debug: Check what we have for names
            name_samples = sheet_data["Name"].head(5).tolist() if len(sheet_data) > 0 else []
            
            # Filter out rows where Name is empty, None, or just whitespace
            valid_rows = sheet_data[
                (sheet_data["Name"].str.strip() != "") & 
                (sheet_data["Name"].str.strip() != "nan") & 
                (sheet_data["Name"].str.strip() != "None") & 
                (sheet_data["Name"].str.strip() != "null")
            ].copy()
            
            if valid_rows.empty:
                skipped_sheets.append(f"{sheet} (no valid names found, cols: {columns_found[:3]}, samples: {name_samples[:2]})")
                continue
            
            # Add sheet info for tracking
            valid_rows["__source_sheet__"] = sheet_name
            
            # Debug: Check organization data
            org_sample = valid_rows["Organization"].head(3).tolist() if len(valid_rows) > 0 else []
            
            all_incoming.append(valid_rows)
            processed_sheets.append(f"{sheet_name} ({len(valid_rows)} rows, org: {org_sample[0] if org_sample else 'N/A'})")
            
        except Exception as e:
            # Skip problematic sheets but continue with others
            skipped_sheets.append(f"{sheet} (error: {str(e)[:50]})")
            continue
    
    # Combine all sheets
    if not all_incoming:
        return 0, 0, {"processed": processed_sheets, "skipped": skipped_sheets}
    
    incoming = pd.concat(all_incoming, ignore_index=True)
    
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
        return 0, skipped, {"processed": processed_sheets, "skipped": skipped_sheets}

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
    return len(out_rows), skipped, {"processed": processed_sheets, "skipped": skipped_sheets}


def export_staff_excel() -> Tuple[bytes, str]:
    df = load_staff_df()
    out = BytesIO()
    
    # Load speakers data
    try:
        import json
        from pathlib import Path
        speakers_file = Path("data/speakers.json")
        if speakers_file.exists():
            with open(speakers_file, "r", encoding="utf-8") as f:
                speakers_data = json.load(f)
            
            # Convert speakers to DataFrame
            speakers_df = pd.DataFrame(speakers_data)
            # Rename columns to match delegate format
            if not speakers_df.empty:
                speakers_df = speakers_df.rename(columns={
                    'name': 'Name',
                    'position': 'RoleTitle', 
                    'organization': 'Organization',
                    'email': 'Email',
                    'phone': 'Phone',
                    'nationality': 'Nationality',
                    'photo': 'BadgePhoto'
                })
                # Add missing columns
                for col in df.columns:
                    if col not in speakers_df.columns:
                        if col == 'Category':
                            speakers_df[col] = 'Speaker'
                        elif col == 'ID':
                            speakers_df[col] = speakers_df.index + 10000  # Start speaker IDs from 10000
                        else:
                            speakers_df[col] = ''
                
                # Reorder columns to match delegates
                speakers_df = speakers_df[df.columns]
        else:
            speakers_df = pd.DataFrame()
    except Exception:
        speakers_df = pd.DataFrame()
    
    with pd.ExcelWriter(out, engine="openpyxl") as w:
        # All delegates sheet
        df.to_excel(w, sheet_name="All Delegates", index=False)
        
        # Delegates by category (separate sheets)
        categories = df['Category'].dropna().unique()
        for category in sorted(categories):
            category_df = df[df['Category'] == category].copy()
            safe_sheet_name = str(category)[:31]  # Excel sheet name limit
            category_df.to_excel(w, sheet_name=f"Delegates - {safe_sheet_name}", index=False)
        
        # Speakers sheet (if available)
        if not speakers_df.empty:
            speakers_df.to_excel(w, sheet_name="Speakers", index=False)
        
        # Statistics sheets
        by_cat = df.groupby("Category", dropna=False).agg(Count=("ID","count")).reset_index()
        by_org = df.groupby("Organization", dropna=False).agg(Count=("ID","count")).reset_index()
        by_nationality = df.groupby("Nationality", dropna=False).agg(Count=("ID","count")).reset_index()
        
        by_cat.to_excel(w, sheet_name="Stats - By Category", index=False)
        by_org.to_excel(w, sheet_name="Stats - By Organization", index=False)
        by_nationality.to_excel(w, sheet_name="Stats - By Nationality", index=False)
        
        # Summary sheet
        summary_data = {
            'Metric': ['Total Delegates', 'Total Speakers', 'Total Categories', 'Total Organizations'],
            'Count': [
                len(df),
                len(speakers_df) if not speakers_df.empty else 0,
                len(categories),
                len(df['Organization'].dropna().unique())
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(w, sheet_name="Summary", index=False)
    
    out.seek(0)
    fname = f"conference_export_{dt.datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    return out.read(), fname
