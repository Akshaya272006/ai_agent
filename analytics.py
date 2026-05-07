import pandas as pd
import numpy as np

# ==========================================
# LOAD DATA
# ==========================================

def load_data(path):

    df = pd.read_csv(path)

    # Create Profit Column
    df["Profit"] = (
        df["Sales (INR)"] -
        df["Expenses (INR)"]
    )

    # Profit Margin
    df["Profit Margin %"] = (
        df["Profit"] / df["Sales (INR)"]
    ) * 100

    return df


# ==========================================
# OVERALL SUMMARY
# ==========================================

def overall_summary(df):

    total_sales = df["Sales (INR)"].sum()
    total_expenses = df["Expenses (INR)"].sum()
    total_profit = df["Profit"].sum()
    avg_customers = df["Customers"].mean()

    best_month = df.loc[
        df["Profit"].idxmax(),
        "Month"
    ]

    return {
        "Total Sales": total_sales,
        "Total Expenses": total_expenses,
        "Total Profit": total_profit,
        "Average Customers": avg_customers,
        "Best Month": best_month
    }


# ==========================================
# MONTH ANALYSIS
# ==========================================

def month_analysis(df, month):

    row = df[df["Month"] == month]

    if row.empty:
        return None

    row = row.iloc[0]

    return {
        "Month": row["Month"],
        "Sales": row["Sales (INR)"],
        "Expenses": row["Expenses (INR)"],
        "Profit": row["Profit"],
        "Customers": row["Customers"],
        "Inventory": row["Inventory Cost (INR)"],
        "Marketing": row["Marketing Spend (INR)"],
        "Profit Margin": row["Profit Margin %"]
    }


# ==========================================
# QUARTER SUMMARY
# ==========================================

def quarter_summary(df, quarter):

    quarter_map = {
        1: [0, 1, 2],
        2: [3, 4, 5],
        3: [6, 7, 8],
        4: [9, 10, 11]
    }

    idx = quarter_map.get(quarter)

    if idx is None:
        return None

    q_df = df.iloc[idx]

    return {
        "Quarter": quarter,
        "Sales": q_df["Sales (INR)"].sum(),
        "Expenses": q_df["Expenses (INR)"].sum(),
        "Profit": q_df["Profit"].sum(),
        "Customers": q_df["Customers"].mean()
    }


# ==========================================
# TOP / LOWEST MONTHS
# ==========================================

def highest_profit_month(df):

    row = df.loc[df["Profit"].idxmax()]

    return row["Month"], row["Profit"]


def lowest_profit_month(df):

    row = df.loc[df["Profit"].idxmin()]

    return row["Month"], row["Profit"]


# ==========================================
# BUSINESS HEALTH SCORE
# ==========================================

def business_health_score(df):

    avg_margin = df["Profit Margin %"].mean()

    if avg_margin >= 40:
        score = 95
    elif avg_margin >= 30:
        score = 85
    elif avg_margin >= 20:
        score = 70
    else:
        score = 50

    return score


# ==========================================
# GROWTH RATE
# ==========================================

def sales_growth(df):

    first = df.iloc[0]["Sales (INR)"]
    last = df.iloc[-1]["Sales (INR)"]

    growth = ((last - first) / first) * 100

    return round(growth, 2)