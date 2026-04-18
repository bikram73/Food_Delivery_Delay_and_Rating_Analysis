from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parent
RAW_FILE = BASE_DIR / "Rider-Info.csv"
CLEAN_FILE = BASE_DIR / "food_delivery.csv"
REPORT_FILE = BASE_DIR / "analysis_summary.md"
FIGURE_DIR = BASE_DIR / "outputs"

TIME_COLUMNS = [
    "order_time",
    "order_date",
    "allot_time",
    "accept_time",
    "pickup_time",
    "delivered_time",
    "cancelled_time",
]

NUMERIC_COLUMNS = [
    "order_id",
    "rider_id",
    "first_mile_distance",
    "last_mile_distance",
    "alloted_orders",
    "delivered_orders",
    "cancelled",
    "undelivered_orders",
    "lifetime_order_count",
    "session_time",
    "reassignment_method",
    "reassignment_reason",
    "reassigned_order",
]

SPARSE_COLUMNS = [
    "cancelled_time",
    "reassignment_method",
    "reassignment_reason",
    "reassigned_order",
]


def load_data(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()

    for column in TIME_COLUMNS:
        if column in cleaned.columns:
            cleaned[column] = pd.to_datetime(cleaned[column], errors="coerce")

    for column in NUMERIC_COLUMNS:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    if "order_id" in cleaned.columns:
        cleaned = cleaned.drop_duplicates(subset=["order_id"], keep="first")

    key_columns = [column for column in ["order_id", "order_time"] if column in cleaned.columns]
    if key_columns:
        cleaned = cleaned.dropna(subset=key_columns)

    if "delivered_time" in cleaned.columns and "order_time" in cleaned.columns:
        cleaned["delivery_duration_min"] = (
            cleaned["delivered_time"] - cleaned["order_time"]
        ).dt.total_seconds() / 60

    for start_col, end_col, new_col in [
        ("allot_time", "accept_time", "allot_to_accept_min"),
        ("accept_time", "pickup_time", "accept_to_pickup_min"),
        ("pickup_time", "delivered_time", "pickup_to_delivery_min"),
    ]:
        if start_col in cleaned.columns and end_col in cleaned.columns:
            cleaned[new_col] = (cleaned[end_col] - cleaned[start_col]).dt.total_seconds() / 60

    if {"first_mile_distance", "last_mile_distance"}.issubset(cleaned.columns):
        cleaned["total_distance_km"] = cleaned["first_mile_distance"] + cleaned["last_mile_distance"]

    if "order_time" in cleaned.columns:
        cleaned["order_hour"] = cleaned["order_time"].dt.hour
        cleaned["order_dayofweek"] = cleaned["order_time"].dt.day_name()

    if "delivery_duration_min" in cleaned.columns and "cancelled" in cleaned.columns:
        cleaned["delay_category"] = np.select(
            [
                cleaned["cancelled"].fillna(0).astype(int).eq(1),
                cleaned["delivery_duration_min"].notna() & (cleaned["delivery_duration_min"] <= 30),
                cleaned["delivery_duration_min"].notna() & (cleaned["delivery_duration_min"] > 30),
            ],
            ["Cancelled", "On-Time", "Late"],
            default="Unknown",
        )
    elif "cancelled" in cleaned.columns:
        cleaned["delay_category"] = np.where(cleaned["cancelled"].fillna(0).astype(int).eq(1), "Cancelled", "Unknown")

    if "delivery_duration_min" in cleaned.columns:
        cleaned["duration_band"] = pd.cut(
            cleaned["delivery_duration_min"],
            bins=[-np.inf, 15, 30, 45, 60, np.inf],
            labels=["<=15", "15-30", "30-45", "45-60", ">60"],
            right=True,
        )

    if "total_distance_km" in cleaned.columns:
        cleaned["distance_band_km"] = pd.cut(
            cleaned["total_distance_km"],
            bins=[-np.inf, 1, 2, 3, 5, 10, np.inf],
            labels=["<=1", "1-2", "2-3", "3-5", "5-10", ">10"],
            right=True,
        )

    if "delivery_duration_min" in cleaned.columns:
        cleaned["is_outlier_duration"] = cleaned["delivery_duration_min"].gt(120)

    drop_columns = [column for column in SPARSE_COLUMNS if column in cleaned.columns]
    cleaned = cleaned.drop(columns=drop_columns)

    preferred_order = [
        "order_id",
        "rider_id",
        "order_time",
        "order_date",
        "allot_time",
        "accept_time",
        "pickup_time",
        "delivered_time",
        "cancelled",
        "delivery_duration_min",
        "allot_to_accept_min",
        "accept_to_pickup_min",
        "pickup_to_delivery_min",
        "first_mile_distance",
        "last_mile_distance",
        "total_distance_km",
        "alloted_orders",
        "delivered_orders",
        "undelivered_orders",
        "lifetime_order_count",
        "session_time",
        "order_hour",
        "order_dayofweek",
        "delay_category",
        "duration_band",
        "distance_band_km",
        "is_outlier_duration",
    ]
    existing_order = [column for column in preferred_order if column in cleaned.columns]
    remaining_columns = [column for column in cleaned.columns if column not in existing_order]
    return cleaned[existing_order + remaining_columns]


def write_summary(cleaned: pd.DataFrame, raw: pd.DataFrame, output_path: Path) -> str:
    completed_mask = cleaned.get("delay_category", pd.Series(index=cleaned.index, dtype="object")).isin(["On-Time", "Late"])
    completed = cleaned.loc[completed_mask].copy()

    lines: list[str] = []
    lines.append("# Food Delivery Delay & Rating Analysis")
    lines.append("")
    lines.append("## Data Cleaning")
    lines.append(f"- Raw rows: {len(raw):,}")
    lines.append(f"- Cleaned rows: {len(cleaned):,}")
    lines.append(f"- Duplicate order IDs removed: {int(raw['order_id'].duplicated().sum()):,}")
    lines.append("- Sparse columns removed: cancelled_time, reassignment_method, reassignment_reason, reassigned_order")
    lines.append("- Time columns parsed to datetime and numeric columns coerced to numeric types")
    lines.append("")
    lines.append("## Core Findings")
    lines.append(f"- Completed orders analyzed: {len(completed):,}")
    lines.append(f"- Cancelled orders: {int((cleaned['delay_category'] == 'Cancelled').sum()):,}")
    if not completed.empty:
        lines.append(f"- Average delivery duration: {completed['delivery_duration_min'].mean():.2f} minutes")
        lines.append(f"- Median delivery duration: {completed['delivery_duration_min'].median():.2f} minutes")
        lines.append(f"- Share of completed orders delivered after 30 minutes: {(completed['delivery_duration_min'].gt(30).mean() * 100):.2f}%")
        lines.append(f"- Correlation between delivery duration and total distance: {completed[['delivery_duration_min', 'total_distance_km']].corr().iloc[0, 1]:.4f}")
        lines.append(f"- Correlation between delivery duration and last-mile distance: {completed[['delivery_duration_min', 'last_mile_distance']].corr().iloc[0, 1]:.4f}")
    else:
        lines.append("- No completed orders were available for duration analysis")

    lines.append("")
    lines.append("## Important Note")
    lines.append("- The source file does not contain a rating column, so the analysis focuses on delivery delay, distance, cancellations, and rider throughput.")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return "\n".join(lines)


def make_plots(cleaned: pd.DataFrame) -> None:
    FIGURE_DIR.mkdir(exist_ok=True)
    sns.set_theme(style="whitegrid")

    completed = cleaned[cleaned["delay_category"].isin(["On-Time", "Late"])].copy()

    if not completed.empty:
        plt.figure(figsize=(10, 5))
        sns.histplot(completed["delivery_duration_min"], bins=50, kde=True, color="#0f766e")
        plt.title("Delivery Duration Distribution")
        plt.xlabel("Delivery Duration (minutes)")
        plt.ylabel("Orders")
        plt.tight_layout()
        plt.savefig(FIGURE_DIR / "delivery_duration_distribution.png", dpi=150)
        plt.close()

        plt.figure(figsize=(10, 5))
        sns.scatterplot(
            data=completed.sample(min(len(completed), 5000), random_state=42),
            x="total_distance_km",
            y="delivery_duration_min",
            alpha=0.35,
            color="#2563eb",
            edgecolor=None,
        )
        plt.title("Delivery Duration vs Total Distance")
        plt.xlabel("Total Distance (km)")
        plt.ylabel("Delivery Duration (minutes)")
        plt.tight_layout()
        plt.savefig(FIGURE_DIR / "distance_vs_duration.png", dpi=150)
        plt.close()

        hour_summary = (
            completed.groupby("order_hour", dropna=True)["delivery_duration_min"].mean().reset_index()
        )
        plt.figure(figsize=(10, 5))
        sns.lineplot(data=hour_summary, x="order_hour", y="delivery_duration_min", marker="o", color="#b45309")
        plt.title("Average Delivery Duration by Order Hour")
        plt.xlabel("Order Hour")
        plt.ylabel("Average Delivery Duration (minutes)")
        plt.tight_layout()
        plt.savefig(FIGURE_DIR / "duration_by_hour.png", dpi=150)
        plt.close()

    plt.figure(figsize=(8, 4))
    sns.countplot(data=cleaned, x="delay_category", order=["On-Time", "Late", "Cancelled"], palette="viridis")
    plt.title("Order Status Mix")
    plt.xlabel("Status")
    plt.ylabel("Orders")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "status_mix.png", dpi=150)
    plt.close()


