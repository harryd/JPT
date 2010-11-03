from irc.irc import LogBotFactory
from irc.commands import commandHandler
from twisted.internet import reactor, protocol
from twisted.python import log
import sys

if __name__ == '__main__':
    # initialize logging
    log.startLogging(sys.stdout)
    
    # create factory protocol and application
    f = LogBotFactory('anapnea2', 'jp.log')
    
    # connect factory to this host and port
    reactor.connectTCP("irc.freenode.net", 6667, f)

    # run bot
    reactor.run()

@commandHandler("echo2")
def echothing(user, msg):
    '''@description echos hi to the user
       @usage'''
    user.message(msg)
    print "hi2"
