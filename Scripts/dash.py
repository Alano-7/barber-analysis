import streamlit as st
import sqlite3
import pandas as pd
import os
import plotly.express as px

conn=sqlite3.connect(r'C:\Users\alano\OneDrive\Documents\barber_analysis\cleaned_barber.db')





# print(os.getcwd())

# #THE TOTAL REVENUE:

revenue_df = pd.read_sql(
     "SELECT SUM(price) AS total_revenue FROM bookings",
     conn
 )

total_revenue = revenue_df["total_revenue"][0]

# st.metric(
#     "Total Revenue",
#     f"R{total_revenue}"
# )

#THE TOTAL BOOKINGS:

bookings_df=pd.read_sql(
     "SELECT COUNT(book_date) AS total_bookings FROM bookings",
     conn
 )

total_bookings=bookings_df["total_bookings"][0]

# st.metric(
#     "Total Bookings :",
#     f"{total_bookings} bookings made"

# )

#RETURNING CLIENT %:

# returning_perc_df= pd.read_sql(
#     "SELECT COUNT(*) AS total,SUM(CASE WHEN returning_client='Yes' THEN 1 ELSE 0 END) AS returning_count,SUM(CASE WHEN returning_client='No' THEN 1 ELSE 0 END) FROM bookings",
#     conn
# )

# returning_clients=int(returning_perc_df["returning_count"].iloc[0])
# total_clients=int(returning_perc_df["total"].iloc[0])
# returning_perc_clients=round((returning_clients/total_clients)*100,2)

#print(f"{returning_perc_clients} % are returning clients")# To check if calculation works

client_count = pd.read_sql(
    """
    SELECT
        CASE
            WHEN returning_client = 'Yes' THEN 'Returning'
            ELSE 'New'
        END AS client_type,
        COUNT(*) AS count
    FROM bookings
    GROUP BY client_type
    """,
    conn
)
fig=px.pie(
    client_count,
    names="client_type",
    values="count",
    title="Returning vs new clients ratio",
    hole=0.4
)

fig.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

st.plotly_chart(fig, width='stretch')

#AVERAGE BOOKING INCOME

average_booking_df=pd.read_sql(
     "SELECT AVG(price) AS avg_booking_value FROM bookings",
     conn
 )

avg_booking=round(average_booking_df["avg_booking_value"][0],2)

# st.metric(
#     "Average income per session : " ,
#     f"R{avg_booking} per session"
    
# )

#REVENUE BY SERVICE
revenue_by_service_df=pd.read_sql(
     "SELECT service ,SUM (price) AS revenue FROM bookings GROUP BY service ORDER BY revenue DESC" ,
     conn
       
)

# st.markdown(" 📊 Revenue Breakdown by Service Type")
# st.bar_chart(
#     data=revenue_by_service_df,
#     x="service",
#     y="revenue",
#     color="#ffaa00"
# )


# =====================================
# KPI ROW
# =====================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Revenue",
        f"R{total_revenue}"
    )

with col2:
    st.metric(
        "Total Bookings",
        total_bookings
    )

with col3:
    st.metric(
        "Average Session Value",
        f"R{avg_booking}"
    )

with col4:

    returning_clients = int(
        client_count.loc[
            client_count["client_type"] == "Returning",
            "count"
        ].iloc[0]
    )

    total_clients = client_count["count"].sum()

    returning_percentage = round(
        (returning_clients / total_clients) * 100,
        1
    )

    st.metric(
        "Returning Clients",
        f"{returning_percentage}%"
    )


# =====================================
# SECOND ROW
# =====================================

left, right = st.columns(2)

with left:

    st.markdown("### 📊 Revenue Breakdown by Service")

    st.bar_chart(
        data=revenue_by_service_df,
        x="service",
        y="revenue",
        color="#ffaa00"
    )

#with right:

    #st.plotly_chart(
       #width='stretch'
    #)


# =====================================
# THIRD ROW (placeholders for now)
# =====================================

# left, right = st.columns(2)

# with left:
#     st.subheader("Peak Booking Times")
#     st.info("Coming soon")

# with right:
#     st.subheader("Upcoming Appointments")
#     st.info("Coming soon")