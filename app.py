import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import streamlit as st
import pandas as pd
import ollama

from utils.analytics import *
from utils.charts import *
from utils.memory import *
from utils.forecast import *
from utils.rag_engine import *

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI SME/MSME Consultant",
    layout="wide"
)

# ==========================================
# LOAD DATA
# ==========================================

df = load_data("data/sme_data.csv")

# ==========================================
# MEMORY
# ==========================================

initialize_memory()

# ==========================================
# VECTOR DATABASE
# ==========================================

vector_db = create_vector_db(df)

# ==========================================
# TITLE
# ==========================================

st.title("AI SME/MSME Business Consultant")

st.subheader("Business Dataset")

st.dataframe(df)

# ==========================================
# CHARTS
# ==========================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("Sales Trend")
    sales_chart(df)

with col2:

    st.subheader("Profit Trend")
    profit_chart(df)

st.subheader("Customer Trend")
customer_chart(df)

# ==========================================
# BUSINESS HEALTH SCORE
# ==========================================

score = business_health_score(df)

st.metric(
    "Business Health Score",
    f"{score}/100"
)

# ==========================================
# SALES FORECAST
# ==========================================

prediction = predict_next_month_sales(df)

st.metric(
    "Predicted Next Month Sales",
    f"₹{prediction:,}"
)

# ==========================================
# CHAT HISTORY
# ==========================================

show_chat_history()

# ==========================================
# USER INPUT
# ==========================================

question = st.chat_input(
    "Ask your business question..."
)

# ==========================================
# MONTH LIST
# ==========================================

months = df["Month"].tolist()

# ==========================================
# MAIN QUESTION HANDLING
# ==========================================

