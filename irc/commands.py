class Commands:
    def __init__(self):
	self.commands = {}
    def register(self, user, channel, text):
	channel.message("nazgjunk: send HarryD the !register code damn it")
    def echo(self, user, channel, text):
	channel.message("%s: good day" % user.nick)
