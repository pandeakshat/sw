import streamlit as st
import pandas as pd
import sqlite3
from datetime import date

# --- Auth ---
USERNAME = st.secrets["admin"]["username"]
PASSWORD = st.secrets["admin"]["password"]

# --- DB ---
DB_PATH = "status_window.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

# --- Login ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username == USERNAME and password == PASSWORD:
                st.session_state["password_correct"] = True
                st.success("Login successful!")
            else:
                st.error("Incorrect username or password")
        st.stop()

check_password()

st.title("Admin Panel - Status Window")

# --- Table Selection ---
tables = {
    "Campaigns": "campaigns",
    "Projects": "projects",
    "Skills": "skills",
    "Status Effects": "status_effects",
    "Experience Log": "experience_log",
    "Attributes Log": "attributes_log"
}

selected_table = st.sidebar.selectbox("Select Table to Manage", list(tables.keys()))
table_name = tables[selected_table]

conn = get_connection()
df = pd.read_sql_query(f'SELECT rowid, * FROM "{table_name}"', conn)
conn.close()

st.subheader(f"Editing Table: {selected_table}")
st.dataframe(df)

# --- CRUD Operations ---
action = st.radio("Choose Action", ["Add Row", "Update Row", "Delete Row"])

if action == "Add Row":
    st.subheader("Add New Record")
    new_data = {}
    for col in df.columns:
        if col == "rowid":
            continue
        if "date" in col.lower():
            value = st.date_input(f"{col}", key=f"new_{col}")
            value = value.isoformat()
        else:
            value = st.text_input(f"{col}", key=f"new_{col}")
        new_data[col] = value
    if st.button("Insert Record"):
        conn = get_connection()
        placeholders = ','.join(['?'] * len(new_data))
        cols = ','.join([f'"{col}"' for col in new_data.keys()])
        conn.execute(f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})", list(new_data.values()))
        conn.commit()
        conn.close()
        st.success("Record inserted successfully!")
        st.rerun()

elif action == "Update Row":
    st.subheader("Update Existing Record")
    row_id = st.number_input("Row ID", min_value=1, step=1)
    selected = df[df["rowid"] == row_id]
    if not selected.empty:
        updated = {}
        for col in df.columns:
            if col == "rowid":
                continue
            default = str(selected[col].values[0])
            if "date" in col.lower():
                default_date = pd.to_datetime(default).date() if default else date.today()
                updated[col] = st.date_input(f"{col}", value=default_date, key=f"upd_{col}").isoformat()
            else:
                updated[col] = st.text_input(f"{col}", value=default, key=f"upd_{col}")
        if st.button("Update Record"):
            set_clause = ', '.join([f'"{col}" = ?' for col in updated])
            values = list(updated.values()) + [row_id]
            conn = get_connection()
            conn.execute(f"UPDATE {table_name} SET {set_clause} WHERE rowid = ?", values)
            conn.commit()
            conn.close()
            st.success("Record updated successfully!")
            st.rerun()
    else:
        st.warning("Row ID not found.")

elif action == "Delete Row":
    st.subheader("Delete Record")
    row_id = st.number_input("Row ID", min_value=1, step=1)
    if st.button("Delete Record"):
        conn = get_connection()
        conn.execute(f"DELETE FROM {table_name} WHERE rowid = ?", (row_id,))
        conn.commit()
        conn.close()
        st.success("Record deleted successfully!")
        st.rerun()