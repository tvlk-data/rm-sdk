import os
from rm_sdk.entities import ModelRun


base_path = os.path.dirname(os.path.realpath(__file__))

with ModelRun("c75ecf51-db02-4488-a3a7-08f421695199", base_path) as model_run:
    model_run.log_param('abc', 'pqa')
    model_run.log_param('pq', '2324234')
    model_run.log_metric('mete1', 'wewrwe')
    model_run.log_metric('sdfqqw', 'sdfwerew')
    #model_run.upload_model_directory('/outputs/models')
    #model_run.upload_model_directory()
