import pandas as pd
import sqlite3
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pandas as pd
from googleapiclient.errors import HttpError

df= pd.read_csv(r"C:\Users\alano\OneDrive\Documents\barber_analysis\data\cleaned_barber_data.csv")
print("Cleaned dataset")
print(df)

SCOPES =["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE=r"C:\Users\alano\OneDrive\Documents\barber_analysis\creds\service_account.json.json"

creds=Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

service=build("calendar","v3",credentials=creds)

for _, row in df.iterrows():

    start = datetime.strptime(
        f"{row['book_date']} {str(row['book_time'])[:5]}",
        "%Y-%m-%d %H:%M"
    )

    end = start + timedelta(minutes=20)

    # CHECK FIRST
    existing = service.events().list(
        calendarId="e175e2162f7075126eb97fd795c30fac4830f5511f3b06beb206fe7ef7e11844@group.calendar.google.com",
        timeMin=start.isoformat() +"Z",
        timeMax=end.isoformat() +"Z",
        privateExtendedProperty=f"booking_id={row['booking_id']}",
        singleEvents=True
    ).execute()

    if existing.get("items"):
        print(f"Skipping {row['name_surname']} (already exists)")
        continue

    # CREATE ONLY IF NOT FOUND
    event = {
        
        "summary": f"{row['service']} - {row['name_surname']}",
        "id": str(row["booking_id"]).strip().lower(),
        "extendedProperties": {
            "private": {
                "booking_id": str(row["booking_id"]).strip().lower()
            }
        },    
    
        "start": {
            "dateTime": start.isoformat(),
            "timeZone": "Africa/Johannesburg",

        },
        "end": {
            "dateTime": end.isoformat(),
            "timeZone": "Africa/Johannesburg",
        },
    }
   

    try:
        service.events().insert(
            calendarId="e175e2162f7075126eb97fd795c30fac4830f5511f3b06beb206fe7ef7e11844@group.calendar.google.com",
            body=event
        ).execute()

        print(f"Created event for {row['name_surname']}")

    except HttpError as e:
    
        if e.resp.status == 409:
            print(f"{row['name_surname']} already exists. Skipping.")

        else:
         raise





df= pd.read_csv(r"C:\Users\alano\OneDrive\Documents\barber_analysis\data\cleaned_barber_data.csv")
conn = sqlite3.connect(r"C:\Users\alano\OneDrive\Documents\barber_analysis\cleaned_barber.db")
#df.drop_duplicates(subset=["booking_id"], inplace=True)
df.to_sql(
    "bookings",
    conn,
    if_exists="replace",
    index=False
)

# df.to_sql(
#     "bookings",
#     conn,
#     if_exists="append",   # FIX
#     index=False
# )


print("Bookings pushed to calendar")

conn.close()

print("Connected successfully")
