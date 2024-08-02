from flask import request, jsonify, current_app as app
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from app.models import Users, Portfolio, StockHoldings, Cash, Debt, RealEstate
from app.utils import getAllHoldingsFromPortfolio, getPortfolioHistoricalData
from app.yfinance_utils import stockIsInYF
from datetime import datetime

jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():

    data = request.get_json()
    username = data['username']
    password = data['password']
    
    user = Users.query.filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Bad username or password. Try again."}), 401
    
    access_token = create_access_token(identity={'user_id': user.user_id, 'username': user.username})
    return jsonify(access_token=access_token), 200

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    print('protected route')
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/register', methods=['POST'])
def register():
    print('register route')
    
    data = request.json
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    
    #check if users exists already
    if Users.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'User already exists'}), 409
    
    if data['country'].lower() == "canada":
        country_id = 1
    else:
        country_id = 2
        
    new_user = Users(
        username=data['username'],
        password=hashed_password,
        firstname=data['firstname'],
        lastname=data['lastname'],
        email=data['email'],
        country_id=country_id
    )
    db.session.add(new_user)
    db.session.commit()
    
    access_token = create_access_token(identity={'username': data['username']})

    return jsonify(access_token=access_token)

@app.route('/delete_user', methods=['DELETE'])
def delete():
    data = request.json
    user_to_delete = Users.query.filter_by(user_id=data['user_id'],password=data['formData']['password']).first()

    db.session.delete(user_to_delete)
    db.session.commit()
    return jsonify({"message": "User deleted successfully!"}), 200

@app.route('/add_portfolio', methods=['POST'])
def add_portfolio():

    data = request.get_json()
    
    # print(data)

    new_portfolio = Portfolio(
        user_id=data['user_id'],
        name=data['formData']['portfolio_name']
    )
    
    db.session.add(new_portfolio)
    db.session.commit()

    return jsonify({'message': 'Portfolio created successfully'}), 201

@app.route('/portfolios/<id>', methods=['GET'])
def portfolios(id):

    # need to use user_id instead of username
    portfolios = Portfolio.query.filter_by(user_id=id).all()
    
    if portfolios == []:
        return jsonify({'message': 'No portfolios found'}), 404
    
    if portfolios:
        portfolios = [portfolio.to_dict() for portfolio in portfolios]

    return jsonify({'portfolios': portfolios}), 201


@app.route('/portfolio/<id>', methods=['GET'])
def get_portfolios(id):
    
    # TODO: check if portfolio exists in database
    
    portfolio_holdings = getAllHoldingsFromPortfolio(id)
    
    if not portfolio_holdings:
        return jsonify({'message': 'Portfolio information not found'}), 404

    return jsonify({'portfolio': portfolio_holdings}), 201

@app.route('/chart_data/<portfolio_id>', methods=['GET'])
def get_chart_data(portfolio_id):
    # TODO: check if portfolio exists in database
    
    # get current date and time of the request
    # TODO: adapt to timezone of user, maybe.
    current_datetime = datetime.now()
    
    portfolio_historical_data = getPortfolioHistoricalData(portfolio_id, current_datetime)
        
    if not portfolio_historical_data:
        return jsonify({'message': "Couldn't retrieve historical data"}), 400
    
    return jsonify({'historical_data': portfolio_historical_data}), 201

# add stocks to stock holdings
@app.route('/stocks/<portfolio_id>', methods=['POST'])
def stocks(portfolio_id):
    
    data = request.json
    # print(f"data: {data}")
    
    portfolio_id = portfolio_id
    ticker = data['ticker']
    average_price = data['price']
    number_shares = data['quantity']
    action = 'add'
    
    if "fees" in data:
        fees = data['fees']
    else:
        fees = None
        
    if stockIsInYF(ticker) == False:
        return jsonify({'message': 'Stock not found in Yahoo Finance'}), 404

    new_holding = StockHoldings(
        portfolio_id=portfolio_id,
        ticker=ticker,
        price=average_price,
        amount=number_shares,
        fees=fees,
        action=action
    )

    # add stocks to stock holdings
    # add to stock_data table and stock_holdings table for the current date
    if (new_holding):
        db.session.add(new_holding)
        db.session.commit()
        return jsonify({'message': 'Stock added successfully!'}), 201
    
    return jsonify({'message': 'Stock not added'}), 400

