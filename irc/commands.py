class Commands:
    def __init__(self, callback):
	self.commands = {}
	self.callback = callback
    def register(self, user, channel, text):
	if user.nick in self.callback.allowed:
	    channel.message("%s has registered. (not really)" % user.nick)
	    channel.message("nazgjunk: send HarryD the !register code damn it")
	else:
	    channel.message("NO")
    def allow(self, user, channel, text):
	channel.message("%s: go ahead and !register" % text.strip())
	self.callback.allowed.append(text.strip())
