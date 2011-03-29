from twisted.words.protocols import irc
from twisted.internet import reactor, protocol


from commands import commandmanager
from users import User
from logging import Logger
from plugins import PluginManager

# system imports
import time, sys
       
class JPTBot(irc.IRCClient):
    '''A higly configurable IRC bot.'''
    def __init__(self):
        self.nickname = 'JPT'
        #self.lineRate = 1
        self.users = {}
        self.channels = {}
        self.queue = []
        self.sent = []
        
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)    
        self.logger = Logger(open(self.factory.filename, 'a'))
        self.logger.log('[connected at %s]' % 
                        time.asctime(time.localtime(time.time())))
        
    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        self.logger.log('[disconnected at %s]' % 
                        time.asctime(time.localtime(time.time())))
        self.logger.close()
        
    def signedOn(self):
        for channel in self.factory.channels:
            self.join(channel)

    def joined(self, channel):
        self.logger.log('[I have joined %s]' % channel)
        self.who(channel)

    def msg(self, user, message, length=512):
        fmt = "PRIVMSG %s :%%s" % (user,)

        # NOTE: minimumLength really equals len(fmt) - 2 (for '%s') + 2
        # (for the line-terminating CRLF)
        minimumLength = len(fmt)
        if length <= minimumLength:
            raise ValueError("Maximum length must exceed %d for message "
                             "to %s" % (minimumLength, user))
        self.sendLine(fmt % (message,))

    def privmsg(self, user, channel, msg):
        user = user.split('!', 1)[0]
        if user in self.users:
            user = self.users[user]
        else:
            user = User(self, host=user)
        print commandmanager.onMsg(self, user, channel, msg)

    def who(self, channel):
        self.sendLine('WHO %s' % channel.lower())
        self.new_users = {}

    def irc_RPL_WHOREPLY(self, prefix, args):
        me, chan, uname, host, server, nick, modes, name = args
        user = User(self, nick, chan, host, modes)
        if user not in self.users:
            self.users[str(user)] = user
        self.new_users[str(user)] = user

    def irc_RPL_ENDOFWHO(self, prefix, args):
        for user in self.users:
            if user not in self.new_users:
                del self.users[str(user)]

    def irc_NICK(self, prefix, params):
        self.who(channel)
    
    def invalidate_chanmodes(self, user, channel, *args, **kwargs):
        self.who(channel)
    modeChanged = invalidate_chanmodes
    userJoined  = invalidate_chanmodes
    userLeft    = invalidate_chanmodes
    userKicked  = invalidate_chanmodes

class JPTBotFactory(protocol.ClientFactory):
    '''A factory for JPTBots.

    A new protocol instance will be created each time we connect to the server.
    '''

    # the class of the protocol to build when new connection is made
    protocol = JPTBot

    def __init__(self, channels, filename):
        self.channels = channels
        self.filename = filename

    def clientConnectionLost(self, connector, reason):
        '''If we get disconnected, reconnect to server.'''
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print 'connection failed:', reason
        reactor.stop()

