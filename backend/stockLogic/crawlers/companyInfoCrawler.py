import sys
import time
import threading

# ADDING ITEMS TO SYS.PATH #
sys.path.append("\\git\\SoSI\\backend")

from dateutil import parser
from datetime import datetime
from helpers.parser import Parser
from helpers.web import Web
from models.companyInfoModel import CompanyInfoModel

## GLOBAL
URL = "https://www.bussoladoinvestidor.com.br/guia-empresas/empresa/%s/acionistas"

class CompanyInfoCrawler(CompanyInfoModel):

    def __init__(self, stockCode):
        self.__setMajorShareholder(stockCode)
    
    def __setMajorShareholder(self, stockCode):
        if stockCode == "" or stockCode == None: return None
        
        urlFormatted = URL % stockCode
        page = Web.GetWebPage(urlFormatted)
        if page is None: 
            self.MajorShareholder = ""
            return

        # table = page.find("table", {"class": "table table-striped table-hover"})
        table = page.find("table")
        
        if table is None:
            self.MajorShareholder = ""
            return

        # Major Shareholder
        
        # <TABLE>
        if table.contents is None or len(table.contents) < 2: 
            self.MajorShareholder = ""
            return
        
        # <TR>
        if table.contents[1] is None or len(table.contents[1]) == 0:
            self.MajorShareholder = ""
            return

        # <TD>
        if table.contents[1].contents is None or len(table.contents[1].contents) == 0:
            self.MajorShareholder = ""
            return

        # POPULATIN THE OBJECT
        self.MajorShareholder = str(table.contents[1].contents[0].get_text()).lstrip().rstrip()