import os
import http.client
import json
import base64

import googleapiclient.discovery
from graphqlclient import GraphQLClient
from retrying import retry

from rm_sdk.storage import GoogleCloudStorage


GRAPHQL_API_URL_ENV = 'RM_GRAPHQL_API_URL'
AUTH0_CONFIG_URI = 'gs://rm-config/auth0-stg.json.enc'

def retry_if_exception(exception):
    print("Got some exception during HTTP request from rm-sdk. Retrying..")
    return True

@retry(retry_on_exception=retry_if_exception, stop_max_attempt_number=3, wait_random_min=1000, wait_random_max=2000)
def get_auth0_config(project_id='tvlk-data-dev-179204',location_id="global",
                key_ring_id='rm-config', crypto_key_id='rm-config'):
    storage = GoogleCloudStorage(AUTH0_CONFIG_URI)
    blob = storage.get_artifact()
    kms_client = googleapiclient.discovery.build('cloudkms', 'v1')
    name = 'projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}'.format(
        project_id, location_id, key_ring_id, crypto_key_id)
    ciphertext = blob.download_as_string()
    crypto_keys = kms_client.projects().locations().keyRings().cryptoKeys()
    request = crypto_keys.decrypt(
        name=name,
        body={'ciphertext': base64.b64encode(ciphertext).decode('ascii')})
    response = request.execute()
    plaintext = base64.b64decode(response['plaintext'].encode('ascii'))
    return json.loads(plaintext)


@retry(retry_on_exception=retry_if_exception, stop_max_attempt_number=3, wait_random_min=1000, wait_random_max=2000)
def get_auth0_token():
    auth0_data = get_auth0_config()
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
