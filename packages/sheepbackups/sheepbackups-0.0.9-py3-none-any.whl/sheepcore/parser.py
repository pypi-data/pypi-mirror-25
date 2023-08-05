from datetime import datetime
import time
import os, sys
import yaml
import shutil
import base64
import json
import socket
import subprocess

import delegator

from sheepcore import get_logger
from sheepcore.options import *
from sheepcore.api import api_request, create_api_payload, SheepRequest, SheepResponse
from sheepcore.upload import upload
from sheepcore.humanize import naturalsize
from sheepcore.exceptions import *
from sheepcore.utils import hash_zip

logger = get_logger('backup')

def format_log_text(fileloc):
    text = ''
    with open(fileloc, 'r') as f:
        text = base64.b64encode(bytes(f.read(), "utf-8")).decode('utf-8')
    return text

def load_config(config=None):
    if config is None:
        config = os.path.join(os.path.expanduser("~"), ".sheepbackups", "config.yaml")
    
    # Also check env
    
    if not os.path.isfile(config):
        raise RuntimeError("Config path not found: {0}".format(config))
    
    c = Parser.load(config)
    
    try:
        c
    except NameError:
        raise RuntimeError("No config loaded. Either the path was not found, or the yaml config could not be parsed.")
        sys.exit(2)
    
    return c

class Option(object):
    """
    Type, blah blah
    """
    type = None
    
    def __init__(self, opttype):
        self.type = opttype

class Parser(object):
    """
    Holds configuration options
    """
    
    yamldoc = {}
    prefixes = []
    projects = []
    parsed = {}
    actions = {}
    all_options = []
    locations = {}
    
    def __init__(self, yamldoc, path=None):
        self.path = path
        self.yamldoc = yamldoc
        self.backups = self.yamldoc['backups']
        
        # Fix defaults
        try:
            self.yamldoc['backups_dir']
        except KeyError:
            self.yamldoc['backups_dir'] = '/tmp/sheepbackups'
        try: 
            self.yamldoc['zips_dir']
        except KeyError:
            self.yamldoc['zips_dir'] = '/tmp/sheepbackups/zips'
        
        # Extract location
        for proj, opts in self.yamldoc['backups'].items():
            self.prefixes.append(proj)
            self.projects.append(proj)
            try:
                self.locations[proj] = opts['to']
            except KeyError:
                raise SheepConfigException('no_to_config_found', proj) from None
        
        self.actions = self.link_classes(self.yamldoc['backups'])
        #print('actions',self.actions)
        
    @staticmethod
    def link_classes(config):
        """Pass args to constructors"""
        actions = {}
        for prefix, opts in config.items():
            if prefix not in actions:
                actions[prefix] = []
            
            if 'mysql' in opts:
                #backup_path = [temp_dir, prefix, 'db']
                actions[prefix].append(db.MySQL(opts['mysql']))
            if 'sqlite' in opts:
                # Collect it
                actions[prefix].append(db.Sqlite(opts['sqlite']))
                    
            # Collect directories
            if 'collect' in opts:
                if 'dirs' in opts['collect']:
                    include_dirs = opts['collect'].get('dirs', None)
                    exclude = opts['collect'].get('exclude', None)
                    actions[prefix].append(files.Collect(dirs=include_dirs, exclude=exclude))
        return actions
    
    @staticmethod
    def api_url(endpoint, **kwargs):
        return os.environ['SHEEPURL'] + endpoint
    
    def includes(self, prefix):
        """Check if this is in the current config"""
        return prefix in self.prefixes
    
    def __str__(self):
        # dump all the info for cli
        return yaml.dump(self.yamldoc)
    
    def __getitem__(self, key):
        return self.yamldoc[key]
    
    @staticmethod
    def load(path):
        try:
            with open(path, 'r') as stream:
                try:
                    yamldoc = yaml.load(stream)
                except yaml.YAMLError as exc:
                    print(exc)
                    raise
        except FileNotFoundError:
            raise
        
        try:
            os.environ['SHEEPURL'] = yamldoc['api_url']
            os.environ['SHEEPKEY'] = yamldoc['api_key']
        except TypeError:
            print('ERROR: Please make sure the API url and API key are set in the config file. ({0})'.format(path))
            sys.exit(1)
            
        return Parser(yamldoc, path=path)
        
    def show_info(self):
        confline = 'Config file location: {0}'.format(self.path)
        line = '-' * len(confline)
        appendline = "\nUse `sheep configbackup` to upload this file to the Sheep Backups website. Keys will be scrubbed."
        #return "{1}\n{0}\n{1}\n{2}{3}".format(confline, line, yaml.dump(self.yamldoc), appendline)
        return "{1}\n{0}\n{1}\n{2}".format(confline, line, yaml.dump(self.yamldoc))
        
    def has(self, which): 
        """
        Which options we're using
        """
        return which in self.all_options
        
    def backup_path(self, extra):
        pass
    
    def run_backup(self, temp_dir):
        """
        Loop through self.actions, run them
        @todo: put in upload
        """
        results = []
        TEST = os.environ['TEST'] == 'True'
        logger.debug('is test: {0}'.format(TEST))
        for prefix, all_opts in self.actions.items():
            
            for opt in all_opts:
                logger.debug('Running action {0}'.format(opt.type))
                opt.setup(temp_dir=temp_dir)
                opt.run()
                
            # Now zip temp_dir, and upload it to specified s3 @todo: configurable archive name
            datestamp = datetime.now().strftime('%Y%m%d.%f')
            new_zip_name = '{0}.{1}'.format(prefix, datestamp)
            fname = shutil.make_archive(os.path.join(self.yamldoc['zips_dir'], new_zip_name), 'zip', temp_dir)
            archive_size = naturalsize(os.path.getsize(fname))
            archive_md5 = hash_zip(fname)
            logger.info('Archive name: {0}, size: {1}, md5: {2}'.format(fname, archive_size, archive_md5))
            
            # Somehow integrity check
            
            # Run upload
            use = self.locations[prefix]['location'] # {location, bucket, prefix}
            s3opts = self.yamldoc['locations'][use]
            s3opts.update(self.locations[prefix])
            destkey = '{0}/{1}'.format(s3opts['prefix'], os.path.basename(fname))
            logger.info('Destination key: {0}'.format(destkey))
            
            if not TEST:
                logger.debug('Uploading')
                upload(fname, destkey, to=use, opts=s3opts)
                
            # Send upload notification
            sheepreq = SheepRequest(s3_bucket=s3opts['bucket'], s3_key=destkey, prefix=prefix)
            sheepreq.meta({'size': archive_size, 'hash': archive_md5})
            
            logger.debug('postdata: {0}'.format(sheepreq))
            if TEST:
                fatal_api_error = False
                logger.debug('Test run, not uploading')
                resp = SheepResponse(resp=None, sheepreq=sheepreq, test=True)
            else:
                # Call api
                sheepreq.log(temp_dir, '_meta', 'backup.log')
                
                resp = api_request('new', post=sheepreq)
                if resp.ok():
                    # Success, clean up
                    if self.yamldoc.get('keep', True) is False:
                        #logger.debug('Removing stored archive and temp dir')
                        shutil.rmtree(temp_dir)
                        os.remove(fname)
            
            if not resp.ok():
                print('ERROR: API status error: {0}: {1}'.format(*resp.error()))
            else:
                # Can't log here since it's already zipped and uploaded
                results.append({
                    'fname': fname,
                    'ok': resp.ok(),
                    'resp': resp,
                    'req': sheepreq,
                })
        
        return results
        
