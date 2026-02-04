from pydantic import BaseModel
from typing import List, Optional


# ---------------------------
# Outlet-level input metrics
# ---------------------------
class OutletMetrics(BaseModel):
    name: str
    google_rating: float
    zomato_rating: float
    swiggy_rating: float
    food_cost_percentage: float
    online_activity_percentage_zomato: float
    online_activity_percentage_swiggy: float
    kitchen_prep_time_zomato: float
    kitchen_prep_time_swiggy: float
    bad_order_percentage: float
    delay_order_percentage: float
    outlet_audit_mistakes: int
    total_sale: float
    add_on_sale: float


# ---------------------------
# Main input from frontend
# ---------------------------
class ManagerInput(BaseModel):
    manager_name: str
    mall_name: str
    month: Optional[str] = None   # ✅ month selector (e.g. "2026-02")
    amritsari_express: OutletMetrics
    cafe_chennai: OutletMetrics


# ---------------------------
# Score breakdown per metric
# ---------------------------
class ScoreBreakdown(BaseModel):
    metric_name: str
    score: float
    max_score: float
    details: str


# ---------------------------
# Final scorecard output
# ---------------------------
class ScoreCard(BaseModel):
    manager_name: str
    mall_name: str
    total_score: float
    breakdown: List[ScoreBreakdown]