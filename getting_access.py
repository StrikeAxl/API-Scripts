import requests
import json
import webbrowser

authorize_url = "https://app.practicepanther.com/OAuth/Authorize"
token_url = "https://app.practicepanther.com/oauth/token"
#callback url specified when the application was defined
callback_uri = "https://localhost:8000"
#client (application) credentials
client_id = '18a8f1d9-5b2d-491d-bc7c-679edd5650df'
client_secret = '3998ae2f-2b55-42a0-8030-c64976fb787e'
#step A - simulate a request from a browser on the authorize_url - will return an authorization code after the user is
# prompted for credentials.
authorization_redirect_url = authorize_url + '?response_type=code&client_id=' + client_id + '&redirect_uri=' + callback_uri + '&state=random'
webbrowser.open(authorization_redirect_url)
authorization_code = input('Enter the code: ')

#Turn the authorization code into a access token, etc
data = {'grant_type': 'authorization_code', 'code': authorization_code, 'redirect_uri': callback_uri}
print ("requesting access token")
access_token_response = requests.post(token_url, data=data, auth=(client_id, client_secret))

# we can now use the access_token as much as we want to access protected resources.
tokens = json.loads(access_token_response.text)
access_token = tokens['access_token']
print ("access token: " + access_token)
#function to get the token
def get_token():
    return access_token