import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------- Page Config --------------------
st.set_page_config(
    page_title="Cyber Crime Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# -------------------- Load & Clean Data --------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Dataset_CyberCrime_Sean.csv")

    # Clean City column
    df["City"] = df["City"].astype(str)

    # Replace missing numeric values with 0
    numeric_cols = df.columns.drop("City")
    df[numeric_cols] = df[numeric_cols].fillna(0)

    return df

df = load_data()

crime_columns = df.columns[1:-1]  # Exclude City & Total

# -------------------- Sidebar --------------------
st.sidebar.title("🔍 Filters")

cities = sorted(df["City"].unique().tolist())

selected_city = st.sidebar.selectbox(
    "Select City",
    ["All Cities"] + cities
)

# -------------------- Filter Data --------------------
if selected_city == "All Cities":
    filtered_df = df
else:
    filtered_df = df[df["City"] == selected_city]

# -------------------- Header --------------------
st.title("🛡️ Cyber Crime Analysis Dashboard")
st.markdown("Interactive analysis of cyber crime types across cities")

# -------------------- KPIs --------------------
total_crimes = int(filtered_df["Total"].sum())
crime_totals = filtered_df[crime_columns].sum()
top_crime = crime_totals.idxmax()

col1, col2, col3 = st.columns(3)

col1.metric("🚨 Total Crimes", total_crimes)
col2.metric("🏙️ Cities Covered", filtered_df["City"].nunique())
col3.metric("🔥 Top Crime Type", top_crime)

st.divider()

# -------------------- Bar Chart --------------------
st.subheader("📊 Crime Type Distribution")

bar_df = crime_totals.reset_index()
bar_df.columns = ["Crime Type", "Cases"]

bar_fig = px.bar(
    bar_df,
    x="Crime Type",
    y="Cases",
    color="Crime Type"
)

bar_fig.update_layout(showlegend=False)
st.plotly_chart(bar_fig, use_container_width=True)

# -------------------- Pie Chart --------------------
st.subheader("🥧 Crime Percentage Share")

pie_fig = px.pie(
    bar_df,
    names="Crime Type",
    values="Cases",
    hole=0.4
)

st.plotly_chart(pie_fig, use_container_width=True)

# -------------------- Data Table --------------------
st.subheader("📋 City-wise Crime Data")

st.dataframe(
    filtered_df.sort_values("Total", ascending=False),
    use_container_width=True
)

# -------------------- Footer --------------------
st.markdown("---")
st.caption("📌 Cyber Crime Dashboard | Built with Streamlit")
