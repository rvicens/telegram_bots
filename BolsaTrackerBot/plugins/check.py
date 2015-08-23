from yapsy.IPlugin import IPlugin

class Check(IPlugin):

    name = "Check Plugin"
    command = "/check"
    description = "Plugin to check quotes. e.g. /check INDITEX"

    def run(self,msg):
        return "This is check plugin"
