# -*- coding: utf-8 -*-


import outlookHelperFunctions as ohf
import pandas as pd
import requests

url = ohf.get_url()
headers = ohf.get_headers()
acces_token = ohf.get_token()

response = requests.request("GET", "https://app.practicepanther.com/api/v2/matters", headers=headers)
data = response.json()

export = pd.DataFrame.from_dict(data)
#export.to_csv("EventsBackUp.csv", index = None, header=True)
export.to_json("matters.json", orient = 'records')