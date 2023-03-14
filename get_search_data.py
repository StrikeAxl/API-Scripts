import requests
import json
#import getting_access


url = "https://app.practicepanther.com/api/v2/"

#access_token = getting_access.get_token()
access_token = "HPk_4C4GSutxgi-ahEFq5_njCmhiFHEeg9TTxmVAEq_cK8W-dzaQTA1LqaS1oyWSGnfDJHIcy4Uidgo2dOgx8IQ4CzRpC-2GfN2LrvaQsJ1EIlB63AXiSXKAYpO7tMkjQa2DIbhqMnLFtNs4kSZuHU8YZjCHAbsooibuXPCfZkU_WTjdrfI_5ZlCsk9H51RihjtzmEGttMMTzp85qwY52GNf_JuWx7QwXTdoal-zRB_F5bbo7wXz4r-oijh2PH4W2MT-2eWPyMtt8eCqB652fkHs38dqhXp7f5GJW1S5KhG83SUMgXpWPUjVKnRyIR3JUrJOywy86dXp1qjnNAQz52Iy6L6-S9d9EImQIKc2tUrCLfeN9bZboY5_2Qqd-YKaQZEgh-6Px4tG1b4lTCpcjJN44Js5fJGILtdoRZ0w1LSaZGeoY37482-7TeUn23wUacQ3cUWev0s1g0I45f4OcPfaUUryNbl_GRWn-n3trVfdKEgdfptYb5BfmOvUWyYzIpB4sM5ityJQ44bKSmd1TKVPcmb7k2gly71eB6b1pqy3bD7wqwA0fVyoI1o2WLAB"

def get_token():
  return access_token

headers = {
   'Authorization': "Bearer " + access_token,
   'Accept': "/",
   'Content-Type': "application/json",
   'Cache-Control': "no-cache",
   'Host': "app.practicepanther.com",
   'Accept-Encoding': "gzip, deflate",
   'Connection': "keep-alive",
   'cache-control': "no-cache"
    }
def get_headers():
  return headers

matter_numbers = {}
contact_numbers = {}
displayName_ids = {}
user_ids = {}
indexes = {}
exp_category = {}
primary_contact = {}
time_items = {}
errors = []
timeGuids = []
contactsByMatterIds = {}
contact_accountIds = {}

#This function returns a dictionary of Matter Numbers with Matters ID (references)
def get_matters():
  response = requests.request("GET", url + "matters", headers=headers)
  matters = json.loads(response.text)
  if response.status_code == 200:
    for matter in matters:  #parsing the response
        number = {            
          matter['number']:  matter['id'] #building dictionary "number" with matter number and id only from my json response
        }
        matter_numbers.update(number)  #updating global dictionary "numbers" with whatever "number" receives
      
      #index = {
        #matter['number']: matter['account_ref']['id']
      #}
      #contactsByMatterId = {
      #matter['id']: matter['account_ref']['id']    
      #}
      #indexes.update(index)
      #contactsByMatterIds.update(contactsByMatterId)
      
    return matter_numbers
  else:
    errors.append("Error: The request failed with status code " + str(response.status_code))
    
def get_account_primaryContactID():
    response = requests.request("GET", url + "accounts", headers = headers)
    accounts = json.loads(response.text)
    if response.status_code == 200:
        for account in accounts:
            contact_accountId = {
                #contact['id']:contact['account_ref']['id']
                account['id']:account['primary_contact']['id']
                }
            contact_accountIds.update(contact_accountId)
        return contact_accountIds
    else:
        errors.append("Error: The request failed with status code " + str(response.status_code))
        
def get_contactID_accountRef():
    response = requests.request("GET", url + "contacts", headers = headers)
    contacts = json.loads(response.text)
    conID_accRef = {}
    if response.status_code == 200:
        for contact in contacts:
            contactID_accountID = {
                contact['id']:contact['account_ref']['id']
                }
            conID_accRef.update(contactID_accountID)
        return conID_accRef
    else:
        errors.append("Error: The request failed with status code " + str(response.status_code))


def accountSearchByContactID(contactID):
    accountID = contact_accountIds[contactID]
    return accountID
    
def get_timeGuids():
    response = requests("GET", url + "timeentries", headers=headers)
    timeEntries = json.loads(response.text)
    if response.status_code == 200:
        for timeEntry in timeEntries:
            timeGuids.append(timeEntry["Id"])
        
#This function returns a dictionary of Contact Numbers with Contacts ID (references)
def get_accounts():
  response = requests.request("GET", url + "accounts", headers = headers)
  contacts = json.loads(response.text)
  if response.status_code == 200:
    for contact in contacts:
      number = {
        contact['number']: contact['id']
        #contact['display_name']: contact['id']
      }
      primary = {
        contact['number']: contact['primary_contact']['id']
      }
      #primary = {
          #contact['id']: contact['primary_contact']['id']
          #}
      contact_numbers.update(number)
      primary_contact.update(primary)
    return contact_numbers
  else:
    errors.append("Error: The request failed with status code " + str(response.status_code))
    
