from yapsy.IPlugin import IPlugin
from lib.stockQuotesAPI.yahooAPI import *

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
        companies = self.getCompanies(msg)
        y = yahooAPI()
        results = y.getQuote(companies)
        results += y.getChart(companies)
        return results
