import axiosInstance  from '../hooks/interceptor';

export const chat = async (message: string, token: string) => {
  const response = await axiosInstance.post(
    `/api/v1/chatbot/chat`,
    { message },
    { headers: { Authorization: `Bearer ${token}` } }
  );
  return response.data;
};

export const uploadDocument = async (file: File, token: string) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await axiosInstance.post(`/api/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
}; 