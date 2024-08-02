import React from 'react';
import { Link } from 'react-router-dom';

export const AccountButton: React.FC = () => {
  return (
    <form>
      <Link to="/account">
        <button>Go to Account</button>
      </Link>
    </form>
  );
};

export const LoginButton: React.FC = () => {
  return (
    <form>
      <Link to="/login">
        <button>Log In Page</button>
      </Link>
    </form>
  );
};

export const RegisterButton: React.FC = () => {
  return (
    <form>
      <Link to="/register">
        <button>Go to Register Page</button>
      </Link>
    </form>
  );
};

export const PortfolioButton: React.FC = () => {
  return (
    <form>
      <Link to="/portfolio">
        <button>Portfolio Management</button>
      </Link>
    </form>
  );
};
