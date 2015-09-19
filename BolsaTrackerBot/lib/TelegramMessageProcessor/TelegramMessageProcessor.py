#!/usr/bin/env python
import logging
import os
from yapsy.PluginManager import PluginManager

class TelegramMessageProcessor():

    def __init__(self):
        self.msg = None
        self.cmd = None
        self.logger = logging.getLogger("Main.TelegramMessageProcessor")


    def extractMessage(self, tlg_msg):
        try:
            self.msg = tlg_msg.message.text.encode('utf-8')
        except:
            self.logger.exception("Exception occurred while encoding message at 'extractMessage' with message:{0}".format(self.msg))
            self.msg = None
            return False
        return True


    def extractCmd(self):

        if not str(self.msg).startswith("/"):
            return False

        first_space = str(self.msg).find(" ")
        if first_space == -1:
            self.cmd = self.msg.lower()
        else:
            self.cmd = self.msg[:first_space].lower()

        self.logger.debug("Extracted command:'{0}' form message '{1}'".format(self.cmd,self.msg))
        return True

    def validateMessage(self):
        return self.extractCmd()


    def process(self, tlg_msg):
        self.extractMessage(tlg_msg)
        if self.validateMessage():
            self.logger.debug("Message seems OK. Seeking for plugins")
            return self.execPlugin()
        return None


    def execPlugin(self):

        out_message = {"text":"","replay_markup":""}

        pm = PluginManager()

        plugins_dir = []
        plugins_dir.append(os.getcwd() + os.sep + "plugins")

        pm.setPluginPlaces(plugins_dir)
        pm.collectPlugins()

        try:
            # Trigger 'some action' from the loaded plugins
            for pluginInfo in pm.getAllPlugins():
                if pluginInfo.plugin_object.command == self.cmd:
                    self.logger.debug("Running '{0}' plugin".format(pluginInfo.plugin_object.name))
                    msg = self.msg.replace(self.cmd,"")
                    out_message = pluginInfo.plugin_object.run(msg)
                    break
        except:
            self.logger.exception("Error executing command:{0}".format(self.cmd))

        return out_message
