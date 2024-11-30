from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional

class Users(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False, max_length=255)
    password: str = Field(nullable=False, max_length=255)
    firstname: Optional[str] = Field(default=None, max_length=255)
    lastname: Optional[str] = Field(default=None, max_length=255)
    email: Optional[str] = Field(default=None, max_length=255)
    country_id: Optional[int] = Field(default=None)

    def __repr__(self):
        return f"<User {self.username}>"

class Portfolio(SQLModel, table=True):
    portfolio_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(nullable=False, max_length=255)
    name: Optional[str] = Field(default=None, max_length=255)
    date_created: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

    def to_dict(self):
        return {
            "id": self.portfolio_id,
            "name": self.name,
            "user_id": self.user_id,
            "date_created": self.date_created
        }

    def __repr__(self):
        return f"<Portfolio {self.name}>"

class StockHoldings(SQLModel, table=True):
    transaction_id: Optional[int] = Field(default=None, primary_key=True)
    portfolio_id: int = Field(nullable=False)
    ticker: str = Field(nullable=False, max_length=255)
    amount: float = Field(nullable=False)
    price: float = Field(nullable=False)
    fees: Optional[float] = Field(default=None)
    action: str = Field(nullable=False, max_length=255)
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f"<StockHoldings {self.transaction_id}>"

class Cash(SQLModel, table=True):
    transaction_id: Optional[int] = Field(default=None, primary_key=True)
    portfolio_id: int = Field(nullable=False)
    name: Optional[str] = Field(default=None, max_length=255)
    amount: float = Field(nullable=False)
    interest: Optional[float] = Field(default=None)
    action: str = Field(nullable=False, max_length=255)
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f"<Cash {self.transaction_id}>"

class RealEstate(SQLModel, table=True):
    transaction_id: Optional[int] = Field(default=None, primary_key=True)
    portfolio_id: int = Field(nullable=False)
    name: Optional[str] = Field(default=None, max_length=255)
    worth: float = Field(nullable=False)
    action: str = Field(nullable=False, max_length=255)
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f"<RealEstate {self.transaction_id}>"

class Debt(SQLModel, table=True):
    transaction_id: Optional[int] = Field(default=None, primary_key=True)
    portfolio_id: int = Field(nullable=False)
    name: Optional[str] = Field(default=None, max_length=255)
    amount: float = Field(nullable=False)
    interest: Optional[float] = Field(default=None)
    action: str = Field(nullable=False, max_length=255)
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f"<Debt {self.transaction_id}>"
