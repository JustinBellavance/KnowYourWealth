import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

def stockIsInYF(ticker: str):
    try:
        yf.Ticker(ticker).info
        return True
    except:
        return False
    

def getStockFromYF(ticker: str):
    yf_ticker = yf.Ticker(ticker)
    hist = yf_ticker.history(period="5d")
    hist.drop(["Stock Splits", "High", "Low", "Volume"], axis=1, inplace=True)
    hist.reset_index(inplace=True)
    hist["Ticker"] = ticker
    hist.rename(columns={"Date": "date", "Open": "open", "Close": "close", "Adj Close": "adj_close"}, inplace=True)
    hist = hist.to_dict(orient="records")
    return hist

def insertWeekends(ticker_history_df: pd.DataFrame) -> pd.DataFrame:
    
    # we will iterate over the dataframe and check if the next date is not the next day
    # if it isn't, we will insert a row with the next date and the same values as the previous date
    # we will do this until we reach the last date, where we will order the dataframe by date ascending, and rerun the function until no new dates are added
    
    ticker_history_df = ticker_history_df.sort_values(by="date")
    ticker_history_df.reset_index(drop=True, inplace=True)
    
    for index, row in ticker_history_df.iterrows():
        if index == len(ticker_history_df) - 1:
            break
        
        if (ticker_history_df.loc[index + 1, "date"] - row["date"]).days > 1:
            # copy the row but change the date to the next day and open column to the close column of the previous row
            new_row = row.copy()
            new_row["date"] = row["date"] + timedelta(days=1)
            new_row["open"] = row["close"]
            ticker_history_df = ticker_history_df._append(new_row, ignore_index=True)
            
    ticker_history_df = ticker_history_df.sort_values(by="date")
    ticker_history_df.reset_index(drop=True, inplace=True)
    
    for index, row in ticker_history_df.iterrows():
        if index == len(ticker_history_df) - 1:
            break
        
        if (ticker_history_df.loc[index + 1, "date"] - row["date"]).days > 1:
            return insertWeekends(ticker_history_df)
        
    return ticker_history_df
    

#Data cleaning in this step
def getStockHistory(ticker: str, date1 : str, date2: str) -> pd.DataFrame:
    
    ticker_history_df = yf.Ticker(ticker).history(start=date1, end=date2, interval="1d")
    ticker_history_df.drop(["Stock Splits", "High", "Low", "Volume"], axis=1, inplace=True)
    ticker_history_df.reset_index(inplace=True)
    ticker_history_df["Ticker"] = ticker
    ticker_history_df.rename(columns={"Date": "date", "Open": "open", "Close": "close", "Adj Close": "adj_close"}, inplace=True)
    
    # yahoo doesn't give weekend data, we we will populate it ourselves.
    ticker_history_with_weekends_df = insertWeekends(ticker_history_df)
    
    return ticker_history_with_weekends_df


# returns a dict of portfolio worth of that ticker over the first transaction date to present date
# worth updated daily (for now)
# format {date : worth, date : worth, ...}
def getStockWorth(ticker_history: pd.DataFrame, holding_transactions: any) -> dict:
        
    # TODO: current logic is that we buy on the open price and price ends on close price
    # TODO: most times the open price is not the same as the previous clsoe price, but this function assumes it is.
        # maybe we just use the close price of the previous day as the open price of the current day
    
    # iterate over row of ticker_history
    ht_index = 0
    historical_worth = {}
    for index, row in ticker_history.iterrows():
                
        value_change = 0
        
        if (ht_index < len(holding_transactions)):
            
            while holding_transactions[ht_index][1] == str(row['date'].date()):
                # number of shares and current price + gains from current price
                if holding_transactions[ht_index][0] == 'add':
                    value_change += (holding_transactions[ht_index][2] * row['open']) + (holding_transactions[ht_index][2] * row['open'] - holding_transactions[ht_index][2] * holding_transactions[ht_index][3])
                elif holding_transactions[ht_index][0] == 'remove':
                    value_change -= (holding_transactions[ht_index][2] * row['open']) + (holding_transactions[ht_index][2] * row['open'] - holding_transactions[ht_index][2] * holding_transactions[ht_index][3])
                ht_index = ht_index + 1
                if ht_index >= len(holding_transactions):
                    break
            
        value_change += row['close'] - row['open']
        
        # current logic assumed dividends are automatically reinvested
        value_change += row['Dividends']
        
        # if it's the first day, add the value change (rounded to 2 decimal places)
        # TODO: rounding logic is not always accurate
        if index != 0:
            historical_worth[str(row['date'].date())] = round(historical_worth[str(row['date'].date() - timedelta(days=1))] + value_change,2)
        else:
            historical_worth[str(row['date'].date())] = round(value_change,2)
        
    return historical_worth

#return a dict of dates and value of holding until given date, incremented daily
def getDailyValue(ticker:str, holding_transactions:any, date:datetime) -> dict:
    
    # add one day to the date because history is end date exclusive
    date_ex = date + timedelta(days=1)

    # we will assume that the system doesn't allow selling if you have not bought yet
    # and so the first transaction must be a buy (since it's asc sorter we will use that date)
    first_buy_date = holding_transactions[0][1]
    
    ticker_history = getStockHistory(ticker, first_buy_date, date_ex)
    
    # now we will get daily value of holding while considering the transactions
    stockWorth = getStockWorth(ticker_history, holding_transactions)
    
    # print(stockWorth)
    
    #default interval is one day, but for robustness we still specify
    return stockWorth
    