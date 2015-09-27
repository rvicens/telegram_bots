import logging
import telegram
from yapsy.IPlugin import IPlugin
from lib.cnmvAPI import *

class Check(IPlugin):

    name = "HR Plugin"
    command = "/hr"
    description = "Plugin to check 'Hechos Relevantes'. e.g. /hr"

    def getCompanies(self,msg):
        out = []
        msgs = msg.split(",")
        for item in msgs:
            if item:
                out.append(item.replace(" ","").upper())
        return out

    def run(self,msg):

        results = {"text":"","replay_markup":""}

        logger = logging.getLogger("Main.HR")
        logger.debug("Running HR plugin")
        companies = self.getCompanies(msg)
        cnmv = cnmvAPI()

        if len(companies) > 0:
            results["text"] = cnmv.getComapanyHR(companies)
            results["replay_markup"] = None
        else:
            results["text"] = "Try the following companies typing:\n\n"
            custom_keyboard = []
            for key in sorted(cnmv.companies.keys()):
                custom_keyboard.append(["/hr {0}".format(key)])

            results["replay_markup"] = telegram.ReplyKeyboardMarkup(custom_keyboard)

        logger.debug("Finished HR plugin")

        return results
