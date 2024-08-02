import React, { useState, ChangeEvent, FormEvent } from 'react';
import axios from 'axios';
import authService from '../services/authService.tsx';
import { useHistory } from 'react-router-dom';

interface FormData {
  username: string;
  password: string;
  portfolio_name?: string;
}

const AccountPage: React.FC = () => {
  const user_id: string | null = authService.getCurrentUser();
  const username: string | null = authService.getCurrentUsername();

  const [formData, setFormData] = useState<FormData>({
    username: '',
    password: ''
  });

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const deleteUser = async (e: FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post('/delete_user', { formData, user_id });
      console.log(response.data);
    } catch (error) {
      console.error('There was an error!', error);
    }
  };

  const createPortfolio = async (e: FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post('/add_portfolio', { formData, user_id });
      console.log(response.data);
    } catch (error) {
      console.error('There was an error!', error);
    }
  };

  const [message, setMessage] = useState<string>('');
  const history = useHistory();

  const handleLogout = async (e: FormEvent) => {
    e.preventDefault();
    try {
      await authService.logout();
      history.push('/');
    } catch (error) {
      setMessage('Could not log out user. Please try again.');
    }
  };

  return (
    <div>
      <h1>Account Page</h1>
      <br></br>
      <h1>Username: {username}</h1>
      <form onSubmit={createPortfolio}>
        <label>
          <h2>Create a new portfolio</h2>
          Name:
          <input
            type="text"
            name="portfolio_name"
            value={formData.portfolio_name || ''}
            onChange={handleChange}
          />
        </label>
        <br />
        <button type="submit">Create Portfolio</button>
      </form>
      <br />
      <form onSubmit={deleteUser}>
        <h2>Delete your account</h2>
        <label>
          Password:
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
          />
        </label>
        <br />
        <button type="submit">Delete Account</button>
      </form>
      <br />
      <form>
        <button onClick={handleLogout}>Log Out</button>
        {message && <p>{message}</p>}
      </form>
    </div>
  );
};

export default AccountPage;
