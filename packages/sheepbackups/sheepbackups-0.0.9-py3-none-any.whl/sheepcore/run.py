import argparse
import sys, os
import requests
from tabulate import tabulate
import yaml
import time
import shutil
import json

from boto3.session import Session

from sheepcore import VERSION, setup_logging, get_logger
from sheepcore.parser import Parser, load_config, Restore
from sheepcore.api import api_request, create_api_payload, api_ping
from sheepcore.exceptions import *
from sheepcore.upload import download
from sheepcore.utils import retrieve_backup, checklist, Checklist, program_exists
from sheepcore.schedule import Schedule

def entries_lookup(prefix=None, match=None, limit=10, dataset=None):
    endpoint = 'entries/'
    
    if prefix is None:
        prefix = 'all'
    endpoint += prefix
        
    if match is not None:
        endpoint += '/' + match
    
    if limit is None:
        limit = 10
    
    if dataset is not None:
        j = dataset
    else:
        r = api_request(endpoint, limit=limit)
        j = r.data
    table = []
    num = 1
    for result in j['entries']:
        if result['meta']:
            meta = ', '.join([ '{0}: {1}'.format(k,v) for k, v in result['meta'].items() ])
        else:
            meta = ''
            
        table.append([num, result['id'], result['prefix'], result['created_servertime'], meta])
        num += 1
    return tabulate(table, headers=['', 'uuid', 'project', 'date', 'meta'])
    

def run_backup(only_prefix=None):
    # Check config
    # Create temp dir
    temp_dir = os.path.join(CONFIG['backups_dir'], 'backup{0}'.format(time.time()))
    try:
        os.makedirs(temp_dir)
        os.makedirs(os.path.join(temp_dir, '_meta'))
    except:
        raise
    
    logger = setup_logging(filehandler=open(os.path.join(temp_dir, '_meta', 'backup.log'), 'w'), tag='backup')
    logger.debug('Begin logging')
    
    if only_prefix is None:
        loop = CONFIG.backups.items()
    else:
        loop = (only_prefix, CONFIG.backups[only_prefix])
        
    try:
        results = CONFIG.run_backup(temp_dir)
    except SheepAPIError as e:
        pass
    except: 
        raise
    
    # Success
    s = "Backup complete\n"
    for result in results:
        resp = result['resp']
        s += "\n    [{0}]:".format(result['req'].project)
        s += "\n        - {0} uploaded to s3 bucket {1}".format(result['fname'], result['req'].s3_bucket)
        if not resp.test:
            s += "\n        - Sheep Backups link: https://app.sheepbackups.com/entry/{0}".format(result['resp'].id)
    
    s += "\n"
    return s

def run_restore(idmatch=None):
    
    # Get information from api
    if idmatch is None:
        return 'ERROR: Provide an id to restore to'
        
    req = api_request(endpoint='entries/all/{0}'.format(idmatch))
    resp = req.data
    if resp['_num'] != 1:
        r = "ERROR: Cannot find specified id. Please provide more characters.\n\n"
        r += entries_lookup(dataset=resp)
        return r
        
    # Ensure the prefix on the api resp is the same as one in the current config
    entry = resp['entries'][0]
    if not CONFIG.includes(entry['prefix']):
        raise SheepConfigException('no_restore_no_key', entry['prefix'])
    
    setup_logging(filehandler=open(os.path.join('/tmp', 'sheepbackups', 'restore.log'), 'w'), tag='restore')
    
    # Unzip
    fname = download(CONFIG['backups_dir'], entry)
    filesdir = retrieve_backup(fname, entry)
    
    # Create and run
    restore = Restore(CONFIG, entry['prefix'], filesdir, fname)
    output, resp, log_success = restore.run()
    
    if not log_success:
        print('Unable to upload log file.')
        log_link = ''
    else:
        rjson = resp.data
        log_link = 'Your log information has been uploaded: https://app.sheepbackups.com/restores/{0}'.format(rjson['uuid'])
        
    if output == 'cancelled':
        finish_text = '\nRestore cancelled. Remove downloaded backup? [Y/n] '
    elif output == 'complete':
        finish_text = '\nRestore completed. Remove downloaded backup? [Y/n] '
    
    i = input(finish_text)
    if i == 'Y':
        restore.cleanup()
    
    # Shoudl have run, or been cancelled, do cleanup
    # Remove zip (ask)
    return 'Finished.'
    
