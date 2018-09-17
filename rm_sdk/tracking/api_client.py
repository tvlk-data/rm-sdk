from rm_sdk.api_client import RMGraphQLClientBase


class RMTrackingClient(RMGraphQLClientBase):
    
    def sync_params(self, params):
        query = '''
            mutation AddModelParam($modelParams: [ModelParamInput]) {
                addModelParam(
                    params: $modelParams
                )
            }
        '''
        return self.execute(query, params)