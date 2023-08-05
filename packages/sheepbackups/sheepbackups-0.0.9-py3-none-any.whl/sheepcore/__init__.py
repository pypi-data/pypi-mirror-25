import os
import logging

from sheepcore.version import *
VERSION = __version_info__

os.environ['SHEEPNAME'] = 'sheepbackups-py' # Also include version number in this?
os.environ['SHEEPVERSION'] = __version__
    
# Set up logging
def setup_logging(level=logging.DEBUG, filehandler=None, tag=None):
    #os.environ['SHEEPLOG'] = fileloc
    if tag is not None:
        os.environ['SHEEPACTION'] = tag
    format_string = "%(asctime)s,%(name)s,%(levelname)s,%(message)s"
    logger = get_logger(tag)
    logger.setLevel(level)
    handler = logging.StreamHandler(filehandler)
    handler.setLevel(level)
    formatter = logging.Formatter(format_string, datefmt="%Y-%m-%d %H:%I:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger
    
def get_logging():
    pass

def get_logger(tag=None):
    if tag is None:
        tag = os.environ.get('SHEEPACTION', 'none')
    logger = logging.getLogger('{0}:{1}'.format(os.environ['SHEEPNAME'], tag))
    return logger