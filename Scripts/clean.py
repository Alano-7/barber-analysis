import  pandas as pd
import os
import hashlib

df=pd.read_csv(r"C:\Users\alano\OneDrive\Documents\barber_analysis\data\raw_responses.csv")
#print(df)#Use to test if df is coming through

df["Select your service:"] = df["Select your service:"].str.replace(r"\s*\(", " (", regex=True) #Fixing the brackets spacing with price
df[["service","price"]]= df["Select your service:"].str.extract(r"(.+)\s\(R(\d+)\)") # Splitting the joint service and price into sperate columns
df["price"]= pd.to_numeric(df["price"]) #Converts the price data type to numeric
df.drop(columns=["Select your service:"],inplace=True) #This is to remove the old serviceprice column
df["Select a date and time"] = pd.to_datetime(
    df["Select a date and time"],
    errors="coerce",
    dayfirst=True
)
df["book_date"] = df["Select a date and time"].dt.date
df["book_time"] = df["Select a date and time"].dt.time

# df["Select a date and time"] = df["Select a date and time"].dt.strftime("%Y-%m-%d %H:%M:%S") #Converts the select date and time to the correct date data type
# df["book_date"]=df["Select a date and time"].dt.date #Seperates date from date and time
# df["book_time"]=df["Select a date and time"].dt.time#Seperates time from date and time
df.drop(columns=["Select a date and time","Timestamp"],inplace=True)#Remove mix date and time column
df=df.rename(columns={"Have you visited this barber before?":"returning_client","Name and Surname:":"name_surname"})#Renaming the have you been heere before column and name and surname column
df=df[["name_surname","service","price", "book_date","book_time","returning_client"]]

#Making the booking ID
df["booking_id"]=(
    df["name_surname"]
    +"_"
    +df["book_date"].astype(str)
    +"_"
    +df["book_time"].astype(str)
)

df["booking_id"]=df["booking_id"].apply(
    lambda x: hashlib.md5(x.encode()).hexdigest()
)

print(df.columns)
print(df.head())

print(df.groupby("service")["price"].sum())
print(os.getcwd())
df.to_csv(r"C:\Users\alano\OneDrive\Documents\barber_analysis\data\cleaned_barber_data.csv",index=False)#Creates cleaned data file








'''
df.columns = (df.columns
              .str.strip() #Remove behind or ahead whitespace
              .str.lower() #Convert the text to lowercase
              

)
'''