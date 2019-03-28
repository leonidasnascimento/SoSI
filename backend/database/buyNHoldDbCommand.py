import sys

# ADDING ITEMS TO SYS.PATH #
sys.path.append("\\git\\SoSI\\backend")

from database.base.dbCommand import DbCommand
from stockLogic.models.buynHoldModel import BuyNHoldeModel

class BuyNHoldDbCommand:
    def Save(self, obj):
        if obj is None:
            raise Exception 

        print("############# passei aqui '1 - BuyNHoldDbCommand' ##################")

        args = (obj.Code, obj.Company, obj.Sector, obj.SecondSector, 
            obj.StockPrice, obj.Type, obj.Valuation, obj.StockAvailableAmount, obj.Avg21Negociation, 
            obj.DividendPeriod, obj.DividendLastPrice,  
            obj.NetProfit, obj.DividendYeld, obj.AvgPayout12Months, obj.AvgPayout5Years, obj.MajorShareholder,
            obj.ReturnOnEquity, obj.ReturnOnEquity_5yrAvg, obj.GrossDebitOverEbitda, 
            obj.DividendYeld_5yrAvg, obj.HasDividendBeenSharedInLast5Yrs, 
            obj.HasDividendGrowthInLast5Yrs, obj.HasNetProfitBeenRegularFor5Yrs)
        

        print("############# passei aqui '2 - BuyNHoldDbCommand' ##################")

        strCmd = "CALL SP_INSERT_DIVIDEND ('%s', '%s', '%s', '%s', %.6f, '%s', %.6f, %d, %.6f, %d, %.6f, %.6f, %.6f, %.6f, %.6f, '%s', %.6f, %.6f, %.6f, %.6f, %i, %i, %i);" % args

        print("############# passei aqui '2 - BuyNHoldDbCommand' ##################")
        print (strCmd)
        
        return DbCommand().Commit(strCmd)        
        # return DbCommand().CallProcedure("SP_INSERT_DIVIDEND", args)