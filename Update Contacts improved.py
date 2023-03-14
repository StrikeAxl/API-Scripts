# -*- coding: utf-8 -*-
"""
Created on Wed Jan 8 21:15:55 2020

@author: Axel
"""

import requests
import json
import time
import get_search_data as gsd
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

url = "https://app.practicepanther.com/api/v2/"
headers = gsd.get_headers()
acces_token = gsd.get_token()

url2 = "https://app.practicepanther.com/api/v2/matters?account_tag="

response = requests.request("GET", url + "accounts", headers = headers)
# with open('account_response.json', 'r') as jsonfile:
#     response_text = jsonfile.read()
# with open('account_response.json', 'w') as jsonfile:
#     json.dump(response.text, jsonfile)
response_text = response.text
# accounts = pd.read_json(response_text, dtype=str)
#accounts = pd.read_csv("Accounts.csv", index_col=None)
accounts = json.loads(response_text)
Tk().withdraw()
filename = askopenfilename()
#file2 = askopenfilename()
file = pd.read_csv(filename, index_col = "Guid")
errors = []

updatedNickname = []

for c in range(len(accounts)):
    try:
        account = accounts[c]
        accountId = account["id"]
        if accountId not in file.index:
            continue
        #company = file.loc[accountId]["Contact: CompanyName"]
        firstName = file.loc[accountId]["Contact: FirstName"]
        lastName = file.loc[accountId]["Contact: LastName"]
        
        # try:
        #     nickname = file.loc[account["number"].astype(int)]["CliNickName"]
        # except:
        #    pass
        account["primary_contact"]["first_name"] = firstName
        account["primary_contact"]["last_name"] = lastName
        #account["primary_contact"]["email"] = file.loc[account["primary_contact"]["id"]]["Contact: Email"]
        #account["other_contacts"] = []
        #account["number"] = account["number"].astype(int)
        #account.dropna(inplace=True)
        Id = account["id"]
        #account = account.to_dict()
        # for key in account.keys():
        #     try:
        #         if type(account[key])
        #     except:
        #         continue
        account = json.dumps(account)
        updatedNickname.append(account)
        response = requests.request("PUT", url + "accounts?id=" + str(Id), data=account, headers=headers)
        response_body = json.loads(response.text)
        if response.status_code == 200:
            print('Successful update ' + str(c))
        else:
            try:
                new_error = response.reason + " " +  response_body['modelState']
                errors.append(new_error)
            except:
                new_error = response.reason + " " +  response_body['message'] 
                pass
    except:
        print("error in contact " + firstName)
        errors.append(str(firstName))
        pass
    time.sleep(0.1)
df = pd.DataFrame(errors)
df.to_csv('errors.csv')