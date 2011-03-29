import os

class PluginManager():
    def __init__(self, plugins_path='plugins'):
        self.plugins_path = plugins_path
        self.plugin_modules = []
    def loadPlugins(self):
        files = os.listdir(self.plugins_path)
        for file in files:
            if file[0] != '.' and file[-2:] == 'py':
                path = os.path.basename(self.plugins_path) + '.' + os.path.splitext(file)[0]
                try:
                    self.plugin_modules.append(__import__(path))
                except ImportError as e:
                    print 'Plugin (%s) not loaded. [%s]' % (path, e)
                else:
                    print 'Plugin (%s) loaded.' % path
def main():
    pm = PluginManager()
    pm.loadPlugins()
main()
