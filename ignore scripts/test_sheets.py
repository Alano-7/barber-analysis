import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

#This is the path to the RELATIVE path to the json file
SERVICE_ACCOUNT_FILE=r"C:\Users\alano\OneDrive\Documents\barber_analysis\creds\service_account.json.json"

#Giving permission to read Google Sheets
SCOPES=["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]
    

#Authetication, loging in as Robot/Waiter
creds=Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES

)

client=gspread.authorize(creds)

#Opening the sheet
sheet=client.open_by_key("1XKe0tq8TFIZjTFVPOFAjHiH3IGdbSoH2A-aIzzCAmx0").sheet1

#GETTING ALL ROWS
data=sheet.get_all_records()

#CONVERT TO DF
df=pd.DataFrame(data)

print(df.head())