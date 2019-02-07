import pprint
import sys

# ADDING ITEMS TO SYS.PATH #
sys.path.append("\\git\\SoSI\\backend")

from database.buyNHoldDbCommand import BuyNHoldDbCommand
from helpers.parser import Parser
from models.buynHoldModel import BuyNHoldeModel
from crawlers.financialHistoryCrawler import FinancialHistoryCrawler
from crawlers.companyStatisticCrawler import CompanyStatisticCrawler
from crawlers.companyInfoCrawler import CompanyInfoCrawler
from crawlers.stockCrawler import StockCrawler
from crawlers.dividendHistoryCrawler import DividendHistoryCrawler
from crawlers.stockPriceHistoryCrawler import StockPriceHistoryCrawler

### GLOBAL CONSTANTS ###
STOCK_TYPE_TO_FILTER = ""  # Leave it empty for all types

### GLOBAL VARIABLES ###
gStockTotalAmountObj = None
global_AvailableStocksSingleton = None

# FIELDS #
FIELD_RESULTS = "results"
FIELD_TYPE = "type"

# METHODS #
def GetBuyNHoldModel(stockObj):
    if stockObj is None:
        return

    if stockObj.AvailableStockCode is None:
        return

    returnObj = []

    for stock in stockObj.AvailableStockCode:
        buyHoldModelAux = BuyNHoldeModel()
        companyInfo = CompanyInfoCrawler(stock["stockCode"])
        companyStatistic = CompanyStatisticCrawler(stock["stockCode"])
        financialHistData = FinancialHistoryCrawler(stock["stockCode"])
        stockPriceCrawler = StockPriceHistoryCrawler(stock["stockCode"], 30)
        dividendCrawler = DividendHistoryCrawler(stock["stockCode"], 12)

        buyHoldModelAux.Code = companyInfo.Code
        buyHoldModelAux.Company = companyInfo.Company
        buyHoldModelAux.Type = companyInfo.Type
        buyHoldModelAux.StockPrice = stockPriceCrawler.GetLastStockPrice()
        buyHoldModelAux.Sector = companyInfo.Sector
        buyHoldModelAux.SecondSector = companyInfo.SecondSector
        buyHoldModelAux.Equity = financialHistData.GetLastNetWorth()
        buyHoldModelAux.Avg21Negociation = stockPriceCrawler.GetAvgVolume()
        buyHoldModelAux.DividendLastPrice = dividendCrawler.GetDividendLastValue()
        buyHoldModelAux.DividendPeriod = dividendCrawler.GetDividendPeriod()
        buyHoldModelAux.DividendYeld = companyStatistic.DividendYeld
        buyHoldModelAux.NetProfit = financialHistData.GetLastNetIncome()
        buyHoldModelAux.StockAvailableAmount = companyInfo.StockAmountAvailable
        buyHoldModelAux.AvgPayout12Months = companyStatistic.PayoutRatio
        buyHoldModelAux.DividendTotalValueShared = companyStatistic.PayoutRatio * buyHoldModelAux.NetProfit
        buyHoldModelAux.MajorShareholder = companyInfo.MajorShareholder
        buyHoldModelAux.Valuation = companyStatistic.Valuation
        buyHoldModelAux.ReturnOnEquity = companyStatistic.ReturnOnEquity
        buyHoldModelAux.ReturnOnEquity_5yrAvg = companyStatistic.ReturnOnEquity_5yrAvg
        buyHoldModelAux.GrossDebitOverEbitda = companyStatistic.GrossDebitOverEbitida
        buyHoldModelAux.DividendYeld_5yrAvg = companyStatistic.DividendYeld_5yrAvg
        buyHoldModelAux.AvgPayout5Years = financialHistData.GetAvgDividendShared() / financialHistData.GetAvgNetIncome()
        buyHoldModelAux.HasDividendBeenSharedInLast5Yrs = financialHistData.HasDividendBeenSharedInLast5Yrs()
        buyHoldModelAux.HasDividendGrowthInLast5Yrs = financialHistData.HasDividendGrowthInLast5Yrs()
        buyHoldModelAux.HasNetProfitBeenRegularFor5Yrs = financialHistData.HasNetProfitBeenRegularFor5Yrs()

        print("%s - OK" % companyInfo.Code)

        companyInfo = None
        companyStatistic = None
        financialHistData = None
        dividendCrawler = None

        returnObj.append(buyHoldModelAux)
    return returnObj

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
