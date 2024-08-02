import React, { useEffect, useState, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import portfolioService from '../services/portfolioService.tsx';
import { Stocks, Cash, RealEstate, Debt } from './popups.tsx';
import WorthChart from "./worthChart.tsx"
import '../styles/styles.css';

const Portfolio: React.FC = () => {

  interface RouteParams {
    id: string;
    [key: string]: string | undefined;
  }

  interface StockData {
    id: number;
    ticker: string;
    amount: number;
    price: number;
  }

  interface CashData {
    name: string;
    amount: string;
    interest: number;
  }

  interface RealEstateData {
    name: string;
    worth: number;
  }

  interface DebtData {
    name: string;
    amount: number;
    interest: number;
  }

  interface PortfolioData {
    name: string;
    stocks: StockData[];
    cash: CashData[];
    real_estate: RealEstateData[];
    debt: DebtData[];
  }

  interface WorthChartData {
    stocks?: { [ticker: string]: { [date: string]: number } };
    real_estate?: { [name: string]: { [date: string]: number } };
    cash?: { [name: string]: { [date: string]: number } };
    debt?: { [name: string]: { [date: string]: number } };
  }

  interface PortfolioDataResponse {
    historical_data: WorthChartData;
    portfolio_data?: {} | null;
    message?: string;
    details?: any;
  }

  const { id } = useParams<RouteParams>(); // Get the id parameter from the URL
  const [portfolio, setPortfolio] = useState<PortfolioData>();
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // State variables to manage popup visibility
  const [isStocksOpen, setIsStocksOpen] = useState<boolean>(false);
  const [isCashOpen, setIsCashOpen] = useState<boolean>(false);
  const [isRealEstateOpen, setIsRealEstateOpen] = useState<boolean>(false);
  const [isDebtOpen, setIsDebtOpen] = useState<boolean>(false);

  // worth chart
  const [worthChartData, setWorthChartData] = useState<WorthChartData>({});
  const [chartLoading, setChartLoading] = useState<boolean>(true);
  const [chartError, setChartError] = useState<string | null>(null);

  const fetchPortfolio = useCallback(async () => {
    try {
      const data = await portfolioService.getPortfolioById(id ?? '');
      setPortfolio(data.portfolio);
    } catch (err) {
      setError((err as Error).message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  }, [id]);

  const fetchWorthChartData = useCallback(async () => {
    try {
      const chartData: PortfolioDataResponse = await portfolioService.getPortfolioChartData(id);
      setWorthChartData(chartData.historical_data);
    } catch (err) {
      setChartError((err as Error).message || 'An error occurred');
    } finally {
      setChartLoading(false);
    }
  }, [id]);

  useEffect(() => {
    fetchPortfolio();
    fetchWorthChartData();
  }, [fetchPortfolio, fetchWorthChartData]);

  const openStocksPopup = () => {
    setIsStocksOpen(true);
  };

  const openCashPopup = () => {
    setIsCashOpen(true);
  };

  const openRealEstatePopup = () => {
    setIsRealEstateOpen(true);
  };

  const openDebtPopup = () => {
    setIsDebtOpen(true);
  };

  const closePopup = async () => {
    setIsStocksOpen(false);
    setIsCashOpen(false);
    setIsRealEstateOpen(false);
    setIsDebtOpen(false);
    await fetchPortfolio(); // Re-fetch the portfolio data when a popup is closed
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!portfolio) {
    return <div>No portfolio found for id: {id}</div>;
  }

  return (
    <div className="container">
      <h1>{portfolio.name}</h1>
      <div className="sidebar">
        <div>
          <button onClick={openStocksPopup}>Stocks</button>
        </div>
        <div>
          {portfolio.stocks.map(stock => <p key={stock.id}>{stock.ticker}, ${stock.price} x {stock.amount}</p>)}
        </div>
        <div>
          <button onClick={openCashPopup}>Cash</button>
        </div>
        <div>
          {portfolio.cash.map(cash => <p key={cash.name}>{cash.name}, ${cash.amount} + {cash.interest}%</p>)}
        </div>
        <div>
          <button onClick={openRealEstatePopup}>Real Estate</button>
        </div>
        <div>
          {portfolio.real_estate.map(re => <p key={re.name}>{re.name}: ${re.worth}</p>)}
        </div>
        <div>
          <button onClick={openDebtPopup}>Debt</button>
        </div>
        <div>
          {portfolio.debt.map(debt => <p key={debt.name}>{debt.name}, ${debt.amount} + {debt.interest}%</p>)}
        </div>
        {isStocksOpen && <Stocks onClose={closePopup} />}
        {isCashOpen && <Cash onClose={closePopup} />}
        {isRealEstateOpen && <RealEstate onClose={closePopup} />}
        {isDebtOpen && <Debt onClose={closePopup} />}
      </div>
      <div className="main">
        {chartLoading ? (
          <div>Loading Chart...</div>
        ) : chartError ? (
          <div>Error: {chartError}</div>
        ) : (
          <WorthChart data={worthChartData} />
        )}
      </div>
    </div>
  );
};

export default Portfolio;
