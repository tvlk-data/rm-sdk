import os

from rm_sdk.storage import GoogleCloudStorage

MODEL_UPLOAD_BASE_PATH = os.getenv('MODEL_UPLOAD_URI', 'gs://rm-run-outputs')

def upload_model_directory(model_run, local_dir, destination_dir=None):
    store = GoogleCloudStorage(MODEL_UPLOAD_BASE_PATH)
    model_upload_relative_path = "%s/%s/models" % (model_run.model_name, model_run.runId)
    store.log_artifacts(local_dir, model_upload_relative_path)
