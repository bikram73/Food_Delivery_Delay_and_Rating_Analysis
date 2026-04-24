# Food Delivery Delay & Rating Analysis

## Data Cleaning
- Raw rows: 100,000
- Cleaned rows: 100,000
- Duplicate order IDs removed: 0
- Columns were standardized to snake_case and key fields were converted to numeric types
- Delay category is derived using delivery time (>30 min = Late) and Delivery Delay flag
- Validation check (key nulls): PASS
- Validation check (numeric dtypes): PASS
- Validation check (duplicate order_id after cleaning): PASS
- Validation check (order_hour in 0-23): PASS

## Core Findings
- Average delivery duration: 29.54 minutes
- Average service rating: 3.24 / 5
- Share of late orders: 46.16%
- Average rating (On-Time): 3.24
- Average rating (Late): 3.24
- Correlation between delivery duration and rating: 0.0001
- Refund rate for Late orders: 45.94%
- Refund rate for On-Time orders: 45.71%
- Platform with highest average delivery time: JioMart (29.63 min)

## Time-Based Analysis
- Peak average delay hour: 00:00 (29.54 min)
- Top 3 order volume hours: 00:00 (100000 orders)
- Note: source order time appears to be minute-second format, so hourly spread is limited
- Peak 5-minute bucket by delay: 50-54 min (29.71 min)

## Product Category Analysis
- Category with highest average delay: Grocery (29.58 min)
- Category with lowest average rating: Grocery (3.22)

## Order Value vs Rating
- Correlation between order value and rating: -0.0027
- Best rated order value segment: (481.0, 770.0] (3.25)

## Refund Analysis
- Avg rating when refund requested: 1.67
- Avg rating when no refund requested: 4.57
- Refund rate Late vs On-Time: 45.94% vs 45.71%
- Late orders have 1.00x higher refund rate than On-Time orders

## Baseline ML Model (Predict Rating)
- Model: LinearRegression (features: delivery_duration_min)
- Test MAE: 1.4842
- Test R^2: -0.0001
- Estimated rating change per +1 minute delivery time: -0.0003

## Business Recommendations
- If predicted or observed delivery exceeds 30 minutes, trigger proactive apology coupon communication
- Prioritize high-delay product categories for dispatch optimization and packaging process fixes
- Increase delivery partner availability during peak delay hours to reduce backlog
- Use refund-risk monitoring for late orders to trigger faster support intervention
- Track value-segment experience to ensure high-value customers receive consistently high service

## Data Limitations
- This dataset does not include delivery distance, restaurant prep time, delivery partner ID, or city-level location
- Order Date & Time appears to be a time-like value rather than full timestamp, limiting temporal trend depth