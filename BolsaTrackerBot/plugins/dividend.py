import logging
import telegram
from yapsy.IPlugin import IPlugin
from lib.stockQuotesAPI.pcbolsaSearch import *

class Check(IPlugin):

    name = "Dividend Plugin"
    command = "/dividend"
    description = "Plugin to check upcomming dividends. e.g. /dividend"

    def beautify(self,dividend_info):

        return []

    def run(self):

        results = {"text":"","replay_markup":""}

        logger = logging.getLogger("Main.Dividend")
        logger.debug("Running Dividend plugin")

        pcbolsa = pcbolsaSearch()
        results["text"] = self.beautify(pcbolsa.getDividend())
        results["replay_markup"] = None

        logger.debug("Finished Dividend plugin")
        return results
