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

gsd.get_contacts()
response = requests.request("GET", url + "accounts", headers = headers)
accounts = json.loads(response.text)

Tk().withdraw()
filename = askopenfilename()

with open(filename) as csvfile:
    csv_reader = csv.DictReader(csvfile)
    line_count = 1
    for row in csv_reader:
      if line_count == 1:
          print(f'Column names are {", ".join(row)}')
          line_count += 1
      
        
      line_count += 1
      account = gsd.EventSearchC(row["Contact: Number"])
      primary = gsd.RelSearchPrimary(row["Contact: Number"])
      #User = gsd.EventSearchU(row["Contact: AssignedTo"])
      
      #tags_string = row["Contact: Tags"]
      #tags_list = tags_string.split(",")
      #response = requests.request("GET", url + "accounts/" + account, headers = headers)
      
      #print(response.text)
      
      put_data = {
        "id": account,
        "number": row["Contact: Number"],
        "company_name": row["Contact: CompanyName"],
        "address_street_1": row["Contact: Street1"],
        "address_street2": row["Contact: Street2"],
        "address_city": row["Contact: City"],
        "address_state": row["Contact: ProvinceState"],
        "address_country": row["Contact: Country"],
        "address_zip_code": row["Contact: ZipPostalCode"],
        #"tags": tags_list,
        "assigned_to_users": [
            {
                "id": "87c48729-4ed6-40a0-95ef-c79184893f90",
            }
        ],
        #"notes": row["Contact: CompanyNotes"],
        "primary_contact": {
            "id": primary,
            "account_ref": {
            "id": account
            },
            "is_primary_contact": True,
            "first_name": row["Contact: FirstName"],
            "last_name": row["Contact: LastName"],
            "phone_home": row["Contact: HomeNumber"],
            "phone_mobile": row["Contact: MobileNumber"],
            #"phone_fax": row["Contact: FaxNumber"],
            "phone_ work": row["Contact: OfficeNumber"],
            #"email": row["Contact: Email"],
            "custom_field_values": [
              {
                "custom_field_ref": {
                  "id": "8208e6c4-1dc0-413c-a919-db785c8192fe",
                  "label": "Prefix",
                  "value_type": "TextBox"
                },
                "value_string": row["Contact: Prefix"]
              },
              {
                "custom_field_ref": {
                  "id": "c78f21e2-7286-491e-9b49-5e749f70635e",
                  "label": "Type",
                  "value_type": "DropDownList"
                },
                "value_string": row["Contact: Type"]
              },
              {
                "custom_field_ref": {
                  "id": "07a1e8c5-0030-4091-9c3e-97a62776bb51",
                  "label": "Other Phone",
                  "value_type": "TextBox"
                },
                "value_string": row["Contact: Other Phone"]
              },
              {
                "custom_field_ref": {
                  "id": "07a1e8c5-0030-4091-9c3e-97a62776bb51",
                  "label": "Other Info",
                  "value_type": "TextBox"
                },
                "value_string": row["Contact: Other Info"]
              }
            ]
          }
      }
          
      time.sleep(0.25)
      if put_data == {}:
          next
      else:
          put_data_json = json.dumps(put_data)                                                                    
          
          response = requests.request("PUT", url + "accounts?id=" + account, data=put_data_json, headers=headers)
          reponse_body = json.loads(response.text)
          if response.status_code == 200:
              print("Contact Successfully updated " + str(line_count))
              next
          else:
              print("The request returned the following error: " + str(reponse_body['modelState']))