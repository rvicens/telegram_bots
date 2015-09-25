import requests
import logging
from bs4 import BeautifulSoup

class cnmvAPI():


    def __init__(self):

        self.logger = logging.getLogger("Main.CNMV_API")
        self.proto = "http://"
        self.host = "www.cnmv.es"
        self.path = "/Portal/HR/ResultadoBusquedaHR.aspx"
        self.page = ""

        self.companies = {"ABERTIS":"A-48010615","ABENGOA-A":"","ABENGOA-B":"ES0105200002","ACCIONA":"ES0125220311","ACS":"ES0167050915","ACERINOX":"ES0132105018",
                          "AENA":"ES0105046009","AMADEUS-IT":"ES0109067019","BBVA":"ES0113211835","BANKIA":"ES0113307021","BANKINTER":"ES0113679I37","CAIXABANK":"ES0140609019",
                          "DIA":"ES0126775032","ENDESA":"ES0130670112","ENAGAS":"ES0130960018","FCC":"ES0122060314","FERROVIAL":"ES0118900010","GAMESA":"ES0143416115","GASNATURAL":"ES0116870314",
                          "GRIFOLS":"ES0171996012","IAG":"ES0177542018","IBERDROLA":"ES0144580Y14","INDRA":"ES0118594417","INDITEX":"ES0148396007","MAPFRE":"ES0124244E34","ACELORMITTAL":"LU0323134006",
                          "OHL":"ES0142090317","POPULAR":"ES0113790226","REE":"ES0173093115","REPSOL":"ES0173516115","B.SABADELL":"ES0113860A34","SANTANDER":"ES0113900J37","SACYR":"ES0182870214",
                          "TELEFONICA":"ES0178430E18", "MEDIASET":"ES0152503035","TEC.REUNIDAS":"ES0178165017"}

    def setNif(self,company):
        out_id = company.upper()
        if self.companies.has_key(company.upper()):
            out_id = self.companies[company.upper()]
        return out_id


    def parsePage(self):

        out = ""
        soup = BeautifulSoup(self.page,"html5lib")

        tblHR = soup.find_all(id="ctl00_ContentPrincipal_gridHechos")
        rows = tblHR[0].find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            if len(cells) > 0:
                hr_date = cells[0].get_text().encode("utf-8")
                hr_type = cells[1].get_text().encode("utf-8")
                hr_desc = cells[2].get_text().encode("utf-8")
                print "-{0}-".format(hr_date)
                print "-{0}-".format(hr_type)
                print "-{0}-".format(hr_desc)
                break

        return out


    def getHR(self,company):

        nif = self.setNif(company)
        url = "{0}{1}{2}".format(self.proto,self.host,self.path)

        payload = { 'division': '1', 'nif': nif }

        if True:
        #try:
            r = requests.get(url, verify=False, timeout=60, params=payload)
            self.page = r.text
            s = self.parsePage()
            out = str(s)
        #except Exception, e:
        #    self.logger.exception("Something went wrong querying the stock database. Data:{0}".format(url))
        #    self.logger.exception("Error parsing CNMV Website")
        #    out = "Something went wrong querying the HR webpage\n\n"

        return out


    def validateCompany(self,company):

        if not company.upper() in self.companies.keys():
            return False

        return True

    def getComapanyHR(self,companies):

        out = ""
        self.logger.debug("Querying companies:{0}".format(companies))
        for company in companies:
            if self.validateCompany(company):
                self.logger.debug("Company:{0} is validated".format(company))
                out += self.getHR(company)
                out += "\n\n"
            else:
                self.logger.info("Company '{0}' does not exist".format(company))
                out += "Company '{0}' does not exist. Please verify company list \n\n".format(company)

        return out

if __name__ == '__main__':

    companies = ["abertis"]
    cnmv = cnmvAPI()
    print cnmv.getComapanyHR(companies)
