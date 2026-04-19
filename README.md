# 🍽️ Food Delivery Delay and Rating Analysis

This project analyzes food delivery operations and customer experience data to understand delay behavior, ratings impact, refund patterns, and actionable service improvements.

## 📌 Overview

The repository contains a Python analysis pipeline and a Jupyter notebook for exploratory work.

Primary workflow:
1. Read raw order data from `Ecommerce_Delivery_Analytics_New.csv`.
2. Clean and transform time and numeric fields.
3. Engineer operational features (order hour, delay categories, duration bands).
4. Save a cleaned dataset, analysis summary, and visualizations.

The current implementation also includes:
- 📈 Time-based analysis (orders per hour, average delay per hour)
- 🛒 Product category analysis (highest-delay and lowest-rated categories)
- 💰 Order value vs rating analysis
- 🔁 Refund deep-dive (refund vs rating, refund vs delay)
- 🤖 Baseline ML model to predict rating from delivery duration

## 🗃️ Dataset Details

- **Dataset name:** E-Commerce Analytics (Swiggy, Zomato, Blinkit)
- **Source:** Kaggle
- **Kaggle link:** https://www.kaggle.com/datasets/logiccraftbyhimanshi/e-commerce-analytics-swiggy-zomato-blinkit
- **Local file used in this project:** `Ecommerce_Delivery_Analytics_New.csv`
- **Note:** Please follow Kaggle dataset licensing/usage terms when redistributing data.

## 🗂️ Repository Structure

```text
Food_Delivery_Delay_and_Rating_Analysis/
├── Ecommerce_Delivery_Analytics_New.csv
├── README.md
├── analysis_summary.md
├── food_delivery.csv
├── food_delivery_analysis.ipynb
├── food_delivery_analysis.py
├── netlify.toml
├── outputs/
│   ├── avg_delay_per_5min_bucket.png
│   ├── avg_delay_per_hour.png
│   ├── category_avg_delay.png
│   ├── category_avg_rating.png
│   ├── correlation_heatmap.png
│   ├── delay_category_vs_rating_boxplot.png
│   ├── delivery_duration_distribution.png
│   ├── delivery_duration_vs_rating_scatter.png
│   ├── order_value_vs_rating.png
│   ├── orders_per_5min_bucket.png
│   ├── orders_per_hour.png
│   ├── rating_distribution.png
│   └── refund_rate_by_duration_band.png
└── templates/
    ├── analysis.html
    ├── index.html
    └── style.css
```

## 🧠 Data Processing and Feature Engineering

The script performs the following key steps:
- Standardizes source columns to snake_case
- Coerces numeric fields (`delivery_duration_min`, `order_value_inr`, `rating`)
- Removes duplicate rows by `order_id`
- Engineers features:
  - `order_minute_of_day`, `order_hour`
  - `delay_category` (`On-Time`, `Late`)
  - `duration_band`, `rating_band`
- Computes KPI blocks for delay, rating, refund, and category performance
- Trains a baseline `LinearRegression` model for rating prediction

## 📊 Current Headline Findings

From the latest generated summary (`analysis_summary.md`):
- 📦 Raw rows: 450,000
- ✅ Cleaned rows: 449,999
- 🚚 Completed orders analyzed: 444,782
- ❌ Cancelled orders: 5,217
- ⏱️ Average delivery duration: 32.46 minutes
- 📉 Median delivery duration: 29.32 minutes
- 🕒 Completed orders delivered after 30 minutes: 47.56%
- 🔗 Correlation (duration vs total distance): 0.0834
- 🔗 Correlation (duration vs last-mile distance): 0.0852

These values can change when the source data changes.

## 🖼️ Generated Visualizations

Running the script creates figures in `outputs/`, including:
- 📈 `delivery_duration_distribution.png`
- ⭐ `rating_distribution.png`
- 📉 `delivery_duration_vs_rating_scatter.png`
- ⏰ `orders_per_hour.png`
- ⏰ `avg_delay_per_hour.png`
- 🛒 `category_avg_delay.png`
- 🛒 `category_avg_rating.png`
- 💰 `order_value_vs_rating.png`
- 🔁 `refund_rate_by_duration_band.png`
- 🧠 `correlation_heatmap.png`

## 🚀 Setup and Run

### 1) 🛠️ Create and activate a virtual environment (PowerShell)

```powershell
python -m venv .venv
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& .\.venv\Scripts\Activate.ps1)
```

### 2) 📦 Install dependencies

```powershell
pip install -r requirements.txt
```

### 3) ▶️ Run the analysis pipeline

```powershell
python .\food_delivery_analysis.py
```

After completion, you should see:
- ✅ Updated `food_delivery.csv`
- ✅ Updated `analysis_summary.md`
- ✅ Refreshed plot images in `outputs/`

## 🔁 Reproducibility Notes

- The script uses deterministic random sampling (`random_state=42`) for plotting large scatter data.
- Matplotlib is configured with a non-interactive backend (`Agg`) so plots can be generated in non-GUI environments.

## 💡 Possible Next Enhancements

- Add SLA-based alerting by platform-hour-category segment
- Add classification model for refund risk prediction
- Incorporate weather/traffic context if available
- Build an interactive dashboard (Streamlit/Power BI) using generated outputs
