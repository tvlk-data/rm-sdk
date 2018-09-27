import os

from rm_sdk.storage import GoogleCloudStorage

MODEL_UPLOAD_BASE_PATH = os.getenv('MODEL_UPLOAD_URI')

def upload_model_directory(run_id, local_dir, destination_dir=None):
    model_name = 'ters' # giving some random name, need to fix it
    store = GoogleCloudStorage(MODEL_UPLOAD_BASE_PATH)

    model_upload_relative_path = "%s/%s/models" % (model_name, run_id)

    store.log_artifacts(local_dir, model_upload_relative_path)
