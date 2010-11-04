class Commands:
    def __init__(self, callback):
      	self.callback = callback
        self.callback.badcmd = ['__init__', 'badcmd', 'callback', 'msg', 'users']
        
    def register(self, user, channel, text):
	if self.callback.users[user]['allowed']:
	    self.callback.msg(channel, "%s has registered. (not really)" % user)
	    self.callback.users[user]['allowed'] = False
	elif self.callback.users[user]['voice']:
	    self.callback.msg(channel, "%s has registered. (not really)" % user)
            self.callback.devoice(user, channel)
	else:
	    self.callback.msg(channel, "%s: you are not allowed to register now" % user)
            self.callback.msg(channel, "%s: read the TOS and FAQ then ask an op for an account")
	    
    def allow(self, user, channel, text):
	if self.callback.users[user]['op']:
	    self.callback.msg(channel, "%s: go ahead and !register" % text.strip())
	    self.callback.users[nick]['allowed'] = True
	else:
	    self.callback.msg(channel, "%s: only ops can use this command" % user.nick)
