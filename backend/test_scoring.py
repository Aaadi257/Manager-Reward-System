from models import ManagerInput, OutletMetrics
from scoring import calculate_score

def test_scoring():
    # Construct a sample input based on the prompt's diverse cases
    input_data = ManagerInput(
        manager_name="John Doe",
        mall_name="City Mall",
        amritsari_express=OutletMetrics(
            name="Amritsari Express",
            google_rating=4.2,      # >= 4 -> 10pt
            zomato_rating=3.9,
            swiggy_rating=4.0,
            food_cost_percentage=22.0, # <= 22 -> 10pt (Amritsari)
            online_activity_percentage_zomato=99.0,
            online_activity_percentage_swiggy=97.0,
            kitchen_prep_time_zomato=9.0,
            kitchen_prep_time_swiggy=12.0,
            bad_order_percentage=2.0,  # <=3 -> 5pt
            delay_order_percentage=9.0, # <=10 -> 5pt
            outlet_audit_mistakes=0,   # 0 -> 20pt
            total_sale=10000,
            add_on_sale=1600          # 16% -> 12pt (10+2)
        ),
        cafe_chennai=OutletMetrics(
            name="Cafe Chennai",
            google_rating=3.7,      # 3.7 -> 7pt
            zomato_rating=3.5,
            swiggy_rating=3.0,      # (3.9+4.0+3.5+3.0)/4 = 3.6 -> 6pt (Zomato+Swiggy Avg)
            food_cost_percentage=18.0, # <= 18 -> 10pt (Cafe)
            online_activity_percentage_zomato=95.0,
            online_activity_percentage_swiggy=90.0,
            kitchen_prep_time_zomato=16.0,
            kitchen_prep_time_swiggy=21.0, # Avg 4: (9+12+16+21)/4 = 14.5 -> 10pt
            bad_order_percentage=4.0,  # <=5 -> 4pt
            delay_order_percentage=13.0, # <=14 -> 3pt
            outlet_audit_mistakes=5,   # 5 -> 10pt
            total_sale=20000,
            add_on_sale=2000          # 10% -> 0pt
        )
    )

    score_card = calculate_score(input_data)
    
    print(f"Total Score: {score_card.total_score}")
    for item in score_card.breakdown:
        print(f"{item.metric_name}: {item.score} / {item.max_score} ({item.details})")

if __name__ == "__main__":
    test_scoring()
