import os

from graphqlclient import GraphQLClient
from retrying import retry

GRAPHQL_API_URL_ENV = 'RM_GRAPHQL_API_URL'


def retry_if_exception(exception):
    print("Got some exception while trying to send data to the server from rm-sdk. Retrying..")
    return True


class RMGraphQLClientBase(object):
    base_url = None
    client   = None

    def __init__(self, base_url=os.getenv(GRAPHQL_API_URL_ENV)):
        self.base_url = base_url
        self.client = GraphQLClient(self.base_url)
    
    @retry(retry_on_exception=retry_if_exception, stop_max_attempt_number=3, wait_random_min=1000, wait_random_max=2000)
    def execute(self, query, variable=None):
        resp = self.client.execute(query, variable)
        return resp
    
    def __str__(self):
        return "Raring Meerkat GraphQL client with endpoint %s" % self.base_url
