from datetime import datetime
import time


class Param(object):
    runId = None
    paramKey = None
    paramValue = None
    generatedAt = None

    def __init__(self, runId, key, val, generatedAt = None):
        self.runId = runId
        self.paramKey = key
        self.paramValue = val
        self.generatedAt = generatedAt if generatedAt else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def get_dict(self):
        ret_dict = {
            'runId': self.runId,
            'paramKey': self.paramKey,
            'paramValue': self.paramValue,
            'generatedAt': self.generatedAt
        }
        
        return ret_dict
    
    def __str__(self):
        return "Parameter with key %s and value %s" % (self.paramKey, self.paramValue)


class ParamList(object):
    
    runId = None
    params = []

    def __init__(self, runId, params=[]):
        self.runId = runId
        self.params = params
    
    def add(self, key, val):
        param = Param(self.runId, key, val)
        self.params.append(param)
    
    def get_graphql_body(self):
        ret = {
            "modelParams": [param.get_dict() for param in self.params]
        }
        return ret


class ModelRun(object):
    runId = None
    startTime = None
    endTime = None

    metrics = []
    params  = None

    def __init__(self, runId):
        self.runId = runId
        self.params = ParamList(runId)
    
    def start(self):
        self.startTime = time.time()
    
    def end(self):
        self.endTime = time.time()

    def sync(self):
        ''' Sync data to the server '''
        pass

    def log_param(self, key, val):
        self.params.add(key, val)
    
    def __enter__(self):
        self.start()
    
    def __exit__(self, *args):
        self.end()
        self.sync()