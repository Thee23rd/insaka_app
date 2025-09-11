# backend.py
import os
from functools import lru_cache
from supabase import create_client, Client

URL  = os.environ.get("SUPABASE_URL")
ANON = os.environ.get("SUPABASE_ANON_KEY")

@lru_cache(maxsize=1)
def _client() -> Client:
    return create_client(URL, ANON)

def get_speakers():
    return _client().table("speakers").select("*").order("name").execute().data

def get_sessions():
    return _client().table("sessions").select("*").order("start_time").execute().data

def get_exhibitors():
    return _client().table("exhibitors").select("*").order("name").execute().data

def get_sponsors():
    # Higher tiers first
    tier_order = {"Platinum":1,"Gold":2,"Silver":3,"Bronze":4}
    rows = _client().table("sponsors").select("*").execute().data
    return sorted(rows, key=lambda r: tier_order.get(r.get("tier","Bronze"), 99))

def get_materials():
    return _client().table("materials").select("*").order("created_at", desc=True).execute().data

def get_venue():
    rows = _client().table("venues").select("*").limit(1).execute().data
    return rows[0] if rows else None
