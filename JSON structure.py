import requests
import json
import time
import get_search_data as gsd
import create_csv_error as EF
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter import filedialog
import firm_support as fs
from swagger_client.models.custom_field_ref import CustomFieldRef
from swagger_client.models.custom_field_value import CustomFieldValue
from swagger_client.models.account_reference import AccountReference
from swagger_client.models.contact_reference import ContactReference
from swagger_client.models.matter import Matter



url = "https://app.practicepanther.com/api/v2/"
url2 = 'https://app.practicepanther.com/api/v2/matters?id='

headers = gsd.get_headers()
acces_token = gsd.get_token()
matterNumbers = gsd.get_matters()
contactNumbers = gsd.get_accounts()
gsd.get_users()

cfInfo = {}
custom_fields = []
accounts_contacts = gsd.get_account_primaryContactID()
contact_accounts = gsd.get_contactID_accountRef()
pPMatterCustomFields = fs.get_matter_custom_fields(headers)
matter_defaults = pd.read_csv('matter_defaults.csv')

Tk().withdraw()
EF.filename = askopenfilename()
orig_f = EF.generate_original_file()
err_f = EF.generate_error_file(orig_f)


original_file = pd.read_csv(EF.filename, index_col=None, dtype=str, encoding='ANSI')

def is_default(field):
    if field in matter_defaults:
        return True
    else:
        return False

for c in range(len(original_file.columns)):
    if not is_default(original_file.columns[c]):
        custom_fields.append(original_file.columns[c])
    else:
        continue
    
for pPMatterCustomField in pPMatterCustomFields:
    cfr = CustomFieldRef(id = pPMatterCustomField["id"], value_type=pPMatterCustomField["value_type"])
    cfInfo.update({"Matter: " + pPMatterCustomField["label"]:cfr})
    
def sep_custom_fields(series):
    """

    :param series: row of the dataframe containing the  data
    :return: list of the custom fields for the file
    """
    custom_fields = []
    keys = series.keys()
    for c in range(len(keys)):
        if not is_default(keys[c]):
            custom_fields.append(keys[c])
        else:
            continue
    return custom_fields
    
def get_custom_field_values(row, cfinfo):
    cfvals = []
    row.dropna(inplace=True)  # get rid of the empty fields to save time
    non_default_fields = sep_custom_fields(row)  # get rid of the default fields
    for c in range(len(non_default_fields)):  # go through all of the custom fields
        try:
            cfv = CustomFieldValue(custom_field_ref=cfinfo[non_default_fields[c]])
            cfobject =  cfinfo[non_default_fields[c]]
            fieldType = cfobject.value_type
            if fieldType == 'TextBox':
                cfv.value_string = row.get(non_default_fields[c])
                cfvals.append(cfv)
            elif fieldType == 'Contact':
                try:
                    #acc_ref = AccountReference(id=accounts_contacts[row.get(non_default_fields[c])])
                    acc_ref = AccountReference(id=row[non_default_fields[c]])
                    con_ref = ContactReference(id=accounts_contacts[row.get(non_default_fields[c])], account_ref=acc_ref)
                    cfv.contact_ref = con_ref
                    cfvals.append(cfv)
                    continue
                except:
                    next
                x  = None    
                if x is None:
                    cfv = CustomFieldValue(custom_field_ref=cfinfo[non_default_fields[c]])
                    cfobject =  cfinfo[non_default_fields[c]]
                    fieldType = cfobject.value_type
                    if fieldType == 'Contact':
                        acc_ref = AccountReference(id=contact_accounts[row.get(non_default_fields[c])])
                        con_ref = ContactReference(id=row.get(non_default_fields[c]), account_ref=acc_ref)
                        cfv.contact_ref = con_ref
                        cfvals.append(cfv)
            elif fieldType == 'Date':
                cfv.value_date_time = row.get(non_default_fields[c])
                cfvals.append(cfv)
            elif fieldType == 'TextEditor':
                cfv.value_string = row.get(non_default_fields[c])
                cfvals.append(cfv)
            elif fieldType == 'DropDownList':
                cfv.value_string = row.get(non_default_fields[c])
                cfvals.append(cfv)
            else:
                next
        except:
            pass  
    return cfvals
line = 1

for r in range(len(original_file)):
    row = pd.Series(original_file.loc[r])
    row.dropna(inplace = True)
    try:
        matterID = matterNumbers[int(row["Matter: Number"])]
    except KeyError:
        gsd.errors.append('Matter Number not found. Please make sure it is correct')
        continue
    try:
        matter = Matter(name = row["Matter: Name"], status=row['Matter: Status'])
    except KeyError:
        gsd.errors.append('No matter name passed! Must pass a matter name.')
        pass
    try:
        matter.account_ref = AccountReference(id=contactNumbers[int(row["Contact: Number"])])
    except Exception as e:
        gsd.errors.append(e)
        pass
    try:
        matter.number = row['Matter: Number']
    except:
        pass

    try:
        matter.notes = row['Matter: Notes']
    except:
        pass

    try:
        matter.open_date = row['Matter: OpenDate']
    except:
        pass

    try:
        matter.close_date = row['Matter: CloseDate']
    except:
        pass

    try:
        matter.statute_of_limitation_date = row['Matter: DueDate']
    except:
        pass

    try:
        matter.tags = row['Matter: Tags'].split(sep=',')
    except:
        pass
    try:
        users = row["Matter: AssignedTo"]
        usersDicts = gsd.EventSearchU(users)
        matter.assigned_to_users = usersDicts
    except:
        pass
    try:
        matter.custom_field_values = get_custom_field_values(row, cfInfo)
    except Exception as e:
        print(e)
        pass
    matter_to_post = matter.to_dict()
    post_data = json.dumps(matter_to_post)
    
    if post_data == {}:
      next
    else:
      #response = requests.request("POST", url + "matters", data=post_data, headers=headers)
      response = requests.request("PUT", url2 + matterID, data = post_data, headers = headers)
      reponse_body = json.loads(response.text)
      if response.status_code == 200:
                print("Processing row " + str(line) + ": Matter successfully uploaded") #posting data and printing the response
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
      other_columns = EF.error.append(orig_f.loc[line-1])
      err_f = err_f.append(other_columns,ignore_index=True)
      print(all_errors)
      gsd.clear_errors()

    post_data = ""
    line += 1
    time.sleep(0.2)

print(str(line) + " rows were processed on file " + EF.filename)


while True:
  try:
    export_csv = err_f.to_csv(filedialog.askdirectory() + "\MatterErrors.csv", index = None, header=True)
    break
  except:
    continue
