from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

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

# ------------------------------------------------
# 1️⃣ CALCULATE SCORE (NO SAVE)
# ------------------------------------------------
@app.post("/api/calculate-score", response_model=ScoreCard)
def calculate_score_only(data: ManagerInput):
    """
    Calculates score but does NOT save it.
    """
    result = calculate_score(data)

    # ensure month flows into scorecard
    result.month = data.month

    return result

# ------------------------------------------------
# 2️⃣ SAVE SCORE (EXPLICIT ACTION)
# ------------------------------------------------
@app.post("/api/save-score")
def save_score(score: ScoreCard):
    """
    Saves a score to PostgreSQL leaderboard.
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
                score.month,                     # ✅ month saved here
                score.total_score,
                [b.dict() for b in score.breakdown]  # ✅ list[dict]
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

# ------------------------------------------------
# 3️⃣ DELETE SCORE
# ------------------------------------------------
@app.delete("/api/score/{score_id}")
def delete_score(score_id: int):
    cur.execute("DELETE FROM scores WHERE id = %s", (score_id,))
    conn.commit()
    return {"message": "Score removed"}

# ------------------------------------------------
# 4️⃣ LEADERBOARD (MONTH FILTER)
# ------------------------------------------------
@app.get("/api/leaderboard")
def get_leaderboard(month: Optional[str] = Query(None)):
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
        # Testing / All months
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
@app.get("/api/manager-of-the-month")
def manager_of_the_month(month: str):
    """
    Returns the top manager for a given month.
    """
    cur.execute(
        """
        SELECT id, manager_name, mall_name, total_score
        FROM scores
        WHERE month = %s
        ORDER BY total_score DESC
        LIMIT 1
        """,
        (month,)
    )

    row = cur.fetchone()

    if not row:
        return None

    return {
        "id": row[0],
        "manager_name": row[1],
        "mall_name": row[2],
        "total_score": row[3]
    }