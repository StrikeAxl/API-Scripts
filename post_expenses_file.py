import requests
import json
import csv
import time
import get_search_data as gsd
from tkinter import Tk
from tkinter.filedialog import askopenfilename

url = "https://app.practicepanther.com/api/v2/"
headers = gsd.get_headers()
acces_token = gsd.get_token()
gsd.get_matters() #call function to get the matters
gsd.get_users()
gsd.get_categories()

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

    contact = gsd.ExpSearchC(row["matter_ref"])
    matter = gsd.ExpSearchM(row["matter_ref"]) #calls search function which receives what the spreadsheet has in that column as param and returns the matter ref and assigns it to "matter"
    user = gsd.ExpSearchU(row["billed_by_user_ref"])
    expense_category = gsd.ExpSearch_categories(row["expense_category_ref"])

    if matter is None or user is None or matter == user == None:
      continue
    elif expense_category is None:
      continue
    elif expense_category == "":
      post_data = {
        "is_billable": row["is_billable"],
        "is_billed": row["is_billed"],
        "date": row["date"],
        "qty": row["qty"],
        "price": row["price"],
        "description": row["description"],
        "private_notes":row["private_notes"],
        "matter_ref": {
          "id": matter
        },
        "account_ref":{
          "id": contact
        },
        "billed_by_user_ref": {
          "id": user
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
        "private_notes":row["private_notes"],
        "matter_ref": 
          {
          "id": matter
          },
        "account_ref":
          {
          "id": contact
          },
        "billed_by_user_ref": 
          {
          "id": user
          },
        "expense_category_ref": 
          {
          "id": expense_category
          }
        }

    post_data_json = json.dumps(post_data) 
    response = requests.request("POST", url + "Expenses", data=post_data_json, headers=headers)
    reponse_body = json.loads(response.text)
    try:
      print("The request returned the following error on row " + str(line_count) + ": " + str(reponse_body['message']) + str(reponse_body['modelState']))
    except:
      print("Processing row #" + str(line_count) + ": Expense successfully uploaded")
    pass
print(str(line_count-1) + " rows were processed")