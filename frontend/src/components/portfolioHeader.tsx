import React from 'react';

interface Portfolio {
  name: string;
}

interface PortfolioHeaderProps {
  portfolio: Portfolio;
}

const PortfolioHeader: React.FC<PortfolioHeaderProps> = ({ portfolio }) => {
  return (
    <div className="portfolio">
      <h2>{portfolio.name}</h2>
      {/* add elements belonging to the portfolio here */}
    </div>
  );
};

export default PortfolioHeader;
