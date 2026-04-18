# 🍽️ Food Delivery Delay and Rating Analysis

This project analyzes rider-level food delivery operations data to understand delivery delays, distance effects, cancellations, and throughput trends.

## 📌 Overview

The repository contains a Python analysis pipeline and a Jupyter notebook for exploratory work.

Primary workflow:
1. Read raw rider/order data from `Rider-Info.csv`.
2. Clean and transform time and numeric fields.
3. Engineer operational features (duration, stage times, distance bands, delay categories).
4. Save a cleaned dataset, analysis summary, and visualizations.

## ⚠️ Important Scope Note

The current dataset does **not** include a customer rating column.

Because of that, the implemented analysis focuses on:
- ⏱️ Delivery duration and delay behavior
- 📍 Distance vs duration relationship
- ❌ Cancellation patterns
- 🚴 Rider/order throughput indicators

## 🗂️ Repository Structure

- 🐍 `food_delivery_analysis.py`: Main reproducible analysis script
- 📓 `food_delivery_analysis.ipynb`: Notebook version for interactive exploration
- 📥 `Rider-Info.csv`: Raw input dataset
- 🧹 `food_delivery.csv`: Cleaned output dataset (generated/updated by script)
- 📝 `analysis_summary.md`: Auto-generated summary report
- 🖼️ `outputs/`: Generated charts

## 🧠 Data Processing and Feature Engineering

The script performs the following key steps:
- Parses datetime columns (`order_time`, `allot_time`, `accept_time`, `pickup_time`, `delivered_time`, etc.)
- Coerces numeric fields to numeric dtypes
- Removes duplicate rows by `order_id`
- Drops sparse columns:
  - `cancelled_time`
  - `reassignment_method`
  - `reassignment_reason`
  - `reassigned_order`
- Creates derived metrics:
  - `delivery_duration_min`
  - `allot_to_accept_min`
  - `accept_to_pickup_min`
  - `pickup_to_delivery_min`
  - `total_distance_km`
  - `order_hour`, `order_dayofweek`
  - `delay_category` (`On-Time`, `Late`, `Cancelled`)
  - Duration and distance bands
  - Outlier flag for very long durations

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

Running the script creates the following figures in `outputs/`:
- 📈 `delivery_duration_distribution.png`
- 🎯 `distance_vs_duration.png`
- 🕐 `duration_by_hour.png`
- 🧩 `status_mix.png`

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

- Add SLA-based delay thresholds by city/time window
- Segment performance by rider cohorts and workload bands
- Incorporate weather/traffic context if available
- Add rating analysis once a rating-enabled dataset is provided
