from rm_sdk.api_client import RMGraphQLClientBase


class RMTrackingClient(RMGraphQLClientBase):
    
    def get_run_history(self, runId):
        query = '''
            query {
                getRunHistoryById(id:"%s") {
                    id
                    model {
                        name
                    }
                }
            }
        ''' % (runId)
        
        return self.execute(query)

    def sync_model_run(self, modelRun):
        query = '''
            mutation UpdateRunHistory($id:String!, $startTime:Date, $endTime:Date, $status:RunStatus){
                updateRunHistory(
                    id: $id
                    startTime: $startTime
                    endTime: $endTime
                    status: $status
                ){
                    id
                }
            }
        '''

        return self.execute(query, modelRun)

        
    def sync_params(self, params):
        query = '''
            mutation AddModelParam($modelParams: [ModelParamInput]) {
                addModelParam(
                    params: $modelParams
                )
            }
        '''
        return self.execute(query, params)
    

    def sync_metrics(self, metrics):
        query = '''
            mutation AddModelMetric($modelMetrics: [ModelMetricInput]) {
                addModelMetric(
                    metrics: $modelMetrics
                )
            }
        '''
        return self.execute(query, metrics)
    
    def delete_all_params_by_runId(self, runId):
        query = '''
            mutation{
                deleteAllParamsByRunId(runId: "%s")
            }
            ''' % runId
        return self.execute(query)
    
    def delete_all_metrics_by_runId(self, runId):
        query = '''
            mutation{
                deleteAllMetricsByRunId(runId: "%s")
            }
            ''' % runId
        return self.execute(query)



tracker = RMTrackingClient()