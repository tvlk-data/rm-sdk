import os
from rm_sdk.entities import ModelRun


with ModelRun("3849e808-dc79-4888-bfda-c6c38462f6d2") as model_run:
    model_run.log_param('abc', 'pqa')
    model_run.log_param('pq', '2324234')
    model_run.log_metric('mete1', 'wewrwe')
    model_run.log_metric('sdfqqw', 'sdfwerew')
    dir_path = os.path.dirname(os.path.realpath(__file__))
    model_path = dir_path + '/outputs/models'
    #model_run.upload_model_directory(model_path)
    model_run.upload_model_directory()
