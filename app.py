import streamlit as st
import pandas as pd

# ======================
# LOAD DATA
# ======================
leads = pd.read_csv("leads.csv")
funnel = pd.read_csv("funnel.csv")
cost = pd.read_csv("marketing_cost.csv")

# Convert Date (if exists)
if "Date" in leads.columns:
    leads["Date"] = pd.to_datetime(leads["Date"])

# Merge data
df = leads.merge(funnel, on="Lead_ID")

# ======================
# CORE ANALYSIS
# ======================
leads_count = df.groupby("Lead_Source")["Lead_ID"].count()
enrollments = df[df["Enrolled"]=="Yes"].groupby("Lead_Source")["Lead_ID"].count()
conversion = (enrollments / leads_count) * 100

channel_stats = pd.DataFrame({
    "Leads": leads_count,
    "Enrollments": enrollments
}).fillna(0)

channel_stats = channel_stats.merge(cost, left_index=True, right_on="Channel")
channel_stats["Cost_per_Enrollment"] = channel_stats["Cost"] / channel_stats["Enrollments"]

# ======================
# UI START
# ======================
st.title("📊 Lead Source Performance Dashboard")

# ======================
# KPIs
# ======================
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)
col1.metric("Total Leads", int(leads_count.sum()))
col2.metric("Total Enrollments", int(enrollments.sum()))
col3.metric("Avg Conversion (%)", round(conversion.mean(), 2))

# ======================
# TABLE
# ======================
st.subheader("📊 Channel Performance Table")
st.dataframe(channel_stats)

# ======================
# CHARTS
# ======================
col1, col2 = st.columns(2)

with col1:
    st.subheader("Leads by Channel")
    st.bar_chart(leads_count)

with col2:
    st.subheader("Conversion Rate (%)")
    st.bar_chart(conversion)

st.subheader("💰 Cost per Enrollment")
st.bar_chart(channel_stats.set_index("Channel")["Cost_per_Enrollment"])

# ======================
# CITY ANALYSIS
# ======================
st.subheader("🏙️ City-wise Leads")
city_leads = df.groupby("City")["Lead_ID"].count()
st.bar_chart(city_leads)

# ======================
# COURSE ANALYSIS
# ======================
st.subheader("📚 Course Interest by Channel")
course_analysis = df.groupby(["Lead_Source", "Course_Interest"])["Lead_ID"].count().unstack()
st.dataframe(course_analysis)

# ======================
# TIME TREND
# ======================
if "Date" in df.columns:
    st.subheader("📈 Leads Over Time")
    time_trend = df.groupby("Date")["Lead_ID"].count()
    st.line_chart(time_trend)

# ======================
# FUNNEL ANALYSIS
# ======================
st.subheader("🔻 Funnel by Channel")

funnel_data = df.groupby("Lead_Source").agg({
    "Lead_ID": "count",
    "Counselling": lambda x: (x=="Yes").sum(),
    "Application": lambda x: (x=="Yes").sum(),
    "Enrolled": lambda x: (x=="Yes").sum()
})

st.dataframe(funnel_data)

# ======================
# INSIGHTS
# ======================
best_channel = channel_stats.sort_values("Cost_per_Enrollment").iloc[0]["Channel"]
worst_channel = channel_stats.sort_values("Cost_per_Enrollment").iloc[-1]["Channel"]

st.subheader("🧠 Insights")

st.success(f"Best Channel: {best_channel}")
st.error(f"Worst Channel: {worst_channel}")

st.info(f"Recommendation: Invest more in {best_channel} and reduce spending on {worst_channel}")