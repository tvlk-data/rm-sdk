import gzip
import os
import shutil
import tarfile
import tempfile

def is_directory(name):
    return os.path.isdir(name)


def is_file(name):
    return os.path.isfile(name)


def exists(name):
    return os.path.exists(name)


def build_path(*path_segments):
    """ Returns the path formed by joining the passed-in path segments. """
    return os.path.join(*path_segments)

def get_file_info(path, rel_path):
    """
    Returns file meta data : location, size, ... etc
    :param path: Path to artifact
    :return: `FileInfo` object
    """
    if is_directory(path):
        return FileInfo(rel_path, True, None)
    else:
        return FileInfo(rel_path, False, os.path.getsize(path))


def get_relative_path(root_path, target_path):
    """
    Remove root path common prefix and return part of `path` relative to `root_path`.
    :param root_path: Root path
    :param target_path: Desired path for common prefix removal
    :return: Path relative to root_path
    """
    if len(root_path) > len(target_path):
        raise Exception("Root path '%s' longer than target path '%s'" % (root_path, target_path))
    common_prefix = os.path.commonprefix([root_path, target_path])
    return os.path.relpath(target_path, common_prefix)

def get_parent_dir(path):
    return os.path.abspath(os.path.join(path, os.pardir))