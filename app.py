import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Transaction Categorizer",
    page_icon="📊",
    layout="wide"
)

# ---------------- HEADER ----------------
st.title("📊 Smart Transaction Categorizer")
st.caption("Automate bank statement classification in seconds")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Controls")

uploaded_file = st.sidebar.file_uploader(
    "Upload Excel File",
    type=["xlsx"]
)

# ---------------- MAIN APP ----------------
if uploaded_file is not None:

    # ---------------- READ FILE ----------------
    df = pd.read_excel(uploaded_file)

    # ---------------- CLEAN DATA ----------------
    df.columns = df.columns.str.strip()
    df = df.loc[:, ~df.columns.astype(str).str.startswith("Unnamed")]
    df = df.dropna(axis=1, how="all")
    df = df.dropna(how="all")

    # ---------------- CATEGORY COLUMN ----------------
    df["Category"] = ""

    # ---------------- CREDIT RULE ----------------
    credit_mask = (
        df["Credit"].notna() &
        df["Description"].astype(str).str.contains(
            "Deposit Midtown|Proceeds|Deposit Himilton",
            case=False,
            na=False
        )
    )

    df.loc[credit_mask, "Category"] = "Revenue"

    # ---------------- DEBIT RULES ----------------
    df.loc[
        df["Debit"].notna() &
        df["Description"].astype(str).str.contains("CHQ", na=False),
        "Category"
    ] = "Loan to world eyewear"

    df.loc[
        df["Debit"].notna() &
        df["Description"].astype(str).str.contains("TRANSFER TO", case=False, na=False),
        "Category"
    ] = "Loan to world eyewear"

        df.loc[
        df["Debit"].notna() &
        df["Description"].astype(str).str.contains("TRANSFER FROM", case=False, na=False),
        "Category"
    ] = "Investment income"

    df.loc[
        df["Debit"].notna() &
        df["Description"].astype(str).str.contains("SERVICE CHARGE", case=False, na=False),
        "Category"
    ] = "Bank Charges"

    # ---------------- OUTPUT TABLE ----------------
    st.subheader("📊 Categorized Transactions")
    st.dataframe(df, use_container_width=True)

    # ---------------- SUMMARY DASHBOARD ----------------
    st.subheader("📊 Summary Dashboard")

    revenue_count = (df["Category"] == "Revenue").sum()
    bank_charges = (df["Category"] == "Bank Charges").sum()
    loan_count = df["Category"].str.contains("Loan", na=False).sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("Revenue Transactions", revenue_count)
    col2.metric("Bank Charges", bank_charges)
    col3.metric("Loan / Transfer", loan_count)

    # ---------------- DOWNLOAD ----------------
    output_file = "categorized_financials.xlsx"
    df.to_excel(output_file, index=False)

    with open(output_file, "rb") as f:
        st.download_button(
            "⬇️ Download Categorized File",
            f,
            file_name="categorized_financials.xlsx"
        )

else:
    st.info("Please upload an Excel file from the sidebar to start processing.")
