# Food Delivery Delay and Rating Analysis – Project Report

## Abstract

This project analyzes food delivery operations and customer experience data from major e-commerce platforms (Swiggy, Zomato, Blinkit) to understand delay patterns, rating impacts, refund behaviors, and identify actionable service improvements. The analysis processes 100,000 order records to extract operational insights and predict customer satisfaction metrics based on delivery performance metrics.

## Technologies Used

- **Programming Language:** Python 3.x
- **Data Processing & Analysis:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn
- **Machine Learning:** Scikit-learn (LinearRegression)
- **Notebook Environment:** Jupyter Notebook
- **Web Dashboard:** HTML, CSS, JavaScript
- **Data Format:** CSV
- **Version Control:** Git

## Methodology / Working

### Data Pipeline Overview
1. **Data Ingestion:** Load raw order data from `Ecommerce_Delivery_Analytics_New.csv` (100,000 records)
2. **Data Cleaning & Transformation:**
   - Standardize column names to snake_case format
   - Convert key fields to numeric types
   - Derive delay categories (Late: >30 min delivery time)
   - Handle missing values and validate data integrity
3. **Feature Engineering:**
   - Extract order hour from timestamp
   - Create delay categories and duration bands
   - Generate platform and product category aggregations
4. **Analysis Modules:**
   - **Time-based Analysis:** Orders per hour, average delay trends, 5-minute bucket analysis
   - **Category Analysis:** Delay and rating patterns across product categories
   - **Order Value Impact:** Correlation between order value and customer ratings
   - **Refund Deep-Dive:** Analyze refund patterns vs delivery performance
   - **ML Modeling:** Baseline LinearRegression model to predict rating from delivery duration
5. **Output Generation:** Generate visualizations, cleaned datasets, and analysis summary reports

## Outcomes / Results

### Key Performance Findings
- **Average Delivery Duration:** 29.54 minutes
- **Average Service Rating:** 3.24 / 5.0
- **Late Order Share:** 46.16% (orders exceeding 30 min)
- **Rating Distribution:** Minimal correlation between delivery duration and rating (0.0001)

### Platform Performance
- **Platform with Highest Delivery Time:** JioMart (29.63 min average)

### Category Insights
- **Highest Delay Category:** Grocery (29.58 min)
- **Lowest Rated Category:** Grocery (3.22 rating)

### Refund Patterns
- **Average Rating (Refund Requested):** 1.67
- **Average Rating (No Refund):** 4.57
- **Refund Rate - Late Orders:** 45.94%
- **Refund Rate - On-Time Orders:** 45.71%
- Strong inverse correlation between refund requests and customer satisfaction

### Order Value vs Rating
- **Correlation:** -0.0027 (weak negative)
- **Best Rated Segment:** Order value range $481–$770 (3.25 rating)

### ML Model Performance
- **Model Type:** LinearRegression
- **Test MAE:** 1.4842
- **Test R²:** -0.0001
- **Insight:** Delivery duration alone is insufficient to predict ratings; other factors dominate satisfaction

### Deliverables
- 10+ visualizations (delay trends, category analysis, correlation heatmaps, scatter plots)
- Cleaned dataset for downstream analysis
- Comprehensive analysis summary with metrics
- Interactive web dashboard (HTML/CSS)

## Conclusion / Future Scope

### Key Learnings
1. **Delivery Duration vs Satisfaction:** Surprisingly weak correlation suggests customer satisfaction is driven by factors beyond speed (quality, food freshness, communication, etc.)
2. **Refund as Satisfaction Indicator:** Refund requests are a strong proxy for customer dissatisfaction and should be prioritized in service improvements
3. **Categorical Variability:** Grocery orders show higher delays—likely due to inventory availability or larger order complexity
4. **Data Limitations:** Lack of distance, prep time, delivery partner ID, and city fields limits deeper operational insights

### Future Scope & Improvements
1. **Enhanced Feature Engineering:**
   - Incorporate distance and delivery partner metrics
   - Add prep time, wait time, and handoff time breakdowns
   - Segment analysis by city and seasonal trends

2. **Advanced ML Models:**
   - Implement tree-based models (Random Forest, XGBoost) to capture non-linear patterns
   - Use NLP to analyze customer review text for sentiment analysis
   - Develop clustering models to identify distinct customer segments

3. **Real-time Monitoring:**
   - Build live dashboards for real-time delay prediction
   - Implement alerting system for service degradation
   - Develop recommendation engine for operational adjustments

4. **Causal Analysis:**
   - Conduct A/B testing for service interventions
   - Investigate root causes of delays beyond delivery time
   - Analyze impact of communication touchpoints on ratings

5. **Operational Recommendations:**
   - Optimize routing algorithms for high-delay categories
   - Prioritize quality over speed for customer satisfaction
   - Implement proactive refund policies based on predicted satisfaction
   - Develop targeted improvement plans by platform and product category

6. **Scalability:**
   - Automate pipeline for continuous data ingestion and analysis
   - Implement cloud-based solutions for handling larger datasets
   - Develop API for third-party integration and insights sharing
