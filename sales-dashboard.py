import pandas as pd
import plotly.express as px
import streamlit as st
import os

# --- 1. Dashboard Setup ---
st.set_page_config(page_title="📊 Sales Analytics Dashboard", layout="wide")
st.title("📊 Sales Analytics Dashboard")
st.write("Interactive dashboard for sales KPIs")
st.write("This is task 1 of data analytics by tech-horizon")

# --- 2. Upload a sales file ---
uploaded_file = st.file_uploader(
    "Upload your sales data (CSV or Excel)", type=["csv", "xlsx"]
)

if uploaded_file:
    # --- 3. Load the file ---
    file_ext = os.path.splitext(uploaded_file.name)[-1].lower()  # Get file extension
    if file_ext == ".csv":
        df = pd.read_csv(uploaded_file)
    else:  # Excel file
        df = pd.read_excel(uploaded_file)

    # --- 4. Clean column names ---
    # Remove extra spaces and make first letter capital for consistency
    df.columns = df.columns.str.strip().str.title()

    # --- 5. Show preview of uploaded data ---
    st.subheader("Preview of your data")
    st.dataframe(df.head())  # first 5 rows
    st.dataframe(df.tail()) # last 5 rows

    # --- 6. Check for required columns ---
    required_cols = ["Revenue", "Product"]
    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        st.error(f"Missing required columns: {', '.join(missing_cols)}")
    else:
        # --- 7. KPIs ---
        st.header("Key Performance Indicators")
        total_revenue = df["Revenue"].sum()
        st.metric("Total Revenue", f"${total_revenue:,.0f}")

        top_product = df.groupby("Product")["Revenue"].sum().idxmax()
        st.metric("Top Product", top_product)

        # --- 8. Charts ---
        st.subheader("Revenue by Product")
        fig1 = px.bar(df, x="Product", y="Revenue")
        st.plotly_chart(fig1)

        if "Date" in df.columns:
            st.subheader("Revenue Over Time")
            fig2 = px.line(df, x="Date", y="Revenue")
            st.plotly_chart(fig2)

        st.subheader("Revenue Share")
        fig3 = px.pie(df, names="Product", values="Revenue")
        st.plotly_chart(fig3)

        # --- 9. Export Report ---
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Report as CSV",
            data=csv,
            file_name="sales_report.csv",
            mime="text/csv",
        )
st.success("Congratulations!, we have succesfully displayed your data!")
