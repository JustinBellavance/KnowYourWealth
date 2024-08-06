import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import portfolioService from '../services/portfolioService.tsx';
import PortfolioHeader from './portfolioHeader.tsx';
import '../styles/styles.css';

interface Portfolio {
  id: string;
  name: string;
  [key: string]: any; 
}

const PortfolioPage: React.FC = () => {
  const [portfolios, setPortfolios] = useState<Portfolio[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPortfolios = async () => {
      try {
        const data = await portfolioService.getPortfolios();
        setPortfolios(data.portfolios || []);
      } catch (err) {
        setError((err as Error).message || 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchPortfolios();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      <h1>My Portfolios</h1>
      <form>
        {portfolios.length === 0 ? (
          <p>No portfolios found</p>
        ) : (
          <div>
            {portfolios.map((portfolio, i) => (
              <div className="portfolio-container" key={portfolio.id}>
                <Link to={`/portfolio/${portfolio.id}`}>
                  <div className="portfolio-item">
                    <h2>{i + 1}</h2>
                    <div className="portfolio-element">
                      <PortfolioHeader portfolio={portfolio} />
                    </div>
                  </div>
                </Link>
              </div>
            ))}
          </div>
        )}
      </form>
    </div>
  );
};

export default PortfolioPage;
