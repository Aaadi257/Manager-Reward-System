from pydantic import BaseModel, Field
from typing import List

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

class ManagerInput(BaseModel):
    manager_name: str
    mall_name: str
    amritsari_express: OutletMetrics
    cafe_chennai: OutletMetrics

class ScoreBreakdown(BaseModel):
    metric_name: str
    score: float
    max_score: float
    details: str

class ScoreCard(BaseModel):
    manager_name: str
    mall_name: str
    total_score: float
    breakdown: List[ScoreBreakdown]
