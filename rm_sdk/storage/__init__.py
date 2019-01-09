import os
from six.moves import urllib

from rm_sdk.utils.file_utils import build_path, get_relative_path


class GoogleCloudStorage(object):
    """A helper class to upload files to GCS
    """
    def __init__(self, client=None):

        if client:
            self.gcs = client
        else:
            from google.cloud import storage as gcs_storage
            self.gcs = gcs_storage

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
    
    def get_artifact(self, artifact_path):
        """This method can get a file from GCS
           :param artifact_path: the gcs_uri to download the file
           :type artifact_path: str
           :return: a binary object of the file
           :rtype: blob
        """
        (bucket, dest_path) = self.parse_uri(artifact_path)
        gcs_bucket = self.gcs.Client().get_bucket(bucket)
        blob = gcs_bucket.get_blob(dest_path)
        return blob
    
    def log_artifact(self, local_file, artifact_path):
        """This method can upload a single file to GCS
           :param local_dir: which local single user wants to upload
           :type local_dir: str
           :param artifact_path: as what remote file user wants to upload
        """
        (bucket, dest_path) = self.parse_uri(artifact_path)
        dest_path = build_path(dest_path, os.path.basename(local_file))

        gcs_bucket = self.gcs.Client().get_bucket(bucket)
        blob = gcs_bucket.blob(dest_path)
        blob.upload_from_filename(local_file)
    
    def log_artifacts(self, local_dir, artifact_path):
        """This method can upload a folder to GCS
           :param local_dir: which local folder user wants to upload
           :type local_dir: str
           :param artifact_path: to which remote folder user wants to upload
        """
        (bucket, dest_path) = self.parse_uri(artifact_path)
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
    
