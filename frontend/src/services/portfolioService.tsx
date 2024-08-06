import axios from 'axios';
import authService from './authService.tsx';

interface PortfoliosResponse {
  portfolios?: any[] | null;
  message?: string;
  details?: any;
}

interface PortfolioResponse {
  portfolio?: any | null;
  message?: string;
  details?: any;
}

interface StocksResponse {
  stocks?: any[] | null;
  message?: string;
  details?: any;
}

interface DebtResponse {
  debt?: any[] | null;
  message?: string;
  details?: any;
}

interface RealEstateResponse {
  real_estate?: any[] | null;
  message?: string;
  details?: any;
}

interface CashResponse {
  cash?: any | null;
  message?: string;
  details?: any;
}

interface PortfolioDataResponse {
  historical_data: WorthChartData;
  portfolio_data?: {} | null;
  message?: string;
  details?: any;
}

interface WorthChartData {
  stocks?: { [ticker: string]: { [date: string]: number } };
  real_estate?: { [name: string]: { [date: string]: number } };
  cash?: { [name: string]: { [date: string]: number } };
  debt?: { [name: string]: { [date: string]: number } };
}

const getPortfolios = async (): Promise<PortfoliosResponse> => {
  const user_id: string | null = authService.getCurrentUser();

  try {
    const response = await axios.get(`/portfolios/${user_id}`);
    console.log("response: ", response);
    return response.data;
  } catch (error: any) {
    if (error.response) {
      if (error.response.status === 404) {
        console.error('No portfolios found');
        return { portfolios: [] };
      } else {
        console.error('An error occurred:', error.response.data);
        return { message: 'An error occurred', details: error.response.data };
      }
    } else if (error.request) {
      console.error('No response received:', error.request);
      return { message: 'No response received' };
    } else {
      console.error('Error:', error.message);
      return { message: 'An error occurred', details: error.message };
    }
  }
};

const getPortfolioById = async (portfolioId: string): Promise<PortfolioResponse> => {
  try {
    const response = await axios.get(`/portfolio/${portfolioId}`);
    return response.data;
  } catch (error: any) {
    if (error.response) {
      if (error.response.status === 404) {
        console.error('Portfolio not found');
        return { portfolio: null };
      } else {
        console.error('An error occurred:', error.response.data);
        return { message: 'An error occurred', details: error.response.data };
      }
    } else if (error.request) {
      console.error('No response received:', error.request);
      return { message: 'No response received' };
    } else {
      console.error('Error:', error.message);
      return { message: 'An error occurred', details: error.message };
    }
  }
};

const getStocksFromPortfolio = async (portfolioId: string): Promise<StocksResponse> => {

  try {
    const response = await axios.get(`/stocks/${portfolioId}`);
    console.log("response: ", response);
    return response.data;
  } catch (error: any) {
    if (error.response) {
      if (error.response.status === 404) {
        console.error('No portfolios found');
        return { stocks: [] };
      } else {
        console.error('An error occurred:', error.response.data);
        return { message: 'An error occurred', details: error.response.data };
      }
    } else if (error.request) {
      console.error('No response received:', error.request);
      return { message: 'No response received' };
    } else {
      console.error('Error:', error.message);
      return { message: 'An error occurred', details: error.message };
    }
  }
};

const getDebtFromPortfolio = async (portfolioId: string): Promise<DebtResponse> => {

  try {
    const response = await axios.get(`/debt/${portfolioId}`);
    console.log("response: ", response);
    return response.data;
  } catch (error: any) {
    if (error.response) {
      if (error.response.status === 404) {
        console.error('No stocks found');
        return { debt: [] };
      } else {
        console.error('An error occurred:', error.response.data);
        return { message: 'An error occurred', details: error.response.data };
      }
    } else if (error.request) {
      console.error('No response received:', error.request);
      return { message: 'No response received' };
    } else {
      console.error('Error:', error.message);
      return { message: 'An error occurred', details: error.message };
    }
  }
};

const getRealEstateFromPortfolio = async (portfolioId: string): Promise<RealEstateResponse> => {

  try {
    const response = await axios.get(`/real_estate/${portfolioId}`);
    console.log("response: ", response);
    return response.data;
  } catch (error: any) {
    if (error.response) {
      if (error.response.status === 404) {
        console.error('No portfolios found');
        return { real_estate: [] };
      } else {
        console.error('An error occurred:', error.response.data);
        return { message: 'An error occurred', details: error.response.data };
      }
    } else if (error.request) {
      console.error('No response received:', error.request);
      return { message: 'No response received' };
    } else {
      console.error('Error:', error.message);
      return { message: 'An error occurred', details: error.message };
    }
  }
};

const getCashFromPortfolio = async (portfolioId: string): Promise<CashResponse> => {
  try {
    const response = await axios.get(`/cash/${portfolioId}`);
    console.log("response: ", response);
    return response.data;
  } catch (error: any) {
    if (error.response) {
      if (error.response.status === 404) {
        console.error('No portfolios found');
        return { cash: [] };
      } else {
        console.error('An error occurred:', error.response.data);
        return { message: 'An error occurred', details: error.response.data };
      }
    } else if (error.request) {
      console.error('No response received:', error.request);
      return { message: 'No response received' };
    } else {
      console.error('Error:', error.message);
      return { message: 'An error occurred', details: error.message };
    }
  }
};

const getPortfolioData = async (portfolioId: string): Promise<PortfolioDataResponse> => {

  try {
    const response = await axios.get(`/portfolio_data/${portfolioId}`);
    console.log("response: ", response);
    return response.data;
  } catch (error: any) {
    if (error.response) {
      if (error.response.status === 404) {
        console.error('No portfolios found');
        return { portfolio_data: [] };
      } else {
        console.error('An error occurred:', error.response.data);
        return { message: 'An error occurred', details: error.response.data };
      }
    } else if (error.request) {
      console.error('No response received:', error.request);
      return { message: 'No response received' };
    } else {
      console.error('Error:', error.message);
      return { message: 'An error occurred', details: error.message };
    }
  }
};

const getPortfolioChartData = async (portfolioId: string): Promise<PortfolioDataResponse> => {

  try {
    const response = await axios.get(`/chart_data/${portfolioId}`);
    console.log("response: ", response);
    return response.data;
  } catch (error: any) {
    if (error.response) {
      if (error.response.status === 404) {
        console.error('No portfolios found');
        return { portfolio_data: [] };
      } else {
        console.error('An error occurred:', error.response.data);
        return { message: 'An error occurred', details: error.response.data };
      }
    } else if (error.request) {
      console.error('No response received:', error.request);
      return { message: 'No response received' };
    } else {
      console.error('Error:', error.message);
      return { message: 'An error occurred', details: error.message };
    }
  }
};

const portfolioService = {
  getPortfolios,
  getPortfolioById,
  getStocksFromPortfolio,
  getDebtFromPortfolio,
  getRealEstateFromPortfolio,
  getCashFromPortfolio,
  getPortfolioData,
  getPortfolioChartData
};

export default portfolioService;
