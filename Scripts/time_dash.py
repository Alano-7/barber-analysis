import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
# -----------------------------
# DATABASE CONNECTION
# -----------------------------
conn = sqlite3.connect(
    r'C:\Users\alano\OneDrive\Documents\barber_analysis\cleaned_barber.db'
)

df = pd.read_csv(
    r"C:\Users\alano\OneDrive\Documents\barber_analysis\data\cleaned_barber_data.csv"
)

today=datetime.today()
#Start of current week
week_start = today - timedelta(days=today.weekday())
#Ending of week
week_end = week_start + timedelta(days=5)

print("Current week: ")
print(week_start.date())
print(week_end.date())


# =============================
# WEEKLY ACTIVITY
# =============================
weekly_activity_df = pd.read_sql(
    """
    SELECT
        CASE strftime('%w', date(book_date))
            WHEN '1' THEN 'Monday'
            WHEN '2' THEN 'Tuesday'
            WHEN '3' THEN 'Wednesday'
            WHEN '4' THEN 'Thursday'
            WHEN '5' THEN 'Friday'
            WHEN '6' THEN 'Saturday'
        END AS weekday,
        COUNT(*) AS bookings
    FROM bookings
    WHERE strftime('%w', date(book_date)) != '0'
    GROUP BY weekday
    ORDER BY strftime('%w', date(book_date))
    """,
    conn
)

fig_weekly = px.line(
    weekly_activity_df,
    x="weekday",
    y="bookings",
    markers=True,
    title="Weekly Activity"
)

st.plotly_chart(
    fig_weekly,
    width="stretch",
    key="weekly_activity"
)


# =============================
# CHAIR UTILIZATION
# =============================
utilization_df = pd.read_sql(
    """
    SELECT
        CASE strftime('%w', date(book_date))
            WHEN '1' THEN 'Monday'
            WHEN '2' THEN 'Tuesday'
            WHEN '3' THEN 'Wednesday'
            WHEN '4' THEN 'Thursday'
            WHEN '5' THEN 'Friday'
            WHEN '6' THEN 'Saturday'
        END AS weekday,
        ROUND(COUNT(*)*100.0/8,1) AS utilization
    FROM bookings
    WHERE strftime('%w', date(book_date)) != '0'
    GROUP BY strftime('%w', date(book_date))
    ORDER BY strftime('%w', date(book_date))
    """,
    conn
)

fig_util = px.bar(
    utilization_df,
    x="weekday",
    y="utilization",
    title="Chair Utilization Rate (%)"
)

st.plotly_chart(
    fig_util,
    width="stretch",
    key="utilization"
)


# =============================
# DAILY ACTIVITY (BUSIEST HOURS)
# =============================
selected_day = st.selectbox(
    "Select Day",
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
)

# FIX: safe datetime parsing
df["book_date"] = pd.to_datetime(df["book_date"], errors="coerce")
df["weekday"] = df["book_date"].dt.day_name()

# FIX: copy to avoid warnings
day_df = df[df["weekday"] == selected_day].copy()

# Extract hour safely
day_df["hour"] = day_df["book_time"].astype(str).str[:2].astype(int)

# Count bookings per hour
hour_counts = (
    day_df.groupby("hour")
    .size()
    .reindex(range(9, 17), fill_value=0)
)

# Build clean x-axis labels
x_labels = [f"{h:02d}-{h+1:02d}" for h in range(9, 17)]

fig_daily = px.line(
    x=x_labels,
    y=hour_counts.values,
    markers=True,
    title=f"{selected_day} Peak Booking Hours"
)

fig_daily.update_xaxes(type="category")

fig_daily.update_yaxes(dtick=1)

st.plotly_chart(
    fig_daily,
    width="stretch",
    key="daily_activity"
)