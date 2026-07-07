import pandas as pd

df=pd.read_csv("raw_responses.csv")

print(df.head()) #Shows the first 5 rows of data
print(df.columns) # Shows all the columns
print(df.info()) #Gives null counts and data type information