from datetime import datetime
import time

from rm_sdk.tracking.api_client import tracker
from rm_sdk.logger import logger


class BaseEntity(object):

    def get_graphql_body(self):
        raise NotImplementedError


class Param(BaseEntity):
    runId = None
    paramKey = None
    paramValue = None
    generatedAt = None

    def __init__(self, runId, key, val, generatedAt = None):
        self.runId = runId
        self.paramKey = key
        self.paramValue = val
        self.generatedAt = generatedAt if generatedAt else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def get_graphql_body(self):
        ret_dict = {
            'runId': self.runId,
            'key': str(self.paramKey),
            'value': str(self.paramValue),
            'generatedAt': self.generatedAt
        }
        
        return ret_dict
    
    def __str__(self):
        return "Parameter with key %s and value %s" % (self.paramKey, self.paramValue)


class ParamList(BaseEntity):
    
    runId = None
    params = []

    def __init__(self, runId, params=[]):
        self.runId = runId
        self.params = params
    
    def add(self, key, val):
        param = Param(self.runId, key, val)
        self.params.append(param)
    

    def sync(self):
        if not self.params:
            logger.info("No params available")
            return
        
        logger.info("syncing param data to server")
        resp = tracker.sync_params(self.get_graphql_body())

    def get_graphql_body(self):
        ret = {
            "modelParams": [param.get_graphql_body() for param in self.params]
        }
        return ret


class Metric(BaseEntity):
    runId = None
    metricKey = None
    metricValue = None
    generatedAt = None

    def __init__(self, runId, key, val, generatedAt = None):
        self.runId = runId
        self.metricKey = key
        self.metricValue = val
        self.generatedAt = generatedAt if generatedAt else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def get_graphql_body(self):
        ret_dict = {
            'runId': self.runId,
            'key': str(self.metricKey),
            'value': str(self.metricValue),
            'generatedAt': self.generatedAt
        }
        
        return ret_dict
    
    def __str__(self):
        return "Metric with key %s and value %s" % (self.metricKey, self.metricValue)


class MetricList(BaseEntity):
    
    runId = None
    metrics = []

    def __init__(self, runId, metrics=[]):
        self.runId = runId
        self.metrics = metrics
    
    def add(self, key, val):
        metric = Metric(self.runId, key, val)
        self.metrics.append(metric)
    

    def sync(self):
        if not self.metrics:
            logger.info("no metrics available")
            return
        logger.info("syncing metric data to server")
        resp = tracker.sync_metrics(self.get_graphql_body())

    def get_graphql_body(self):
        ret = {
            "modelMetrics": [metric.get_graphql_body() for metric in self.metrics]
        }
        return ret


class ModelRun(BaseEntity):
    runId = None
    startTime = None
    endTime = None
    status = "Preparing"
    metrics = None
    params  = None

    def __init__(self, runId):
        self.runId = runId
        self.params = ParamList(runId)
        self.metrics = MetricList(runId)
    
    def start(self):
        self.startTime = int(time.time())
        self.status = "Running"
        logger.info("Model run started")
        self.sync()
    
    def end(self):
        self.endTime = int(time.time())
        self.status = "Done"
        logger.info("Model run finished")
        self.sync()
    
    def sync(self):
        ''' Sync data to the server '''
        logger.info("syncing model run data to server")
        resp = tracker.sync_model_run(self.get_graphql_body())

        self.params.sync()
        self.metrics.sync()



    def log_param(self, key, val):
        self.params.add(key, val)
        logger.info("param logged with key %s : val %s" % (key, val))
    
    def log_metric(self, key, val):
        self.metrics.add(key, val)
        logger.info("metric logged with key %s : val %s" % (key, val))
    
    def __enter__(self):
        self.start()
        logger.info("Model run context started")
        return self
    
    def __exit__(self, *args):
        self.end()
        logger.info("Model run context ended")
    
    def get_graphql_body(self):
        ret = {
            "id": self.runId,
            "startTime": self.startTime,
            "endTime": self.endTime,
            "status": self.status
        }
        return ret