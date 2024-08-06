// src/services/authService.ts
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

axios.defaults.baseURL = 'http://127.0.0.1:5000';

interface LoginResponse {
  access_token: string;
  [key: string]: any; // additional properties that might be present in the response
}

interface DecodedToken {
  sub: {
    user_id: string;
  };
  [key: string]: any; // additional properties that might be present in the decoded token
}

const login = async (username: string, password: string): Promise<LoginResponse> => {
  try {
    const response = await axios.post<LoginResponse>(`/login`, { username, password });

    console.log("authService - login", response);

    if (response.data.access_token) {
      console.log("adding token to server");
      const decodedToken: DecodedToken = jwtDecode(response.data.access_token);
      console.log("decodedToken: ", decodedToken);

      localStorage.setItem('user_id', decodedToken.sub.user_id);
    }
    return response.data;
  } catch (error) {
    throw error;
  }
};

const logout = (): void => {
  console.log("authService - logout");
  localStorage.removeItem('user_id');
};

const getCurrentUser = (): string | null => {
  const user_id = localStorage.getItem('user_id');
  return user_id ? user_id : null; 
};

const getCurrentUsername = (): string | null => {
  const user_id = localStorage.getItem('username');
  return user_id ? user_id : null; 
}

const authService = {
  login,
  logout,
  getCurrentUser,
  getCurrentUsername
};

export default authService;
