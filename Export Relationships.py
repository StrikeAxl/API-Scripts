# -*- coding: utf-8 -*-
"""
Created on Mon Mar 4 20:40:59 2019

@author: Axel
"""

import requests
import json
import get_search_data as gsd
#import pandas as pd
import csv

url = "https://app.practicepanther.com/api/v2/"
headers = gsd.get_headers() 
acces_token = gsd.get_token()

response = requests.request("GET", url + "relationships", headers=headers)
data = json.loads(response.text)
export_data = data
export_file = open('Relationships_Export.csv','w')
csv_writer = csv.writer(export_file)
count = 0
#reponse_body = json.loads(response.text)

for rel in export_data:
    if count == 0:
        header = rel.keys()
        csv_writer.writerow(header)
        count += 1
        
    csv_writer.writerow(rel.values())
    
export_file.close()

