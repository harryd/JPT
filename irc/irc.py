from twisted.words.protocols import irc
from twisted.internet import reactor, protocol

from users import User
import commands, plugins
import time, sys
       
class JPTBot(irc.IRCClient):
    '''A higly configurable IRC bot.'''
    def __init__(self):
        self.nickname = 'JPT'
        #self.lineRate = 1
        self.users = {}
        self.queue = []
        self.sent = []
        
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)    
        print 'Connected to server.'
        
    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        print 'Disconnected from server.'

    def signedOn(self):
        for channel in self.factory.channels:
            self.join(channel)

    def joined(self, channel):
        self.who(channel)
        print "Joined channel: %s" % channel

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
        user = user.split('!', 1)
        if len(user) == 2:
            user, hostmask = user[0], user[1]
        else:
            user = user[0]
        if msg == '!reload':
            print 'Reloading'
            commands.commandmanager.clear()
            reload(plugins)
            return
        if user in self.users:
            user = self.users[user]
        else:
            user = User(self, user, channel)
        commands.commandmanager.onMsg(self, user, channel, msg)

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
        try:
            for user in self.users:
                if user not in self.new_users:
                    del self.users[str(user)]
        except RuntimeError:
            print 'ERROR: WHO happened too fast.'

    def invalidate_chanmodes(self, user, channel, *args, **kwargs):
        self.who(channel)
    #irc_NICK    = invalidate_chanmodes
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

    def __init__(self, channels):
        self.channels = channels

    def clientConnectionLost(self, connector, reason):
        '''If we get disconnected, reconnect to server.'''
        print 'Reconnecting.'
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print 'connection failed:', reason
        reactor.stop()

