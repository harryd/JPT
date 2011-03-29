class User():
    def __init__(self, cb, nick='', channel=None, host='', modes=''):
        self.callback = cb
        self.nick = nick
        self.channel = channel
        self.host = host
        self.modes = modes

    def __str__(self):
        return "'%s'" % self.nick

    def message(self, message):
        self.callback.msg(str(self), message)
    
    def channel_message(self, message):
        self.callback.msg(self.channel, '%s: %s' % (str(self), message))
