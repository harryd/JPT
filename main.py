#!/usr/bin/python2.6
from irc.irc import LogBotFactory
from twisted.internet import reactor, protocol
from twisted.python import log
import sys

if __name__ == '__main__':
    # temporary - perhaps replaced with optparse or a config file.
    if len(sys.argv) != 2:
        print "usage: %s <channel>" % sys.argv[0]
        sys.exit()

    # initialize logging
    log.startLogging(sys.stdout)
    
    # create factory protocol and application
    f = LogBotFactory(sys.argv[1], 'jp.log')
    
    # connect factory to this host and port
    reactor.connectTCP("irc.freenode.net", 6667, f)

    # run bot
    reactor.run()
