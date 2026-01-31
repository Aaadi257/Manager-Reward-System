try:
    from .models import ManagerInput, OutletMetrics, ScoreBreakdown, ScoreCard
except ImportError:
    from models import ManagerInput, OutletMetrics, ScoreBreakdown, ScoreCard
from typing import List

def calculate_google_rating_points(avg_rating: float) -> int:
    if avg_rating >= 4.0: return 10
    if avg_rating >= 3.9: return 9
    if avg_rating >= 3.8: return 8
    if avg_rating >= 3.7: return 7
    if avg_rating >= 3.6: return 6
    if avg_rating >= 3.5: return 5
    return 0

def calculate_food_cost_points(brand: str, percentage: float) -> int:
    # Amritsari Express
    if brand == "Amritsari Express":
        if percentage <= 22: return 10
        if percentage <= 23: return 9
        if percentage <= 24: return 8
        if percentage <= 25: return 7 # Prompt says 25% = 7pt AND 25% = 5pt. Assuming tiers: 25=7, 26=6, then maybe >26 logic? 
        # Re-reading prompt: 
        # 22% & below = 10pt
        # 23% = 9pt
        # 24% = 8pt
        # 25% = 7pt
        # 26% = 6pt
        # 25% = 5pt (Duplicated/Conflicting?) -> I will assume 27% or maybe a typo. 
        # Let's check Cafe Chennai logic: 18<=10, 19=9, 20=8, 21=7, 22=5, >22=0.
        # Back to Amritsari: 22<=10, 23=9, 24=8, 25=7, 26=6. 
        # Then "25% = 5pt" appears again differently? Maybe "27% = 5pt"? 
        # Or maybe the first 25 was inclusive and the second was something else.
        # Rule of thumb: Higher cost = lower points.
        # 23->9, 24->8, 25->7, 26->6. 
        # The prompt says: "25% = 5pt" AGAIN. This is likely a typo for 27%. 
        # And "Below 25% = 0pt" -> This must be "Above 2X% = 0pt" because lower is better.
        # So likely: > 26 or > 27 is 0.
        # Let's implement: 
        # <= 22: 10
        # 23: 9
        # 24: 8
        # 25: 7
        # 26: 6
        # 27: 5 (Assuming typo correction)
        # > 27: 0
        if percentage <= 26: return 6
        if percentage <= 27: return 5
        return 0

    # Cafe Chennai
    # 18% & below = 10pt
    # 19% = 9pt
    # 20% = 8pt
    # 21% = 7pt
    # 22% = 5pt
    # Below 22% = 0pt (Must mean Above 22%)
    if percentage <= 18: return 10
    if percentage <= 19: return 9
    if percentage <= 20: return 8
    if percentage <= 21: return 7
    if percentage <= 22: return 5
    return 0

def calculate_online_activity_points(avg_percentage: float) -> int:
    if avg_percentage >= 98: return 10
    if avg_percentage >= 97: return 8
    if avg_percentage >= 96: return 6
    if avg_percentage >= 95: return 4
    return 0

def calculate_kitchen_prep_points(avg_time: float) -> int:
    if avg_time < 10: return 12
    if avg_time <= 15: return 10
    if avg_time <= 16: return 9
    if avg_time <= 17: return 8
    if avg_time <= 18: return 7
    if avg_time <= 19: return 6
    if avg_time <= 20: return 5
    return 0

def calculate_bad_order_points(percentage: float) -> int:
    # 3% - 5pt
    # 5% - 4pt
    # 7% - 3pt
    # 9% - 2pt
    # 11% - 1pt
    # Below 11% - 0pt (Must mean Above)
    # Interpretation: <=3 is 5, <=5 is 4, etc.
    if percentage <= 3: return 5
    if percentage <= 5: return 4
    if percentage <= 7: return 3
    if percentage <= 9: return 2
    if percentage <= 11: return 1
    return 0

def calculate_delay_order_points(percentage: float) -> int:
    # 10% - 5pt
    # 12% - 4pt
    # 14% - 3pt
    # 16% - 2pt
    # 18% - 1pt
    # Above 18% - 0pt
    if percentage <= 10: return 5
    if percentage <= 12: return 4
    if percentage <= 14: return 3
    if percentage <= 16: return 2
    if percentage <= 18: return 1
    return 0

def calculate_outlet_audit_points(mistakes: int) -> int:
    if mistakes >= 10: return 0
    if mistakes == 9: return 2
    if mistakes == 8: return 4
    if mistakes == 7: return 6
    if mistakes == 6: return 8
    if mistakes == 5: return 10
    if mistakes == 4: return 12
    if mistakes == 3: return 14
    if mistakes == 2: return 16
    if mistakes == 1: return 18
    return 20

def calculate_addon_sale_points(percentage: float) -> float:
    if percentage >= 16: return 12 # 10 + 2 bonus
    if percentage >= 15: return 10
    if percentage >= 14: return 8
    if percentage >= 13: return 6
    if percentage >= 12: return 4
    if percentage >= 11: return 2
    return 0

