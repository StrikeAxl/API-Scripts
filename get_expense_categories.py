import requests
import json
import getting_access
import csv

url = "https://app.practicepanther.com/api/v2/ExpenseCategories"
acces_token = getting_access.get_token()
headers = {
   'Content-Type': "application/json",
   'Authorization': 'Bearer ' + acces_token,
   'Accept': "*/*", 
    'Accept-Encoding': "gzip, deflate",
    'Content-Length': "1014",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

get_data = {
  "created_since": "2018-03-12T00:00:00+00:00",
  "updated_since": "2018-03-12T00:00:00+00:00"
    }

get_data_json = json.dumps(get_data) 
response = requests.request("GET", url, data = get_data_json, headers=headers)
print(response.text)