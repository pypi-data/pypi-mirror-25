from __future__ import with_statement
import zipfile
import os
import sys
import hashlib
import shutil
from distutils import spawn
import six
from collections import namedtuple

def program_exists(name):
    if six.PY3:
        path = shutil.which(name)
    else:
        # Distutils
        path = spawn.find_executable(name)
    return path
    
def success_text(checklist_entry):
    if not isinstance(checklist_entry, Checklist):
        raise Exception('success_text requires Checklist instance')
    
    success = checklist_entry.ok
    warn = checklist_entry.warn
    red = '\033[0;31m'
    green = '\033[0;32m'
    orange = '\033[0;33m'
    ok = '\033[0m'
    
    if checklist_entry.extra_note is not None:
        extra = ' - {0}'.format(checklist_entry.extra_note)
    else:
        extra = ''
    
    if success is True and warn is None:
        txt = '[{0}ok{1}]'.format(green, ok)
    elif warn is not None and success is not None:
        txt = '[{0}warn{1}{2}]'.format(orange, ok, extra)
    else:
        txt = '[{0}ERROR{1}{2}]'.format(red, ok, extra)
    return txt

ChecklistBase = namedtuple('ChecklistBase', ['tag', 'msg', 'ok', 'warn', 'extra_note'])
ChecklistBase.__new__.__defaults__ = (None,) * len(ChecklistBase._fields)
class Checklist(ChecklistBase):
    def type(self):
        return 'asd'

def checklist(listings, title=None, simple=False):
    s = ''
    if title is not None:
        s += "{0}\n".format(title)
    
    for p in listings:
        if p is None: # sometimes no checks made
            continue
        
        if not simple:
            tag = p[0].tag
            s += "\n    {0}:".format(tag)
            for step in p:
                s += "\n        {0} {1}".format(success_text(step), step.msg)
        else:
            s += "\n    - {0}".format(p)
            
    return s + "\n"

def retrieve_backup(zipname, entry):
    destpath = os.path.join(os.path.dirname(zipname), entry['id'])
    with zipfile.ZipFile(zipname,"r") as zip_ref:
        zip_ref.extractall(destpath)
    
    return destpath

BUFFER_SIZE = 1024 ** 2
def hash_zip(fname, onlydigest=True):
    md5 = hashlib.md5()
    
    with open(fname, 'rb') as f:
        while True:
            data = f.read(BUFFER_SIZE)
            if not data:
                break
            md5.update(data)
    
    if onlydigest:
        return md5.hexdigest()
    else:
        return md5