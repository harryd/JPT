import sys, traceback

class UsageError(Exception):
    '''Invalid client usage of command'''
    def __init__(self, value=''):
        Exception.__init__(self, value)

class ExtraArgumentError(UsageError):
    '''Argument specified when none expected'''
    def __init__(self):
        UsageError.__init__(self, 'Extra argument specified')

class StateError(Exception):
    '''State of server is invalid for command'''
    def __init__(self, value):
        Exception.__init__(self, value)

class ArgumentValueError(Exception):
    '''Value of an argument is erroneous'''
    def __init__(self, value):
        Exception.__init__(self, value)

class CommandManager:
    def __init__(self):
        self.prefixes = '#.!'
        self.command_handlers = {}
    
    def register(self, command, func):
        if not self.command_handlers.has_key(command):
            self.command_handlers[command] = []
        self.command_handlers[command].append(func)
    
    def trigger(self, cb, user, channel, command, text):
        if self.command_handlers.has_key(command):
            for func in self.command_handlers[command]:
                try:
                    func(cb, user, channel, text)
                except UsageError, e:
                    try:
                        usages = command_info[command].usages
                    except KeyError:
                        usages = []
                    user.message('Invalid Usage of #' + command + ' command. ' + str(e))
                    for usage in usages:
                        user.message('Usage: ' + command + ' ' + usage)
                except StateError, e:
                    user.message(str(e))
                except ArgumentValueError, e:
                    user.message('Invalid argument. ' + str(e))
                except ValueError:
                    user.message('Value Error: Did you specify a valid user?')
                except:
                    pass
        else:
            user.message('Command not found')
    
    def onMsg(self, cb, user, channel, text):
        if len(text) > 0 and self.prefixes.find(text[0]) != -1:
            cmd = text[1:].split(' ')[0]
            self.trigger(cb, user, channel, cmd, text[len(cmd)+2:])
            return False
        return True

commandmanager = CommandManager()

def registerCommandHandler(command, func):
    commandmanager.register(command, func)

class commandHandler(object):
    def __init__(self, name):
        self.command_name = name
    def __call__(self, f):
        self.__doc__ = f.__doc__
        self.__name__ = f.__name__
        registerCommandHandler(self.command_name, f)
        return f

@commandHandler('notr')
def notrfunc(cb, user, channel, text):
    print "yo"
    user.message("hi")

