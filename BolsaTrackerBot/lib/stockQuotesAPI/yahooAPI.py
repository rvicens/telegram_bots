import requests

class yahooAPI():


    def __init__(self):

        self.proto = "http://"
        self.host = "download.finance.yahoo.com"
        self.path = "/d/quotes.csv"
        self.filter = "nsl1op"
        self.chartHost = "chart.finance.yahoo.com"
        self.chartPath ="/z"

        self.companies = {"ABERTIS":"ABE.MC","ABENGOA-A":"ABG.MC","ABENGOA-B":"ABG-P.MC","ACS":"ACS.MC","ACERINOX":"ACX.MC",
                          "AENA":"AENA.MC","AMADEUS-IT":"AMS.MC","BBVA":"BBVA.MC","BANKIA":"BKIA.MC","BANKINTER":"BKT.MC","CAIXABANK":"CABK.MC",
                          "DIA":"DIA.MC","ENDESA":"ELE.MC","ENAGAS":"ENG.MC","FCC":"FCC.MC","FERROVIAL":"FER.MC","GAMESA":"GAM.MC","GASNATURAL":"GAS.MC",
                          "GRIFOLS":"GRF.MC","IAG":"IAG.MC","IBERDROLA":"IBE.MC","INDRA":"IDR.MC","INDITEX":"ITX.MC","MAPFRE":"MAP.MC","ACELORMITTAL":"MTS.MC",
                          "OHL":"OHL.MC","POPULAR":"POP.MC","REE":"REE.MC","REPSOL":"REP.MC","B.SABADELL":"SAB.MC","SANTANDER":"SAN.MC","SACYR":"SACYR.MC",
                          "TELEFONICA":"TEF.MC", "MEDIASET":"TL5.MC","TEC. REUNIDAS":"TRE.MC"}

    def setYahooFilter(self,new_filter):
        if new_filter:
            self.filter = str(new_filter)


    def setYahooId(self,company):
        yahoo_id = company.upper()
        if self.companies.has_key(company.upper()):
            yahoo_id = self.companies[company.upper()]

        return yahoo_id


    def getQuote(self,company):

        stockIndex = self.setYahooId(company)
        url = "{0}{1}{2}".format(self.proto,self.host,self.path)

        payload = {'f':self.filter, 'e':'.csv', 's':stockIndex }
        try:
            r = requests.get(url, verify=False, timeout=60, params=payload)
            resp = r.text

            s = resp.split(",")
            if len(s)<= 0:
                out = resp
                return out

            out = "Company Name:{0}\nSymbol:{1}\nLast Trade Price:{2}\nMin. Price:{3}\nMax. Price:{4}\n".format(s[0].replace('"',''),s[1].replace('"',''),s[2],s[3],s[4])

        except:
            out = "Something went wrong querying the stock database"

        return out

    def getChart(self,company):

        stockIndex = self.setYahooId(company)
        time_frame = "5d"
        url = "{0}{1}{2}?s={3}&t={4}".format(self.proto,self.chartHost,self.chartPath,stockIndex,time_frame)

        return url


    def validateCompany(self,company):

        if not company.upper() in self.companies.keys():
            return False

        return True

    def getComapanyQuote(self,companies):

        out = ""
        for company in companies:
            if self.validateCompany(company):
                out += self.getQuote(company)
                out += self.getChart(company)
                out += "\n\n"
            else:
                out += "Company '{0}' does not exist. Please verify companies with /list \n\n".format(company)

        return out

if __name__ == '__main__':

    companies = ["MSFT","bankia"]
    y = yahooAPI()
    print y.getComapanyQuote(companies)
