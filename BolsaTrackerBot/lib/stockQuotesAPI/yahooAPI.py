import requests

class yahooAPI():
    def __init__(self):
        self.proto = "http://"
        self.host = "download.finance.yahoo.com"
        self.path = "/d/quotes.csv"
        self.query_string = ""
        self.filter = "nsl1op"

    def setYahooFilter(self,new_filter):
        if new_filter:
            self.filter = str(new_filter)

    def setQueryString(self,queryValue):
        self.query_string = "?f={0}&e=.csv&s={1}".format(self.filter,queryValue)

    def getQuote(self,yahoo_id):
        stockIndex = yahoo_id
        self.setQueryString(stockIndex)
        url = "{0}{1}{2}{3}".format(self.proto,self.host,self.path,self.query_string)
        return True


