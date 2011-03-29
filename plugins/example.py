from irc.commands import commandHandler

@commandHandler('example', 'e') # This handles !example and !e
def example_command(cb, user, channel, text):
    '''A standard command with the usage here.

    And the help here.'''
    user.message('A private message to the user.')
    user.channel_message('A message directed at the user.')
    print 'I log to JPT.log'
    cb.join('#example')
    
