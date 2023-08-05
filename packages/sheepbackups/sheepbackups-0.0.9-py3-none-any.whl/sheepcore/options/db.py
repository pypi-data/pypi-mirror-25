import shutil, subprocess, os

from sheepcore import get_logger
from sheepcore.options import BaseOption
from sheepcore.utils import Checklist, program_exists
logger = get_logger('backup')

class Database(BaseOption): pass

class MySQL(Database): 
    type = 'mysql'
    required_programs = ['mysqldump', 'mysql']
    
    def __init__(self, opts=None):
        self._opts = opts
        self.dbname = opts.get('dbname', 'db')
        
        try:
            self.config = opts['config']
        except KeyError:
            raise Exception('mysql setting has no `config` variable. See docs/100')
            
        self._export_cmd = ['mysqldump', '--defaults-extra-file={0}'.format(self.config)]
        
        if self.dbname != 'db':
            self._export_cmd.extend(['-B', self.dbname])
            
        logger.debug('mysql export cmd: {0}'.format(' '.join(self._export_cmd)))
        
    def setup(self, temp_dir, *args, **kwargs):
        self._temp_dir = temp_dir
        
    def check(self):
        # program exists
        checklists = self.check_required()
            
        return checklists
        
    def run(self, temp_dir=None):
        dest_dir = os.path.join(self._temp_dir, 'mysql.{0}'.format(self.dbname))
        os.makedirs(dest_dir)
        
        with open(os.path.join(dest_dir, 'export.sql'), 'w') as f:
            dump = subprocess.call(self._export_cmd, stdout=f, stderr=f)
        # Log
        logger.info('mysqldump output code: {0}'.format(dump))
        
    def setup_reverse(self, source_dir, opts=None): 
        error = ''
        text = ''
        warn = None
        sqlfile = os.path.join(source_dir, 'mysql.{0}'.format(opts['dbname']), 'export.sql')
        
        cmd = ['mysql']
        
        if not os.path.exists(sqlfile):
            error = 'Cannot find .sql file in backup'
            
        if not os.path.exists(opts['config']):
            warn = 'No config file found (tried {0}), using without'.format(opts['config'])
        else:
            cmd.append('--defaults-extra-file={0}'.format(opts['config']))
        
        cmd.extend(['-h', opts['dbname'], '<', sqlfile])
        
        text = 'Restoring .sql file for {0}'.format(opts['dbname'])
        
        actions = [{
            'cmd': cmd,
            'error': error,
            'text': text,
            'warn': warn
        }]
        
        return {'actions': actions, 'errors': int(error != '')}
    

class Sqlite(Database):
    """
    For now, just copy the .sqlite file
    """
    type = 'sqlite'
    required_programs = ['sqlite3']
    
    def __init__(self, opts=None):
        self._opts = opts
        
    def setup(self, temp_dir, *args, **kwargs):
        self._temp_dir = temp_dir
        
    def check(self):
        # program exists
        checklists = self.check_required()
            
        return checklists
        
        
    def run(self):
        for sqlitepath in self._opts:
            try:
                os.makedirs(os.path.join(self._temp_dir, 'sqlite'))
            except FileExistsError:
                pass
            
            try:
                # Copy file tree
                shutil.copy2(sqlitepath, os.path.join(self._temp_dir, 'sqlite', os.path.basename(sqlitepath)))
                
                # logging
                logger.info('Copied sqlite db {0}'.format(sqlitepath))
            except Exception as err:
                logger.error(err)
            
    def reverse(self):
        pass
    
    def setup_reverse(self, source_dir, opts=None): 
        actions = []
        errcount = 0
        if opts is None:
            return
    
        for file in opts:
            error = ''
            warn = None
            
            basefile = os.path.basename(file)
            sqlite_file = os.path.join(source_dir, 'sqlite', basefile)
            cmd = ['cp', '-vf', sqlite_file, file]
            
            # Check existence/permissions
            if not os.path.exists(sqlite_file):
                error = 'sqlite file does not exist in backup: {0}'.format(basefile)
            overwrite = os.path.exists(file)
                
            text = 'Copying {0} to {1}'.format(basefile, os.path.dirname(file))
            if overwrite is True:
                warn = 'will overwrite directory'
            actions.append({
                'cmd': cmd,
                'error': error,
                'text': text,
                'warn': warn
            })
            
            if error != '':
                errcount += 1
        
        return {'actions': actions, 'errors': errcount}