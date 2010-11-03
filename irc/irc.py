from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

from commands import Commands

# system imports
import time, sys

class User:
    def __init__(self, nick, messager):
        self.nick = nick
        self.messager = messager
    def message(self, msg):
        self.messager.msg(self.nick, msg)
        
class Channel:
    def __init__(self, name, messager):
        self.name = name
        self.messager = messager
    def message(self, msg):
        self.messager.msg(self.name, msg)
        
class MessageLogger:
    """
    An independent logger class (because separation of application
    and protocol logic is a good thing).
    """
    def __init__(self, file):
        self.file = file

    def log(self, message):
        """Write a message to the file."""
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        self.file.write('%s %s\n' % (timestamp, message))
        self.file.flush()

    def close(self):
        self.file.close()


class LogBot(irc.IRCClient):
    """A logging IRC bot."""
    
    nickname = "jp2"
    
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.cmds = Commands(self)
        self.logger = MessageLogger(open(self.factory.filename, "a"))
        self.logger.log("[connected at %s]" % 
                        time.asctime(time.localtime(time.time())))

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        self.logger.log("[disconnected at %s]" % 
                        time.asctime(time.localtime(time.time())))
        self.logger.close()



    # callbacks for events

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        self.join(self.factory.channel)

    def joined(self, channel):
        """This will get called when the bot joins the channel."""
        self.logger.log("[I have joined %s]" % channel)

    def handleCommand(self, command, prefix, params):
        pass

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        print user
        user = User(user.split('!', 1)[0], self)
        channel = Channel(channel, self)
        self.logger.log("<%s> %s" % (user, msg))
        

        if msg[0] == '!':
            cmd = msg[1:].split(' ')[0]
            if hasattr(self.cmds, cmd) and cmd != '__init__':
                func = getattr(self.cmds, cmd, None)
                func(user, channel, msg[len(cmd)+2:])
            else:
                channel.message('%s: Command not found.' % user.nick)
        # Check to see if they're sending me a private message
        if channel.name == self.nickname:
            msg = "It isn't nice to whisper!  Play nice with the group."
            user.message(msg)
            return

        # Otherwise check to see if it is a message directed at me

    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        user = user.split('!', 1)[0]
        self.logger.log("* %s %s" % (user, msg))

    # irc callbacks

    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        old_nick = prefix.split('!')[0]
        new_nick = params[0]
        self.logger.log("%s is now known as %s" % (old_nick, new_nick))

class LogBotFactory(protocol.ClientFactory):
    """A factory for LogBots.

    A new protocol instance will be created each time we connect to the server.
    """

    # the class of the protocol to build when new connection is made
    protocol = LogBot

    def __init__(self, channel, filename):
        self.channel = channel
        self.filename = filename

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()

