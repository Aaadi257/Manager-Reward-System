from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
try:
    from .models import ManagerInput, ScoreCard
    from .scoring import calculate_score
except ImportError:
    from models import ManagerInput, ScoreCard
    from scoring import calculate_score
import json
import os


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Backend is running"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "submissions.json"

def load_submissions():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_submission(score_card: ScoreCard):
    submissions = load_submissions()
    submissions.append(score_card.dict())
    with open(DB_FILE, "w") as f:
        json.dump(submissions, f, indent=2)

@app.post("/api/calculate-score", response_model=ScoreCard)
def calculate_and_save_score(data: ManagerInput):
    try:
        result = calculate_score(data)
        save_submission(result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/leaderboard")
def get_leaderboard():
    submissions = load_submissions()
    # Sort by total_score descending
    sorted_submissions = sorted(submissions, key=lambda x: x['total_score'], reverse=True)
    return sorted_submissions
