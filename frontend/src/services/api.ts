import axiosInstance  from '../hooks/interceptor';

export const chat = async (message: string) => {
  const response = await axiosInstance.post(
    `/api/v1/chatbot/chat`,
    { message }
  );
  return response.data;
};

export const uploadDocument = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await axiosInstance.post(`/api/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
}; 