# -*- coding: utf-8 -*-
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

#response = requests.request("GET", url2 + "Export", headers = headers)
#response_text = response.text
#projects = json.loads(response_text)
#projects.set_index('id', inplace = True)

Tk().withdraw()
filename = askopenfilename()
file2 = askopenfilename()
matters = pd.read_csv(filename, index_col = "GUID")
projects = pd.read_json(file2)
projects.set_index('id', inplace = True)
projects.drop(labels=['created_at', 'updated_at', 'tags'], inplace = True, axis = 1)
errors = []

#updatedNickname = []

for c in range(len(matters)):
    try:
        matter = matters.iloc[c]
        matterGuid = matter.name
        if matterGuid not in projects.index:
            continue
        
        project = projects.loc[matterGuid]
        #project["number"] = matter["Matter: Number"]
        #tagsString = matter["Matter: Tags"]
        #tagsList = tagsString.split(",")
        #project["tags"] = tagsList
        newAccount = matter["account_ref"]
        project["account_ref"] = {"id": newAccount}
        project.dropna(inplace = True)
        newProject = project.to_dict()
        newProject = json.dumps(newProject)
        response = requests.request("PUT", url + "matters?id=" + str(matterGuid), data=newProject, headers=headers)
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
        print("error in matter " + matterGuid)
        errors.append(str(matterGuid))
        pass
    time.sleep(0.1)
df = pd.DataFrame(errors)
df.to_csv('errors.csv')