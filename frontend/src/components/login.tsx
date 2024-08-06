// src/components/Login.tsx
import React, { useState } from 'react';
import authService from '../services/authService.tsx';
import { useHistory } from 'react-router-dom';

const Login: React.FC = () => {
  let history = useHistory();
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [message, setMessage] = useState<string>('');

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      await authService.login(username, password);
      history.push('/');
    } catch (error) {
      console.log(error);
      setMessage('Invalid credentials');
    }
  };

  return (
    <div>
      <form onSubmit={handleLogin}>
        <div>
            <label htmlFor="username">Username</label>
            <input type="text" id="username" value={username} onChange={(e) => setUsername(e.target.value)} />
        </div>
        <div>
          <label htmlFor="password">Password</label>
          <input type="password" id="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </div>
        <button type="submit">Login</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default Login;
