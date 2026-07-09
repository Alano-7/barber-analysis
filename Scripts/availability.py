from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import streamlit as st

SCOPES =["https://www.googleapis.com/auth/calendar"] #WHAT IDENTITIES IM USING
#SERVICE_ACCOUNT_FILE=r"C:\Users\alano\OneDrive\Documents\barber_analysis\creds\service_account.json.json"

#creds = Credentials.from_service_account_file(
#    SERVICE_ACCOUNT_FILE,
#    scopes=SCOPES
#)

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=SCOPES
)

#Connect to calendar
service=build("calendar","v3",credentials=creds)

events = service.events().list(
    calendarId="0de5ec9c5517c39f0e210c197455f52a68559732388e8870d1d2be626a959e36@group.calendar.google.com",
    singleEvents=True
).execute()


booked_slots = []

# for event in events["items"]:

#     start_time = event["start"]["dateTime"]

#     booked_slots.append(start_time)

# print(booked_slots)

for event in events["items"]:
    start_time=event["start"]["dateTime"]
    start_time=datetime.fromisoformat(
        start_time.replace("Z","+00:00")
    )

    start_time=start_time.replace(tzinfo=None)
    booked_slots.append(start_time)



#All possible availble slots:

all_possible_slots=[]
today= datetime.today()

#start and end hour was here
slot_minutes=20

for i in range (7):
    current_day= today + timedelta(days=i)

    weekday=current_day.weekday()

    #M,W,T,F
    if weekday in [0,2,3,4]:
        start_hour = 9
        end_hour = 18

    #S
    elif weekday ==5:
        start_hour=8
        end_hour=16
    #T&S
    else:
        continue
    for hour in range(start_hour, end_hour):
        for minute in range(0,60,slot_minutes):
            slot_time =current_day.replace(
                hour=hour,
                minute=minute,
                second=0,
                microsecond=0
            )

            all_possible_slots.append(slot_time)    


                
        
available_slots=[]

for slot in all_possible_slots:
    if slot not in booked_slots:
        available_slots.append(slot)

       

#Function to be used in the booking form!!!
def get_slots():
    return available_slots

