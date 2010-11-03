class Commands:
    def __init__(self, callback):
	self.commands = {}
	self.callback = callback
    def register(self, user, channel, text):
	channel.message("nazgjunk: send HarryD the !register code damn it")
    def echo(self, user, channel, text):
	channel.message("%s: good day" % user.nick)
    def who(self, user, channel, text):
	channel.message(self.callback.irc_LIST(user.nick, channel.name))
