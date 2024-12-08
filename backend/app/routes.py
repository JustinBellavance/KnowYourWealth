#app/routes.py
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
import os
import jwt
from sqlmodel import Session, select
from app.models import Users, Portfolio, StockHoldings, Cash, Debt, RealEstate
from app.utils import getStockFromPortfolio, getHistoricalCash, getRemainingCash, getRemainingShares, getHistoricalStocks, getHistoricalAssets
from app.yfinance_utils import stockIsInYF
from datetime import datetime, timedelta
from instance.config import db

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('SECRET_KEY')

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_session():
    with db as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# Create a FastAPI app instance
app = FastAPI()

# JWT Authentication Helper Functions
def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None

# FastAPI Routes
@app.put("/stocks/add/{portfolio_id}")
async def add_stock(portfolio_id: int, request: Request, session: SessionDep):
    data = await request.json()
    ticker = data['ticker']
    price = data['price']
    quantity = data['quantity']
    date = data['date']

    # if not stockIsInYF(ticker):
    #     raise HTTPException(status_code=404, detail="Stock not found in Yahoo Finance")
    
    new_holding = StockHoldings(portfolio_id=portfolio_id, ticker=ticker, price=price, amount=quantity, action="add")
    
    session.add(new_holding)
    session.commit()
    
    return {"message": f"Successfully added {quantity} of {ticker} @ {price} in {portfolio_id=} at {date}"}, 200

@app.put("/stocks/remove/{portfolio_id}")
async def remove_stock(portfolio_id: int, request: Request, session: SessionDep):
    data = await request.json()
    ticker = data['ticker']
    price = data['price']
    quantity = data['quantity']
    date = data['date']

    # TODO : check if stock is (and correct number of shares) in the portfolio before selling
    remaining_shares = getRemainingShares(session, portfolio_id, ticker)
    
    if quantity > remaining_shares:
        raise HTTPException(
            status_code=403,
            detail=f"Only {remaining_shares} shares of {ticker} in the portfolio, but you tried to remove {quantity}. Could not remove shares."
        )

    # if not stockIsInYF(ticker):
    #     raise HTTPException(status_code=404, detail="Stock not found in Yahoo Finance")

    new_holding = StockHoldings(portfolio_id=portfolio_id, ticker=ticker, price=price, amount=quantity, action="remove")
    
    session.add(new_holding)
    session.commit()
    
    return {"message": f"Successfully sold {quantity} of {ticker} @ {price} in {portfolio_id=} at {date}"}, 200

@app.put("/cash/add/{portfolio_id}")
async def add_cash(portfolio_id: int, request: Request, session: SessionDep):
    data = await request.json()
    name = None
    amount = data['amount']
    date = data['date']
    interest = None

    new_cash = Cash(
        portfolio_id=portfolio_id,
        name=name,
        amount=amount,
        interest=interest,
        action='add'
    )

    session.add(new_cash)
    session.commit()

    return {"message": f"Successfully added {amount} of cash in {portfolio_id=} at {date}"}, 200

@app.put("/cash/remove/{portfolio_id}")
async def remove_cash(portfolio_id: int, request: Request, session: SessionDep):
    data = await request.json()
    name = None
    amount = data['amount']
    date = data['date']
    interest = None
    
    remaining_cash = getRemainingCash(session, portfolio_id)
        
    if amount > remaining_cash:
        raise HTTPException(
            status_code=403,
            detail=f"Only ${remaining_cash} remains in the portfolio, but you tried to remove ${amount}. Could not remove cash."
        )
    
    new_cash = Cash(
        portfolio_id=portfolio_id,
        name=name,
        amount=amount,
        interest=interest,
        action='remove'
    )

    session.add(new_cash)
    session.commit()
    return {"message": f"Successfully removed {amount} of cash in {portfolio_id=} at {date}"}, 200

@app.get('/assets/{portfolio_id}')
async def get_assets(portfolio_id: int, session: SessionDep):
    
    current_date = datetime.now()
    
    all_assets = getHistoricalAssets(session, portfolio_id, current_date)
    
    print(all_assets)
    
    return all_assets
    
@app.get('/stocks/{portfolio_id}')
async def get_stocks(portfolio_id: int, session: SessionDep):
        
    current_date = datetime.now()
    historical_stocks = getHistoricalStocks(session, portfolio_id, current_date)
      
    return historical_stocks
    
