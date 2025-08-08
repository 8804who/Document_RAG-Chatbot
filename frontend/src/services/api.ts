import axios from 'axios';

export const chat = async (message: string, token: string) => {
  const response = await axios.post(
    `/api/v1/chatbot/chat`,
    { message },
    { headers: { Authorization: `Bearer ${token}` } }
  );
  return response.data;
};

export const uploadDocument = async (file: File, token: string) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await axios.post(`/api/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
}; 