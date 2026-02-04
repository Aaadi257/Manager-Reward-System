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
  month TEXT,
  total_score FLOAT,
  breakdown JSONB,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
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
def save_score(score: ScoreCard, month: str | None = None):
    """
    Saves a score to the leaderboard (PostgreSQL).
    """
    try:
        cur.execute(
            """
            INSERT INTO scores (manager_name, mall_name, month, total_score, breakdown)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                score.manager_name,
                score.mall_name,
                month,
                score.total_score,
                [b.dict() for b in score.breakdown]  # ✅ breakdown only
            )
        )

        score_id = cur.fetchone()[0]
        conn.commit()

        return {
            "message": "Score saved successfully",
            "id": score_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.delete("/api/score/{score_id}")
def delete_score(score_id: int):
    cur.execute("DELETE FROM scores WHERE id = %s", (score_id,))
    conn.commit()
    return {"message": "Score removed"}

# ✅ READ LEADERBOARD FROM DATABASE
@app.get("/api/leaderboard")
def get_leaderboard(month: str | None = None):
    if month:
        cur.execute(
            """
            SELECT id, manager_name, mall_name, month, total_score, breakdown
            FROM scores
            WHERE month = %s
            ORDER BY total_score DESC
            """,
            (month,)
        )
    else:
        cur.execute(
            """
            SELECT id, manager_name, mall_name, month, total_score, breakdown
            FROM scores
            ORDER BY total_score DESC
            """
        )

    rows = cur.fetchall()

    return [
        {
            "id": r[0],
            "manager_name": r[1],
            "mall_name": r[2],
            "month": r[3],
            "total_score": r[4],
            "breakdown": r[5]
        }
        for r in rows
    ]