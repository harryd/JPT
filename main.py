#!/usr/bin/python2
from irc.irc import JPTBotFactory
from twisted.internet import reactor, protocol
from twisted.python import log
import sys

DEBUG = True
if __name__ == '__main__':
    # temporary - perhaps replaced with optparse or a config file.
    if len(sys.argv) != 2:
        print "usage: %s <channel>" % sys.argv[0]
        sys.exit()

    # initialize logging
    if DEBUG == False:
        log.startLogging(open('JPT.log', 'a+'))
    
    # create factory protocol and application
    f = JPTBotFactory(sys.argv[1:])
    
    # connect factory to this host and port
    reactor.connectTCP("irc.freenode.net", 6667, f)
    log.msg("thing started")
    # run bot
    reactor.run()
