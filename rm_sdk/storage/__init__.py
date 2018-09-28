import os

from six.moves import urllib

from rm_sdk.utils.file_utils import build_path, get_relative_path


class GoogleCloudStorage(object):
    def __init__(self, artifact_uri=None, client=None):
        self.artifact_uri = artifact_uri

        if client:
            self.gcs = client
        else:
            from google.cloud import storage as gcs_storage
            self.gcs = gcs_storage
    
    def update_artifact_uri(self, artifact_uri):
        self.artifact_uri = artifact_uri

    @staticmethod
    def parse_uri(uri):
        """Parse an GCS URI, returning (bucket, path)"""
        parsed = urllib.parse.urlparse(uri)
        if parsed.scheme != "gs":
            raise Exception("Not a GCS URI: %s" % uri)
        path = parsed.path
        if path.startswith('/'):
            path = path[1:]
        return parsed.netloc, path
    
    def log_artifact(self, local_file, artifact_path=None):
        (bucket, dest_path) = self.parse_uri(self.artifact_uri)
        if artifact_path:
            dest_path = build_path(dest_path, artifact_path)
        dest_path = build_path(dest_path, os.path.basename(local_file))

        gcs_bucket = self.gcs.Client().get_bucket(bucket)
        blob = gcs_bucket.blob(dest_path)
        blob.upload_from_filename(local_file)
    
    def log_artifacts(self, local_dir, artifact_path=None):
        (bucket, dest_path) = self.parse_uri(self.artifact_uri)
        if artifact_path:
            dest_path = build_path(dest_path, artifact_path)
        gcs_bucket = self.gcs.Client().get_bucket(bucket)

        local_dir = os.path.abspath(local_dir)
        for (root, _, filenames) in os.walk(local_dir):
            upload_path = dest_path
            if root != local_dir:
                rel_path = get_relative_path(local_dir, root)
                upload_path = build_path(dest_path, rel_path)
            for f in filenames:
                path = build_path(upload_path, f)
                gcs_bucket.blob(path).upload_from_filename(build_path(root, f))
    
