import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from collections import defaultdict
from availability import get_slots
# -----------------------------
# GOOGLE SHEETS SETUP
# -----------------------------
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SERVICE_ACCOUNT_FILE = r"C:\Users\alano\OneDrive\Documents\barber_analysis\creds\service_account.json.json"

creds = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

client = gspread.authorize(creds)



sheet = client.open_by_key(
    "1XKe0tq8TFIZjTFVPOFAjHiH3IGdbSoH2A-aIzzCAmx0"
).sheet1

#print(sheet.title) ####CHANGE 1

# -----------------------------
# WRITE FUNCTION (FIXED)
# -----------------------------
def write_booking(name, service, selected_time, visited_before):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sheet.append_row([
        timestamp,
        name,
        service,
        selected_time.strftime("%d/%m/%Y %H:%M:%S"),
        visited_before
    ])

#print(sheet.get_all_values())#####CHANGE 2
# -----------------------------
# UI TITLE
# -----------------------------
st.title("Book your appointment")
st.info("📅 Barber closed on Tuesdays and Sundays.")

# -----------------------------
# GET SLOTS FROM BACKEND
# -----------------------------
slots = get_slots()


# -----------------------------
# GROUP SLOTS BY DAY
# -----------------------------
grouped = defaultdict(list)

for slot in slots:
    day = slot.date()
    grouped[day].append(slot)


# -----------------------------
# FORMAT DAYS FOR UI
# -----------------------------
day_options = {
    day.strftime("%a %d %b"): day
    for day in sorted(grouped.keys())
}


# -----------------------------
# USER INPUTS
# -----------------------------
name = st.text_input("Name and Surname:")

service = st.selectbox(
    "Select your service:",
    [
        "Trim or beard shave (R80)",
        "Normal haircut (R140)",
        "Cut and shave (R180)",
        "Cut and wash (R200)"
    ]
)


# -----------------------------
# DAY SELECTION
# -----------------------------
selected_day_label = st.selectbox(
    "Select Day",
    list(day_options.keys())
)

selected_day = day_options[selected_day_label]


# -----------------------------
# TIME SELECTION
# -----------------------------
available_times = grouped[selected_day]

time_options = {
    t.strftime("%H:%M"): t
    for t in available_times
}

selected_time_label = st.selectbox(
    "Select Time",
    list(time_options.keys())
)

selected_time = time_options[selected_time_label]


# -----------------------------
# RADIO INPUT
# -----------------------------
visited_before = st.radio(
    "Have you visited this barber before?",
    ["Yes", "No"]
)


# -----------------------------
# BOOKING BUTTON
# -----------------------------
if st.button("Book Appointment"):

    if not name:
        st.error("Name is required")

    elif not selected_day_label:
        st.error("Please select a day")

    elif not selected_time_label:
        st.error("Please select a time")

    elif not visited_before:
        st.error("Please select yes or no")

    else:
        write_booking(
            name,
            service,
            selected_time,
            visited_before
        )

        st.success(
            f"Booking confirmed for {name} on {selected_day_label} at {selected_time_label}"
        )
