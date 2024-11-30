from instance import config
from sqlmodel import SQLModel, Field, create_engine, Session
from sqlalchemy import text
from datetime import datetime, timedelta
from dateutil.rrule import rrule, DAILY
from .yfinance_utils import getDailyValue

# SQLModel engine setup
engine = create_engine(config.DATABASE_URL)

def getDailyValueRealEstate(real_estate_transactions:list[tuple], until_date) -> dict:
    
    first_buy = real_estate_transactions[0]
    
    transactions_daily_historical_data = {}
    
    transaction_index = 0
    
    for date in rrule(DAILY, dtstart=datetime.strptime(first_buy[2], "%Y-%m-%d %H:%M:%S.%f"), until=until_date):
        date_str = date.strftime("%Y-%m-%d")
        
        change_in_cash = 0
        
        transaction_date_at_index = str(datetime.strptime(real_estate_transactions[transaction_index][2], "%Y-%m-%d %H:%M:%S.%f").date())


        # check for transaction on this date
        while(date_str == transaction_date_at_index):
            
            if (real_estate_transactions[transaction_index][3] == 'add'):
                change_in_cash += real_estate_transactions[transaction_index][1]
            elif (real_estate_transactions[transaction_index][3] == 'sell'):
                change_in_cash -= real_estate_transactions[transaction_index][1]

            if (transaction_index + 1 >= len(real_estate_transactions)):
                break
            transaction_date_at_index = str(datetime.strptime(real_estate_transactions[transaction_index][2], "%Y-%m-%d %H:%M:%S.%f").date())
            transaction_index += 1
            
        if (transactions_daily_historical_data != {}):
            # add interest to the cash
            change_in_cash += transactions_daily_historical_data[str(date.date() - timedelta(1))]
            transactions_daily_historical_data[date_str] = round(transactions_daily_historical_data[str(date.date() - timedelta(1))] + change_in_cash, 2)
        else:
            transactions_daily_historical_data[date_str] = round(change_in_cash,2)
    
    return transactions_daily_historical_data
    
def getAverageInterestRate(currentCash, currentInterestRate, newCash, newInterestRate) -> float:
    return (currentCash * currentInterestRate + newCash * newInterestRate) / (currentCash + newCash)

def calculateAccruedInterestCash(cash_transactions:list[tuple], until_date) -> dict:
    
    # TODO: we assume the interest is annual, but calculated on a daily basis
    
    # get first transaction (we assume it's an addition of cash)
    first_buy = cash_transactions[0]
    
    transactions_daily_historical_data = {}
    transaction_index = 0
    average_daily_interest = 0
    
    for date in rrule(DAILY, dtstart=datetime.strptime(first_buy[3], "%Y-%m-%d %H:%M:%S.%f"), until=until_date):
        date_str = date.strftime("%Y-%m-%d")
        
        change_in_cash = 0

        # check for transaction on this date
        transaction_date_at_index = str(datetime.strptime(cash_transactions[transaction_index][3], "%Y-%m-%d %H:%M:%S.%f").date())
        
        while(date_str == transaction_date_at_index):
            
            if (cash_transactions[transaction_index][4] == 'add'):
                change_in_cash += cash_transactions[transaction_index][1]
                if (transactions_daily_historical_data == {}):
                    average_daily_interest = (cash_transactions[transaction_index][2]/ 100 )/ 365
                else:
                    average_daily_interest = (getAverageInterestRate(transactions_daily_historical_data[str(date.date() - timedelta(1))], average_daily_interest, cash_transactions[transaction_index][1], cash_transactions[transaction_index][2]) / 100 )/ 365
            elif (cash_transactions[transaction_index][4] == 'sell'):
                change_in_cash -= cash_transactions[transaction_index][1]
                # this cannot be the first date, so no if statement
                average_daily_interest = (cash_transactions[transaction_index][2]/ 100 )/ 365

            if (transaction_index + 1 >= len(cash_transactions)):
                break
            transaction_date_at_index = str(datetime.strptime(cash_transactions[transaction_index][3], "%Y-%m-%d %H:%M:%S.%f").date())
            transaction_index += 1
            
        if (transactions_daily_historical_data != {}):
            # add interest to the cash
            change_in_cash += transactions_daily_historical_data[str(date.date() - timedelta(1))] * average_daily_interest
            transactions_daily_historical_data[date_str] = round(transactions_daily_historical_data[str(date.date() - timedelta(1))] + change_in_cash, 2)
        else:
            transactions_daily_historical_data[date_str] = round(change_in_cash,2)

    
    return transactions_daily_historical_data

