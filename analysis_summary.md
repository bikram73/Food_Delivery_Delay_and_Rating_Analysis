# Food Delivery Delay & Rating Analysis

## Data Cleaning
- Raw rows: 100,000
- Cleaned rows: 100,000
- Duplicate order IDs removed: 0
- Columns were standardized to snake_case and key fields were converted to numeric types
- Delay category is derived using delivery time (>30 min = Late) and Delivery Delay flag

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

## Business Recommendations
- Prioritize operations improvements for orders crossing 30 minutes, as late deliveries are linked with lower ratings
- Use platform and category level monitoring to target where high duration and low ratings overlap
- Trigger proactive communication and compensation flows for likely-late orders to reduce refund requests

## Data Limitations
- This dataset does not include delivery distance, restaurant prep time, delivery partner ID, or city-level location
- Order Date & Time appears to be a time-like value rather than full timestamp, limiting temporal trend depth