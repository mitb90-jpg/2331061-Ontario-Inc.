import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
            "Proceeds|Deposit",
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
        df["Description"].astype(str).str.contains("TRANSFER OTHER", case=False, na=False),
        "Category"
    ] = "Investment income"

    df.loc[
        df["Debit"].notna() &
        df["Description"].astype(str).str.contains("SERVICE CHARGE", case=False, na=False),
        "Category"
    ] = "Interest and Bank charges"

    # ---------------- OUTPUT TABLE ----------------
    st.subheader("📊 Categorized Transactions")
    st.dataframe(df, use_container_width=True)

    # ---------------- SUMMARY DASHBOARD ----------------
    st.subheader("📊 Summary Dashboard")

    # Transaction Counts
    revenue_count = (df["Category"] == "Revenue").sum()

    bank_charges_count = (
        df["Category"] == "Interest and Bank charges"
    ).sum()

    loan_count = (
        df["Category"] == "Loan to world eyewear"
    ).sum()

    investment_count = (
        df["Category"] == "Investment income"
    ).sum()

    st.markdown("### Transaction Counts")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Revenue Transactions", revenue_count)
    col2.metric("Bank Charges", bank_charges_count)
    col3.metric("Loan Transactions", loan_count)
    col4.metric("Investment Income Transactions", investment_count)

    # Financial Amounts
    revenue_amount = df.loc[
        df["Category"] == "Revenue",
        "Credit"
    ].fillna(0).sum()

    investment_amount = df.loc[
        df["Category"] == "Investment income",
        "Debit"
    ].fillna(0).sum()

    bank_charge_amount = df.loc[
        df["Category"] == "Interest and Bank charges",
        "Debit"
    ].fillna(0).sum()

    loan_amount = df.loc[
        df["Category"] == "Loan to world eyewear",
        "Debit"
    ].fillna(0).sum()

    st.markdown("### Financial Amounts")

    col5, col6, col7, col8 = st.columns(4)

    col5.metric("Revenue Amount", f"${revenue_amount:,.2f}")
    col6.metric("Investment Income Amount", f"${investment_amount:,.2f}")
    col7.metric("Loan Amount", f"${loan_amount:,.2f}")
    col8.metric("Bank Charges Amount", f"${bank_charge_amount:,.2f}")

# ---------------- CATEGORY PIE CHART BY AMOUNT ----------------
st.subheader("🥧 Category Distribution by Amount")

amounts = {
    "Revenue": revenue_amount,
    "Investment Income": investment_amount,
    "Loan": loan_amount,
    "Bank Charges": bank_charge_amount
}

amounts = {k: v for k, v in amounts.items() if v > 0}

fig, ax = plt.subplots(figsize=(6, 6))

ax.pie(
    amounts.values(),
    labels=amounts.keys(),
    autopct="%1.1f%%"
)

ax.set_title("Financial Distribution by Amount")

st.pyplot(fig)

    # ---------------- DOWNLOAD ----------------
    output_file = "categorized_financials.xlsx"
    df.to_excel(output_file, index=False)

    with open(output_file, "rb") as f:
        st.download_button(
            "⬇️ Download Categorized File",
            f,
            file_name="categorized_financials.xlsx"
        )
