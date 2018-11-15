import os
import http.client
import json
import base64

import googleapiclient.discovery
from graphqlclient import GraphQLClient
from retrying import retry

from rm_sdk.storage import GoogleCloudStorage
from rm_sdk.utils.http_utils import retry_if_exception


class RMGraphQLClientBase(object):
    base_url = None
    client   = None

    def __init__(self, base_url, token=None):
        self.base_url = base_url
        self.client = GraphQLClient(self.base_url)

        if token:
            bearer_token = 'Bearer '+ token
            self.client.inject_token(bearer_token)

    
    @retry(retry_on_exception=retry_if_exception, stop_max_attempt_number=3, wait_random_min=1000, wait_random_max=2000)
    def execute(self, query, variable=None):
        resp = self.client.execute(query, variable)
        return resp
    
    def __str__(self):
        return "Raring Meerkat GraphQL client with endpoint %s" % self.base_url