def calculateAccruedInterestDebt(debt_transactions:list[tuple], until_date) -> dict:
        
    # TODO: we assume the interest is annual, but calculated on a daily basis
    
    # get first transaction (we assume it's an addition of cash)
    first_buy = debt_transactions[0]
    
    transactions_daily_historical_data = {}
    transaction_index = 0
    average_daily_interest = 0
    
    for date in rrule(DAILY, dtstart=datetime.strptime(first_buy[3], "%Y-%m-%d %H:%M:%S.%f"), until=until_date):
        date_str = date.strftime("%Y-%m-%d")
        
        change_in_cash = 0

        # check for transaction on this date
        transaction_date_at_index = str(datetime.strptime(debt_transactions[transaction_index][3], "%Y-%m-%d %H:%M:%S.%f").date())
        
        while(date_str == transaction_date_at_index):
            
            if (debt_transactions[transaction_index][4] == 'add'):
                change_in_cash -= debt_transactions[transaction_index][1]
                if (transactions_daily_historical_data == {}):
                    average_daily_interest = (debt_transactions[transaction_index][2]/ 100 )/ 365
                else:
                    average_daily_interest = (getAverageInterestRate(transactions_daily_historical_data[str(date.date() - timedelta(1))], average_daily_interest, debt_transactions[transaction_index][1], debt_transactions[transaction_index][2]) / 100 )/ 365
            elif (debt_transactions[transaction_index][4] == 'sell'):
                change_in_cash += debt_transactions[transaction_index][1]
                # this cannot be the first date, so no if statement
                average_daily_interest = (debt_transactions[transaction_index][2]/ 100 )/ 365

            if (transaction_index + 1 >= len(debt_transactions)):
                break
            transaction_date_at_index = str(datetime.strptime(debt_transactions[transaction_index][3], "%Y-%m-%d %H:%M:%S.%f").date())
            transaction_index += 1
            
        if (transactions_daily_historical_data != {}):
            # add interest to the cash
            change_in_cash += transactions_daily_historical_data[str(date.date() - timedelta(1))] * average_daily_interest
            transactions_daily_historical_data[date_str] = round(transactions_daily_historical_data[str(date.date() - timedelta(1))] + change_in_cash, 2)
        else:
            transactions_daily_historical_data[date_str] = round(change_in_cash,2)

    
    return transactions_daily_historical_data

# Function to fetch historical data
def getPortfolioHistoricalData(portfolioid: int, present_date: datetime) -> dict:
    with Session(engine) as session:
        allHistoricalData = {}

        # Fetch unique tickers
        unique_tickers_list = session.exec(text(
            f"SELECT DISTINCT(ticker) FROM stock_holdings WHERE portfolio_id = {portfolioid} ORDER BY date ASC"
        )).all()

        stocks_historical_daily_data = {}
        for ticker in unique_tickers_list:
            ticker_transactions = session.exec(text(
                f"SELECT action, DATE(date), amount, price FROM stock_holdings WHERE ticker = '{ticker}' ORDER BY date ASC"
            )).all()
            ticker_daily_value = getDailyValue(ticker, ticker_transactions, present_date.date())
            stocks_historical_daily_data[ticker] = ticker_daily_value
        
        allHistoricalData['stocks'] = stocks_historical_daily_data

        # Fetch and process cash data
        cash_transactions = session.exec(text(
            f"SELECT name, amount, interest, date, action FROM cash WHERE portfolio_id = {portfolioid} ORDER BY date ASC"
        )).all()

        cash_historical_daily_data = calculateAccruedInterestCash(cash_transactions, present_date.date())
        allHistoricalData['cash'] = cash_historical_daily_data

        # Fetch and process debt data
        debt_transactions = session.exec(text(
            f"SELECT name, amount, interest, date, action FROM debt WHERE portfolio_id = {portfolioid} ORDER BY date ASC"
        )).all()

        debt_historical_daily_data = calculateAccruedInterestDebt(debt_transactions, present_date.date())
        allHistoricalData['debt'] = debt_historical_daily_data

        # Fetch and process real estate data
        real_estate_transactions = session.exec(text(
            f"SELECT name, worth, date, action FROM real_estate WHERE portfolio_id = {portfolioid} ORDER BY date ASC"
        )).all()

        real_estate_historical_daily_data = getDailyValueRealEstate(real_estate_transactions, present_date.date())
        allHistoricalData['real_estate'] = real_estate_historical_daily_data

    return allHistoricalData