if question:

    add_message("user", question)

    with st.chat_message("user"):
        st.write(question)

    question_lower = question.lower()

    direct_answer = ""

    ai_text = ""

    # ======================================
    # MONTH DETECTION
    # ======================================

    month_found = None

    for month in months:

        short_month = month.lower().split("-")[0]

        if short_month in question_lower:
            month_found = month
            break

    # ======================================
    # STRATEGY / RECOMMENDATION QUESTIONS
    # ======================================

    if any(word in question_lower for word in [
        "strategy",
        "strategies",
        "improve",
        "increase",
        "recommend",
        "suggest",
        "advice",
        "tips",
        "how to"
    ]):

        if month_found:

            row = df[df["Month"] == month_found].iloc[0]

            direct_answer = f"""
BUSINESS STRATEGY ANALYSIS

Month: {row['Month']}

Sales: ₹{row['Sales (INR)']:,}

Expenses: ₹{row['Expenses (INR)']:,}

Profit: ₹{row['Profit']:,}
"""

            # LOW PROFIT CASE
            if row["Profit"] < 150000:

                ai_text = f"""
1. Reduce operational and inventory costs because expenses are high compared to sales.

2. Improve targeted marketing campaigns to increase customer acquisition and boost monthly revenue.
"""

            # GOOD PROFIT CASE
            else:

                ai_text = f"""
1. Increase customer retention through loyalty programs and repeat purchase offers.

2. Expand marketing toward high-performing products and profitable customer segments.
"""

        else:

            total_profit = df["Profit"].sum()

            direct_answer = f"""
BUSINESS IMPROVEMENT SUMMARY

Total Profit:
₹{total_profit:,}
"""

            ai_text = f"""
1. Focus on increasing repeat customers and customer satisfaction.

2. Optimize operational expenses and improve marketing efficiency for better profit margins.
"""

    # ======================================
    # PROFIT QUESTIONS
    # ======================================

    elif any(word in question_lower for word in [
        "profit",
        "earning",
        "income",
        "gain"
    ]):

        if month_found:

            row = df[df["Month"] == month_found].iloc[0]

            profit = row["Profit"]

            direct_answer = f"""
PROFIT ANALYSIS

Month: {row['Month']}

Sales: ₹{row['Sales (INR)']:,}

Expenses: ₹{row['Expenses (INR)']:,}

Profit: ₹{profit:,}
"""

        else:

            total_profit = df["Profit"].sum()

            best = df.loc[df["Profit"].idxmax()]

            direct_answer = f"""
OVERALL PROFIT SUMMARY

Total Profit: ₹{total_profit:,}

Highest Profit Month:
{best['Month']} — ₹{best['Profit']:,}
"""

    # ======================================
    # SALES QUESTIONS
    # ======================================

    elif any(word in question_lower for word in [
        "sales",
        "revenue"
    ]):

        if "highest" in question_lower or "best" in question_lower:

            row = df.loc[df["Sales (INR)"].idxmax()]

            direct_answer = f"""
HIGHEST SALES MONTH

Month: {row['Month']}

Sales: ₹{row['Sales (INR)']:,}
"""

        elif "lowest" in question_lower:

            row = df.loc[df["Sales (INR)"].idxmin()]

            direct_answer = f"""
LOWEST SALES MONTH

Month: {row['Month']}

Sales: ₹{row['Sales (INR)']:,}
"""

        elif month_found:

            row = df[df["Month"] == month_found].iloc[0]

            direct_answer = f"""
SALES ANALYSIS

Month: {row['Month']}

Sales:
₹{row['Sales (INR)']:,}
"""

        else:

            total_sales = df["Sales (INR)"].sum()

            avg_sales = int(
                df["Sales (INR)"].mean()
            )

            direct_answer = f"""
SALES SUMMARY

Total Sales:
₹{total_sales:,}

Average Monthly Sales:
₹{avg_sales:,}
"""

    # ======================================
    # EXPENSE QUESTIONS
    # ======================================

    elif any(word in question_lower for word in [
        "expense",
        "cost",
        "spending"
    ]):

        if month_found:

            row = df[df["Month"] == month_found].iloc[0]

            direct_answer = f"""
EXPENSE ANALYSIS

Month:
{row['Month']}

Expenses:
₹{row['Expenses (INR)']:,}

Inventory Cost:
₹{row['Inventory Cost (INR)']:,}

Marketing Spend:
₹{row['Marketing Spend (INR)']:,}
"""

        else:

            total_expenses = df["Expenses (INR)"].sum()

            high = df.loc[df["Expenses (INR)"].idxmax()]

            direct_answer = f"""
EXPENSE SUMMARY

Total Expenses:
₹{total_expenses:,}

Highest Expense Month:
{high['Month']}
"""

    # ======================================
    # CUSTOMER QUESTIONS
    # ======================================

    elif "customer" in question_lower:

        high = df.loc[df["Customers"].idxmax()]

        direct_answer = f"""
CUSTOMER ANALYSIS

Highest Customer Month:
{high['Month']}

Customers:
{high['Customers']}
"""

    # ======================================
    # INVENTORY QUESTIONS
    # ======================================

    elif "inventory" in question_lower:

        high = df.loc[
            df["Inventory Cost (INR)"].idxmax()
        ]

        direct_answer = f"""
INVENTORY ANALYSIS

Highest Inventory Cost Month:
{high['Month']}

Inventory Cost:
₹{high['Inventory Cost (INR)']:,}
"""

    # ======================================
    # MARKETING QUESTIONS
    # ======================================

    elif "marketing" in question_lower:

        high = df.loc[
            df["Marketing Spend (INR)"].idxmax()
        ]

        direct_answer = f"""
MARKETING ANALYSIS

Highest Marketing Spend Month:
{high['Month']}

Marketing Spend:
₹{high['Marketing Spend (INR)']:,}
"""

    # ======================================
    # Q1 QUESTIONS
    # ======================================

    elif "q1" in question_lower:

        q1 = df.iloc[0:3]

        direct_answer = f"""
Q1 BUSINESS SUMMARY

Sales:
₹{q1['Sales (INR)'].sum():,}

Expenses:
₹{q1['Expenses (INR)'].sum():,}

Profit:
₹{q1['Profit'].sum():,}
"""

    # ======================================
    # Q2 QUESTIONS
    # ======================================

    elif "q2" in question_lower:

        q2 = df.iloc[3:6]

        direct_answer = f"""
Q2 BUSINESS SUMMARY

Sales:
₹{q2['Sales (INR)'].sum():,}

Expenses:
₹{q2['Expenses (INR)'].sum():,}

Profit:
₹{q2['Profit'].sum():,}
"""

    # ======================================
    # Q3 QUESTIONS
    # ======================================

    elif "q3" in question_lower:

        q3 = df.iloc[6:9]

        direct_answer = f"""
Q3 BUSINESS SUMMARY

Sales:
₹{q3['Sales (INR)'].sum():,}

Expenses:
₹{q3['Expenses (INR)'].sum():,}

Profit:
₹{q3['Profit'].sum():,}
"""

    # ======================================
    # Q4 QUESTIONS
    # ======================================

    elif "q4" in question_lower:

        q4 = df.iloc[9:12]

        direct_answer = f"""
Q4 BUSINESS SUMMARY

Sales:
₹{q4['Sales (INR)'].sum():,}

Expenses:
₹{q4['Expenses (INR)'].sum():,}

Profit:
₹{q4['Profit'].sum():,}
"""

    # ======================================
    # BEST MONTH
    # ======================================

    elif "best month" in question_lower:

        best = df.loc[df["Profit"].idxmax()]

        direct_answer = f"""
BEST BUSINESS MONTH

Month:
{best['Month']}

Profit:
₹{best['Profit']:,}
"""

    # ======================================
    # DEFAULT SUMMARY
    # ======================================

    else:

        summary = overall_summary(df)

        direct_answer = f"""
BUSINESS OVERVIEW

Total Sales:
₹{summary['Total Sales']:,}

Total Expenses:
₹{summary['Total Expenses']:,}

Total Profit:
₹{summary['Total Profit']:,}

Average Customers:
{int(summary['Average Customers'])}

Best Month:
{summary['Best Month']}
"""

    # ======================================
    # SAFE AI INSIGHTS
    # ======================================

    if ai_text == "":

        try:

            insight_prompt = f"""
You are an MSME business consultant.

Use ONLY this verified result:

{direct_answer}

Rules:
- Do NOT create fake numbers
- Do NOT create fake tables
- Give only:
  1. One short insight
  2. Two business recommendations
- Keep response under 60 words
"""

            response = ollama.chat(
                model="tinyllama",
                messages=[
                    {
                        "role": "user",
                        "content": insight_prompt
                    }
                ]
            )

            ai_text = response["message"]["content"]

        except:

            ai_text = """
1. Reduce unnecessary operational expenses.
2. Improve customer engagement and retention.
"""

    # ======================================
    # FINAL ANSWER
    # ======================================

    final_answer = f"""
{direct_answer}

-----------------------------------

BUSINESS INSIGHTS:

{ai_text}
"""

    add_message(
        "assistant",
        final_answer
    )

    with st.chat_message("assistant"):
        st.write(final_answer)