from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
import sqlite3

app = FastAPI()

# Allow frontend dev port
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4321"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Constants
class Constants:
    name = 'Akshat Pande'
    weight = 77.15
    height = 180
    bmi = 25.1
    bfat = 24.7
    age = 29

c = Constants()

# DB Connection Utility
def get_db_connection():
    return sqlite3.connect("status_window.db")

# Attribute calculation logic (same as yours)
def calculate_strength(row, constants):
    baselines = {
        "Bench Press (Kg)": constants.weight,
        "BW PullUps (Rep)": 10,
        "BW PushUps (Rep)": 20,
        "Barbell Curl (Kg)": 0.5 * constants.weight,
        "Shoulder Press (Kg)": 0.6 * constants.weight,
        "BW Dips (Rep)": 10,
        "Squats (Kg)": 1.5 * constants.weight,
        "Grip Strength": 50,
        "Leg Press": 2 * constants.weight,
        "Dead Lift": 1.8 * constants.weight,
        "Resting Heart Rate": 60,
        "BW Plank": 120,
    }
    metric = row["metric"]
    value = row["value"]
    baseline = baselines.get(metric, 0)
    height_adjustment = (constants.height - 175) * 0.001
    age_adjustment = (constants.age - 25) * 0.01
    bf_adjustment = (1 - (constants.bfat / 100)) * 0.1
    if metric == "Resting Heart Rate":
        return (baseline / value) * (1 - bf_adjustment) if value > 0 else 0
    return (
        (value / baseline)
        * (1 + height_adjustment)
        * (1 - age_adjustment)
        * (1 + bf_adjustment)
        if baseline > 0
        else 0
    )

def calculate_intelligence(row):
    return row["value"] * row.get("weightage", 1)

def calculate_resilience(row, constants):
    value = row["value"]
    baseline = row.get("baseline", 1)
    age_adjustment = (constants.age - 25) * 0.01
    if row["metric"] == "Stress Recovery Time (Minutes)":
        return (baseline / value) * (1 - age_adjustment) if value > 0 else 0
    return (value / baseline) * (1 - age_adjustment) if baseline > 0 else 0

def calculate_creativity(row):
    return row["value"] * row.get("weightage", 1)

def calculate_luck(row):
    return row["value"]

# Fetch and calculate from DB
def calculate_total_score(attribute, constants):
    conn = get_db_connection()
    df = pd.read_sql_query(
        f"SELECT * FROM attributes_log WHERE attribute = ?",
        conn,
        params=(attribute.lower(),)
    )
    conn.close()

    if df.empty:
        return 0, {"error": "No data found"}

    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["baseline"] = pd.to_numeric(df.get("baseline", None), errors="coerce")
    df["weightage"] = pd.to_numeric(df.get("weightage", None), errors="coerce")

    if attribute.lower() == "strength":
        df["score"] = df.apply(calculate_strength, axis=1, constants=constants)
    elif attribute.lower() == "intelligence":
        df["score"] = df.apply(calculate_intelligence, axis=1)
    elif attribute.lower() == "resilience":
        df["score"] = df.apply(calculate_resilience, axis=1, constants=constants)
    elif attribute.lower() == "creativity":
        df["score"] = df.apply(calculate_creativity, axis=1)
    elif attribute.lower() == "luck":
        df["score"] = df.apply(calculate_luck, axis=1)
    else:
        return 0, {"error": "Invalid attribute"}

    breakdown = df[["metric", "score"]].set_index("metric").to_dict()["score"]
    return df["score"].sum(), breakdown

# Pydantic model
class Stat(BaseModel):
    name: str
    value: float
    breakdown: dict

# Endpoints
@app.get("/")
def root():
    return {"message": "Status Window API is running!"}

@app.get("/stats/{stat_name}", response_model=Stat)
def get_stat(stat_name: str):
    total, breakdown = calculate_total_score(stat_name, c)
    return Stat(name=stat_name.capitalize(), value=round(total, 2), breakdown=breakdown)

@app.get("/experience")
def get_experience():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM experience_log", conn)
    conn.close()

    total_exp = int(df["experience"].sum())

    def exp_for_level(lvl):
        return 100 * (lvl - 1)

    level = 1
    while total_exp >= exp_for_level(level + 1):
        level += 1

    current_exp = exp_for_level(level)
    next_exp = exp_for_level(level + 1)
    progress = float(round(((total_exp - current_exp) / (next_exp - current_exp)) * 100, 2))

    return {
        "current_level": level,
        "current_experience": total_exp,
        "current_level_exp": current_exp,
        "next_level_exp": next_exp,
        "progress_percentage": progress
    }

@app.get("/projects")
def get_projects():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM projects", conn)
    conn.close()
    return df.to_dict(orient="records")

@app.get("/skills")
def get_skills():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM skills", conn)
    conn.close()
    return df.to_dict(orient="records")

@app.get("/status-effects")
def get_status_effects():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM status_effects", conn)
    conn.close()
    return df.to_dict(orient="records")

@app.get("/campaigns")
def get_campaigns():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM campaigns", conn)
    conn.close()
    return df.to_dict(orient="records")

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
