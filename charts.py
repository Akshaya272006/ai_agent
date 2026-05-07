import streamlit as st

def sales_chart(df):

    st.line_chart(
        df.set_index("Month")["Sales (INR)"]
    )


def profit_chart(df):

    st.bar_chart(
        df.set_index("Month")["Profit"]
    )


def customer_chart(df):

    st.line_chart(
        df.set_index("Month")["Customers"]
    )