@app.get('/cash/{portfolio_id}')
async def get_cash(portfolio_id: int, session: SessionDep):
    
    current_date = datetime.now()
    historical_cash = getHistoricalCash(session, portfolio_id, current_date)
        
    return historical_cash


# @app.post("/login")
# async def login(request: Request):
#     data = await request.json()
#     username = data['username']
#     password = data['password']
    
#     user = Users.query.filter_by(username=username).first()
    
#     if not user or user.password != password:
#         raise HTTPException(status_code=400, detail="Bad username or password")
    
#     access_token = create_access_token({"user_id": user.user_id, "username": user.username})
#     return {"access_token": access_token}

# @app.get("/protected")
# async def protected(token: str = Depends(oauth2_scheme)):
#     current_user = verify_token(token)
#     if current_user is None:
#         raise HTTPException(status_code=401, detail="Invalid token or expired")
#     return current_user

# @app.post("/register")
# async def register(request: Request):
#     data = await request.json()
#     username = data['username']
#     password = data['password']
#     firstname = data['firstname']
#     lastname = data['lastname']
#     email = data['email']
#     country = data['country']

#     # Check if user already exists
#     if Users.query.filter_by(username=username).first():
#         raise HTTPException(status_code=400, detail="User already exists")
    
#     country_id = 1 if country.lower() == "canada" else 2

#     new_user = Users(
#         username=username,
#         password=password,  # Password should be hashed in production
#         firstname=firstname,
#         lastname=lastname,
#         email=email,
#         country_id=country_id
#     )

#     db.session.add(new_user)
#     db.session.commit()

#     access_token = create_access_token({"username": username})
#     return {"access_token": access_token}

# @app.delete("/delete_user")
# async def delete_user(request: Request):
#     data = await request.json()
#     user_to_delete = Users.query.filter_by(user_id=data['user_id'], password=data['password']).first()
    
#     if not user_to_delete:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     db.session.delete(user_to_delete)
#     db.session.commit()
#     return {"message": "User deleted successfully!"}

# @app.post("/add_portfolio")
# async def add_portfolio(request: Request):
#     data = await request.json()
#     new_portfolio = Portfolio(user_id=data['user_id'], name=data['portfolio_name'])
#     db.session.add(new_portfolio)
#     db.session.commit()
#     return {"message": "Portfolio created successfully"}

# @app.get("/portfolios/{id}")
# async def get_portfolios(id: int):
#     portfolios = Portfolio.query.filter_by(user_id=id).all()
#     if not portfolios:
#         raise HTTPException(status_code=404, detail="No portfolios found")
#     return {"portfolios": [portfolio.to_dict() for portfolio in portfolios]}

# @app.get("/portfolio/{id}")
# async def get_portfolio(id: int):
#     portfolio_holdings = getAllHoldingsFromPortfolio(id)
#     if not portfolio_holdings:
#         raise HTTPException(status_code=404, detail="Portfolio not found")
#     return {"portfolio": portfolio_holdings}

# @app.get("/chart_data/{portfolio_id}")
# async def get_chart_data(portfolio_id: int):
#     current_datetime = datetime.now()
#     portfolio_historical_data = getPortfolioHistoricalData(portfolio_id, current_datetime)
#     if not portfolio_historical_data:
#         raise HTTPException(status_code=404, detail="Couldn't retrieve historical data")
#     return {"historical_data": portfolio_historical_data}


# @app.post("/stocks/{portfolio_id}")
# async def add_stock(portfolio_id: int, request: Request):
#     data = await request.json()
#     ticker = data['ticker']
#     price = data['price']
#     quantity = data['quantity']
#     action = 'add'

#     if not stockIsInYF(ticker):
#         raise HTTPException(status_code=404, detail="Stock not found in Yahoo Finance")
    
#     new_holding = StockHoldings(portfolio_id=portfolio_id, ticker=ticker, price=price, amount=quantity, action=action)
#     db.session.add(new_holding)
#     db.session.commit()
#     return {"message": "Stock added successfully!"}

# @app.post('/remove_stocks/{id}')
# async def remove_stocks(id: int, request: Request):
#     data = await request.json()

