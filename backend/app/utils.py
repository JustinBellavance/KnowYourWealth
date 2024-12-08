from instance import config
from sqlmodel import SQLModel, Field, create_engine, Session
from sqlalchemy import text
from datetime import datetime, timedelta
from dateutil.rrule import rrule, DAILY
from .yfinance_utils import getDailyValue, getStockHistory

from collections import defaultdict

def getRemainingCash(session: Session, portfolio_id: int) -> float:
    # Parameterized query to avoid SQL injection
    query = text("""
        WITH adjusted_cash AS (
            SELECT name, interest,
                CASE
                    WHEN action = 'remove' THEN -amount
                    ELSE amount
                END AS adjusted_amount
            FROM cash
            WHERE portfolio_id = :portfolio_id
        )
        SELECT name, SUM(adjusted_amount) AS amount, interest
        FROM adjusted_cash
        GROUP BY name, interest
    """)

    # Execute the query with the parameter
    result = session.exec(query.params(portfolio_id=portfolio_id)).first()

    if result is None:
        #print("No results found.")
        return 0.0

    #print(f"Name: {result.name}, Amount: {result.amount}, Interest: {result.interest}")
    return result.amount

def getRemainingShares(session : Session, portfolio_id : int, ticker = str) -> float:
    
    query = text("""
        WITH adjusted_shares AS (
            SELECT ticker,
                CASE
                    WHEN action = 'remove' THEN -amount
                    ELSE amount
                END AS adjusted_amount
            FROM stock_holdings
            WHERE portfolio_id=:portfolio_id AND ticker=:ticker
        )
        SELECT ticker, SUM(adjusted_amount) AS amount
        FROM adjusted_shares
        GROUP BY ticker
    """)

    result = session.exec(query.params(portfolio_id=portfolio_id, ticker=ticker)).first()
    
    if result is None:
        print("No results found.")
        return 0.0
    
    #print(f"Name: {result.ticker}, Amount: {result.amount}")

    return result.amount

def getFirstTransactionDate(session: Session, portfolio_id: int, until_date: datetime) -> datetime:
    
    query = text("""
                 SELECT MIN(date(date)) as first_transaction_date
                 FROM stock_holdings sh
                 WHERE sh.portfolio_id = :portfolio_id AND sh.date < :until_date
                 UNION
                 SELECT MIN(date(date)) as first_transaction_date
                 FROM cash c
                 WHERE c.portfolio_id = :portfolio_id AND c.date < :until_date
                 """)
    
    result = session.exec(query.params(portfolio_id=portfolio_id, until_date=until_date)).first()
    
    if result and result.first_transaction_date:
        return result.first_transaction_date
    else:
        # Return None if no results found or if the date is invalid
        return None
    
def getHistoricalAssets(session : Session, portfolio_id : int, until_date : datetime) -> list:
    allStocks = getHistoricalStocks(session, portfolio_id, until_date, True)
    allCash = getHistoricalCash(session, portfolio_id, until_date, True)
    
    return(allStocks + allCash)

def getHistoricalStocks(session : Session, portfolio_id : int, until_date : datetime, consider_all_assets : bool = False) -> list:

    query = text("""
        WITH calculated_basis AS (
            SELECT 
                ticker,
                CASE
                    WHEN action = 'add' THEN amount
                    ELSE -amount
                END AS adjusted_amount,
                CASE
                    WHEN action = 'add' THEN (amount * price + COALESCE(fees, 0))
                    ELSE 0
                END AS adjusted_cost,
                date(date) AS transaction_date
            FROM stock_holdings
            WHERE portfolio_id = :portfolio_id AND date < :until_date
        )
        SELECT 
            ticker,
            transaction_date,
            SUM(adjusted_cost) / NULLIF(SUM(CASE WHEN adjusted_amount > 0 THEN adjusted_amount ELSE 0 END), 0) AS avg_cost_basis,
            SUM(adjusted_amount) AS total_shares
        FROM calculated_basis
        GROUP BY ticker, transaction_date
        HAVING SUM(adjusted_amount) > 0;
    """)

    results = session.exec(query.params(portfolio_id=portfolio_id, until_date=until_date)).all()
    
    if results is None:
        print("No results found.")
        return 0.0
    
    current_stocks = [
        {
            'name' : result.ticker,
            'quantity' : result.total_shares,
            'price' : result.avg_cost_basis,
            'date' : result.transaction_date,
        }
    for result in results]
    
    #print(current_stocks)
    first_date = None
    
    if consider_all_assets:
        first_date = getFirstTransactionDate(session, portfolio_id, until_date)
    
    
    historical_stocks = populateDailyStocks(until_date, current_stocks, first_date)

    print(f"{historical_stocks=}")

    return historical_stocks

