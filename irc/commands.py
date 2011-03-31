#import sys, traceback

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
        self.command_help = {}
        self.command_usage = {}
    
    def register(self, command, func):
        if not self.command_handlers.has_key(command):
            self.command_handlers[command] = []
            self.command_help[command] = []
            self.command_usage[command] = []
        self.command_handlers[command].append(func)
        self.command_help[command].append(''.join(func.__doc__.split('\n')[2:]))
        self.command_usage[command].append(func.__doc__.split('\n')[0])
    
    def trigger(self, cb, user, channel, command, text):
        if self.command_handlers.has_key(command):
            for func in self.command_handlers[command]:
                try:
                    func(cb, user, channel, text)
                except UsageError, e:
                    try:
                        usages = command_usage[command]
                    except KeyError:
                        usages = []
                    user.channel_message('Invalid Usage of !' + command + ' command. ' + str(e))
                    for usage in usages:
                        user.channel_message('Usage: ' + command + ' ' + usage)
                except StateError, e:
                    user.channel_message(str(e))
                except ArgumentValueError, e:
                    user.channel_message('Invalid argument. ' + str(e))
                except ValueError:
                    user.channel_message('Value Error: Did you specify a valid user?')
                except e:
                    print e
        else:
            user.channel_message('Command not found')
             
    def onMsg(self, cb, user, channel, text):
        if len(text) > 0 and self.prefixes.find(text[0]) != -1:
            cmd = text[1:].split(' ')[0]
            self.trigger(cb, user, channel, cmd, text[len(cmd)+2:])
            return False
        return True
    
    def clear(self):
        self.command_handlers = {}
        self.command_help = {}
        self.command_usage = {}
  

commandmanager = CommandManager()

def registerCommandHandler(command, func):
    if func.__doc__ == None:
        func.__doc__ = 'This function has no usage.\n\nThis function has no help.'
    commandmanager.register(command, func)


class commandHandler(object):
    def __init__(self, name, alias= None):
        self.command_name = name
        self.command_alias = alias
    def __call__(self, f):
        self.__doc__ = f.__doc__
        self.__name__ = f.__name__
        registerCommandHandler(self.command_name, f)
        if self.command_alias != None:
            commandmanager.register(self.command_alias, f)

        return f


