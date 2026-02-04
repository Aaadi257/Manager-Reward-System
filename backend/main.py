from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

try:
    from .models import ManagerInput, ScoreCard
    from .scoring import calculate_score
except ImportError:
    from models import ManagerInput, ScoreCard
    from scoring import calculate_score

from db import get_conn

app = FastAPI()

# ------------------ CORS ------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ DB SETUP ------------------
conn = get_conn()
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS scores (
  id SERIAL PRIMARY KEY,
  manager_name TEXT,
  mall_name TEXT,
  total_score FLOAT,
  breakdown JSONB
)
""")
conn.commit()

# ------------------ ROUTES ------------------

@app.get("/")
def root():
    return {"message": "Backend is running"}

# ✅ SAVE SCORE TO DATABASE
@app.post("/api/calculate-score", response_model=ScoreCard)
def calculate_score_only(data: ManagerInput):
    """
    Calculates the score but DOES NOT save it.
    """
    result = calculate_score(data)
    return result
@app.post("/api/save-score")
def save_score(score: ScoreCard):
    """
    Saves a score to the leaderboard (PostgreSQL).
    """
    try:
        cur.execute(
            """
            INSERT INTO scores (manager_name, mall_name, total_score, breakdown)
            VALUES (%s, %s, %s, %s)
            """,
            (
                score.manager_name,
                score.mall_name,
                score.total_score,
                score.dict()
            )
        )
        conn.commit()
        return {"message": "Score saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.delete("/api/score/{score_id}")
def delete_score(score_id: int):
    cur.execute("DELETE FROM scores WHERE id = %s", (score_id,))
    conn.commit()
    return {"message": "Score removed"}

# ✅ READ LEADERBOARD FROM DATABASE
@app.get("/api/leaderboard")
def get_leaderboard():
    cur.execute("""
        SELECT manager_name, mall_name, total_score, breakdown
        FROM scores
        ORDER BY total_score DESC
    """)
    rows = cur.fetchall()

    return [
        {
            "manager_name": r[0],
            "mall_name": r[1],
            "total_score": r[2],
            "breakdown": r[3]
        }
        for r in rows
    ]