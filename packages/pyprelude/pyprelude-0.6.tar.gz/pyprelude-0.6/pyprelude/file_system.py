############################################################
#
# pyprelude.file_system
# Copyright (C) 2017, Richard Cook
# Released under MIT License
# https://github.com/rcook/pyprelude
#
############################################################

import os
import shutil
import stat

from .util import unpack_args

def _remove_dir_on_error(func, path, exc_info):
    if os.access(path, os.W_OK):
        raise
    else:
        os.chmod(path, stat.S_IWUSR)
        func(path)

def remove_dir(path):
    try:
        shutil.rmtree(path, onerror=_remove_dir_on_error)
    except WindowsError:
        with temp_dir() as d:
            status, output, error = execute("robocopy.exe", d, path, "/mir", can_fail=True)
            if status != 2:
                raise RuntimeError("robocopy failed with status {} (output={}, error={})".format(status, output, error))

        os.rmdir(path)

def make_path(*args):
    """
    >>> make_path("/a", "b")
    '/a/b'
    >>> make_path(["/a", "b"])
    '/a/b'
    >>> make_path(*["/a", "b"])
    '/a/b'
    >>> make_path("/a")
    '/a'
    >>> make_path(["/a"])
    '/a'
    >>> make_path(*["/a"])
    '/a'
    """
    paths = unpack_args(*args)
    return os.path.abspath(os.path.join(*[p for p in paths if p is not None]))
