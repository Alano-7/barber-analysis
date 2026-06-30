from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta


SCOPES =["https://www.googleapis.com/auth/calendar"] #WHAT IDENTITIES IM USING
SERVICE_ACCOUNT_FILE=r"C:\Users\alano\OneDrive\Documents\barber_analysis\creds\service_account.json.json"

creds = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

#Connect to calendar
service=build("calendar","v3",credentials=creds)

events = service.events().list(
    calendarId="e175e2162f7075126eb97fd795c30fac4830f5511f3b06beb206fe7ef7e11844@group.calendar.google.com",
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

start_hour=9
end_hour=17
slot_minutes=30

for i in range(7):

    current_day = today + timedelta(days=i)

    if current_day.weekday() !=6:
        for hour in range(start_hour, end_hour):

            for minute in range(0,60,slot_minutes):

                slot_time =current_day.replace(
                    hour=hour,
                    minute=minute,
                    second=0,
                    microsecond=0
                )

                all_possible_slots.append(slot_time)

                print(slot_time)
        
available_slots=[]

for slot in all_possible_slots:
    if slot not in booked_slots:
        available_slots.append(slot)

print("Availible slots")
for slot in available_slots:
    print(slot)        

#Function to be used in the booking form!!!
def get_slots():
    return available_slots

if slot not in booked_slots:
    available_slots.append(slot)