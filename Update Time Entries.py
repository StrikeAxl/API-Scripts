# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 23:41:03 2019

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

Tk().withdraw()
EF.filename = askopenfilename()
orig_f = EF.generate_original_file()
err_f = EF.generate_error_file(orig_f)

all_errors = []

with open(EF.filename) as csvfile:

  csv_reader = csv.DictReader(csvfile)
  line_count = 1
  for row in csv_reader:

    put_data = {}
    line_count += 1
    TeID = row["id"]
    status = ""
    if row["is_billable"] == "TRUE":
        billable = "True"
    else:
        billable = "False"
    if row["is_billed"] == "TRUE":
        status = "True"
    else:
        status = "False"
    put_data = {
        "is_billable": billable,
        "is_billed": status,
        "date": row["date"],
        "hours": row["hours"],
        "rate": row["rate"],
        "description": row["description"],
        "account_ref": {
          "id": row["account_ref"],
        },
        "matter_ref": {
          "id": row["matter_ref"],
        },
        "billed_by_user_ref": {
          "id": row["billed_by_user_ref"],
        }
      }
    
    if put_data == {}:
        next
    else:
        put_data_json = json.dumps(put_data)
        try:
            response = requests.request("PUT", url + "timeentries?id=" + TeID, data=put_data_json, headers=headers)
            next
            reponse_body = json.loads(response.text)
            if response.status_code == 200:
                print("Processing row " + str(line_count) + ": Time Entry successfully updated") #posting data and printing the response
                next
            elif response.status_code == 401:
                print("Access Token expired, please re-start the app")
                break
            else:
                gsd.new_error("The request returned the following error: " + str(reponse_body['modelState']))
        except Exception as err:
            exception_type = type(err).__name__
            gsd.new_error(exception_type)
            next
    
    all_errors = gsd.get_errors()

    if all_errors == []:
        next
    else:
        EF.error = pd.Series({'Error': '\n'.join(all_errors)})
        other_columns = EF.error.append(orig_f.loc[line_count-1])
        err_f = err_f.append(other_columns,ignore_index=True)
        print("Row number " + str(line_count) + " has the following erros: " + str(all_errors))
        gsd.clear_errors()

    put_data.clear()    
    
    time.sleep(0.15)

print(str(line_count) + " rows were processed on file " + EF.filename)


while True:
  try:
    export_csv = err_f.to_csv(filedialog.askdirectory() + "\TimeEntryErrors.csv", index = None, header=True)
    break
  except:
    continue