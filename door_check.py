# door_check.py (optional page)
import streamlit as st
from staff_service import load_staff_df, set_checked_in

st.title("Complimentary Pass Check-in")
q = st.text_input("Search name/org")
df = load_staff_df()
if q.strip():
    qq = q.lower().strip()
    df = df[
        df["Name"].str.lower().str.contains(qq, na=False) |
        df["Organization"].str.lower().str.contains(qq, na=False)
    ]
st.dataframe(df, width='stretch', height=420)

picked = st.multiselect("Select IDs to mark checked-in", options=df["ID"].tolist())
if st.button("Check-in Selected"):
    upd, nf = set_checked_in(picked, True)
    st.success(f"Checked-in {upd}; Not found {nf}")