def populateDailyStocks(until_date: datetime, historical_stocks: list, first_transaction_date: datetime = None) -> list:
    if not historical_stocks:
        return []

    historical_dict = defaultdict(lambda: defaultdict(lambda: 0))  # Default value of 0 for missing data
    for entry in historical_stocks:
        key = (entry["name"], entry["date"])
        historical_dict[key] = {
            "price": entry["price"],
            "amount": entry["quantity"],
        }

    tickers = {entry["name"] for entry in historical_stocks}

    first_date = datetime.strptime(historical_stocks[0]["date"], "%Y-%m-%d").date()
    
    if first_transaction_date:
        first_date = datetime.strptime(first_transaction_date, "%Y-%m-%d").date()    
    
    last_date = until_date.date()
    
    populated_stocks = {ticker: [] for ticker in tickers}

    for ticker in tickers:
        
        # get stock price change via yfinance
        stock_history = getStockHistory(ticker, first_date, until_date )
        print(stock_history)
        print(stock_history.shape)
        
        last_known_price = 0
        last_known_amount = 0
        stock_purchased = False  # Track if any stock has been purchased

        current_date = first_date
        while current_date <= last_date:
            date_str = current_date.strftime("%Y-%m-%d")
            key = (ticker, date_str)
            
            price_change = 0
            price_today = 0
            price_yesterday = 0
            
            price_today_series = stock_history[stock_history['date'] == date_str]['close']
            if len(price_today_series.values) > 0:
                price_today = price_today_series.values[0]
                
            if (current_date - timedelta(days=1)) > first_date and price_today != 0:
                price_yesterday_series = stock_history[stock_history['date'] == (current_date - timedelta(days=1)).strftime("%Y-%m-%d")]['close']

                if len(price_yesterday_series.values) > 0:
                    price_yesterday = price_yesterday_series.values[0]
                
            
            if price_yesterday:
                price_change = price_today - price_yesterday
                
            if key in historical_dict:
                data = historical_dict[key]
                last_known_price = data["price"]
                last_known_amount = data["amount"]
                stock_purchased = True
                value = (data["price"] + price_change) * data['amount']
            else:
                if stock_purchased:
                    value = (last_known_price + price_change) * last_known_amount
                else:
                    value = 0  # If no stock purchased yet, set value to 0

            populated_stocks[ticker].append({
                "name": ticker,
                "date": date_str,
                "price": last_known_price,
                "quantity": last_known_amount,
                "value": value
            })

            current_date += timedelta(days=1)

    result = []
    for records in populated_stocks.values():
        result.extend(records)

    return result

def getHistoricalCash(session : Session, portfolio_id : int, until_date : datetime, consider_all_assets : bool = False) -> list:
    
    historical_cash = []
    
    query = text("""
    SELECT 
        date(date) AS transaction_date,
        SUM(CASE WHEN action = 'add' THEN amount ELSE -amount END) AS daily_net_change,
        SUM(SUM(CASE WHEN action = 'add' THEN amount ELSE -amount END)) OVER (
            PARTITION BY portfolio_id
            ORDER BY date(date)
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS cumulative_value
    FROM cash
    WHERE portfolio_id = :portfolio_id AND date < :until_date
    GROUP BY transaction_date, portfolio_id
    ORDER BY transaction_date;
    """)

    results = session.exec(query.params(portfolio_id=portfolio_id, until_date=until_date)).all()
    
    historical_cash = [{"value": row[1], "date": row[0]} for row in results]
    
    first_date = None
    
    if consider_all_assets:
        first_date = getFirstTransactionDate(session, portfolio_id, until_date)
    
    
    historical_cash = populateDailyCash(until_date, historical_cash, first_date)    
    return historical_cash

def populateDailyCash(until_date: datetime, historical_cash: list, first_transaction_date: datetime = None ):
    if not historical_cash:
        return []

    # Create a dictionary for cash data with the date as the key
    historical_cash_dict = {entry["date"]: entry["value"] for entry in historical_cash}

    first_date = datetime.strptime(historical_cash[0]["date"], "%Y-%m-%d").date()
    
    if first_transaction_date:
        first_date = datetime.strptime(first_transaction_date, "%Y-%m-%d").date()

    last_date = until_date.date()

    populated_cash = []
    last_known_value = 0

    current_date = first_date
    while current_date <= last_date:
        date_str = current_date.strftime("%Y-%m-%d")

        value = historical_cash_dict.get(date_str, last_known_value)

        populated_cash.append({
            "name": "Cash",
            "value": value,
            "date": date_str
        })

        # Update the cash value if it's available for this date
        if date_str in historical_cash_dict:
            last_known_value = historical_cash_dict[date_str]

        current_date += timedelta(days=1)

    return populated_cash

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