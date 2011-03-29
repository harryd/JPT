from twisted.python import log
import time
class Logger:
    '''
    An independent logger class (because separation of application
    and protocol logic is a good thing).
    '''
    def __init__(self, file):
        self.log_file = file

    def log(self, message):
        '''Write a message to the file.'''
        timestamp = time.strftime('[%H:%M:%S]', time.localtime(time.time()))
        self.log_file.write('%s %s\n' % (timestamp, message))
        self.log_file.flush()

    def close(self):
        self.log_file.close()
