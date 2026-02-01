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
def calculate_and_save_score(data: ManagerInput):
    try:
        result = calculate_score(data)

        cur.execute(
            """
            INSERT INTO scores (manager_name, mall_name, total_score, breakdown)
            VALUES (%s, %s, %s, %s)
            """,
            (
                data.manager_name,
                data.mall_name,
                result.total_score,
                result.model_dump()  # use .dict() if pydantic v1
            )
        )
        conn.commit()

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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