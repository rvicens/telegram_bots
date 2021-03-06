import requests
import logging
from bs4 import BeautifulSoup
from lib.stockQuotesAPI.pcbolsaSearch import *

class BolsaMadridSearch():


    def __init__(self):

        self.logger = logging.getLogger("Main.BolsaMadridSearch")
        self.proto = "http://"
        self.host = "www.bolsamadrid.es"
        self.path = "/esp/aspx/Empresas/FichaValor.aspx"
        self.page = ""

        self.companies = {"ABERTIS":"ES0111845014","ABENGOA-A":"","ABENGOA-B":"ES0105200002","ACCIONA":"ES0125220311","ACS":"ES0167050915","ACERINOX":"ES0132105018",
                          "AENA":"ES0105046009","AMADEUS-IT":"ES0109067019","BBVA":"ES0113211835","BANKIA":"ES0113307021","BANKINTER":"ES0113679I37","CAIXABANK":"ES0140609019",
                          "DIA":"ES0126775032","ENDESA":"ES0130670112","ENAGAS":"ES0130960018","FCC":"ES0122060314","FERROVIAL":"ES0118900010","GAMESA":"ES0143416115","GASNATURAL":"ES0116870314",
                          "GRIFOLS":"ES0171996012","IAG":"ES0177542018","IBERDROLA":"ES0144580Y14","INDRA":"ES0118594417","INDITEX":"ES0148396007","MAPFRE":"ES0124244E34","ACELORMITTAL":"LU0323134006",
                          "OHL":"ES0142090317","POPULAR":"ES0113790226","REE":"ES0173093115","REPSOL":"ES0173516115","B.SABADELL":"ES0113860A34","SANTANDER":"ES0113900J37","SACYR":"ES0182870214",
                          "TELEFONICA":"ES0178430E18", "MEDIASET":"ES0152503035","TEC.REUNIDAS":"ES0178165017"}

    def setId(self,company):
        out_id = company.upper()
        if self.companies.has_key(company.upper()):
            out_id = self.companies[company.upper()]

        return out_id


    def parsePage(self):
        company = ""
        ticker = ""
        last_price = ""
        last_time = ""
        min_price = ""
        max_price = ""
        opening_price = ""
        diff_price = ""

        soup = BeautifulSoup(self.page,"html5lib")

        company = soup.find_all(class_="TituloPag")[0].get_text().encode("utf-8")
        ticker = soup.find_all(id="ctl00_Contenido_TickerDat")[0].get_text()[:-1].encode("utf-8")

        tblPrices = soup.find_all(id="ctl00_Contenido_tblPrecios")
        row = tblPrices[0].find_all("tr")[1]
        cells = row.find_all("td")
        last_time = "{0} {1}".format(cells[0].get_text().encode("utf-8"),cells[1].get_text().encode("utf-8"))
        opening_price = cells[3].get_text().encode("utf-8")
        diff_price = cells[4].get_text().encode("utf-8")
        last_price = cells[5].get_text().encode("utf-8")
        max_price = cells[6].get_text().encode("utf-8")
        min_price = cells[7].get_text().encode("utf-8")

        out = [company,ticker,last_price,last_time,min_price,max_price,opening_price,diff_price]
        return out


    def getQuote(self,company):

        out = ""
        if self.validateCompany(company):
            isin = self.setId(company)
            url = "{0}{1}{2}".format(self.proto,self.host,self.path)

            payload = {'ISIN':isin }

            try:
                r = requests.get(url, verify=False, timeout=60, params=payload)
                self.page = r.text
                s = self.parsePage()
                out = "Company Name: {0}\nTicker: {1}\nLast Trade Price: {2}\nTime Reference: {3}\nMin. Price: {4}\nMax. Price: {5}\nOpening Price: {6}\nDifference From Opening: {7}%\n".format(s[0],s[1],s[2],s[3],s[4],s[5],s[6],s[7])
            except Exception, e:
                self.logger.exception("Something went wrong querying the stock database. Data:{0}".format(url))
                self.logger.exception("Error parsing BolsaMadrid Website")
                out = "Something went wrong querying the stock database. No data for stock values\n\n"

            return out

        self.logger.info("Company '{0}' does not exist".format(company))
        out += "Company '{0}' does not exist. Please verify company list \n\n".format(company)
        return out

    def getChart(self,company):
        if self.validateCompany(company):
            #y = yahooAPI()
            #return "http://pcbolsa.com/graficopc.aspx?ISIN=ES0105200002&Plaza=55&Time=18:00:39&Mov=0&Sitio=1&Tool=1"
            #return y.getChart(company)
            pcb = pcbolsaSearch()
            return pcb.getChart(company)

        self.logger.info("Company '{0}' does not exist".format(company))
        return None


    def validateCompany(self,company):

        if not company.upper() in self.companies.keys():
            return False

        return True


if __name__ == '__main__':

    companies = "abertis"
    bm = BolsaMadridSearch()
    print bm.getQuote(companies)
