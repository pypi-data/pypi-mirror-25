import shutil, os, logging

from sheepcore.options import BaseOption
from sheepcore import get_logger
logger = get_logger('backup')

class Collect(BaseOption):
    type = 'collect'
    dirs = {}
    
    def __init__(self, dirs=None, exclude=None):
        self.dirs = dirs
        self.exclude = exclude
        
        logger.debug('dirs: {0}'.format(dirs))
        logger.debug('exclude: {0}'.format(exclude))
    
    def setup(self, temp_dir, *args, **kwargs):
        self._temp_dir = temp_dir
        
    def check(self):
        pass
        
    def run(self):
        # Also backup 'files' key
        ignore = None
        if self.exclude is not None:
            ignore = shutil.ignore_patterns(*self.exclude)
        
        for (dest_dir, src_dir) in self.dirs.items():
            try:
                # Copy file tree
                shutil.copytree(src_dir, os.path.join(self._temp_dir, 'files', dest_dir), ignore=ignore)
                
                logger.info('Directory {0} copied'.format(src_dir))
            except Exception as err:
                # Pass back error message
                logger.error(err)
    
    def setup_reverse(self, source_dir, opts=None):
        actions = []
        errcount = 0
        try:
            assert opts is not None
        except:
            return
        
        if 'dirs' not in opts and 'files' not in opts:
            return
        
        # Dirs
        if 'dirs' in opts:
            for directory, dest in opts['dirs'].items():
                #print('file', dest, directory)
                error = ''
                warn = None
                
                filesdir = os.path.join(source_dir, 'files', directory)
                cmd = ['cp', '-rfv', os.path.join(filesdir, '.'), dest]
                
                if not os.path.exists(filesdir):
                    error = '{0} directory does not exist in backup'.format(directory)
                if not os.path.exists(dest):
                    error = 'Destination directory does not exist ({0})'.format(dest)
                    
                # @todo Recursively check directories to see exactly what files will be overwritten
                text = 'Copying directory {0} to {1}'.format(directory, dest)
                actions.append({
                    'cmd': cmd,
                    'error': error,
                    'text': text,
                    'warn': warn
                })
                
                if error != '':
                    errcount += 1
        
        # Files
        if 'files' in opts:
            for file in opts['files']:
                error = ''
                warn = None
                
                basefile = os.path.basename(file)
                filesdir = os.path.join(source_dir, 'files', basefile)
                cmd = ['cp', '-rfv', filesdir, file]
                
                if not os.path.exists(filesdir):
                    error = '{0} does not exist in backup'.format(basefile)
                if os.path.exists(dest):
                    warn = 'File already exists, will overwrite ({0})'.format(file)
                    
                # @todo Recursively check directories to see exactly what files will be overwritten
                text = 'Copying {0} to {1}'.format(os.path.join('files', basefile), file)
                actions.append({
                    'cmd': cmd,
                    'error': error,
                    'text': text,
                    'warn': warn
                })
                
                if error != '':
                    errcount += 1
                
        return {'actions': actions, 'errors': errcount}
    
    def reverse(self, commit=False):
        pass