DELIMITER $$
CREATE PROCEDURE `SP_INSERT_DIVIDEND`(
    IN CODE VARCHAR(10), 
    IN COMPANY VARCHAR(255), 
    IN SECTOR VARCHAR(255), 
    IN SECOND_SECTOR VARCHAR(255),
    IN STOCK_PRICE DECIMAL(20,6),
    IN STOCK_TYPE VARCHAR(2),
    IN VALUATION DECIMAL(20,6),
    IN STOCK_AVAILABLE_AMOUNT DECIMAL(20,6),
    IN AVG_21_NEGOCIATION DECIMAL(20,6),
    IN DIVIDEND_PERIOD DECIMAL(2, 0),
    IN DIVIDEND_LAST_PRICE DECIMAL(20,6),
    IN NET_PROFIT DECIMAL(20,6),
    IN DIVIDEND_YELD DECIMAL(20,6),
    IN AVG_PAYOUT_12_MONTHS DECIMAL(20,6),
    IN AVG_PAYOUT_5_YEARS DECIMAL(20,6),
    IN MAJOR_SHARE_HOLDER VARCHAR(255),
	IN ROE DECIMAL(20,6),
	IN ROE_5_YRS DECIMAL(20,6),
	IN GROSS_DEBT_OVER_EBTIDA DECIMAL(20,6),
	IN DIVIDEND_YIELD_5_YRS DECIMAL(20,6),
	IN HAS_DIVIDEND_SRD_5_YERS BIT,
	IN HAS_DIVIDEND_GRWTH_5_YRS BIT,
	IN HAS_NET_PROFIT_REG_5_YRS BIT
    )
BEGIN
	IF (SELECT COUNT(D.STOCK_CODE) FROM SYS.DIVIDEND AS D WHERE D.STOCK_CODE = CODE) = 0
		THEN
			INSERT INTO `sys`.`dividend`
			(
			`STOCK_CODE`,
			`COMPANY`,
			`SECTOR`,
			`SECOND_SECTOR`,
			`STOCK_PRICE`,
			`STOCK_TYPE`,
			`VALUATION`,
			`STOCK_AVAILABLE_AMOUNT`,
			`AVG_21_NEGOCIATION`,
			`DIVIDEND_PERIOD`,
			`DIVIDEND_LAST_PRICE`,
			`NET_PROFIT`,
			`DIVIDEND_YELD`,
			`AVG_PAYOUT_12_MONTHS`,
			`AVG_PAYOUT_5_YEARS`,
			`MAJOR_SHARE_HOLDER`,
			`ROE`,
			`ROE_5_YRS`,
			`GROSS_DEBT_OVER_EBTIDA`,
			`DIVIDEND_YIELD_5_YRS`,
			`HAS_DIVIDEND_SRD_5_YERS`,
			`HAS_DIVIDEND_GRWTH_5_YRS`,
			`HAS_NET_PROFIT_REG_5_YRS`,
			`DT_LAST_UPDATE`
			)
			VALUES
			(
			CODE,
			COMPANY,
			SECTOR,
			SECOND_SECTOR,
            STOCK_PRICE,
			STOCK_TYPE,
			VALUATION,
			STOCK_AVAILABLE_AMOUNT,
			AVG_21_NEGOCIATION,
			DIVIDEND_PERIOD,
			DIVIDEND_LAST_PRICE,
			NET_PROFIT,
			DIVIDEND_YELD,
			AVG_PAYOUT_12_MONTHS,
			AVG_PAYOUT_5_YEARS,
			MAJOR_SHARE_HOLDER,
			ROE,
			ROE_5_YRS,
			GROSS_DEBT_OVER_EBTIDA,
			DIVIDEND_YIELD_5_YRS,
			HAS_DIVIDEND_SRD_5_YERS,
			HAS_DIVIDEND_GRWTH_5_YRS,
			HAS_NET_PROFIT_REG_5_YRS,
			NOW()
			);
    ELSE
			UPDATE `sys`.`dividend`
				SET
					`STOCK_CODE` = CODE,
					`COMPANY` = COMPANY,
					`SECTOR` = SECTOR,
					`SECOND_SECTOR` = SECOND_SECTOR,
					`STOCK_PRICE` = STOCK_PRICE,
					`STOCK_TYPE` = STOCK_TYPE,
					`VALUATION` = VALUATION,
					`STOCK_AVAILABLE_AMOUNT` = STOCK_AVAILABLE_AMOUNT,
					`AVG_21_NEGOCIATION` = AVG_21_NEGOCIATION,
					`DIVIDEND_PERIOD` = DIVIDEND_PERIOD,
					`DIVIDEND_LAST_PRICE` = DIVIDEND_LAST_PRICE,
					`NET_PROFIT` = NET_PROFIT,
					`DIVIDEND_YELD` = DIVIDEND_YELD,
					`AVG_PAYOUT_12_MONTHS` = AVG_PAYOUT_12_MONTHS,
					`AVG_PAYOUT_5_YEARS` = AVG_PAYOUT_5_YEARS,
					`MAJOR_SHARE_HOLDER` = MAJOR_SHARE_HOLDER,
					`ROE` = ROE,
					`ROE_5_YRS` = ROE_5_YRS,
					`GROSS_DEBT_OVER_EBTIDA` = GROSS_DEBT_OVER_EBTIDA,
					`DIVIDEND_YIELD_5_YRS` = DIVIDEND_YIELD_5_YRS,
					`HAS_DIVIDEND_SRD_5_YERS` = HAS_DIVIDEND_SRD_5_YERS,
					`HAS_DIVIDEND_GRWTH_5_YRS` = HAS_DIVIDEND_GRWTH_5_YRS,
					`HAS_NET_PROFIT_REG_5_YRS` = HAS_NET_PROFIT_REG_5_YRS,
					DT_LAST_UPDATE = NOW()
			WHERE SYS.DIVIDEND.STOCK_CODE = CODE;
	END IF;
	COMMIT;
END$$
DELIMITER ;