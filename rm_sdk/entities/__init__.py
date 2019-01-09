from datetime import datetime
import time
import json
import os

from rm_sdk import model

from rm_sdk.logger import logger
from rm_sdk.utils import file_utils


class BaseEntity(object):
    """This class is the base class of any entity of RM-API
    """
    def get_graphql_body(self):
        raise NotImplementedError

class Param(BaseEntity):
    """This class is for dealing with ModelParam entity
    """
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
    """This class is for dealing with a list ModelParam entity
    """
    runId = None
    params = []

    def __init__(self, rm_client, runId, params=[]):
        self.runId = runId
        self.params = params
        self.rm_client = rm_client
    
    def add(self, key, val):
        param = Param(self.runId, key, val)
        self.params.append(param)
    

    def sync(self):
        """This method will create graphql request to store the model params
        """
        if not self.params:
            logger.info("No params available")
            return
        
        logger.info("syncing param data to server")
        resp = self.rm_client.tracker.sync_params(self.get_graphql_body())
    
    def delete_all_db_row(self):
        resp = self.rm_client.tracker.delete_all_params_by_runId(self.runId)

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

    def __init__(self, rm_client, runId, metrics=[]):
        self.runId = runId
        self.metrics = metrics
        self.rm_client = rm_client
    
    def add(self, key, val):
        metric = Metric(self.runId, key, val)
        self.metrics.append(metric)
    

    def sync(self):
        if not self.metrics:
            logger.info("no metrics available")
            return
        logger.info("syncing metric data to server")
        resp = self.rm_client.tracker.sync_metrics(self.get_graphql_body())
    
    def delete_all_db_row(self):
        resp = self.rm_client.tracker.delete_all_metrics_by_runId(self.runId)

    def get_graphql_body(self):
        ret = {
            "modelMetrics": [metric.get_graphql_body() for metric in self.metrics]
        }
        return ret


class ModelRun(BaseEntity):
    """This class represents the entity of Model Run
       it has with context methods check the __enter__ and __exit__ methods
       One can manually sync to rm-api using the sync method
    """
    runId = None
    startTime = None
    endTime = None
    status = "Preparing"
    metrics = None
    params  = None
    base_path = None
    delete_old_data = True

    def __init__(self, rm_client, runId, base_path, delete_old_data=True):
        """
        Constructs the RMClient object
        
        :param runId: Model Run Id
        :type runId: str
        :param base_path: Absoloute path where the object is being created
        :type base_path: str
        :param delete_old_data: Flag for deleting old data before syncing specially \
        for metrics and params
        :type delete_old_data: bool
        
        """
        self.rm_client = rm_client

        run_history_info = json.loads(self.rm_client.tracker.get_run_history(runId))
        if not run_history_info['data']['getRunHistoryById']:
            raise ValueError("No data found for this runId")
        
        self.model_name = run_history_info['data']['getRunHistoryById']['model']['name']
        self.runId = runId
        self.params = ParamList(self.rm_client, runId)
        self.metrics = MetricList(self.rm_client, runId)

        self.base_path = base_path
        self.delete_old_data = delete_old_data
    
    def start(self):
        self.startTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.status = "Running"
        logger.info("Model run started")
        self.sync()
    
    def end(self):
        self.endTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.status = "Done"
        logger.info("Model run finished")
        self.sync()
    
    def sync(self):
        ''' Sync data to the server '''
        logger.info("syncing model run data to server")
        resp = self.rm_client.tracker.sync_model_run(self.get_graphql_body())

        if self.delete_old_data:
            self.params.delete_all_db_row()
            self.metrics.delete_all_db_row()
        
        self.params.sync()
        self.metrics.sync()

    def log_param(self, key, val):
        self.params.add(key, val)
        logger.info("param logged with key %s : val %s" % (key, val))
    
    def log_metric(self, key, val):
        self.metrics.add(key, val)
        logger.info("metric logged with key %s : val %s" % (key, val))

    def upload_model_directory(self, local_dir=None):

        local_full_path = ''

        if not local_dir:
            local_full_path = self.base_path + '/outputs/models'
        else:
            if not local_dir.startswith('/'):
                local_dir = "/" + local_dir
            
            local_full_path = self.base_path + local_dir
        
        model.upload_model_directory(self, local_full_path, self.rm_client._config.get('MODEL_UPLOAD_URI'))
    
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
    
    def __str__(self):
        return "RunId: %s for Model Name: %s" % (self.runId, self.model_name)