import pprint
import sys

# ADDING ITEMS TO SYS.PATH #
sys.path.append("\\git\\SoSI\\backend")

from crawlers.stockCrawler import StockCrawler
from crawlers.companyInfoCrawler import CompanyInfoCrawler
from crawlers.companyStatisticCrawler import CompanyStatisticCrawler
from crawlers.cashFlowHistoryCrawler import CashFlowHistoryCrawler
from models.buynHoldModel import BuyNHoldeModel
from helpers.parser import Parser
from database.buyNHoldDbCommand import BuyNHoldDbCommand

### GLOBAL CONSTANTS ###
STOCK_TYPE_TO_FILTER = "ON"  # Leave it empty for all types

### GLOBAL VARIABLES ###
gStockTotalAmountObj = None
global_AvailableStocksSingleton = None

# FIELDS #
FIELD_RESULTS = "results"
FIELD_TYPE = "type"

# METHODS #
def GetBuyNHoldModel(stockObj):
    if stockObj is None: return
    
    returnObj = []

    for stock in stockObj.AvailableStockCode:
        buyHoldModelAux = BuyNHoldeModel()
        companyInfo = CompanyInfoCrawler(stock["stockCode"])
        companyStatistic = CompanyStatisticCrawler(stock["stockCode"])
        cashFlowHistData = CashFlowHistoryCrawler(stock["stockCode"])

        buyHoldModelAux.Code = companyInfo.Code
        buyHoldModelAux.Company = stock["companyName"]
        buyHoldModelAux.Type = GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "stockType", ("ON" if str(stock["stockCode"]).find("3") > -1 else "PN"))
        buyHoldModelAux.StockPrice = float(GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "stockPrice", 0.00))
        buyHoldModelAux.Sector = GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "primarySector", "")
        buyHoldModelAux.SecondSector = GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "secondarySector", "")
        buyHoldModelAux.Equity = float(GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "equity", 0.00))
        buyHoldModelAux.Avg21Negociation = companyStatistic.AvgVolume3Months
        buyHoldModelAux.DividendLastPrice = float(GetDividendValue(stockObj.DividendsData, stock["stockCode"], 1, 0.00))
        buyHoldModelAux.DividendPeriod = 0
        buyHoldModelAux.DividendYeld = companyStatistic.DividendYeld
        buyHoldModelAux.NetProfit = float(GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "netProfit", 0.00))
        buyHoldModelAux.StockAvailableAmount = float(GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "stockAmount", 0))
        buyHoldModelAux.AvgPayout12Months = companyStatistic.PayoutRatio
        buyHoldModelAux.DividendTotalValueShared = companyStatistic.PayoutRatio * buyHoldModelAux.NetProfit
        buyHoldModelAux.MajorShareholder = companyInfo.MajorShareholder
        buyHoldModelAux.Valuation = float(GetBasicInfo(stockObj.StocksBasicInfo, stock["stockCode"], "mktValue", 0.00))
        buyHoldModelAux.ReturnOnEquity = companyStatistic.ReturnOnEquity
        buyHoldModelAux.ReturnOnEquity_5yrAvg = companyStatistic.ReturnOnEquity_5yrAvg
        buyHoldModelAux.GrossDebitOverEbitda = companyStatistic.GrossDebitOverEbitida
        buyHoldModelAux.DividendYeld_5yrAvg = companyStatistic.DividendYeld_5yrAvg
        buyHoldModelAux.AvgPayout5Years = cashFlowHistData.GetAvgDividendShared() / cashFlowHistData.GetAvgNetIncome()
        buyHoldModelAux.HasDividendBeenSharedInLast5Yrs = cashFlowHistData.HasDividendBeenSharedInLast5Yrs()
        buyHoldModelAux.HasDividendGrowthInLast5Yrs = cashFlowHistData.HasDividendGrowthInLast5Yrs()
        buyHoldModelAux.HasNetProfitBeenRegularFor5Yrs = cashFlowHistData.HasNetProfitBeenRegularFor5Yrs()

        companyInfo = None
        companyStatistic = None
        cashFlowHistData = None

        returnObj.append(buyHoldModelAux)
    return returnObj

def GetBasicInfo(lstToDigInto, stockCode, fieldToGet, defaultValue):
    if lstToDigInto is None: return defaultValue
    
    lstReturn = []
    lstReturn = [ x[fieldToGet] for x in lstToDigInto if x["stock"] == stockCode ]

    if lstReturn is None or len(lstReturn) == 0: return defaultValue

    return lstReturn[0] if str(lstReturn[0]) != "" or str(lstReturn[0]) != '' else defaultValue 

def GetDividendValue(lstToDigInto, stockCode, order: 1, defaultValue):
    if lstToDigInto is None: return defaultValue
    
    lstDividend = []
    lstDividend = [ x["dividends"] for x in lstToDigInto if x["stockCode"] == stockCode ]
    dividendPrice = defaultValue

    if lstDividend is None or len(lstDividend) == 0: return defaultValue
    if lstDividend[0] is None or len(lstDividend[0]) == 0: return defaultValue

    if order == 1: 
        dividendPrice = lstDividend[0][0]['dividend']
    else:
        dividendPrice = lstDividend[0][len(lstDividend[0]) - 1]['dividend']

    return dividendPrice if dividendPrice != "" else defaultValue

def Save(lstDividend):
    for dividend in lstDividend:
        if BuyNHoldDbCommand().Save(dividend) == False:
            return False
    return True

#########
## INI ##
#########

stockObj = StockCrawler(STOCK_TYPE_TO_FILTER)
lstDividend = GetBuyNHoldModel(stockObj)

if (lstDividend is None) or (Save(lstDividend)) == False:
    raise SystemError()

print("DONE!!!")
