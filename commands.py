import logging

class UsageError(Exception):
	'''Invalid client usage of command'''
	def __init__(self, value=''):
		Exception.__init__(self, value)

class CommandManager:
	def __init__(self):
		self.prefixes = '!'
		self.command_handlers = {}
	def register(self, command, func):
		if not self.command_handlers.has_key(command):
			self.command_handlers[command] = []
		self.command_handlers[command].append(func)
	def trigger(self, user, command, text):
		if self.command_handlers.has_key(command):
			for func in self.command_handlers[command]:
				try:
					func(user, text)
				except UsageError, e:
					user.message('Invalid Usage of !' + command + ' command. ' + str(e))
				except:
					exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()	
					logging.warn('Uncaught exception occured in command handler.')
					logging.warn(traceback.format_exc())
		else:
			user.message('Command not found')
	def onMsg(self, user, text):
		if len(text) > 0 and self.prefixes.find(text[0]) != -1:
			cmd = text[1:].split(' ')[0]
			self.trigger(user, cmd, text[len(cmd)+2:])

commandmanager = CommandManager()

def registerCommandHandler(command, func):
	commandmanager.register(command, func)

class commandHandler(object):
	def __init__(self, name):
		self.command_name = name
	def __call__(self, f):
		self.__doc__ = f.__doc__
		self.__name__ = f.__name__
		registerCommandHandler(self.command_name, f)
		return f

@commandHandler('echo')
def echo(user, msg):
    user.message("hi %s" % user.nick)
