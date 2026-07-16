import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Population Analysis 2020",
    page_icon="🌍",
    layout="wide"
)

# ----------------------------
# Load Dataset
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("C:/Users/Ujjwal/Desktop/github work/Population-Analysis-pro/population_by_country_2020.csv")
    return df

df = load_data()

# ----------------------------
# Title
# ----------------------------
st.title("🌍 Population Analysis Dashboard (2020)")
st.markdown("Interactive dashboard for analyzing world population statistics.")

st.divider()

# ----------------------------
# Sidebar
# ----------------------------
st.sidebar.header("Filters")

country = st.sidebar.selectbox(
    "Select Country",
    sorted(df["Country (or dependency)"].unique())
)

top_n = st.sidebar.slider(
    "Top Countries",
    min_value=5,
    max_value=20,
    value=10
)

# ----------------------------
# Dataset Preview
# ----------------------------
st.subheader("Dataset Preview")

st.dataframe(df)

# ----------------------------
# Summary Statistics
# ----------------------------
st.subheader("Dataset Statistics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Countries", len(df))

col2.metric(
    "Total Population",
    f"{df['Population (2020)'].sum():,}"
)

col3.metric(
    "Average Population",
    f"{int(df['Population (2020)'].mean()):,}"
)

st.divider()

# ----------------------------
# Country Information
# ----------------------------
st.subheader("Country Details")

country_data = df[df["Country (or dependency)"] == country]

st.dataframe(country_data)

st.divider()

# ----------------------------
# Top Population Countries
# ----------------------------
st.subheader(f"Top {top_n} Most Populated Countries")

top = df.sort_values(
    "Population (2020)",
    ascending=False
).head(top_n)

fig = px.bar(
    top,
    x="Country (or dependency)",
    y="Population (2020)",
    color="Population (2020)",
    text="Population (2020)",
)

fig.update_layout(xaxis_title="", yaxis_title="Population")

st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# Least Populated Countries
# ----------------------------
st.subheader(f"Top {top_n} Least Populated Countries")

bottom = df.sort_values(
    "Population (2020)"
).head(top_n)

fig2 = px.bar(
    bottom,
    x="Country (or dependency)",
    y="Population (2020)",
    color="Population (2020)",
    text="Population (2020)"
)

fig2.update_layout(xaxis_title="", yaxis_title="Population")

st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# Population Distribution
# ----------------------------
st.subheader("Population Distribution")

fig3 = px.histogram(
    df,
    x="Population (2020)",
    nbins=50
)

st.plotly_chart(fig3, use_container_width=True)

# ----------------------------
# Density vs Population
# ----------------------------
st.subheader("Population vs Density")

fig4 = px.scatter(
    df,
    x="Density (P/Km²)",
    y="Population (2020)",
    hover_name="Country (or dependency)",
    size="Population (2020)",
    color="Population (2020)"
)

st.plotly_chart(fig4, use_container_width=True)

# ----------------------------
# Correlation Heatmap
# ----------------------------
st.subheader("Correlation Matrix")

numeric_df = df.select_dtypes(include="number")

corr = numeric_df.corr()

fig5 = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="Viridis"
)

st.plotly_chart(fig5, use_container_width=True)

# ----------------------------
# Search Country
# ----------------------------
st.subheader("Search Country")

search = st.text_input("Enter Country Name")

if search:
    result = df[
        df["Country (or dependency)"]
        .str.contains(search, case=False)
    ]

    st.dataframe(result)

# ----------------------------
# Download Dataset
# ----------------------------
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Dataset",
    data=csv,
    file_name="population_2020.csv",
    mime="text/csv"
)

st.divider()

st.success("Dashboard Created Successfully 🚀")