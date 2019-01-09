import os

from rm_sdk.storage import GoogleCloudStorage
from rm_sdk.logger import logger

def upload_model_directory(model_run, local_dir, destination_dir):
  """This method will uploda the local model directory to the GCS bucket
    
    :type model_run: ModelRun
    :type local_dir: str
    :type destination_dir: str
  
  """
  model_upload_relative_path = "%s/%s/%s/models" % (destination_dir, model_run.model_name, model_run.runId)
  store = GoogleCloudStorage()
  logger.info("Uploading models from %s to %s", local_dir, model_upload_relative_path)
  store.log_artifacts(local_dir, model_upload_relative_path)
  logger.info("Model upload finished!")