def calculate_score(data: ManagerInput) -> ScoreCard:
    breakdown = []
    total_score = 0.0

    # 1. Google Rating (Avg of 2 restaurants)
    avg_google = (data.amritsari_express.google_rating + data.cafe_chennai.google_rating) / 2
    google_pts = calculate_google_rating_points(avg_google)
    breakdown.append(ScoreBreakdown(metric_name="Google Rating", score=google_pts, max_score=10, details=f"Avg: {avg_google:.2f}"))
    total_score += google_pts

    # 2. Zomato + Swiggy Rating (Avg of 4 scores)
    avg_zs = (
        data.amritsari_express.zomato_rating + data.amritsari_express.swiggy_rating +
        data.cafe_chennai.zomato_rating + data.cafe_chennai.swiggy_rating
    ) / 4
    zs_pts = calculate_google_rating_points(avg_zs) # Using same table as Google Rating per prompt logic "according to the table"
    # Wait, the prompt has a separate table for Zomato+Swiggy but the points look identical to Google Rating?
    # Google: 4+=10, 3.9=9 ...
    # Zomato+Swiggy: 4+=10, 3.9=9 ... 
    # Yes, identical table.
    breakdown.append(ScoreBreakdown(metric_name="Zomato & Swiggy Rating", score=zs_pts, max_score=10, details=f"Avg: {avg_zs:.2f}"))
    total_score += zs_pts

    # 3. Food Cost
    # Calculated separately then summed? Prompt: "Amritsari Express + Cafe Chennai= Total pt"
    fc_amritsari = calculate_food_cost_points("Amritsari Express", data.amritsari_express.food_cost_percentage)
    fc_cafe = calculate_food_cost_points("Cafe Chennai", data.cafe_chennai.food_cost_percentage)
    fc_total = fc_amritsari + fc_cafe # Max could be 10+10? Or is it averaged? 
    # Prompt: "Amritsari Express + Cafe Chennai= Total pt" implies sum.
    # Note: Logic was confusing in prompt, implemented best guess.
    breakdown.append(ScoreBreakdown(metric_name="Food Cost", score=fc_total, max_score=20, details=f"Amritsari: {fc_amritsari}, Cafe: {fc_cafe}"))
    total_score += fc_total

    # 4. Online Activity
    # Avg of 4 percentages
    avg_online = (
        data.amritsari_express.online_activity_percentage_zomato + data.amritsari_express.online_activity_percentage_swiggy +
        data.cafe_chennai.online_activity_percentage_zomato + data.cafe_chennai.online_activity_percentage_swiggy
    ) / 4
    online_pts = calculate_online_activity_points(avg_online)
    breakdown.append(ScoreBreakdown(metric_name="Online Activity", score=online_pts, max_score=10, details=f"Avg: {avg_online:.1f}%"))
    total_score += online_pts

    # 5. Kitchen Prep Time
    # Avg of 4
    avg_kpt = (
        data.amritsari_express.kitchen_prep_time_zomato + data.amritsari_express.kitchen_prep_time_swiggy +
        data.cafe_chennai.kitchen_prep_time_zomato + data.cafe_chennai.kitchen_prep_time_swiggy
    ) / 4
    kpt_pts = calculate_kitchen_prep_points(avg_kpt)
    breakdown.append(ScoreBreakdown(metric_name="Kitchen Prep Time", score=kpt_pts, max_score=12, details=f"Avg: {avg_kpt:.1f} min"))
    total_score += kpt_pts

    # 6. Bad & Delay Order %
    # Bad Order Avg of 4
    # The `bad_order_percentage` in the model is assumed to be the average for each outlet across its platforms.
    # Therefore, averaging the two outlet percentages gives the overall average of the four underlying platform percentages.
    avg_bad = (data.amritsari_express.bad_order_percentage + data.cafe_chennai.bad_order_percentage) / 2
    bad_pts = calculate_bad_order_points(avg_bad)
    
    avg_delay = (data.amritsari_express.delay_order_percentage + data.cafe_chennai.delay_order_percentage) / 2
    delay_pts = calculate_delay_order_points(avg_delay)
    
    bd_total = bad_pts + delay_pts
    breakdown.append(ScoreBreakdown(metric_name="Bad & Delay Orders", score=bd_total, max_score=10, details=f"Bad Pts: {bad_pts}, Delay Pts: {delay_pts}"))
    total_score += bd_total

    # 7. Outlet Audit Score
    # "Avg of the 2 scores will be taken"
    audit_amritsari = calculate_outlet_audit_points(data.amritsari_express.outlet_audit_mistakes)
    audit_cafe = calculate_outlet_audit_points(data.cafe_chennai.outlet_audit_mistakes)
    audit_avg = (audit_amritsari + audit_cafe) / 2
    breakdown.append(ScoreBreakdown(metric_name="Outlet Audit", score=audit_avg, max_score=20, details=f"Amritsari: {audit_amritsari}, Cafe: {audit_cafe}"))
    total_score += audit_avg

    # 8. Add on Sale
    # "Calculated for both... Then Avg of the scores of the above 2"
    def get_aos_pts(outlet: OutletMetrics):
        if outlet.total_sale == 0: return 0
        pct = (outlet.add_on_sale / outlet.total_sale) * 100
        return calculate_addon_sale_points(pct)
    
    aos_amritsari = get_aos_pts(data.amritsari_express)
    aos_cafe = get_aos_pts(data.cafe_chennai)
    aos_avg = (aos_amritsari + aos_cafe) / 2
    breakdown.append(ScoreBreakdown(metric_name="Add-on Sale", score=aos_avg, max_score=12, details=f"Amritsari: {aos_amritsari}, Cafe: {aos_cafe}"))
    total_score += aos_avg

    return ScoreCard(
        manager_name=data.manager_name,
        mall_name=data.mall_name,
        total_score=total_score,
        breakdown=breakdown
    )
