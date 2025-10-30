# def fetch_live_coupons(store_name):
#     """Return dummy coupon data for testing instead of live API."""
#     store_name = store_name.lower()
#     coupons = []
#
#     if store_name == "amazon":
#         coupons = [
#             {"code": "AMZ10", "discount_percent": 10, "title": "Flat 10% off on Amazon orders", "min_amount": 500},
#             {"code": "SAVE20", "discount_percent": 20, "title": "Big Deal 20% off on orders above ₹1000",
#              "min_amount": 1000},
#             {"code": "FIRSTBUY", "discount_percent": 15, "title": "15% off for first-time buyers", "min_amount": 0},
#         ]
#     elif store_name == "flipkart":
#         coupons = [
#             {"code": "FK5", "discount_percent": 5, "title": "5% off sitewide", "min_amount": 200},
#             {"code": "SUPER15", "discount_percent": 15, "title": "15% off on electronics", "min_amount": 500},
#         ]
#     else:
#         coupons = [
#             {"code": "GEN10", "discount_percent": 10, "title": "Flat 10% off all stores", "min_amount": 300},
#         ]
#
#     return coupons


def fetch_live_coupons(store):
    """Return dummy coupons for a given store (mock data)."""
    coupons = [
        {"code": "AMZ10", "discount_percent": 10, "min_amount": 500, "store": "Amazon"},
        {"code": "AMZ15", "discount_percent": 20, "min_amount": 2000, "store": "Amazon"},
        {"code": "FLIP5", "discount_percent": 5, "min_amount": 300, "store": "Flipkart"},
        {"code": "FLIP15", "discount_percent": 15, "min_amount": 1500, "store": "Flipkart"},
        {"code": "MYN25", "discount_percent": 25, "min_amount": 1000, "store": "Myntra"},
    ]
    # Return only coupons relevant to the store
    return [c for c in coupons if c["store"].lower() == store.lower()]
