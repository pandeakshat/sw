import streamlit as st
import pandas as pd
import json
import os

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
data_type = st.sidebar.selectbox("Select File Type", ["CSV", "JSON"])

# -------- CSV CRUD Operations --------
if data_type == "CSV":
    # Define your CSV file paths and labels.
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
    
    # Choose an action
    action = st.radio("Select Action", ["Create New Row", "Update Row", "Delete Row"])
    
    if action == "Create New Row":
        st.subheader("Add a New Row")
        new_row = {}
        # Create input fields for each column
        for col in df.columns:
            new_row[col] = st.text_input(f"Enter {col}:", key=f"new_{col}")
        if st.button("Add Row"):
            # Append the new row to the DataFrame
            df = df.append(new_row, ignore_index=True)
            df.to_csv(file_path, index=False)
            st.success("Row added successfully!")
            st.experimental_rerun()
            
    elif action == "Update Row":
        st.subheader("Update an Existing Row")
        row_idx = st.number_input("Enter row index to update (0-indexed)", min_value=0, max_value=len(df)-1, step=1)
        # Preload the selected row values into inputs
        selected_row = df.iloc[row_idx].to_dict()
        updated_row = {}
        for col, val in selected_row.items():
            updated_row[col] = st.text_input(f"Update {col}:", value=str(val), key=f"update_{col}")
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
    # Define your JSON file paths and labels.
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
    
    # Choose an action for JSON file records
    action = st.radio("Select Action", ["Create New Record", "Update Record", "Delete Record"])
    
    if action == "Create New Record":
        st.subheader("Add a New Record")
        new_record = {}
        # If there's at least one record, use its keys as a template
        if data and isinstance(data, list):
            keys = list(data[0].keys())
        else:
            # Otherwise, let the admin define keys manually (comma-separated)
            keys_input = st.text_input("Enter comma-separated keys for the new record")
            keys = [k.strip() for k in keys_input.split(",") if k.strip()]
        for key in keys:
            new_record[key] = st.text_input(f"Enter value for {key}:", key=f"new_{key}")
        if st.button("Add Record"):
            data.append(new_record)
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)
            st.success("Record added successfully!")
            st.experimental_rerun()
            
    elif action == "Update Record":
        st.subheader("Update an Existing Record")
        record_index = st.number_input("Enter record index to update (0-indexed)", min_value=0, max_value=len(data)-1, step=1)
        record = data[record_index]
        updated_record = {}
        for key, val in record.items():
            updated_record[key] = st.text_input(f"Update {key}:", value=str(val), key=f"update_{key}")
        if st.button("Update Record"):
            data[record_index] = updated_record
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)
            st.success("Record updated successfully!")
            st.experimental_rerun()
            
    elif action == "Delete Record":
        st.subheader("Delete a Record")
        record_index = st.number_input("Enter record index to delete (0-indexed)", min_value=0, max_value=len(data)-1, step=1)
        if st.button("Delete Record"):
            data.pop(record_index)
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)
            st.success("Record deleted successfully!")
            st.experimental_rerun()
