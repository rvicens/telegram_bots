import logging
from yapsy.IPlugin import IPlugin
from lib.stockQuotesAPI.bolsaMadridSearch import *

class Check(IPlugin):

    name = "Check Plugin"
    command = "/check"
    description = "Plugin to check quotes. e.g. /check INDITEX"

    def getCompanies(self,msg):
        out = []
        msgs = msg.split(",")
        for item in msgs:
            out.append(item.replace(" ",""))
        return out

    def run(self,msg):
        logger = logging.getLogger("Main.Check")
        logger.debug("Running Check plugin")
        companies = self.getCompanies(msg)
        bm = BolsaMadridSearch()
        results = bm.getComapanyQuote(companies)
        logger.debug("Finished Check plugin")
        return results
