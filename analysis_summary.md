# Food Delivery Delay & Rating Analysis

## Data Cleaning
- Raw rows: 450,000
- Cleaned rows: 449,999
- Duplicate order IDs removed: 1
- Sparse columns removed: cancelled_time, reassignment_method, reassignment_reason, reassigned_order
- Time columns parsed to datetime and numeric columns coerced to numeric types

## Core Findings
- Completed orders analyzed: 444,782
- Cancelled orders: 5,217
- Average delivery duration: 32.46 minutes
- Median delivery duration: 29.32 minutes
- Share of completed orders delivered after 30 minutes: 47.56%
- Correlation between delivery duration and total distance: 0.0834
- Correlation between delivery duration and last-mile distance: 0.0852

## Important Note
- The source file does not contain a rating column, so the analysis focuses on delivery delay, distance, cancellations, and rider throughput.