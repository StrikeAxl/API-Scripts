import requests
import json
import csv
import time
from datetime import datetime
import get_search_data as gsd
import create_csv_error as EF
import pandas as pd
from tkinter import Tk, filedialog, messagebox
from tkinter.filedialog import askopenfilename

url = "https://app.practicepanther.com/api/v2/"
headers = gsd.get_headers()
acces_token = gsd.get_token()

gsd.get_contacts()
gsd.get_matters() #call function to get the matters
gsd.get_users()

Tk().withdraw()
EF.filename = askopenfilename()
orig_f = EF.generate_original_file()
err_f = EF.generate_error_file(orig_f)

with open(EF.filename, encoding = 'ANSI') as csvfile:

    csv_reader = csv.DictReader(csvfile)
    line_count = 0
    for row in csv_reader:
        
        post_data = {}
        line_count += 1
        tags_string = row["tags"]
        tags_list = tags_string.split(",")

        account = gsd.EventSearchC(row["account_ref"])
        matter = gsd.EventSearchM(row["matter_ref"])
        user = gsd.EventSearchU(row["assigned_to_users"])

        try:
            original_duedate = row["due_date"]
            date_time = datetime.strptime(original_duedate, "%m/%d/%Y")
            new_date = date_time.strftime("%Y-%m-%dT%H:%M:%S")
            new_due_date = new_date + "-04:00"
        except:
            print("Error in row" + str(line_count) + ": Due Date is invalid")
            next

        if matter is None or user is None or account is None or account == matter == user == None:
            next
        elif account == "" and matter == "":
            post_data = {
                "subject": row["subject"],
                "notes": row["notes"],
                "status": row["status"],
                "due_date": new_due_date,
                "assigned_to_users": user,
                "tags": tags_list
            }
        elif matter == "":
            post_data = {
                "account_ref": {
                    "id": account
                },
                "subject": row["subject"],
                "notes": row["notes"],
                "status": row["status"],
                "due_date": new_due_date,
                "assigned_to_users": user,
                "tags": tags_list
            }
        elif account == "":
            post_data = {
                "matter_ref": {
                    "id": matter
                },
                "subject": row["subject"],
                "notes": row["notes"],
                "status": row["status"],
                "due_date": new_due_date,
                "assigned_to_users": user,
                "tags": tags_list
            }
        else:
            post_data = {
                "account_ref": {
                    "id": account
                },
                "matter_ref": {
                    "id": matter
                },
                "subject": row["subject"],
                "notes": row["notes"],
                "status": row["status"],
                "due_date": new_due_date,
                "assigned_to_users": user,
                "tags": tags_list
        }
            
        if post_data == {}:
            next
        else:
            try:
                post_data_json = json.dumps(post_data)
                response = requests.request("POST", url + "tasks", data=post_data_json, headers=headers)
                reponse_body = json.loads(response.text)
                if response.status_code == 200:
                    print("Processing row " + str(line_count) + ": Task successfully uploaded") #posting data and printing the response
                    next
                elif response.status_code == 401:
                    print("Access Token expired, please re-start the app")
                    break
                else:
                    gsd.new_error("The request returned the following error: " + str(reponse_body['modelState']))
    
                all_errors = gsd.get_errors()
            except:
                print("encoding error")
                all_errors.append("Enconding error")
                next

        if all_errors == []:
            next
        else:
            EF.error = pd.Series({'Error': '\n'.join(all_errors)})
            other_columns = EF.error.append(orig_f.loc[line_count-1])
            err_f = err_f.append(other_columns,ignore_index=True)
            print("Row number " + str(line_count) + " has the following erros: " + str(all_errors))
            gsd.clear_errors()

        post_data.clear()    
        
        time.sleep(0.10)
        
print(str(line_count-1) + " rows were processed on file " + EF.filename)

while True:
    try:
        export_csv = filedialog.askdirectory()
        err_f.to_csv(export_csv + "\AllTasksErrors.csv", index = None, header=True)
        break
    except:
        if(export_csv == ""):
            answer = messagebox.askyesno("Warning", "Do you want to close the program without saving the error file?")
            if answer:
                messagebox.showwarning("Message", "Error file not saved")
                break
            else:
                continue
        else:
            messagebox.showerror("Error", "Error saving file, file is open. Please close it and try again.")
            continue