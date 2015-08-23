import requests

class yahooAPI():
    def __init__(self):
        self.proto = "http://"
        self.host = "download.finance.yahoo.com"
        self.path = "/d/quotes.csv"
        self.filter = "nsl1op"

    def setYahooFilter(self,new_filter):
        if new_filter:
            self.filter = str(new_filter)

    def getQuote(self,yahoo_ids):
        stockIndex = ""
        for yahoo_id in yahoo_ids:
            stockIndex += yahoo_id + ","
        stockIndex = stockIndex[:-1]

        url = "{0}{1}{2}".format(self.proto,self.host,self.path)

        payload = {'f':self.filter, 'e':'.csv', 's':stockIndex }
        r = requests.get(url, verify=False, timeout=60, params=payload)
        resp = r.text
        out = "Company Name, Symbol, Last Trade Price, Min. Price, Max. Price\n"
        out += resp

        return out

if __name__ == '__main__':

    companies = ["GOOG","MSFT"]
    y = yahooAPI()
    print y.getQuote(companies)
