class Commands:
    def __init__(self, callback):
        self._callback = callback
        self._msg = callback.msg
        self._users = callback.users
        
    def register(self, user, channel, text):
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
        if not self._users[user]['op']:
            self._msg(channel, "%s: only ops can use this command" % user)
            return
        target = text.strip()
        if self._isNick(user, channel, target):
            self._msg(channel, "%s: go ahead and !register" % target)
            self._users[target]['allowed'] = True

    def test(self, user, channel, text):
        print 'test'
    def _test(self, user, channel, text):
        print '_test'

    def _isNick(self, user, channel, nick):
        if len(nick) == 0:
            self._msg(channel, "%s: specify a nick, dummy!" % user)
            return False
        elif nick not in self._users:
            self._msg(channel, "%s: specify the nick of someone actually in the channel, dummy!" % user)
            return False
        else:
            return True
    
