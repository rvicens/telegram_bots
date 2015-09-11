import logging
from yapsy.IPlugin import IPlugin

class Help(IPlugin):

    name = "Help Plugin"
    command = "/help"
    description = "Help plugin"

    def run(self,msg):

        results = {"text":"","replay_markup": None }
        logger = logging.getLogger("Main.Help")
        logger.debug("Running Help plugin")

        results["text"] = "You can use the following commands:\n\n\t/check company\n\t/help"
        logger.debug("Finished Help plugin")
        return results
