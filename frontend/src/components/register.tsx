import React, { useState, ChangeEvent, FormEvent } from 'react';
import { useHistory } from 'react-router-dom';
import axios from 'axios';

interface FormData {
  firstname: string;
  lastname: string;
  country: string;
  email: string;
  username: string;
  password: string;
}

const RegisterPage: React.FC = () => {
  const history = useHistory();

  const [formData, setFormData] = useState<FormData>({
    firstname: '',
    lastname: '',
    country: '',
    email: '',
    username: '',
    password: ''
  });

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleRegister = async (e: FormEvent) => {
    e.preventDefault();
    try {
      // Set the base URL of Flask
      axios.defaults.baseURL = 'http://127.0.0.1:5000';

      const response = await axios.post('/register', formData);
      history.push('/');
      console.log(response.data);
    } catch (error) {
      console.error('There was an error!', error);
    }
  };

  return (
    <form onSubmit={handleRegister}>
      <label>
        First Name:
        <input type="text" name="firstname" value={formData.firstname} onChange={handleChange} />
      </label>
      <br />
      <label>
        Last Name:
        <input type="text" name="lastname" value={formData.lastname} onChange={handleChange} />
      </label>
      <br />
      <label>
        Country:
        <input type="text" name="country" value={formData.country} onChange={handleChange} />
      </label>
      <br />
      <label>
        Email:
        <input type="email" name="email" value={formData.email} onChange={handleChange} />
      </label>
      <br />
      <label>
        Username:
        <input type="text" name="username" value={formData.username} onChange={handleChange} />
      </label>
      <br />
      <label>
        Password:
        <input type="password" name="password" value={formData.password} onChange={handleChange} />
      </label>
      <br />
      <button type="submit">Register</button>
    </form>
  );
};

export default RegisterPage;
