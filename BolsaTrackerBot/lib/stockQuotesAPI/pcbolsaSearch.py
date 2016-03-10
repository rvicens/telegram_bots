import requests
import logging
from bs4 import BeautifulSoup

class pcbolsaSearch():


    def __init__(self):

        self.logger = logging.getLogger("Main.PcBolsaSearch")
        self.proto = "http://"
        self.host = "pcbolsa.com"
        self.dividend_path = "/ProximosDividendos.aspx"
        self.chart_path = "/graficosixJpgGranNuevo.aspx"
        self.quote_path = "/Cotizacion"
        self.page = ""

        self.companies = {"ABERTIS":"Abertis","ABENGOA-A":"Abengoa_-A-","ABENGOA-B":"Abengoa_-B-","ACCIONA":"Acciona","ACS":"ACS","ACERINOX":"Acerinox",
                          "AENA":"AENA","AMADEUS-IT":"Amadeus","BBVA":"BBVA","BANKIA":"Bankia","BANKINTER":"Bankinter","CAIXABANK":"Caixabank",
                          "DIA":"DIA","ENDESA":"Endesa","ENAGAS":"Enagas","FCC":"Fomento_Constr","FERROVIAL":"Ferrovial","GAMESA":"Gamesa","GASNATURAL":"Gas_Natural",
                          "GRIFOLS":"Grifols_A","IAG":"IAG","IBERDROLA":"Iberdrola","INDRA":"Indra","INDITEX":"Inditex","MAPFRE":"Mapfre","ACELORMITTAL":"ArcelorMittal",
                          "OHL":"797019,1058,814","POPULAR":"Banco_Popular","REE":"Red_Electrica","REPSOL":"REPSOL","B.SABADELL":"Banco_Sabadell","SANTANDER":"Banco_Santander","SACYR":"Sacyr",
                          "TELEFONICA":"Telefonica", "MEDIASET":"Mediaset_Espana","TEC.REUNIDAS":"Tecnicas_Reunidas"}

        self.chart_companies = {"ABERTIS":"1459044,1058,814","ABENGOA-A":"1268457,1058,814","ABENGOA-B":"19739492,1058,814","ACCIONA":"978954,1058,814","ACS":"1879689,1058,814","ACERINOX":"1876417,1058,814",
                          "AENA":"26876733,1058,814","AMADEUS-IT":"11249889,1058,814","BBVA":"931474,1058,814","BANKIA":"21227982,1058,814","BANKINTER":"3219022,1058,814","CAIXABANK":"3425733,1058,814",
                          "DIA":"13086668,1058,814","ENDESA":"682405,1058,814","ENAGAS":"1438368,1058,814","FCC":"1004613,1058,814","FERROVIAL":"1978482,1058,814","GAMESA":"1873546,1058,814","GASNATURAL":"822398,1058,814",
                          "GRIFOLS":"1905826,1058,814","IAG":"11958148,1058,814","IBERDROLA":"2969533,1058,814","INDRA":"1136946,1058,814","INDITEX":"24956043,1058,814","MAPFRE":"2759010,1058,814","ACELORMITTAL":"3529315,1058,814",
                          "OHL":"797019,1058,814","POPULAR":"21629548,1058,814","REE":"827065,1058,814","REPSOL":"675467,1058,814","B.SABADELL":"2970161,1058,814","SANTANDER":"817651,1058,814","SACYR":"932537,1058,814",
                          "TELEFONICA":"826858,1058,814", "MEDIASET":"1881163,1058,814","TEC.REUNIDAS":"2598963,1058,814","MERLIN":"24705819,1058,814"}

        self.translate_payment_type = {"a cuenta":"on account"}

    def translate_en(self,var):

        if var.lower() in self.translate_payment_type.keys():
            return  self.translate_payment_type[var.lower()]

        return var

    def parseDividendPage(self):
        company = ""
        date = ""
        year = ""
        net = ""
        gross = ""
        payment_type = ""

        ## FUCKING SHIT TO PARSE THE PAGE ##
        soup = BeautifulSoup(self.page, "html5lib")
        tmp_divs = soup.find_all("div")
        tmp_page = str(tmp_divs[0]).replace("\n","")
        ####

        soup = BeautifulSoup(tmp_page, "html5lib")
        table_body = soup.find("tbody")
        out = []

        for row in table_body.find_all("tr"):
            columns = row.find_all("td")
            company = columns[0].get_text().encode("utf-8")
            date = columns[1].get_text().encode("utf-8")
            payment_type = columns[2].get_text().encode("utf-8")
            year = columns[3].get_text().encode("utf-8")
            gross = columns[4].get_text().encode("utf-8")
            net = columns[5].get_text().encode("utf-8")
            out.append({"company":company,"date":date,"year":year,"net":net,"gross":gross,"payment_type":self.translate_en(payment_type)})

        return out


    def getDividend(self):

        out = []
        url = "{0}{1}{2}".format(self.proto,self.host,self.dividend_path)
        try:
            r = requests.get(url, verify=False, timeout=60 )
            self.page = r.text
            out = self.parseDividendPage()
        except Exception, e:
            self.logger.exception("Something went wrong querying the dividend database. Data:{0}".format(url))
            self.logger.exception("Error parsing pcbolsa Website")

        return out


    def getChart(self,company,chart_time="now"):

        company_code = ""
        if self.validateCompany(company):
            company_code = self.chart_companies[company]

        if chart_time == "now":
            query_string = "?Tipo=0&CodigoSix={0}&width=600&height=350".format(company_code)
        if chart_time == "6m":
            query_string = "?Tipo=2&CodigoSix={0}&width=600&height=350".format(company_code)

        url = "{0}www.{1}{2}{3}".format(self.proto,self.host,self.chart_path,query_string)

        return url

    def parseQuotePage(self):

        ticker = ""
        last_price = ""
        last_time = ""
        min_price = ""
        max_price = ""
        opening_price = ""
        diff_price = ""

        soup = BeautifulSoup(self.page,"html5lib")
        #print self.page
        #print soup

        ticker = soup.find_all(id="CotizaTicker")[0].get_text()[:-1].encode("utf-8")
        last_price = soup.find_all(id="CotizaUltimo")[0].get_text()[:-1].encode("utf-8")
        last_time = soup.find_all(id="CotizaHora")[0].get_text()[:-1].encode("utf-8")
        min_price = soup.find_all(id="CotizaMin")[0].get_text()[:-1].encode("utf-8")
        max_price = soup.find_all(id="CotizaMax")[0].get_text()[:-1].encode("utf-8")
        diff_price = soup.find_all(id="CotizaDif")[0].get_text()[:-1].encode("utf-8")

        out = [ticker,last_price,last_time,min_price,max_price,opening_price,diff_price]

        return out


    def getQuote(self,company):

        out = ""
        if self.validateCompany(company):
            company_path = self.companies[company]
            url = "{0}{1}{2}/{3}".format(self.proto,self.host,self.quote_path,company_path)

            try:
                r = requests.get(url, verify=False, timeout=60 )
                self.page = r.text.encode("utf-8")
                s = self.parseQuotePage()
                out = "Company Name: {0}\nTicker: {1}\nLast Trade Price: {2}\nTime Reference: {3}\nMin. Price: {4}\nMax. Price: {5}\nOpening Price: {6}\nDifference From Opening: {7}%\n".format(company,s[0],s[1],s[2],s[3],s[4],s[5],s[6])
            except Exception, e:
                self.logger.exception("Something went wrong querying the quote database. Data:{0}".format(url))
                self.logger.exception("Error parsing pcbolsa Website")

            return out

        self.logger.info("Company '{0}' does not exist".format(company))
        out += "Company '{0}' does not exist. Please verify company list \n\n".format(company)
        return out


    def validateCompany(self,company):

        if not company.upper() in self.chart_companies.keys():
            return False

        return True


if __name__ == '__main__':

    pcb = pcbolsaSearch()
    #print pcb.getDividend()
    print pcb.getQuote("ACCIONA")