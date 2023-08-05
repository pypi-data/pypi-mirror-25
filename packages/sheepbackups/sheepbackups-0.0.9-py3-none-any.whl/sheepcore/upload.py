import os
import boto3 
from botocore.client import Config

from sheepcore import get_logger
logger = get_logger('backup')

def upload(filepath, destkey, to, opts, *args, **kwargs):
    """
    filepath: file to upload
    to: which one ('s3', 'ssh' etc)
    opts: global options, group level options, like prefixes, bucket
    """
    try:
        os.path.isfile(filepath)
    except Exception as err:
        logger.error(err)
        return
    
    if to == 's3':
        # todo: environ for aws keys
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(opts['bucket'])
        bucket.upload_file(filepath, destkey)
        
def download(backups_dir, entry):
    s3opts = entry['s3']
    destdir = os.path.join(backups_dir, 'downloads')
    try:
        os.makedirs(destdir)
    except:
        # Check fi it exists
        pass
    
    destpath =  os.path.join(destdir, os.path.basename(s3opts['key']))
    if os.path.exists(destpath):
        print('Already downloaded, continuing...')
    else:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(s3opts['bucket'])
        bucket.download_file(s3opts['key'], destpath)
    
    # Check if it exists?/md5 check
    # Md5 exists in file meta
    try:
        md5 = entry['meta']['hash']
    except KeyError:
        md5 = None
    
    if md5 is not None:
        pass
    
    return destpath