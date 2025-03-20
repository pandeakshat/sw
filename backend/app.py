from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import json

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4321"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants
class Constants:
    name = 'Akshat Pande'
    weight = 77.15
    height = 180
    bmi = 25.1
    bfat = 24.7
    age = 29

c = Constants()

# ----- Attribute Calculations (unchanged) -----
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
    metric = row["Metric"]
    value = row["Value"]
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
    return row["Value"] * row["Weightage"]

def calculate_resilience(row, constants):
    metric = row["Metric"]
    value = row["Value"]
    baseline = row["Baseline"]
    age_adjustment = (constants.age - 25) * 0.01
    if metric == "Stress Recovery Time (Minutes)":
        return (baseline / value) * (1 - age_adjustment) if value > 0 else 0
    return (value / baseline) * (1 - age_adjustment) if baseline > 0 else 0

def calculate_creativity(row):
    return row["Value"] * row["Weightage"]

def calculate_luck(row):
    return row["Value"]

# ----- Calculate Total Score -----
def calculate_total_score(file_path, attribute, constants):
    df = pd.read_csv(file_path)
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    df["Baseline"] = pd.to_numeric(df.get("Baseline", None), errors="coerce")
    df["Weightage"] = pd.to_numeric(df.get("Weightage", None), errors="coerce")

    if attribute == "Strength":
        df["Score"] = df.apply(calculate_strength, axis=1, constants=constants)
    elif attribute == "Intelligence":
        df["Score"] = df.apply(calculate_intelligence, axis=1)
    elif attribute == "Resilience":
        df["Score"] = df.apply(calculate_resilience, axis=1, constants=constants)
    elif attribute == "Creativity":
        df["Score"] = df.apply(calculate_creativity, axis=1)
    elif attribute == "Luck":
        df["Score"] = df.apply(calculate_luck, axis=1)
    else:
        return 0, {"error": f"Stat not found"}

    breakdown = df[["Metric", "Score"]].set_index("Metric").to_dict()["Score"]
    return df["Score"].sum(), breakdown

# Attribute lookups
attributes = {
    "strength": "data/attributes/strength.csv",
    "intelligence": "data/attributes/intelligence.csv",
    "resilience": "data/attributes/resilience.csv",
    "creativity": "data/attributes/creativity.csv",
    "luck": "data/attributes/luck.csv",
}

class Stat(BaseModel):
    name: str
    value: float
    breakdown: dict

def load_json(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")

@app.get("/projects")
async def get_projects():
    return load_json("data/projects.json")

@app.get("/skills")
async def get_skills():
    return load_json("data/skills.json")

@app.get("/status-effects")
async def get_status_effects():
    return load_json("data/status_effects.json")

@app.get("/campaigns")
async def get_campaigns():
    return load_json("data/campaigns.json")

@app.get("/")  # Add this route
def read_root():
    return {"message": "Backend is running!"}

@app.get("/stats/{stat_name}", response_model=Stat)
async def get_stat(stat_name: str):
    file_path = attributes.get(stat_name.lower())
    if not file_path:
        return Stat(name=stat_name, value=0, breakdown={"error": "Stat not found"})
    total_score, breakdown = calculate_total_score(file_path, stat_name.capitalize(), c)
    return Stat(name=stat_name, value=round(total_score, 3), breakdown=breakdown)

# ----- Experience Calculation Endpoint -----
@app.get("/experience")
async def get_experience():
    df = pd.read_csv("data/experience_log.csv")

    total_exp = int(df["experience"].sum())  # ensures pure Python int

    def exp_for_level(lvl):
        return 100 * (lvl - 1)

    level = 1
    while total_exp >= exp_for_level(level + 1):
        level += 1

    current_exp = exp_for_level(level)
    next_exp = exp_for_level(level + 1)
    progress = float(round(((total_exp - current_exp) / (next_exp - current_exp)) * 100, 2))

    # Example: you want the sum of some columns? Just cast them to Python int:
    # attributes_sum_np = df[["some_column"]].sum()
    # attributes_sum = {k: int(v) for k, v in attributes_sum_np.items()}

    return {
        "current_level": level,
        "current_experience": total_exp,
        "current_level_exp": current_exp,
        "next_level_exp": next_exp,
        "progress_percentage": progress
    }
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)