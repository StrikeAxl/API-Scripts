import requests
import json
import csv
import get_search_data as gsd
from tkinter import Tk
from tkinter.filedialog import askopenfilename

url = "https://app.practicepanther.com/api/v2/Items"
headers = gsd.get_headers()
acces_token = gsd.get_token()

Tk().withdraw()
filename = askopenfilename()

with open(filename) as csvfile:
  
  csv_reader = csv.DictReader(csvfile)
  line_count = 0
  for row in csv_reader:
    if line_count == 0:
      print(f'Column names are {", ".join(row)}')
      line_count += 1
    line_count += 1
  
    name = row["Name"]
    rate = row["Rate"]

    if name == rate == "":
      print("Please enter an Item name and code")
    elif name == "":
      print("Please enter an Item name")
      continue
    elif rate == "":
      print("Please enter a code")
      continue
    else: 
      post_data = {
        "name": row["Name"],
        "code": row["Code"],
        "description": row["Description"],
        "rate": row["Rate"],
      }
  
    post_data_json = json.dumps(post_data) 
    response = requests.request("POST", url, data=post_data_json, headers=headers)
    reponse_body = json.loads(response.text)

    try:
      print("The request returned the following error on row " + str(line_count) + ": " + str(reponse_body['modelState']))
    except:
      print("Processing row #" + str(line_count) + ": Item successfully uploaded")
    pass

print(str(line_count-1) + " rows were processed")