def getStockFromPortfolio(session, portfolioid: int) -> list[dict]:
    result = session.exec(text(
        f"""
        WITH adjusted_amount AS (
            SELECT ticker, price,
            CASE
                WHEN action = 'remove' THEN -amount
                ELSE amount
            END AS adj_amount
            FROM stock_holdings
            WHERE portfolio_id = {portfolioid}
        ), grouped_stocks AS (
            SELECT ticker, SUM(adj_amount) AS amount, price
            FROM adjusted_amount
            GROUP BY ticker, price
        )
        SELECT ROW_NUMBER() OVER (ORDER BY ticker) AS id, ticker, amount, price
        FROM grouped_stocks
        """
    )).all()

    stocks = [
        {'ticker': row.ticker, 'amount': row.amount, 'price': row.price}
        for row in result
    ]

    return stocks

def getRealEstateFromPortfolio(session, portfolioid: int) -> list[dict]:
    result = session.exec(text(
        """
        WITH adjusted_worth AS (
            SELECT name,
            CASE
                WHEN action = 'remove' THEN -worth
                ELSE worth
            END AS worth
            FROM real_estate
            WHERE portfolio_id = :portfolioid
        )
        SELECT name, sum(worth) AS worth
        FROM adjusted_worth
        GROUP BY name
        """
    ), params={"portfolioid": portfolioid}).all()

    real_estate = [
        {'name': row.name, 'worth': row.worth}
        for row in result
    ]

    return real_estate

def getCashFromPortfolio(session, portfolioid: int) -> list[dict]:
    result = session.exec(text(
        f"""
        WITH adjusted_cash AS (
            SELECT name, interest,
            CASE
                WHEN action = 'remove' THEN -amount
                ELSE amount
            END AS adjusted_amount
            FROM cash
            WHERE portfolio_id = {portfolioid}
        )
        SELECT name, SUM(adjusted_amount) AS amount, interest
        FROM adjusted_cash
        GROUP BY name, interest
        """
    )).all()

    cash = [
        {'name': row.name, 'amount': row.amount, 'interest': row.interest}
        for row in result
    ]

    return cash

def getDebtFromPortfolio(session, portfolioid: int) -> list[dict]:
    result = session.exec(text(
        f"""
        WITH adjusted_debt AS (
            SELECT name, interest,
            CASE
                WHEN action = 'remove' THEN -amount
                ELSE amount
            END AS adjusted_amount
            FROM debt
            WHERE portfolio_id = {portfolioid}
        )
        SELECT name, SUM(adjusted_amount) AS amount, interest
        FROM adjusted_debt
        GROUP BY name, interest
        """
    )).all()

    debt = [
        {'name': row.name, 'amount': row.amount, 'interest': row.interest}
        for row in result
    ]

    return debt

def getPortfolioInformation(session, portfolioid: int) -> dict:
    statement = text("SELECT name FROM portfolio WHERE portfolio_id = :portfolioid")
    result = session.exec(statement, params={"portfolioid": portfolioid}).first()
    return result.name if result else None

def getAllHoldingsFromPortfolio(portfolioid: int) -> dict[str, list]:
    with Session(engine) as session:
        holdings = {}
        holdings['name'] = getPortfolioInformation(session, portfolioid)
        holdings['stocks'] = getStockFromPortfolio(session, portfolioid)
        holdings['real_estate'] = getRealEstateFromPortfolio(session, portfolioid)
        holdings['cash'] = getCashFromPortfolio(session, portfolioid)
        holdings['debt'] = getDebtFromPortfolio(session, portfolioid)
    
    return holdings