import logging
import telegram
from yapsy.IPlugin import IPlugin
from lib.stockQuotesAPI.ecobolsaSearch import *

class Check(IPlugin):

    name = "Check Plugin"
    command = "/check"
    description = "Plugin to check quotes. e.g. /check INDITEX"

    def run(self,msg):

        results = {"text":"","replay_markup":"","photo":""}

        logger = logging.getLogger("Main.Check")
        logger.debug("Running Check plugin")
        company = msg
        ecob = ecobolsaSearch()

        if len(company) > 0:
            results["text"] = ecob.getQuote(company)
            results["replay_markup"] = None
            results["photo"] = ecob.getChart(company)
        else:
            results["text"] = "Try the following companies typing:\n\n"
            custom_keyboard = []
            for key in sorted(ecob.companies.keys()):
                custom_keyboard.append(["/check {0}".format(key)])

            results["replay_markup"] = telegram.ReplyKeyboardMarkup(custom_keyboard)

        logger.debug("Finished Check plugin")
        return results
