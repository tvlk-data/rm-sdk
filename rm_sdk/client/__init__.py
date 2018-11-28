from rm_sdk.entities import ModelRun
from rm_sdk.tracking.api_client import RMTrackingClient
from rm_sdk.utils.http_utils import get_auth0_token


class RMConfig(object):
  config_fields = ['RM_GRAPHQL_API_URL', 'AUTH0_CONFIG', 'MODEL_UPLOAD_URI']
  
  def __init__(self, config_dict):
    self._config = {}
    self._config['RM_GRAPHQL_API_URL'] = config_dict['RM_GRAPHQL_API_URL'] # required
    self._config['AUTH0_CONFIG'] = config_dict.get('AUTH0_CONFIG') # optional
    self._config['AUTH0_TOKEN'] = self.get_auth0_token()
    self._config['MODEL_UPLOAD_URI'] = config_dict.get('MODEL_UPLOAD_URI', 'gs://rm-run-outputs')
  
  def get(self, key):
    return self._config.get(key)
  
  @staticmethod
  def check_auth0_config(auth0_config):
    if auth0_config is None:
      return
    
    fields = ['domain', 'audience', 'client_id', 'client_secret']

    for field in fields:
      if not field in auth0_config:
        raise AttributeError(field + "is not found on Auth0 config")

    return
  
  def get_auth0_token(self):
    if not self._config['AUTH0_CONFIG']:
      return None
    self.check_auth0_config(self._config['AUTH0_CONFIG'])
    return get_auth0_token(self._config['AUTH0_CONFIG'])
    
  

class RMClient(object):
  
  def __init__(self, config):
    if isinstance(config,dict):
      self._config = RMConfig(config)
    elif isinstance(config, RMConfig):
      self._config = config
    else:
      raise AssertionError('configuration is not a dict of RMConfig object')
    
    self.tracker = RMTrackingClient(self._config.get('RM_GRAPHQL_API_URL'), self._config.get('AUTH0_TOKEN'))

  def create_model_run(self, runId, base_path, delete_old_data=True):
    return ModelRun(self, runId, base_path, delete_old_data)
  
  def set_run_as_failed(self, kubeJobId):
    return self.tracker.set_run_as_failed(kubeJobId)
  