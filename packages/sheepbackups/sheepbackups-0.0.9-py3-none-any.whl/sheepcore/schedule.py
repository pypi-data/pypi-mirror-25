# add to crontab 
# https://stackoverflow.com/questions/4880290/how-do-i-create-a-crontab-through-a-script
# add a comment with # in the crontab file, and end with a comment if possible, to make sure if we remove it it doesn't break others
import delegator

from sheepcore.utils import program_exists

class Schedule(object):
    
    has_cron = False
    exists = False
    
    min = '*'
    hour = '*'
    day = '*'
    month = '*'
    dayofweek = '*'
    path = None
    action = None
    
    def __init__(self):
        self.has_cron = program_exists('crontab') is not None
        
        self.load()
    
    def load(self):
        # load crontab, ditch random stuff
        if self.has_cron:
            cmd = delegator.run('crontab -l')
            
            if cmd.return_code == 0:
                for line in cmd.out.splitlines():
                    #if 'sheep backup' in line:
                    if 'sheep backup' in line:
                        self.parse_line(line)
                        self.exists = True
                        return True
            
        return None
        
    def parse_line(self, line):
        sp = line.split(' ')
        
        # expectations
        self.min = sp[0]
        self.hour = sp[1]
        self.day = sp[2]
        self.month = sp[3]
        self.dayofweek = sp[4]
        
        self.path = sp[5]
        self.action = sp[6]
        
    def add_new(self):
        # if we want to run at midnight
        new_cmd = '0 0 * * * {0} backup'
        
        fullpath = program_exists('sheep')
        
        croncmd = new_cmd.format(fullpath)
        
        # add croncmd if it doesn't already exist