class Restore(object):
    
    process = None
    
    def __init__(self, config, key, filesdir, zipfile):
        self.config = config
        self.key = key
        self.filesdir = filesdir
        self.zipfile = zipfile
        
        self.create_objectives()
        
    def create_objectives(self):
        """Parse config, and find out what will be done"""
        backups = self.config['backups']
        if self.key not in backups:
            raise SheepConfigException('no_restore_no_key',self.key)
            
        backup = {self.key: backups[self.key]}
        objs = Parser.link_classes(backup)
        process = []
        
        for key, opts in objs.items():
            for opt in opts:
                setup = opt.setup_reverse(self.filesdir, opts=backups[self.key][opt.type])
                process.append({
                    'type': opt.type,
                    'obj': opt,
                    'steps': setup,
                })
        self.process = process
        
    def display_objectives(self):
        # Display results of actions
        s = ''
        s = "\nPerforming actions in backup directory {0}:".format(self.filesdir)
        for p in self.process:
            s += "\n    {0}:".format(p['type'])
            if p['steps'] is not None:
                for step in p['steps']['actions']:
                    text = step['text']
                    if step['error'] != '':
                        text = ''
                    s += "\n        {0} {1}".format(self.success_text(step['error'], step['warn']), text)
        return s
    
    def success_text(self, error, warn=None):
        red = '\033[0;31m'
        green = '\033[0;32m'
        orange = '\033[0;33m'
        ok = '\033[0m'
        if error == '' and warn is None:
            txt = '[{0}ok{1}]'.format(green, ok)
        elif warn is not None and error == '':
            txt = '[{0}warn{1} - {2}]'.format(orange, ok, warn)
        else:
            txt = '[{0}ERROR{1} - {2}]'.format(red, ok, error)
        return txt
        
    def cleanup(self):
        # Remove the zip and temp dir
        print('Removing dir {0}'.format(self.filesdir))
        shutil.rmtree(self.filesdir)
        print('Removing zip {0}'.format(self.zipfile))
        os.remove(self.zipfile)
    
    def run(self):
        # write log
        log = get_logger('restore')
        log.debug('Begin restore for {0}'.format(self.key))
        
        # if warnings
        print(self.display_objectives())
        warnings = True
        if warnings:
            warn_text = ' (errors will be skipped)'
        x = input('Proceed?{0} [Y/n] '.format(warn_text))
        if x != 'Y':
            log.info('Restore cancelled')
            return ('cancelled', None, False)
        else:
            for task in self.process:
                log.info('Running task {0}'.format(task['type']))
                print('Running task {0}...'.format(task['type']))
                
                for step in task['steps']['actions']:
                    if step['error'] != '':
                        log.warning('Skipping due to error: {0}'.format(step['error']))
                        continue
                    
                    cmd = delegator.run(step['cmd'], block=False)
                    
                    if cmd.return_code is None:
                        # Success
                        for line in cmd.out.splitlines():
                            log.info(line)
                    else:
                        log.error('Error: {0}, out: {1}'.format(cmd.return_code, cmd.err))
            
                print(' - complete')
        
        # Send log info 
        data = SheepRequest(prefix=self.key)
        data.meta('restore', 1)
        data.log('/tmp', 'sheepbackups', 'restore.log')
        
        resp = api_request('new_restore', post=data)
        
        return ('complete', resp, resp.ok())