def main() -> None:
    if not RAW_FILE.exists():
        raise FileNotFoundError(f"Source file not found: {RAW_FILE}")

    raw = load_data(RAW_FILE)
    cleaned = clean_data(raw)
    cleaned.to_csv(CLEAN_FILE, index=False)

    summary_text = write_summary(cleaned, raw, REPORT_FILE)
    make_plots(cleaned)

    completed = cleaned[cleaned["delay_category"].isin(["On-Time", "Late"])].copy()
    if not completed.empty:
        duration_mean = completed["delivery_duration_min"].mean()
        late_share = completed["delivery_duration_min"].gt(30).mean() * 100
        correlation = completed[["delivery_duration_min", "total_distance_km"]].corr().iloc[0, 1]
    else:
        duration_mean = float("nan")
        late_share = float("nan")
        correlation = float("nan")

    print("Cleaned file written to:", CLEAN_FILE)
    print("Report written to:", REPORT_FILE)
    print("Figures written to:", FIGURE_DIR)
    print(f"Completed orders analyzed: {len(completed):,}")
    print(f"Average delivery duration: {duration_mean:.2f} minutes")
    print(f"Late share (>30 min): {late_share:.2f}%")
    print(f"Duration vs total distance correlation: {correlation:.4f}")
    print("\nSummary preview:\n")
    print(summary_text)


if __name__ == "__main__":
    main()
