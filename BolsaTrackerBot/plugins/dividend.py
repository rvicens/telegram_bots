import logging
import telegram
from yapsy.IPlugin import IPlugin
from lib.stockQuotesAPI.pcbolsaSearch import *

class Check(IPlugin):

    name = "Dividend Plugin"
    command = "/dividend"
    description = "Plugin to check upcomming dividends. e.g. /dividend"

    def beautify(self,dividend_info):

        out = ""
        for i in dividend_info:
            out += "Company:{0}\nDate:{1}\nYear:{2}\nPayment Type:{3}\n".format(i["company"],i["date"],i["year"],i["payment_type"])
            out += "Gross:{0}\nNet:{1}".format(i["gross"],i["net"])
            out += "\n\n---\n"

        return out

    def run(self,msg):

        results = {"text":"","replay_markup":""}

        logger = logging.getLogger("Main.Dividend")
        logger.debug("Running Dividend plugin")

        pcbolsa = pcbolsaSearch()
        results["text"] = self.beautify(pcbolsa.getDividend())
        results["replay_markup"] = None

        logger.debug("Finished Dividend plugin")
        return results
