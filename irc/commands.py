# This is where all the commands go.
# to make a new command, create a method with the command name you want
# if you need a method that should not be a command prefix it with a '_'
# all commands have the signature 'def command(self, user, channel, text)' 
# user is the user that sent the command
# channel is the channle where the user sent the command ( channel == user for a private message)
# text is the part after !command so if the user sent '!command someparam' then text would be 'someparam'
class Commands:
    '''Usage: !<command> [params]
    
    Some help here'''
    def __init__(self, callback):
        self._callback = callback
        self._msg = callback.msg
        self._users = callback.users
    
    def _isNick(self, user, channel, nick):
        if len(nick) == 0:
            self._msg(channel, "%s: specify a nick, dummy!" % user)
            return False
        elif nick not in self._users:
            self._msg(channel, "%s: specify the nick of someone actually in the channel, dummy!" % user)
            return False
        else:
            return True
    
    def help(self, user, channel, text):
        '''Usage: !help [command]

        Show the help for a command or the general help.'''
        if hasattr(self, text.strip()) and text[0] != '_':
            self._msg(user, ''.join(getattr(self, text).__doc__.split('\n')[2].strip()))
        else:
            self._msg(user, ''.join(self.__doc__.split('\n')[2].strip()))
    
    def usage(self, user, channel, text):
        '''Usage: !usage [command]

        Show the usage of a command or the general usage.'''
        if hasattr(self, text.strip()) and text[0] != '_':
            self._msg(user, getattr(self, text).__doc__.split('\n')[0])
        else:
            self._msg(user, self.__doc__.split('\n')[0])

    def commands(self, user, channel, text):
        '''Usage: !commands

        List all the commands supported by the bot.'''
        self._msg(user, ' !'.join([i for i in dir(self) if not i[0] == '_']))
        self._msg(user, 'Use !help or !usage to show more about the command.')
                
    def register(self, user, channel, text):
        '''Usage: !register

        Registers a user on the server'''
        if self._users[user]['allowed']:
            self._msg(channel, "%s has registered. (not really)" % user)
            self._users[user]['allowed'] = False
        elif self._users[user]['voice']:
            self._msg(channel, "%s has registered. (not really)" % user)
            self._callback.devoice(user, channel)
        else:
            self._msg(channel, "%s: you are not allowed to register now" % user)
            self._msg(channel, "%s: read the TOS and FAQ then ask an op for an account" % user)
            
    def allow(self, user, channel, text):
        '''Usage: !allow <nick>

        allow a user to register using !register'''

        if not self._users[user]['op']:
            self._msg(channel, "%s: only ops can use this command" % user)
            return
        target = text.strip()
        if self._isNick(user, channel, target):
            self._msg(channel, "%s: go ahead and !register" % target)
            self._users[target]['allowed'] = True

