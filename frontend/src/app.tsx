import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

// Services
import authService from './services/authService.tsx';

// Components
import { RegisterButton, LoginButton, AccountButton, PortfolioButton } from './components/buttons.tsx';
import Register from './components/register.tsx';
import Account from './components/account.tsx';
import Login from './components/login.tsx';
import PortfolioPage from './components/portfolioPage.tsx';
import Portfolio from './components/portfolio.tsx';

const App: React.FC = () => {
  const user: string | null = authService.getCurrentUser();
  let isLoggedIn = false;
  if (user && user !== "null" && user !== "undefined" && user !== "") {
    isLoggedIn = true;
  }

  return (
    <Router>
      <Switch>
        <Route path="/register" component={Register} />
        <Route path="/login" component={Login} />
        <Route path="/account" component={Account} />
        <Route exact path="/portfolio" component={PortfolioPage} />
        <Route exact path="/">
          {isLoggedIn ? 
            <>
              <AccountButton />
              <PortfolioButton />
            </>
            : (
              <>
                <RegisterButton />
                <LoginButton />
              </>
            )}
        </Route>
        <Route exact path="/portfolio/:id">
          <Portfolio />
        </Route>
      </Switch>
    </Router>
  );
};

export default App;