# removee stocks from stock belonging to portfolio id
@app.route('/remove_stocks/<id>', methods=['POST'])
def remove_stocks(id):
    
    data = request.json
    # print(f"data: {data}")
    
    portfolio_id = id
    ticker = data['ticker']
    average_price = data['price']
    number_shares = data['quantity']
    action = 'remove'
    
    if "fees" in data:
        fees = data['fees']
    else:
        fees = None


    new_holding = StockHoldings(
        portfolio_id=portfolio_id,
        ticker=ticker,
        price=average_price,
        amount=number_shares,
        fees=fees,
        action=action
    )

    if (new_holding):
        db.session.add(new_holding)
        db.session.commit()
        return jsonify({'message': 'Stock sold successfully!'}), 201
    
    return jsonify({'message': 'Stock not sold'}), 400

@app.route('/cash/<id>', methods=['POST'])
def cash(id):
    
    data = request.json
    # print(f"data: {data}")
    
    portfolio_id = id
    name = data['name']
    amount = data['amount']
    interest = data['interest']
    action = 'add'

    new_cash = Cash(
        portfolio_id=portfolio_id,
        name=name,
        amount=amount,
        interest=interest,
        action=action
    )

    if (new_cash):
        db.session.add(new_cash)
        db.session.commit()
        return jsonify({'message': 'Cash added successfully!'}), 201
    
    return jsonify({'message': 'Cash not added'}), 400

@app.route('/remove_cash/<id>', methods=['POST'])
def remove_cash(id):
    
    data = request.json
    # print(f"data: {data}")
    
    portfolio_id = id
    name = data['name']
    amount = data['amount']
    interest = data['interest']
    action = 'remove'

    remove_cash = Cash(
        portfolio_id=portfolio_id,
        name=name,
        amount=amount,
        interest=interest,
        action=action
    )

    if (remove_cash):
        db.session.add(remove_cash)
        db.session.commit()
        return jsonify({'message': 'Cash removed successfully!'}), 201
    
    return jsonify({'message': 'Cash not removed'}), 400

@app.route('/real_estate/<id>', methods=['POST'])
def real_estate(id):
    
    data = request.json
    # print(f"data: {data}")
    
    portfolio_id = id
    name = data['name']
    worth = data['worth']
    action = 'add'

    new_real_estate = RealEstate(
        portfolio_id=portfolio_id,
        name=name,
        worth=worth,
        action=action
    )

    if (new_real_estate):
        db.session.add(new_real_estate)
        db.session.commit()
        return jsonify({'message': 'Real estate added successfully!'}), 201
    
    return jsonify({'message': 'Real estate not added'}), 400

@app.route('/remove_real_estate/<id>', methods=['POST'])
def remove_real_estate(id):
    
    data = request.json
    # print(f"data: {data}")
    
    portfolio_id = id
    name = data['name']
    worth = data['worth']
    action = 'remove'

    remove_real_estate = RealEstate(
        portfolio_id=portfolio_id,
        name=name,
        worth=worth,
        action=action
    )

    if (remove_real_estate):
        db.session.add(remove_real_estate)
        db.session.commit()
        return jsonify({'message': 'Real estate removed successfully!'}), 201
    
    return jsonify({'message': 'Real estate not removed'}), 400

@app.route('/debt/<id>', methods=['POST'])
def debt(id):
    
    data = request.json
    # print(f"data: {data}")
    
    portfolio_id = id
    name = data['name']
    amount = data['amount']
    interest = data['interest']
    action = 'add'

    new_debt = Debt(
        portfolio_id=portfolio_id,
        name=name,
        amount=amount,
        interest=interest,
        action=action
    )

    if (new_debt):
        db.session.add(new_debt)
        db.session.commit()
        return jsonify({'message': 'Debt added successfully!'}), 201
    
    return jsonify({'message': 'Debt not added'}), 400

@app.route('/remove_debt/<id>', methods=['POST'])
def remove_debt(id):
    
    data = request.json
    # print(f"data: {data}")
    
    portfolio_id = id
    name = data['name']
    amount = data['amount']
    interest = data['interest']
    action = 'remove'

    new_debt = Debt(
        portfolio_id=portfolio_id,
        name=name,
        amount=amount,
        interest=interest,
        action=action
    )

    if (new_debt):
        db.session.add(new_debt)
        db.session.commit()
        return jsonify({'message': 'Debt removed successfully!'}), 201
    
    return jsonify({'message': 'Debt not removed'}), 400
