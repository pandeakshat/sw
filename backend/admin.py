import streamlit as st
import pandas as pd
import json
import os
from datetime import date

USERNAME = st.secrets["admin"]["username"]
PASSWORD = st.secrets["admin"]["password"]

def check_password():
    """Simple authentication using session state."""
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

st.title("Admin Panel")
st.write("Manage your CSV and JSON data files below.")

# -------- File Type Selection --------
data_type = st.sidebar.selectbox("Select File Type", ["CSV", "JSON", "Experience Log"])

# -------- CSV CRUD Operations --------
if data_type == "CSV":
    csv_files = {
        "Strength": "data/attributes/strength.csv",
        "Intelligence": "data/attributes/intelligence.csv",
        "Resilience": "data/attributes/resilience.csv",
        "Luck": "data/attributes/luck.csv",
        "Creativity": "data/attributes/creativity.csv",
    }
    selected_csv = st.sidebar.selectbox("Select CSV File", list(csv_files.keys()))
    file_path = csv_files[selected_csv]

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        st.error(f"File {file_path} not found!")
        st.stop()

    st.header(f"Editing {selected_csv} CSV File")
    st.dataframe(df)

    action = st.radio("Select Action", ["Create New Row", "Update Row", "Delete Row"])

    if action == "Create New Row":
        st.subheader("Add a New Row")
        new_row = {col: st.text_input(f"Enter {col}:", key=f"new_{col}") for col in df.columns}
        if st.button("Add Row"):
            new_row_df = pd.DataFrame([new_row])
            df = pd.concat([df, new_row_df], ignore_index=True)
            df.to_csv(file_path, index=False)
            st.success("Row added successfully!")
            st.experimental_rerun()

    elif action == "Update Row":
        st.subheader("Update an Existing Row")
        row_idx = st.number_input("Enter row index to update (0-indexed)", min_value=0, max_value=len(df)-1, step=1)
        selected_row = df.iloc[row_idx].to_dict()
        updated_row = {col: st.text_input(f"Update {col}:", value=str(val), key=f"update_{col}") for col, val in selected_row.items()}
        if st.button("Update Row"):
            for col in df.columns:
                df.at[row_idx, col] = updated_row[col]
            df.to_csv(file_path, index=False)
            st.success("Row updated successfully!")
            st.experimental_rerun()

    elif action == "Delete Row":
        st.subheader("Delete a Row")
        row_idx = st.number_input("Enter row index to delete (0-indexed)", min_value=0, max_value=len(df)-1, step=1)
        if st.button("Delete Row"):
            df = df.drop(df.index[row_idx])
            df.to_csv(file_path, index=False)
            st.success("Row deleted successfully!")
            st.experimental_rerun()

# -------- JSON CRUD Operations --------
elif data_type == "JSON":
    json_files = {
        "Campaigns": "data/campaigns.json",
        "Projects": "data/projects.json",
        "Skills": "data/skills.json",
        "Status Effects": "data/status_effects.json",
    }
    selected_json = st.sidebar.selectbox("Select JSON File", list(json_files.keys()))
    file_path = json_files[selected_json]

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
    else:
        st.error(f"File {file_path} not found!")
        st.stop()

    st.header(f"Editing {selected_json} JSON File")
    st.json(data)

    action = st.radio("Select Action", ["Create New Record", "Update Record", "Delete Record"])

    if action == "Create New Record":
        st.subheader("Add a New Record")
        keys = list(data[0].keys()) if data and isinstance(data, list) else st.text_input("Enter comma-separated keys for the new record").split(",")
        new_record = {key: st.text_input(f"Enter value for {key.strip()}:", key=f"new_{key}") for key in keys}
        if st.button("Add Record"):
            data.append(new_record)
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)
            st.success("Record added successfully!")
            st.experimental_rerun()

# -------- Experience Log (Simplified) --------
elif data_type == "Experience Log":
    file_path = "data/experience_log.csv"

    # Ensure the 4-column structure
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        df = pd.DataFrame(columns=["date", "category", "description", "experience"])

    st.header("Experience Log")
    st.dataframe(df)

    # CRUD actions for Experience Log
    exp_action = st.radio("Select Action", ["Create Entry", "Update Entry", "Delete Entry"])

    if exp_action == "Create Entry":
        st.subheader("Add a new Experience Log")
        new_date = st.date_input("Date", date.today())
        new_category = st.text_input("Category", "code")
        new_description = st.text_input("Description", "Short detail")
        new_experience = st.number_input("Experience", min_value=1, value=5)
        
        if st.button("Add Experience"):
            row_data = {
                "date": [new_date.isoformat()],
                "category": [new_category],
                "description": [new_description],
                "experience": [new_experience],
            }
            new_df = pd.DataFrame(row_data)
            df = pd.concat([df, new_df], ignore_index=True)
            df.to_csv(file_path, index=False)
            st.success("Logged new experience!")
            st.experimental_rerun()

    elif exp_action == "Update Entry":
        st.subheader("Update an existing experience record")
        if len(df) == 0:
            st.warning("No records found to update.")
        else:
            row_idx = st.number_input("Row index to update (0-indexed)", min_value=0, max_value=len(df)-1, step=1)
            selected_row = df.iloc[row_idx]

            updated_date = st.date_input("Date", pd.to_datetime(selected_row["date"]).date())
            updated_category = st.text_input("Category", selected_row["category"])
            updated_description = st.text_input("Description", selected_row["description"])
            updated_experience = st.number_input("Experience", min_value=1, value=int(selected_row["experience"]))

            if st.button("Save Updates"):
                df.at[row_idx, "date"] = updated_date.isoformat()
                df.at[row_idx, "category"] = updated_category
                df.at[row_idx, "description"] = updated_description
                df.at[row_idx, "experience"] = updated_experience
                df.to_csv(file_path, index=False)
                st.success("Experience entry updated!")
                st.experimental_rerun()

    elif exp_action == "Delete Entry":
        st.subheader("Delete an existing experience record")
        if len(df) == 0:
            st.warning("No records found to delete.")
        else:
            row_idx = st.number_input("Row index to delete (0-indexed)", min_value=0, max_value=len(df)-1, step=1)
            if st.button("Delete"):
                df = df.drop(df.index[row_idx])
                df.to_csv(file_path, index=False)
                st.success("Experience entry deleted!")
