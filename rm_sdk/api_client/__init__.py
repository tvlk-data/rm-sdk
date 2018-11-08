import os
import http.client
import json

from graphqlclient import GraphQLClient
from retrying import retry


GRAPHQL_API_URL_ENV = 'RM_GRAPHQL_API_URL'

def retry_if_exception(exception):
    print("Got some exception during HTTP request from rm-sdk. Retrying..")
    return True

@retry(retry_on_exception=retry_if_exception, stop_max_attempt_number=3, wait_random_min=1000, wait_random_max=2000)
def get_auth0_token():
    AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
    AUTH0_RESOURCE_SERVER = os.getenv('AUTH0_RESOURCE_SERVER')
    AUTH0_CLIENT_ID  = os.getenv('AUTH0_CLIENT_ID')
    AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')

    conn = http.client.HTTPSConnection(AUTH0_DOMAIN)
    payload = "{\"client_id\":\"%s\",\"client_secret\":\"%s\",\"audience\":\"%s\",\"grant_type\":\"client_credentials\"}" \
               % (AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_RESOURCE_SERVER)
    headers = { 'content-type': "application/json" }
    conn.request("POST", "/oauth/token", payload, headers)
    res = conn.getresponse()
    data = res.read()
    dataDict = json.loads(data.decode('utf-8'))
    return dataDict['access_token']

class RMGraphQLClientBase(object):
    base_url = None
    client   = None

    def __init__(self, base_url=os.getenv(GRAPHQL_API_URL_ENV), token=None):
        self.base_url = base_url
        self.client = GraphQLClient(self.base_url)

        if not token:
            token = get_auth0_token()
        bearer_token = 'Bearer '+ token
        
        self.client.inject_token(bearer_token)

    
    @retry(retry_on_exception=retry_if_exception, stop_max_attempt_number=3, wait_random_min=1000, wait_random_max=2000)
    def execute(self, query, variable=None):
        resp = self.client.execute(query, variable)
        return resp
    
    def __str__(self):
        return "Raring Meerkat GraphQL client with endpoint %s" % self.base_url
