class Commands:
    def __init__(self, callback):
        self._callback = callback
        
    def register(self, user, channel, text):
        if self._callback.users[user]['allowed']:
            self._callback.msg(channel, "%s has registered. (not really)" % user)
            self._callback.users[user]['allowed'] = False
        elif self._callback.users[user]['voice']:
            self._callback.msg(channel, "%s has registered. (not really)" % user)
            self._callback.devoice(user, channel)
        else:
            self._callback.msg(channel, "%s: you are not allowed to register now" % user)
            self._callback.msg(channel, "%s: read the TOS and FAQ then ask an op for an account" % user)
            
    def allow(self, user, channel, text):
        if not self._callback.users[user]['op']:
            self._callback.msg(channel, "%s: only ops can use this command" % user)
            return
        target = text.strip()
        if self._isNick(target):
            self._callback.msg(channel, "%s: go ahead and !register" % target)
            self._callback.users[target]['allowed'] = True

    def test(self, user, channel, text):
        print 'test'
    def _test(self, user, channel, text):
        print '_test'

    def _isNick(self,nick):
        if len(target) == 0:
            self._callback.msg(channel, "%s: specify a nick, dummy!" % user)
            return False
        elif target not in self._callback.users:
            self._callback.msg(channel, "%s: specify the nick of someone actually in the channel, dummy!" % user)
            return False
        else:
            return True
    
