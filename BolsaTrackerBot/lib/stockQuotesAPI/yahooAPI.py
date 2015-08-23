import requests

class yahooAPI():
    def __init__(self):
        self.proto = "http://"
        self.host = "download.finance.yahoo.com"
        self.path = "/d/quotes.csv"
        self.filter = "nsl1op"

        self.chartHost = "chart.finance.yahoo.com"
        self.chartPath ="/z"

    def setYahooFilter(self,new_filter):
        if new_filter:
            self.filter = str(new_filter)


    def setYahooIds(self,yahoo_ids):
        stockIndex = ""
        for yahoo_id in yahoo_ids:
            stockIndex += yahoo_id + ","
        stockIndex = stockIndex[:-1]
        return stockIndex

    def getQuote(self,yahoo_ids):

        stockIndex = self.setYahooIds(yahoo_ids)
        url = "{0}{1}{2}".format(self.proto,self.host,self.path)

        payload = {'f':self.filter, 'e':'.csv', 's':stockIndex }
        r = requests.get(url, verify=False, timeout=60, params=payload)
        resp = r.text
        out = "Company Name,Symbol, Last Trade Price, Min. Price, Max. Price\n"
        out += resp

        return out

    def getChart(self,yahoo_ids):

        stockIndex = self.setYahooIds(yahoo_ids)
        time_frame = "5d"
        payload = {'s': stockIndex, 't': time_frame }
        url = "{0}{1}{2}".format(self.proto,self.chartHost,self.chartPath)

        return "http://chart.finance.yahoo.com/z?s="+stockIndex+"&t=5d"

if __name__ == '__main__':

    companies = ["GOOG","MSFT"]
    y = yahooAPI()
    print y.getQuote(companies)
    print y.getChart(companies)