import sys

SHEEPEXC = {
    'no_to_config_found': [100, 'No `to` information was found for `{0}`'],
    'no_restore_no_key': [101, 'Cannot restore. Key `{0}` not found in config file.']
}

class SheepException(Exception): 
    def __init__(self, message, *args):
        if message in SHEEPEXC:
            m = SHEEPEXC[message][1]
            
            # Add help link
            if not m.endswith('.'):
                m += '.'
            m += ' Help: https://docs.sheepbackups.com/fromcli/{0}'.format(SHEEPEXC[message][0])
            
            self.message = m.format(*args)
        else:
            self.message = message.format(*args)
        super(SheepException, self).__init__(self.message)

class SheepConfigException(SheepException): pass

class SheepAPIError(SheepException): pass

class SheepSimpleError(SheepException):
    pass    