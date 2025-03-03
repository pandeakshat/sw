from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pydantic import BaseModel

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4321"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants class (unchanged)
class Constants:
    name = 'Akshat Pande'
    weight = 77.15
    height = 180
    bmi = 25.1
    bfat = 24.7
    age = 29

c = Constants()

# Attribute-specific formulas (unchanged)
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
    metric = row['Metric']
    value = row['Value']
    baseline = baselines.get(metric, 0)
    height_adjustment = (constants.height - 175) * 0.001
    age_adjustment = (constants.age - 25) * 0.01
    bf_adjustment = (1 - (constants.bfat / 100)) * 0.1
    if metric == "Resting Heart Rate":
        return (baseline / value) * (1 - bf_adjustment) if value > 0 else 0
    return (value / baseline) * (1 + height_adjustment) * (1 - age_adjustment) * (1 + bf_adjustment) if baseline > 0 else 0

def calculate_intelligence(row):
    return row['Value'] * row['Weightage']

def calculate_resilience(row, constants):
    metric = row['Metric']
    value = row['Value']
    baselines = {
        "Running Distance (Km)": 3,
        "Plank Time (Seconds)": 90,
        "Mental Focus Duration": 25,
        "Stress Recovery Time": 10,
        "Sleep Quality (Score)": 100,
        "Step Counts (Weekly Avg)": 56000,
    }
    baseline = baselines.get(metric, 0)
    if baseline == 0:
        return 0
    age_adjustment = (constants.age - 25) * 0.01
    if metric == "Stress Recovery Time":
        return (baseline / value) * (1 - age_adjustment) if value > 0 else 0
    return (value / baseline) * (1 - age_adjustment) if baseline > 0 else 0

def calculate_creativity(row):
    return row['Value'] * row['Weightage']

def calculate_luck(row):
    return row['Value']

# Calculate total score (unchanged)
def calculate_total_score(file_path, attribute, constants):
    try:
        df = pd.read_csv(file_path)
        df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
        df['Baseline'] = pd.to_numeric(df.get('Baseline', None), errors='coerce')
        df['Weightage'] = pd.to_numeric(df.get('Weightage', None), errors='coerce')

        if attribute == "Strength":
            df['Score'] = df.apply(calculate_strength, axis=1, constants=constants)
        elif attribute == "Intelligence":
            df['Score'] = df.apply(calculate_intelligence, axis=1)
        elif attribute == "Resilience":
            df['Score'] = df.apply(calculate_resilience, axis=1, constants=constants)
        elif attribute == "Creativity":
            df['Score'] = df.apply(calculate_creativity, axis=1)
        elif attribute == "Luck":
            df['Score'] = df.apply(calculate_luck, axis=1)
        else:
            return 0, {"error": f"Stat not found"}

        breakdown = df[['Metric', 'Score']].set_index('Metric').to_dict()['Score']
        return df['Score'].sum(), breakdown
    except FileNotFoundError:
        return 0, {"error": f"File not found at {file_path}"}

# Attribute files (unchanged)
attributes = {
    "strength": "data/attributes/strength.csv",
    "intelligence": "data/attributes/intelligence.csv",
    "resilience": "data/attributes/resilience.csv",
    "creativity": "data/attributes/creativity.csv",
    "luck": "data/attributes/luck.csv"
}

# Stat model (unchanged)
class Stat(BaseModel):
    name: str
    value: float
    breakdown: dict

@app.get("/stats/{stat_name}", response_model=Stat)
async def get_stat(stat_name: str):
    file_path = attributes.get(stat_name.lower())
    if not file_path:
        return Stat(name=stat_name, value=0, breakdown={"error": "Stat not found"})
    total_score, breakdown = calculate_total_score(file_path, stat_name.capitalize(), c)
    return Stat(name=stat_name, value=round(total_score, 3), breakdown=breakdown)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)