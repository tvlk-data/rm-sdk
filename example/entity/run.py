import os
from rm_sdk.entities import ModelRun


base_path = os.path.dirname(os.path.realpath(__file__))

with ModelRun("c9c279c4-efc5-48f0-bbf3-68c44dcffbc7", base_path) as model_run:
    model_run.log_param('abc', 'pqa')
    model_run.log_param('pq', '2324234')
    model_run.log_metric('mete1', 'wewrwe')
    model_run.log_metric('sdfqqw', 'sdfwerew')
    #model_run.upload_model_directory(model_path)
    model_run.upload_model_directory()
