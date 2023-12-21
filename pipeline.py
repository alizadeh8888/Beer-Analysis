
import pandas as pd
import requests
from datetime import datetime 
import sqlite3
import json


# Extract

url = ('https://api.punkapi.com/v2/beers')

response = requests.get(url)

data = response.json()


#Transform

df = pd.DataFrame(data)

df["volume_unit"] = df["volume"].apply(lambda x: x["unit"])
df["volume"] = df["volume"].apply(lambda x: x["value"])

df["boil_volume_unit"] = df["boil_volume"].apply(lambda x: x["unit"])
df["boil_volume"] = df["boil_volume"].apply(lambda x: x["value"])

del df["method"]
del df["ingredients"]
del df["food_pairing"]


df['brew_year'] = pd.to_datetime(df['first_brewed'], format='%m/%Y', errors='coerce').dt.year

df['brew_month'] = pd.to_datetime(df['first_brewed'], format='%m/%Y', errors='coerce').dt.month


#Lode

# lode Data into csv and Sql database

conn = sqlite3.connect('data.db')
df.to_sql('data' ,conn, if_exists= 'replace',index = False)
conn.close()

df.to_csv('data.csv')

