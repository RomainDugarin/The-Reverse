import json
import os
from functools import partial

utils_open = partial(open, encoding="UTF-8")

def _load_config(name):
    """Open file and return a corresponding JSON object.
    """
    cwfd = os.path.dirname(os.path.realpath(__file__))  # the directory of utils.py
    jsonf = os.path.realpath(os.path.join(cwfd, '_env', name))
    with utils_open(jsonf) as fp:
        return json.load(fp)

def load_custom_config(name, file, path = '_env'):
    """Open file and return a corresponding JSON object.
    """
    cwfd = os.path.dirname(os.path.realpath(file))  # the directory of utils.py
    jsonf = os.path.realpath(os.path.join(cwfd, path, name))
    with utils_open(jsonf) as fp:
        return json.load(fp)

def _create_folder(folder):
    import pathlib
    cwfd = os.path.dirname(os.path.realpath(__file__))  # the directory of utils.py
    jsonf = os.path.realpath(os.path.join(cwfd, '_env', folder))
    pathlib.Path(jsonf).mkdir(parents=True, exist_ok=True)


def _load_logger(name, JSON=False, toArray=True):
    """Open file and return a corresponding file object or JSON.

    JSON=False is an optional boolean that specifies if the log file is a JSON.
    """
    cwfd = os.path.dirname(os.path.realpath(__file__))  # the directory of utils.py
    jsonf = os.path.realpath(os.path.join(cwfd, '_env', name))
    with utils_open(jsonf) as fp:
        if(JSON):
            return json.load(fp)
        if(toArray):
            lines = fp.read().splitlines()
            return lines
        return fp.read()

def load_backend():
    """ Open backend configuration file and return the corresponding JSON object. """
    return _load_config("env.json")
