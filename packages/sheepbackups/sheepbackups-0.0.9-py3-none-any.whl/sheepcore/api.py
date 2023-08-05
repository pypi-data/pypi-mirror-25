import os
import requests
import time
import socket
import base64
import json

from sheepcore import version
from sheepcore.exceptions import *

def format_log_text(fileloc):
    text = ''
    with open(fileloc, 'r') as f:
        text = base64.b64encode(bytes(f.read(), "utf-8")).decode('utf-8')
    return text

def api_request(endpoint, post=None, limit=None):
    url = os.environ['SHEEPURL'] + endpoint
    
    headers = {
        'X-Sheepkey': os.environ['SHEEPKEY'],
        'X-SheepClient': 'sheepbackups-py/{0}'.format(version.__version__),
    }
    
    if limit is not None:
        headers['X-Limit'] = str(limit)
    
    if post is None:
        r = requests.get(url, headers=headers)
    else:
        if isinstance(post, SheepRequest):
            r = requests.post(url, str(post), headers=headers)
        else:
            raise SheepAPIError('post data was not a SheepRequest instance')
    
    if r.status_code == 403:
        raise SheepAPIError('Invalid api key')
    elif r.status_code in [503, 502]:
        raise SheepAPIError('Could not connect to the api')
    
    return SheepResponse(r, post)
        
def create_api_payload(reqtype, log=None, extra=None, **kwargs):
    obj = {}
    obj['created'] = str(time.time()).split('.')[0]
    
    if extra is not None:
        obj.update(extra)
    
    obj['meta'] = {
        "source": os.environ.get('SHEEPNAME', 'sheepbackups-py/unknown'),
        "servername": socket.gethostname(),
    }
    
    if kwargs.get('meta', False):
        obj['meta'].update(kwargs['meta'])
        
    if log is not None:
        obj['text'] = format_log_text(log)
        obj['meta']['logsource'] = 'structured'
    
    return obj
    
def api_ping(verbose=False):
    r = api_request('ping_any')
    if verbose:
        return {
            'ok': r.status == 200,
            'code': r.status,
        }
    else:
        return r.status == 200

class SheepRequest(object):
    
    data = {}
    project = None
    
    def __init__(self, **kwargs):
        # Defaults
        self.data['meta'] = {}
        self.data['meta']['source'] = os.environ.get('SHEEPNAME', 'sheepbackups-py/unknown')
        self.data['meta']['servername'] = socket.gethostname()
        self.data['created'] = str(time.time()).split('.')[0]
        
        # Go this way otherwise __setattr__ will override
        super().__setattr__('project', kwargs.get('prefix'))
        super().__setattr__('s3_bucket', kwargs.get('s3_bucket'))
        
        self.data.update(kwargs)
    
    def __str__(self):  #
        return json.dumps(self.data)

    def __setattr__(self, name, val):
        if name in ['meta', 'created', 'text']:
            raise AttributeError('Cannot set attribute "{0}" since it is reserved'.format(name))
        self.data[name] = val

    def meta(self, key, val=None):
        if val is None and isinstance(key, dict):
            self.data['meta'].update(key)
        else:
            self.data['meta'][key] = val
            
    def log(self, *args):
        path = os.path.join(*args)
        self.data['text'] = format_log_text(path)
        self.data['meta']['logsource'] = 'structured'
            
    def payload(self):
        return json.dumps(self.data)
        
    
class SheepResponse(object):
    resp = None
    test = False
    sheepreq = None
    id = None
    data = None
    status = None
    
    def __init__(self, resp, sheepreq, test=False):
        self.resp = resp
        self.sheepreq = sheepreq
        self.test = test
        
        # convenience
        if not test and resp is not None:
            self.status = resp.status_code
        
        if not test and self.ok():
            self.data = resp.json()
            
            if 'id' in self.data:
                self.id = self.data['id']
        
    def ok(self):
        if self.test:
            return True
        return self.resp.status_code == 200
        
    def error(self):
        if self.test:
            return (000, 'test')
        content = self.resp.content
        if content.startswith(b'<html') or self.resp.status_code >= 500:
            content = 'Server error'
        return (self.resp.status_code, content)