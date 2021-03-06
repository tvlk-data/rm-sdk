from rm_sdk.entities import ModelRun
from rm_sdk.tracking.api_client import RMTrackingClient
from rm_sdk.utils.http_utils import get_auth0_token


class RMConfig(object):
  """
    This is the config object class for RM-SDK which will injected to rm-sdk object
    Config object should have this configurations
    
    RM_GRAPHQL_API_URL (required)
    
    AUTH0_CONFIG (optional, if provided will use the configuration to get token)
    
    MODEL_UPLOAD_URI (Optional, if not provided will use default GCS bucket gs://rm-project-artifacts)
  """
  config_fields = ['RM_GRAPHQL_API_URL', 'AUTH0_CONFIG', 'MODEL_UPLOAD_URI']
  
  def __init__(self, config_dict):
    """
      Constructor for RMConfig
    
      :param config_dict: RM-SDK configuration construction data
      :type config_dict: dict
    
    """
    
    self._config = {}
    self._config['RM_GRAPHQL_API_URL'] = config_dict['RM_GRAPHQL_API_URL'] # required
    self._config['AUTH0_CONFIG'] = config_dict.get('AUTH0_CONFIG') # optional
    self._config['AUTH0_TOKEN'] = self.get_auth0_token()
    self._config['MODEL_UPLOAD_URI'] = config_dict.get('MODEL_UPLOAD_URI')
  
  def get(self, key):
    """
      Config getter method
      
      :param key: key for any configuration property
      :type key: str
      
      :return: Configuration value if exists
    """
    return self._config.get(key)
  
  @staticmethod
  def check_auth0_config(auth0_config):
    """
      This method check whether the auth0_config dict have all the necessary fields
      
      :param auth0_config: the auth0 configuration dict
      :type auth0_config: dict
      
      :raises: AttributeError
    """

    if auth0_config is None:
      return
    
    fields = ['domain', 'audience', 'client_id', 'client_secret']

    for field in fields:
      if not field in auth0_config:
        raise AttributeError(field + "is not found on Auth0 config")

    return
  
  def get_auth0_token(self):
    """
      This method fetches auth0 token from the given configuration
      
      :param auth0_config: the auth0 configuration dict
      :type auth0_config: dict
      
      :raises: AttributeError
      :return: returns the auth0 generated token or None
      :rtype: None or str
    """
    if not self._config['AUTH0_CONFIG']:
      return None
    self.check_auth0_config(self._config['AUTH0_CONFIG'])
    return get_auth0_token(self._config['AUTH0_CONFIG'])
    
  

class RMClient(object):
  """
    This class is the main entrypoint of the RM-SDK which holds a RMTrackingClient object
    with the property tracker. Any method on on RMTrackingClient can be invoked by tracker
    property. This class also holds a config object
  """
  def __init__(self, config):
    """
      Constructor for RMClient
      
      :param config: RM-SDK configuration
      :type config: RMConfig
      :raises: AssertionError
    
    """
    if isinstance(config,dict):
      self._config = RMConfig(config)
    elif isinstance(config, RMConfig):
      self._config = config
    else:
      raise AssertionError('configuration is not a dict of RMConfig object')
    
    self.tracker = RMTrackingClient(self._config.get('RM_GRAPHQL_API_URL'), self._config.get('AUTH0_TOKEN'))

  def create_model_run(self, runId, base_path, delete_old_data=True):
    """
      Factory method for creating ModelRun object.

      :param runId: Run id of the model run on RM
      :type runId: str
      :param base_path: Base path of the project where base_path/models will hold the generated models
      :type base_path: str
      :param delete_old_data: whether RM-SDK is allowed to clean up old metrics of the same runId
      :type delete_old_data: bool
      
      :return: return a ModelRun object which also holds the RM-Configs
      :rtype: ModelRun

    """
    return ModelRun(self, runId, base_path, delete_old_data)
  
  def set_run_as_failed(self, kubeJobId):
    """
    A method to make a run failed on status field by kubeJobId
    
    :param kubeJobId: a string id of the kube job which is being ran for a ModelRun
    :type kubeJobId: str
    
    """
    return self.tracker.set_run_as_failed(kubeJobId)
  