def run_check():
    checks = []
    general_checks = []
    
    # S3 check
    sess = Session()
    if sess is None:
        msg = 's3 Connection is not working. It is possible your credentials weren\'t properly loaded.'
    else:
        msg = 's3 Connection working'
    general_checks.append(Checklist(msg=msg, ok=sess is not None, tag='general'))
    
    ping = api_ping(verbose=True)
    general_checks.append(Checklist(msg='API Connection', ok=ping['ok'], extra_note='http status: {0}'.format(ping['code']), tag='general'))
    
    cron = program_exists('crontab') is not None
    general_checks.append(Checklist(msg='Crontab installed', ok=cron))
    
    checks.append(general_checks)
    
    for project, actions in CONFIG.actions.items():
        for action in actions:
            checks.append(action.check())
    
    return checklist(checks, title='Running checks')
    
def schedule(when=None):
    s = Schedule()
    
    if when is None:
        # Return schedule if found in crontab
        if s.exists:
            return 'Sheep Backups is installed.'
    else:
        return 'Sheep Backups is not set to automatically run. For more information, see here: https://docs.sheepbackups.com/to/schedule'
        
def show_projects():
    s = "Projects found in config file ({0})\n".format(CONFIG.path)
    s += checklist(CONFIG.projects, simple=True)
    return s

def loader(testopt=False):
    sheep_version = '{0}.{1}.{2}'.format(*VERSION)
    
    #parser = argparse.ArgumentParser(description='Sheep Backups {0}. For more information on the Python cli, visit https://docs.sheepbackups.com/python'.format(sheep_version), prog='sheep')
    parser = argparse.ArgumentParser(description='Sheep Backups {0}'.format(sheep_version), prog='sheep')
    parser.add_argument('action', nargs='?', help='What action to perform (backup, restore, list, check, schedule, projects)')
    parser.add_argument('match', nargs='?', help='ID to match')
    parser.add_argument('--project', help='Which project to use when searching')
    parser.add_argument('--limit', help='Number of results returned (default 10)')
    parser.add_argument('--test', action='store_true', help='Do a test backup/restore, but don\'t actually run')
    parser.add_argument('--config', help='Path to config file (default ~/.sheepbackups/config.yaml)')
    parser.add_argument('-V', '--version', action='store_true', help='Return this version')
    
    """
    configbackup - uploads to site [scrub most data], when on site, store in versions, and also links to docs for each item
    configcheck - run through some basic checks like file exists, correct keys
    restore --only-download to just download and not actually apply
    """
    
    opts = parser.parse_args()
        
    global CONFIG    
    CONFIG = load_config(opts.config)
    
    os.environ['TEST'] = str(opts.test)
        
    if opts.action == 'backup':
        return run_backup(opts.match)
    elif opts.action == 'restore':
        return run_restore(idmatch=opts.match)
    elif opts.action == 'list':
        return entries_lookup(opts.project, opts.match, opts.limit)
    elif opts.action == 'config':
        return CONFIG.show_info()
    elif opts.action == 'check':
        return run_check()
    elif opts.action == 'schedule':
        return schedule(opts.match)
    elif opts.action == 'configbackup':
        return NotImplemented
    elif opts.action == 'projects':
        return show_projects()
    elif opts.version:
        return sheep_version
    else:
        #print('Unknown action: {0}. Possible actions: backup, restore, list'.format(opts.action))
        return parser.format_help()
   
if __name__ == "__main__":
    print(loader())