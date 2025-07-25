import axios from 'axios';

const API_BASE_URL = 'http://localhost:10004/api';

export const login = async (username: string, password: string) => {
  const response = await axios.post(`${API_BASE_URL}/login`, { username, password });
  return response.data;
};

export const chat = async (message: string, token: string) => {
  const response = await axios.post(
    `${API_BASE_URL}/chat`,
    { message },
    { headers: { Authorization: `Bearer ${token}` } }
  );
  return response.data;
};

export const uploadDocument = async (file: File, token: string) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
}; 