def get_primConID_byNumber():
    response = requests.request("GET", url + "accounts", headers = headers)
    contacts = json.loads(response.text)
    if response.status_code == 200:
        for contact in contacts:
          primary = {
            contacts['number']: contacts['primary_contact']['id']
          }
          contact_numbers.update(primary)
        return contact_numbers
    else:
        errors.append("Error: The request failed with status code " + str(response.status_code))
    
def get_displayName_Id():
  response = requests.request("GET", url + "accounts", headers = headers)
  accounts = json.loads(response.text)
  if response.status_code == 200:
    for account in accounts:
      number = {
        account['display_name']: account['id']
      }
      displayName_ids.update(number)
    return displayName_ids
  else:
    errors.append("Error: The request failed with status code " + str(response.status_code))

#This function returns a dictionary of User email with User ID (references)
def get_users():
  response = requests.request("GET",url + "users", headers = headers)
  users = json.loads(response.text)
  if response.status_code == 200:
    for user in users:
      users_string = str(user['email']).lower()
      #users_string = str(user['display_name'])
      user_id = {
        users_string: user['id']
      }
      user_ids.update(user_id)
  else:
    errors.append("Error: The request failed with status code " + str(response.status_code))

#This function returnts a dictionary of Category Name and the category ID (reference)
def get_categories():
  response = requests.request("GET",url + "ExpenseCategories", headers = headers)
  category = json.loads(response.text)
  for categories in category:
    exp_cat = {
      categories['name']: categories['id']
    }
    exp_category.update(exp_cat)

def TimeGet_items():
  response = requests.request("GET",url + "Items", headers = headers)
  item = json.loads(response.text)
  for items in item:
    time_item = {
      items['code']: items['id']
    }
    time_items.update(time_item)


#function that receives the matter number as parameter from the excel file
def EventSearchM(mNumber):
    if mNumber == "":
      return ""
    else:
      try:
          mID = matter_numbers[int(mNumber)]  # to lookup a value in a dictionary just pass the key (matter Number)
          return mID  #function returns the reference/ID the dictionary returned
      except:
        errors.append("Error: Matter number doesn't exist, please try getting the correct matter number, otherwise, leave it empty.")
        #print("Processing row #" + str(line_count) + ": Error: Matter number doesn't exist, please try getting the correct matter number, otherwise, leave it empty.")
        return None
            

def EventSearchC(cNumber):
    if cNumber == "":
        return ""
    else:
        try:
            cID = contact_numbers[int(cNumber)]
            return cID
        except:
            errors.append("Error: Contact Number doesn't exist. please try getting the correct contact number, otherwise, leave it empty.")
           # print("Processing row #" + str(line_count) + ": Error: Contact Number doesn't exist. please try getting the correct contact number, otherwise, leave it empty.")
            return None
            

def EventSearchU(email):
    if email == "":
        errors.append("User's email address is required")
        return None
    elif email != "":
      uID = []
      user_list = email.split(",")
      for users in user_list:
        try:
          user = {
              "id": user_ids[users]
          }
          uID.append(user)
          isError = False
        except:
          errors.append("User " + users + " not found, please make sure the email address is correct.")
          isError = True
          continue
      if isError == False:
        return uID
      else:
        return None
            
            
def ExpSearchC(mNumber):
  if mNumber == "":
    return None
  else:
    try:
      cID = indexes[int(mNumber)]
      return cID
    except:
      pass

def ExpSearchContactById(mNumber):
  if mNumber == "":
    return None
  else:
    try:
      cID = contactsByMatterIds[mNumber]
      return cID
    except:
      pass

def ExpSearchM(mNumber): #function that receives the matter number as parameter
  if mNumber == "":
    # print("Error in row " + str(line_count) + ": Matter number is required")
    errors.append("Error: Matter number is required")
    return None
  else:
    try:
      mID = matter_numbers[int(mNumber)]  # to lookup a value in a dictionary just pass the key (matter Number)
      return mID  #function returns the reference/ID the dictionary returned
    except:
      errors.append("Error: Matter number does not exist, please make sure the number is correct")
      return None


def ExpSearchU(email):
    if email == "":
      errors.append("Error: user's email address is required")    
     # print("Error in row " + str(line_count) + ": user's email address is required")
      return None
    else:
        try:
            uID = user_ids[email]
            return uID
        except:
            errors.append("Error: user not found, please make sure the email address is correct.")
            return None
    

def ExpSearch_categories(names):
  if names == "":
    return ""
  else:
    try:
      catID = exp_category[names]
      return catID
    except:
      errors.append("Error: category name is invalid, please correct it or leave it empty")
      return None

def RelSearchC(cNumber):
    if cNumber == "":
        errors.append("Error: Contact Number is required")
        return None
    else:
        try:
            cID = contact_numbers[int(cNumber)]
            return cID
        except:
            errors.append("Error: Contact Number doesn't exist.")
            return None

def RelSearchPrimary(cNumber):
    try:
        pcID = primary_contact[int(cNumber)]
        return pcID 
    except:

        pass

def TimeSearch_items(codes):
  if codes == "":
    return ""
  else:
    try:
      itemID = time_items[codes]
      return itemID
    except:
      errors.append("Error: item name is invalid, please correct it or leave it empty")
      return None
      
def new_error(modelState):
  errors.append(modelState)

def get_errors():
  return errors

def clear_errors():
  errors.clear()
