# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 19:36:40 2019

@author: Axel
"""

import requests
import json
import get_search_data as gsd
import time

url = "https://app.practicepanther.com/api/v2/"
headers = gsd.get_headers() 
acces_token = gsd.get_token()

timeIds = gsd.get_timeGuids()
line = 0
for Id in timeIds:
    line = line + 1
    response = requests.request("DELETE", url + "timeentries?id=" + Id , headers=headers)
    reponse_body = json.loads(response.text)
    if response.status_code == 200:
        print("Time Entry number" + line + "successfully uploaded deleted")
        next
    elif response.status_code == 401:
        print("Access Token expired, please re-start the app")
        break
    else:
        gsd.new_error("The request returned the following error: " + str(reponse_body['modelState']))
    time.sleep(0.1)


