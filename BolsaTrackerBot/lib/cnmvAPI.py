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

        self.companies = {"ABERTIS":"A-08209769","ABENGOA-A":"A41002288","ABENGOA-B":"A41002288","ACCIONA":"A08001851","ACS":"A-28004885","ACERINOX":"A-28250777","AENA":"A86212420","AMADEUS-IT":"A-78876919","BBVA":"A-48265169","BANKIA":"A-14010342","BANKINTER":"A28157360","CAIXABANK":"A-08663619","DIA":"A28164754","ENDESA":"A-28023430","ENAGAS":"A-28294726","FCC":"A-28037224","FERROVIAL":"A81939209","GAMESA":"A-01011253","GASNATURAL":"A-08015497","GRIFOLS":"A-58389123","IAG":"A-28017648","IBERDROLA":"A-48010615","INDRA":"A-28599033","INDITEX":"A-15075062","MAPFRE":"A08055741","ACELORMITTAL":"N0181056C","OHL":"A-48010573","POPULAR":"A-28000727","REE":"A-78003662","REPSOL":"A-78374725","B.SABADELL":"A-08000143", "SANTANDER":"A-39000013","SACYR":"A-28013811","TELEFONICA":"A-28015865", "MEDIASET":"A-79075438","TEC.REUNIDAS":"A-28092583"}


    def setNif(self,company):
        out_id = company.upper()
        if self.companies.has_key(company.upper()):
            out_id = self.companies[company.upper()]
        return out_id


    def setPositions(self,cells):
        pos0 = 0
        pos1 = len(cells) - 2
        pos2 = len(cells) - 1

        return pos0, pos1, pos2


    def parsePage(self):

        out = ""
        soup = BeautifulSoup(self.page,"html5lib")

        tblHR = soup.find_all(id="ctl00_ContentPrincipal_gridHechos")
        rows = tblHR[0].find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            if len(cells) > 0:

                pos0, pos1, pos2 = self.setPositions(cells)

                date_items = cells[pos0].find_all("li")
                hr_date = ""
                if len(date_items) > 0:
                    hr_date = "{0} {1}".format(date_items[1].get_text().strip(),date_items[2].get_text().strip())

                hr_type = cells[pos1].get_text().encode("utf-8").strip()
                hr_desc = cells[pos2].get_text().encode("utf-8").strip()
                out += "Date: {0} - Type: {1}\n{2}\n\n".format(hr_date,hr_type,hr_desc)

        return out


    def getHR(self,company):

        nif = self.setNif(company)
        url = "{0}{1}{2}".format(self.proto,self.host,self.path)

        payload = { 'division': '1', 'nif': nif }

        try:
            r = requests.get(url, verify=False, timeout=60, params=payload)
            self.page = r.text
            s = self.parsePage()
            out = str(s)
        except Exception, e:
            self.logger.exception("Something went wrong querying the stock database. Data:{0}".format(url))
            self.logger.exception("Error parsing CNMV Website")
            out = "Something went wrong querying the HR webpage\n\n"

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
