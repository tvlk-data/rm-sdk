import http.client
import json
from retrying import retry


def retry_if_exception(exception):
    print("Got some exception during HTTP request from rm-sdk. Retrying..")
    return True


@retry(retry_on_exception=retry_if_exception, stop_max_attempt_number=3, wait_random_min=1000, wait_random_max=2000)
def get_auth0_token(auth0_data):
    AUTH0_DOMAIN = auth0_data['domain']
    AUTH0_RESOURCE_SERVER = auth0_data['audience']
    AUTH0_CLIENT_ID  = auth0_data['client_id']
    AUTH0_CLIENT_SECRET = auth0_data['client_secret']

    conn = http.client.HTTPSConnection(AUTH0_DOMAIN)
    payload = "{\"client_id\":\"%s\",\"client_secret\":\"%s\",\"audience\":\"%s\",\"grant_type\":\"client_credentials\"}" \
               % (AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_RESOURCE_SERVER)
    headers = { 'content-type': "application/json" }
    conn.request("POST", "/oauth/token", payload, headers)
    res = conn.getresponse()
    data = res.read()
    dataDict = json.loads(data.decode('utf-8'))
    return dataDict['access_token']