#     portfolio_id = id
#     ticker = data.get('ticker')
#     average_price = data.get('price')
#     number_shares = data.get('quantity')
#     action = 'remove'

#     fees = data.get('fees', None)

#     if not ticker or not average_price or not number_shares:
#         raise HTTPException(status_code=400, detail="Missing required fields")

#     new_holding = StockHoldings(
#         portfolio_id=portfolio_id,
#         ticker=ticker,
#         price=average_price,
#         amount=number_shares,
#         fees=fees,
#         action=action
#     )

#     db.session.add(new_holding)
#     db.session.commit()
#     return {'message': 'Stock sold successfully!'}

# @app.post('/cash/{id}')
# async def add_cash(id: int, request: Request):
#     data = await request.json()

#     portfolio_id = id
#     name = data.get('name')
#     amount = data.get('amount')
#     interest = data.get('interest')
#     action = 'add'

#     if not name or not amount:
#         raise HTTPException(status_code=400, detail="Missing required fields")

#     new_cash = Cash(
#         portfolio_id=portfolio_id,
#         name=name,
#         amount=amount,
#         interest=interest,
#         action=action
#     )

#     db.session.add(new_cash)
#     db.session.commit()
#     return {'message': 'Cash added successfully!'}

# @app.post('/remove_cash/{id}')
# async def remove_cash(id: int, request: Request):
#     data = await request.json()

#     portfolio_id = id
#     name = data.get('name')
#     amount = data.get('amount')
#     interest = data.get('interest')
#     action = 'remove'

#     if not name or not amount:
#         raise HTTPException(status_code=400, detail="Missing required fields")

#     remove_cash = Cash(
#         portfolio_id=portfolio_id,
#         name=name,
#         amount=amount,
#         interest=interest,
#         action=action
#     )

#     db.session.add(remove_cash)
#     db.session.commit()
#     return {'message': 'Cash removed successfully!'}

# @app.post('/real_estate/{id}')
# async def add_real_estate(id: int, request: Request):
#     data = await request.json()

#     portfolio_id = id
#     name = data.get('name')
#     worth = data.get('worth')
#     action = 'add'

#     if not name or not worth:
#         raise HTTPException(status_code=400, detail="Missing required fields")

#     new_real_estate = RealEstate(
#         portfolio_id=portfolio_id,
#         name=name,
#         worth=worth,
#         action=action
#     )

#     db.session.add(new_real_estate)
#     db.session.commit()
#     return {'message': 'Real estate added successfully!'}

# @app.post('/remove_real_estate/{id}')
# async def remove_real_estate(id: int, request: Request):
#     data = await request.json()

#     portfolio_id = id
#     name = data.get('name')
#     worth = data.get('worth')
#     action = 'remove'

#     if not name or not worth:
#         raise HTTPException(status_code=400, detail="Missing required fields")

#     remove_real_estate = RealEstate(
#         portfolio_id=portfolio_id,
#         name=name,
#         worth=worth,
#         action=action
#     )

#     db.session.add(remove_real_estate)
#     db.session.commit()
#     return {'message': 'Real estate removed successfully!'}

# @app.post('/debt/{id}')
# async def add_debt(id: int, request: Request):
#     data = await request.json()

#     portfolio_id = id
#     name = data.get('name')
#     amount = data.get('amount')
#     interest = data.get('interest')
#     action = 'add'

#     if not name or not amount:
#         raise HTTPException(status_code=400, detail="Missing required fields")

#     new_debt = Debt(
#         portfolio_id=portfolio_id,
#         name=name,
#         amount=amount,
#         interest=interest,
#         action=action
#     )

#     db.session.add(new_debt)
#     db.session.commit()
#     return {'message': 'Debt added successfully!'}

# @app.post('/remove_debt/{id}')
# async def remove_debt(id: int, request: Request):
#     data = await request.json()

#     portfolio_id = id
#     name = data.get('name')
#     amount = data.get('amount')
#     interest = data.get('interest')
#     action = 'remove'

#     if not name or not amount:
#         raise HTTPException(status_code=400, detail="Missing required fields")

#     new_debt = Debt(
#         portfolio_id=portfolio_id,
#         name=name,
#         amount=amount,
#         interest=interest,
#         action=action
#     )

#     db.session.add(new_debt)
#     db.session.commit()
#     return {'message': 'Debt removed successfully!'}
