from sheepcore.utils import Checklist, program_exists

parser_choices = ['sqlite', 'mysql', 'collect']

__all__ = ['db', 'files', 'parser_choices']

class BaseOption(object):
    def __init__(self): pass
    def check(self):
        raise NotImplementedError()
        
    def check_required(self):
        checks = []
        for prog in self.required_programs:
            exists = program_exists(prog)
            msg = '{0} is{1} installed'.format(prog, '' if exists else ' not')
            
            checks.append(Checklist(msg=msg, ok=exists is not None, tag=self.__class__.type))
        return checks

# Tools