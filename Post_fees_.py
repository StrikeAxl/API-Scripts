# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 12:10:07 2019

@author: Axel
"""

import requests
import json
import csv
import time
import get_search_data as gsd
import create_csv_error as EF
import pandas as pd
from tkinter import Tk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename

url = "https://app.practicepanther.com/api/v2/"
headers = gsd.get_headers()
acces_token = gsd.get_token()

gsd.get_matters() #call function to get the matters
gsd.get_users()
gsd.TimeGet_items()

Tk().withdraw()
EF.filename = askopenfilename()
orig_f = EF.generate_original_file()
err_f = EF.generate_error_file(orig_f)

with open(EF.filename) as csvfile:

  csv_reader = csv.DictReader(csvfile)
  line_count = 1
  for row in csv_reader:

    post_data = {}
    line_count += 1

    contact = gsd.ExpSearchC(row["matter_ref"])
    matter = gsd.ExpSearchM(row["matter_ref"]) #calls search function which receives what the spreadsheet has in that column as param and returns the matter ref and assigns it to "matter"
    #matter = row["matter_ref"]
    user = gsd.ExpSearchU(row["billed_by_user_ref"])
    items = gsd.TimeSearch_items(row["item_ref"])

    if matter is None or user is None or matter == user == None:
      next
    elif items is None:
      next
    elif items == "":
      post_data = {
        "is_billable": row["is_billable"],
        "is_billed": row["is_billed"],
        "date": row["date"],
        "qty": row["qty"],
        "price": row["price"],
        "description": row["description"],
        "private_notes": row["private_notes"],
        "account_ref": {
          "id": contact,
        },
        "matter_ref": {
          "id": matter,
        },
        "billed_by_user_ref": {
          "id": user,
        },
        "item_ref": {
          "id": "0388e2bf-bff5-4787-a857-0d0ac71bf16e"
        }
      }
    else:
      post_data = {
        "is_billable": row["is_billable"],
        "is_billed": row["is_billed"],
        "date": row["date"],
        "qty": row["qty"],
        "price": row["price"],
        "description": row["description"],
        "private_notes": row["private_notes"],
        "account_ref": {
          "id": contact,
        },
        "matter_ref": {
          "id": matter,
        },
        "billed_by_user_ref": {
          "id": user,
        },
        "item_ref": {
          "id": items,
        }
      }

    if post_data == {}:
      next
    else:
      post_data_json = json.dumps(post_data) 
      response = requests.request("POST", url + "flatfees", data=post_data_json, headers=headers)
      reponse_body = json.loads(response.text)
      if response.status_code == 200:
          print("Processing row " + str(line_count) + ": Fee successfully uploaded") #posting data and printing the response
          next
      elif response.status_code == 401:
          print("Access Token expired, please re-start the app")
          break
      else:
          gsd.new_error("The request returned the following error: " + str(reponse_body['modelState']))

    all_errors = gsd.get_errors()

    if all_errors == []:
      next
    else:
      EF.error = pd.Series({'Error': '\n'.join(all_errors)})
      other_columns = EF.error.append(orig_f.loc[line_count-1])
      err_f = err_f.append(other_columns,ignore_index=True)
      print(all_errors)
      gsd.clear_errors()

    post_data.clear()
    time.sleep(0.2)

print(str(line_count) + " rows were processed on file " + EF.filename)


while True:
  try:
    export_csv = err_f.to_csv(filedialog.askdirectory() + "\FeeErrors.csv", index = None, header=True)
    break
  except:
    continue