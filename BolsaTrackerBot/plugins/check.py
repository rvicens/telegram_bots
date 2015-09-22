import logging
import telegram
from yapsy.IPlugin import IPlugin
from lib.stockQuotesAPI.ecobolsaSearch import *

class Check(IPlugin):

    name = "Check Plugin"
    command = "/check"
    description = "Plugin to check quotes. e.g. /check INDITEX"

    def getCompanies(self,msg):
        out = []
        msgs = msg.split(",")
        for item in msgs:
            if item:
                out.append(item.replace(" ","").upper())
        return out

    def run(self,msg):

        results = {"text":"","replay_markup":""}

        logger = logging.getLogger("Main.Check")
        logger.debug("Running Check plugin")
        companies = self.getCompanies(msg)
        ecob = ecobolsaSearch()

        if len(companies) > 0:
            results["text"] = ecob.getComapanyQuote(companies)
            results["replay_markup"] = None
        else:
            results["text"] = "Try the following companies typing:\n\n"
            custom_keyboard = []
            for key in sorted(ecob.companies.keys()):
                custom_keyboard.append(["/check {0}".format(key)])

            results["replay_markup"] = telegram.ReplyKeyboardMarkup(custom_keyboard)

        logger.debug("Finished Check plugin")
        return results
