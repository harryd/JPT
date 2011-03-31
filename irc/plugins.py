import os

class PluginManager():
    def __init__(self, plugins_path='plugins'):
        self.plugins_path = plugins_path
        self.plugin_modules = []
    def loadPlugins(self):
        files = os.listdir(self.plugins_path)
        for file in files:
            if file[0] != '.' and file[-2:] == 'py':
                path = self.plugins_path + '/' + file
                try:
                    execfile(path)
                except ImportError as e:
                    print 'File [%s] not loaded. (%s)' % (path, e)
                else:
                    print 'File [%s] loaded.' % path
    def clear(self):
        self.plugin_modules = []


pm = PluginManager()
pm.loadPlugins()
