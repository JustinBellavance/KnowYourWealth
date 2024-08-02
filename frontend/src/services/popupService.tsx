import axios from 'axios';

interface ElementResponse {
    elements?: any[];
    element?: any | null;
    message?: string;
    details?: any;
}

const addStockToPortfolio = async (portfolioId: string, ticker: string, quantity: string, price : string): Promise<ElementResponse> => {
  try {
    const response = await axios.post(`/stocks/${portfolioId}`, { ticker, quantity, price });
    console.log("response: ", response.data.message)
    return response.data.message;
  } catch (error: any) {
    if (error.response) {
      if (error.response.status === 404) {
        console.error('Portfolio not found');
        return { element : null };
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

const removeStockFromPortfolio = async (portfolioId: string, ticker: string, quantity: string, price : string): Promise<ElementResponse> => {
    try {
      const response = await axios.post(`/remove_stocks/${portfolioId}`, { ticker, quantity, price });
      console.log("response: ", response.data.message)
      return response.data.message;
    } catch (error: any) {
      if (error.response) {
        if (error.response.status === 404) {
          console.error('Portfolio not found');
          return { element : null };
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
} 

const addCashToPortfolio = async (portfolioId: string, name:string, amount:string, interest:string): Promise<ElementResponse> => {
    try {
      const response = await axios.post(`/cash/${portfolioId}`, { name, amount, interest });
      return response.data.message;
    } catch (error: any) {
      if (error.response) {
        if (error.response.status === 404) {
          console.error('Portfolio not found');
          return { element : null };
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
  
const removeCashFromPortfolio = async (portfolioId: string, name:string, amount:string, interest:string): Promise<ElementResponse> => {
      try {
        const response = await axios.post(`/remove_cash/${portfolioId}`, { name, amount, interest });
        return response.data.message;
      } catch (error: any) {
        if (error.response) {
          if (error.response.status === 404) {
            console.error('Portfolio not found');
            return { element : null };
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
} 

const addRealEstateToPortfolio = async (portfolioId: string, name:string, worth:string): Promise<ElementResponse> => {
    try {
      const response = await axios.post(`/real_estate/${portfolioId}`, { name, worth });
      return response.data.message;
    } catch (error: any) {
      if (error.response) {
        if (error.response.status === 404) {
          console.error('Portfolio not found');
          return { element : null };
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
  
const removeRealEstateFromPortfolio = async (portfolioId: string, name:string, worth:string): Promise<ElementResponse> => {
      try {
        const response = await axios.post(`/remove_real_estate/${portfolioId}`, { name, worth });
        return response.data.message;
      } catch (error: any) {
        if (error.response) {
          if (error.response.status === 404) {
            console.error('Portfolio not found');
            return { element : null };
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
} 

const addDebtToPortfolio = async (portfolioId: string, name:string, amount:string, interest:string): Promise<ElementResponse> => {
    try {
      const response = await axios.post(`/debt/${portfolioId}`, { name, amount, interest });
      return response.data.message;
    } catch (error: any) {
      if (error.response) {
        if (error.response.status === 404) {
          console.error('Portfolio not found');
          return { element : null };
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
  
const removeDebtFromPortfolio = async (portfolioId: string, name:string, amount:string, interest:string): Promise<ElementResponse> => {
  try {
    const response = await axios.post(`/remove_debt/${portfolioId}`, { name, amount, interest });
    return response.data.message;
      } catch (error: any) {
        if (error.response) {
          if (error.response.status === 404) {
            console.error('Portfolio not found');
            return { element : null };
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
} 

const popupService = {
  addStockToPortfolio,
  removeStockFromPortfolio,
  addCashToPortfolio,
  removeCashFromPortfolio,
  addRealEstateToPortfolio,
  removeRealEstateFromPortfolio,
  addDebtToPortfolio,
  removeDebtFromPortfolio
};

export default popupService;
