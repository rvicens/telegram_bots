import requests
import logging
from bs4 import BeautifulSoup

class pcbolsaSearch():


    def __init__(self):

        self.logger = logging.getLogger("Main.PcBolsaSearch")
        self.proto = "http://"
        self.host = "pcbolsa.com"
        self.dividend_path = "/ProximosDividendos.aspx"
        self.page = ""

        self.companies = {"ABERTIS":"ES0111845014","ABENGOA-A":"","ABENGOA-B":"ES0105200002","ACCIONA":"ES0125220311","ACS":"ES0167050915","ACERINOX":"ES0132105018",
                          "AENA":"ES0105046009","AMADEUS-IT":"ES0109067019","BBVA":"ES0113211835","BANKIA":"ES0113307021","BANKINTER":"ES0113679I37","CAIXABANK":"ES0140609019",
                          "DIA":"ES0126775032","ENDESA":"ES0130670112","ENAGAS":"ES0130960018","FCC":"ES0122060314","FERROVIAL":"ES0118900010","GAMESA":"ES0143416115","GASNATURAL":"ES0116870314",
                          "GRIFOLS":"ES0171996012","IAG":"ES0177542018","IBERDROLA":"ES0144580Y14","INDRA":"ES0118594417","INDITEX":"ES0148396007","MAPFRE":"ES0124244E34","ACELORMITTAL":"LU0323134006",
                          "OHL":"ES0142090317","POPULAR":"ES0113790226","REE":"ES0173093115","REPSOL":"ES0173516115","B.SABADELL":"ES0113860A34","SANTANDER":"ES0113900J37","SACYR":"ES0182870214",
                          "TELEFONICA":"ES0178430E18", "MEDIASET":"ES0152503035","TEC.REUNIDAS":"ES0178165017"}

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
            self.logger.exception("Something went wrong querying the dividend database. Data:{0}".format(r.url))
            self.logger.exception("Error parsing pcbolsa Website")

        return out

if __name__ == '__main__':

    pcb = pcbolsaSearch()
    print pcb.getDividend()
