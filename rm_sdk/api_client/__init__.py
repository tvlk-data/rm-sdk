import os
from graphqlclient import GraphQLClient

GRAPHQL_API_URL_ENV = 'RM_GRAPHQL_API_URL'


class RMGraphQLClientBase(object):
    base_url = None
    client   = None

    def __init__(self, base_url=os.getenv(GRAPHQL_API_URL_ENV)):
        self.base_url = base_url
        self.client = GraphQLClient(self.base_url)
    

    def execute(self, query, variable=None):
        return self.client.execute(query, variable)
    
    def __str__(self):
        return "Raring Meerkat GraphQL client with endpoint %s" % self.base_url
