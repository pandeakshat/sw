import pandas as pd
import sqlite3
import json

# Create connection
conn = sqlite3.connect("status_window.db")

# JSON to SQL
with open("data/campaigns.json", "r") as f:
    campaigns = pd.json_normalize(json.load(f))
campaigns.to_sql("campaigns", conn, if_exists="replace", index=False)

with open("data/projects.json", "r") as f:
    projects = pd.json_normalize(json.load(f))
projects.to_sql("projects", conn, if_exists="replace", index=False)

with open("data/skills.json", "r") as f:
    skills = pd.json_normalize(json.load(f))
skills.to_sql("skills", conn, if_exists="replace", index=False)

with open("data/status_effects.json", "r") as f:
    effects = pd.json_normalize(json.load(f))
effects.to_sql("status_effects", conn, if_exists="replace", index=False)

# CSVs
pd.read_csv("data/experience_log.csv").to_sql("experience_log", conn, if_exists="replace", index=False)

csv_files = {
    "strength": "data/attributes/strength.csv",
    "intelligence": "data/attributes/intelligence.csv",
    "resilience": "data/attributes/resilience.csv",
    "creativity": "data/attributes/creativity.csv",
    "luck": "data/attributes/luck.csv"
}

# Standardize and combine
all_entries = []

for attr, file in csv_files.items():
    df = pd.read_csv(file)
    df['attribute'] = attr
    all_entries.append(df)

# Combine into single DataFrame
combined_df = pd.concat(all_entries, ignore_index=True)

# Rename columns if needed (ensure: date, value, notes exist)
combined_df.columns = [col.lower().strip() for col in combined_df.columns]
if 'value' not in combined_df.columns:
    combined_df['value'] = combined_df.iloc[:, 1]  # Fallback to 2nd column

# Save to SQL
combined_df.to_sql("attributes_log", conn, if_exists="replace", index=False)

conn.close()
