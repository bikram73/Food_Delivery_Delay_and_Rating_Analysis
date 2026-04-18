from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
RAW_FILE = BASE_DIR / "Ecommerce_Delivery_Analytics_New.csv"
CLEAN_FILE = BASE_DIR / "food_delivery.csv"
REPORT_FILE = BASE_DIR / "analysis_summary.md"
FIGURE_DIR = BASE_DIR / "outputs"

COLUMN_MAP = {
    "Order ID": "order_id",
    "Customer ID": "customer_id",
    "Platform": "platform",
    "Order Date & Time": "order_time_raw",
    "Delivery Time (Minutes)": "delivery_duration_min",
    "Product Category": "product_category",
    "Order Value (INR)": "order_value_inr",
    "Customer Feedback": "customer_feedback",
    "Service Rating": "rating",
    "Delivery Delay": "delivery_delay",
    "Refund Requested": "refund_requested",
}


def load_data(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def _parse_order_time_to_minutes(series: pd.Series) -> pd.Series:
    # Source values look like MM:SS.s (for example: 19:29.5), so convert to minutes after 00:00.
    formatted = "00:" + series.astype("string").str.strip()
    td = pd.to_timedelta(formatted, errors="coerce")
    return td.dt.total_seconds() / 60


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.rename(columns=COLUMN_MAP).copy()

    if "order_id" in cleaned.columns:
        cleaned["order_id"] = cleaned["order_id"].astype("string").str.strip()
        cleaned = cleaned.drop_duplicates(subset=["order_id"], keep="first")

    for numeric_col in ["delivery_duration_min", "order_value_inr", "rating"]:
        if numeric_col in cleaned.columns:
            cleaned[numeric_col] = pd.to_numeric(cleaned[numeric_col], errors="coerce")

    if "order_time_raw" in cleaned.columns:
        cleaned["order_minute_of_day"] = _parse_order_time_to_minutes(cleaned["order_time_raw"])
        cleaned["order_hour"] = np.floor(cleaned["order_minute_of_day"] / 60).astype("Int64")

    if "delivery_delay" in cleaned.columns:
        cleaned["delivery_delay"] = cleaned["delivery_delay"].astype("string").str.strip().str.title()

    if "refund_requested" in cleaned.columns:
        cleaned["refund_requested"] = cleaned["refund_requested"].astype("string").str.strip().str.title()

    if "delivery_duration_min" in cleaned.columns:
        cleaned["delay_category"] = np.where(cleaned["delivery_duration_min"].gt(30), "Late", "On-Time")

    if {"delivery_delay", "delay_category"}.issubset(cleaned.columns):
        delayed_flag = cleaned["delivery_delay"].eq("Yes")
        cleaned["delay_category"] = np.where(delayed_flag, "Late", cleaned["delay_category"])

    if "delivery_duration_min" in cleaned.columns:
        cleaned["duration_band"] = pd.cut(
            cleaned["delivery_duration_min"],
            bins=[-np.inf, 15, 30, 45, 60, np.inf],
            labels=["<=15", "15-30", "30-45", "45-60", ">60"],
            right=True,
        )

    if "rating" in cleaned.columns:
        cleaned["rating_band"] = pd.cut(
            cleaned["rating"],
            bins=[0, 2, 3, 4, 5],
            labels=["Low (1-2)", "Mid (3)", "Good (4)", "Excellent (5)"],
            include_lowest=True,
            right=True,
        )

    required_non_null = [
        col
        for col in ["order_id", "delivery_duration_min", "rating", "platform", "product_category"]
        if col in cleaned.columns
    ]
    if required_non_null:
        cleaned = cleaned.dropna(subset=required_non_null)

    preferred_order = [
        "order_id",
        "customer_id",
        "platform",
        "product_category",
        "order_time_raw",
        "order_minute_of_day",
        "order_hour",
        "delivery_duration_min",
        "delivery_delay",
        "delay_category",
        "rating",
        "rating_band",
        "order_value_inr",
        "refund_requested",
        "duration_band",
        "customer_feedback",
    ]
    existing_order = [column for column in preferred_order if column in cleaned.columns]
    remaining_columns = [column for column in cleaned.columns if column not in existing_order]
    return cleaned[existing_order + remaining_columns]


def write_summary(cleaned: pd.DataFrame, raw: pd.DataFrame, output_path: Path) -> str:
    late_mask = cleaned.get("delay_category", pd.Series(index=cleaned.index, dtype="object")).eq("Late")

    avg_rating_late = cleaned.loc[late_mask, "rating"].mean() if "rating" in cleaned.columns else float("nan")
    avg_rating_ontime = cleaned.loc[~late_mask, "rating"].mean() if "rating" in cleaned.columns else float("nan")

    duration_rating_corr = float("nan")
    if {"delivery_duration_min", "rating"}.issubset(cleaned.columns):
        duration_rating_corr = cleaned[["delivery_duration_min", "rating"]].corr().iloc[0, 1]

    delay_refund_rate = float("nan")
    ontime_refund_rate = float("nan")
    if {"refund_requested", "delay_category"}.issubset(cleaned.columns):
        refund_yes = cleaned["refund_requested"].eq("Yes")
        delay_refund_rate = refund_yes[late_mask].mean() * 100 if late_mask.any() else float("nan")
        ontime_refund_rate = refund_yes[~late_mask].mean() * 100 if (~late_mask).any() else float("nan")

    lines: list[str] = []
    lines.append("# Food Delivery Delay & Rating Analysis")
    lines.append("")
    lines.append("## Data Cleaning")
    lines.append(f"- Raw rows: {len(raw):,}")
    lines.append(f"- Cleaned rows: {len(cleaned):,}")
    lines.append(f"- Duplicate order IDs removed: {int(raw['Order ID'].duplicated().sum()):,}")
    lines.append("- Columns were standardized to snake_case and key fields were converted to numeric types")
    lines.append("- Delay category is derived using delivery time (>30 min = Late) and Delivery Delay flag")
    lines.append("")
    lines.append("## Core Findings")
    lines.append(f"- Average delivery duration: {cleaned['delivery_duration_min'].mean():.2f} minutes")
    lines.append(f"- Average service rating: {cleaned['rating'].mean():.2f} / 5")
    lines.append(f"- Share of late orders: {(late_mask.mean() * 100):.2f}%")
    lines.append(f"- Average rating (On-Time): {avg_rating_ontime:.2f}")
    lines.append(f"- Average rating (Late): {avg_rating_late:.2f}")
    lines.append(f"- Correlation between delivery duration and rating: {duration_rating_corr:.4f}")

    if np.isfinite(delay_refund_rate) and np.isfinite(ontime_refund_rate):
        lines.append(f"- Refund rate for Late orders: {delay_refund_rate:.2f}%")
        lines.append(f"- Refund rate for On-Time orders: {ontime_refund_rate:.2f}%")

    if "platform" in cleaned.columns:
        platform_stats = (
            cleaned.groupby("platform", dropna=False)
            .agg(avg_delivery_minutes=("delivery_duration_min", "mean"), avg_rating=("rating", "mean"))
            .sort_values("avg_delivery_minutes", ascending=False)
        )
        slowest_platform = platform_stats.index[0]
        lines.append(
            f"- Platform with highest average delivery time: {slowest_platform} ({platform_stats.iloc[0]['avg_delivery_minutes']:.2f} min)"
        )

    lines.append("")
    lines.append("## Business Recommendations")
    lines.append("- Prioritize operations improvements for orders crossing 30 minutes, as late deliveries are linked with lower ratings")
    lines.append("- Use platform and category level monitoring to target where high duration and low ratings overlap")
    lines.append("- Trigger proactive communication and compensation flows for likely-late orders to reduce refund requests")
    lines.append("")
    lines.append("## Data Limitations")
    lines.append("- This dataset does not include delivery distance, restaurant prep time, delivery partner ID, or city-level location")
    lines.append("- Order Date & Time appears to be a time-like value rather than full timestamp, limiting temporal trend depth")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return "\n".join(lines)


def make_plots(cleaned: pd.DataFrame) -> None:
    try:
        import matplotlib
        import matplotlib.pyplot as plt
        import seaborn as sns
    except Exception as exc:
        print(f"Skipping plot generation because plotting libraries are unavailable: {exc}")
        return

    matplotlib.use("Agg")
    FIGURE_DIR.mkdir(exist_ok=True)
    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(8, 4))
    sns.countplot(data=cleaned, x="rating", order=sorted(cleaned["rating"].dropna().unique()), color="#2563eb")
    plt.title("Rating Distribution")
    plt.xlabel("Service Rating")
    plt.ylabel("Orders")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "rating_distribution.png", dpi=150)
    plt.close()

    plt.figure(figsize=(8, 4))
    sns.histplot(cleaned["delivery_duration_min"], bins=30, kde=True, color="#0f766e")
    plt.title("Delivery Duration Distribution")
    plt.xlabel("Delivery Duration (minutes)")
    plt.ylabel("Orders")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "delivery_duration_distribution.png", dpi=150)
    plt.close()

    sample = cleaned.sample(min(len(cleaned), 5000), random_state=42)
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=sample, x="delivery_duration_min", y="rating", hue="delay_category", alpha=0.5)
    plt.title("Delivery Duration vs Rating")
    plt.xlabel("Delivery Duration (minutes)")
    plt.ylabel("Rating")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "delivery_duration_vs_rating_scatter.png", dpi=150)
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.boxplot(
        data=cleaned,
        x="delay_category",
        y="rating",
        hue="delay_category",
        order=["On-Time", "Late"],
        palette="viridis",
        legend=False,
    )
    plt.title("Delay Category vs Rating")
    plt.xlabel("Delay Category")
    plt.ylabel("Rating")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "delay_category_vs_rating_boxplot.png", dpi=150)
    plt.close()

    corr_cols = [col for col in ["delivery_duration_min", "rating", "order_value_inr", "order_minute_of_day"] if col in cleaned.columns]
    if len(corr_cols) >= 2:
        corr_matrix = cleaned[corr_cols].corr(numeric_only=True)
        plt.figure(figsize=(7, 5))
        sns.heatmap(corr_matrix, cmap="coolwarm", center=0, annot=True, fmt=".2f", linewidths=0.5)
        plt.title("Correlation Heatmap")
        plt.tight_layout()
        plt.savefig(FIGURE_DIR / "correlation_heatmap.png", dpi=150)
        plt.close()


def main() -> None:
    if not RAW_FILE.exists():
        raise FileNotFoundError(f"Source file not found: {RAW_FILE}")

    raw = load_data(RAW_FILE)
    cleaned = clean_data(raw)
    cleaned.to_csv(CLEAN_FILE, index=False)

    summary_text = write_summary(cleaned, raw, REPORT_FILE)
    make_plots(cleaned)

    duration_rating_corr = cleaned[["delivery_duration_min", "rating"]].corr().iloc[0, 1]
    late_share = cleaned["delay_category"].eq("Late").mean() * 100

    print("Cleaned file written to:", CLEAN_FILE)
    print("Report written to:", REPORT_FILE)
    print("Figures written to:", FIGURE_DIR)
    print(f"Orders analyzed: {len(cleaned):,}")
    print(f"Average delivery duration: {cleaned['delivery_duration_min'].mean():.2f} minutes")
    print(f"Average rating: {cleaned['rating'].mean():.2f} / 5")
    print(f"Late share (>30 min): {late_share:.2f}%")
    print(f"Duration vs rating correlation: {duration_rating_corr:.4f}")
    print("\nSummary preview:\n")
    print(summary_text)


if __name__ == "__main__":
    main()
