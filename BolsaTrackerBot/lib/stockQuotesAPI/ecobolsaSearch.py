import os
import time
import requests
from cookielib import LWPCookieJar
import logging
from bs4 import BeautifulSoup
from lib.stockQuotesAPI.pcbolsaSearch import *

#from config import *

class ecobolsaSearch():

    def __init__(self):

        self.logger = logging.getLogger("Main.EcoBolsaSearch")
        self.proto = "http://"
        self.loggedin_host = "www2.ecobolsa.com"
        self.loggedout_host = "www.ecobolsa.com"
        self.page = ""

        self.cookiefile = "{0}/tmp/ecobolsa_cookiefile.txt".format(os.getcwd())
        self.reqHndlr = requests.session()
        self.reqHndlr.cookies = LWPCookieJar(self.cookiefile)

        self.companies = {"ABERTIS":"ABERTIS","ABENGOA-A":"ABENGOA-A","ABENGOA-B":"ABENGOA-B","ACCIONA":"ACCIONA","ACS":"ACTIVIDADES-DE-CONSTRUCCION-Y-SERVICIOS-ACS","ACERINOX":"ACERINOX",
                          "AENA":"AENA","AMADEUS-IT":"AMADEUS","BBVA":"BBVA","BANKIA":"BANKIA","BANKINTER":"BANKINTER","CAIXABANK":"CAIXABANK",
                          "DIA":"SUPERMERCADOS-DIA","ENDESA":"ENDESA","ENAGAS":"ENAGAS","FCC":"FOMENTO-DE-CONSTRUCCIONES-Y-CONTRATAS-FCC","FERROVIAL":"FERROVIAL","GAMESA":"GAMESA","GASNATURAL":"GAS-NATURAL",
                          "GRIFOLS":"GRIFOLS","IAG":"IAG-(IBERIA)","IBERDROLA":"IBERDROLA","INDRA":"INDRA","INDITEX":"INDITEX","MAPFRE":"MAPFRE","ACELORMITTAL":"ARCELOR-MITTAL",
                          "OHL":"OBRASCON-HUARTE-LAIN-OHL","POPULAR":"BANCO-POPULAR","REE":"RED-ELECTRICA-DE-ESPANA-REE","REPSOL":"REPSOL","B.SABADELL":"BANCO-SABADELL","SANTANDER":"BANCO-SANTANDER","SACYR":"SACYR",
                          "TELEFONICA":"TELEFONICA", "MEDIASET":"MEDIASET-ESPANA","TEC.REUNIDAS":"TECNICAS-REUNIDAS"}

        if not os.path.isdir('tmp'):
            os.mkdir("tmp")

    def save_cookies(self):

        if not os.path.exists(self.cookiefile):
            # Create a new cookies file and set our Session's cookies
            print('setting cookies')
            self.reqHndlr.cookies.save()
        else:
            # Save the session's cookies back to the file
            self.reqHndlr.cookies.save(ignore_discard=True)

    def load_cookies(self):

        # Load saved cookies from the file and use them in a request
        print('loading saved cookies')
        self.reqHndlr.cookies.load(ignore_discard=True)


    def testLoggedIn(self):

        logged_out_strings = ["/registro/coteja.php","usuarioregistro","passregistro"]
        url = "{0}{1}".format(self.proto,self.loggedin_host)

        try:
            #load cookies and do a request
            self.load_cookies()
            r = self.reqHndlr.get(url, verify=False, timeout=60 )
            pag_content = r.text.encode("utf-8")

            if logged_out_strings[0] in pag_content and logged_out_strings[1] in pag_content and logged_out_strings[2] in pag_content:
                return False
        except:
            self.logger.exception("Error querying logged in resource at EcobolsaSearch")
            return False

        return True


    def doLogin(self):

        if not self.testLoggedIn():

            url = "{0}{1}/registro/coteja.php".format(self.proto,self.loggedout_host)
            payload = {"usuario":eco_bolsa_user,"password":eco_bolsa_pass}

            ## 1st Login Stage
            r = self.reqHndlr.post(url, verify=False, timeout=60, data=payload)
            self.page = r.text.encode("utf-8")

            ## Parse data for 2n Stage
            soup = BeautifulSoup(self.page, "html5lib")
            hidden_vars = soup.find_all("input")

            payload = {}
            for var in hidden_vars:
                varname = var["name"].encode("utf-8")
                varval = var["value"].encode("utf-8")
                payload.update({varname:varval})

            ## 2nd Login Stage
            url = "{0}{1}/foros/ucp.php?mode=login".format(self.proto,self.loggedin_host)
            r = self.reqHndlr.post(url, verify=False, timeout=60, data=payload )

            # Store cookies
            self.save_cookies()

        return True


    def parseQuoteJSON(self):

        last_price = self.page["p"]
        last_time = self.page["h"]
        min_price = self.page["mn"]
        max_price = self.page["m"]
        opening_price = self.page["ca"]
        diff_price = self.page["v"]

        out = [last_price,last_time,min_price,max_price,opening_price,diff_price]

        return out


    def getQuote(self,company):

        out = ""
        timestamp = int(time.time())
        company_path = "js/data/{0}.json?{1}".format(self.companies[company].upper(),timestamp)
        url = "{0}{1}/{2}".format(self.proto,self.loggedin_host,company_path)
        try:
            r = self.reqHndlr.get(url, verify=False, timeout=60 )
            self.page = r.json()
            s = self.parseQuoteJSON()
            out = "Company Name:{0}\nLast Trade Price:{1}\nTime Reference:{2}\nMin. Price:{3}\nMax. Price:{4}\nOpening Price:{5}\nDifference From Opening:{6}%\n".format(company,s[0],s[1],s[2],s[3],s[4],s[5])
        except Exception:
            self.logger.exception("Something went wrong querying the quote database. Data:{0}".format(url))
            self.logger.exception("Error parsing pcbolsa Website")

        return out


    def getAllQuotes(self):

        out = ""
        timestamp = int(time.time())
        path = "js/data/ibex35s.json?{0}".format(timestamp)
        url = "{0}{1}/{2}".format(self.proto,self.loggedin_host,path)
        try:
            r = self.reqHndlr.get(url, verify=False, timeout=60 )
            self.page = r.json()
            out = self.page
        except Exception:
            self.logger.exception("Something went wrong querying the quote database. Data:{0}".format(url))
            self.logger.exception("Error parsing pcbolsa Website")

        return out

    def getChart(self,company):
        pcb = pcbolsaSearch()
        return pcb.getChart(company)


    def validateCompany(self,company):

        if not company.upper() in self.companies.keys():
            return False

        return True


    def getComapanyQuote(self,companies):

        out = ""
        # self.doLogin()
        self.logger.debug("Querying companies:{0}".format(companies))
        for company in companies:
            if self.validateCompany(company):
                self.logger.debug("Company:{0} is validated".format(company))
                out += self.getQuote(company)
                out += self.getChart(company)
                out += "\n\n"
            else:
                self.logger.info("Company '{0}' does not exist".format(company))
                out += "Company '{0}' does not exist. Please verify company list \n\n".format(company)

        return out


if __name__ == '__main__':

    ecob = ecobolsaSearch()
    print ecob.getComapanyQuote(["ACCIONA"])