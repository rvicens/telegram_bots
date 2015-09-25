import logging
import telegram
from yapsy.IPlugin import IPlugin
from lib.stockQuotesAPI.pcbolsaSearch import *

class Check(IPlugin):

    name = "HR Plugin"
    command = "/hr"
    description = "Plugin to check 'Hechos Relevantes'. e.g. /hr"

    def run(self,msg):

        results = {"text":"","replay_markup":""}

        logger = logging.getLogger("Main.HR")
        logger.debug("Running HR plugin")


        results["text"] = ""
        results["replay_markup"] = None

        logger.debug("Finished HR plugin")
        return results
