import axiosInstance  from '../hooks/interceptor';

export const chat = async (message: string) => {
  const response = await axiosInstance.post(
    `/api/v1/chatbot/chat`,
    { message }
  );
  return response.data;
};

export const uploadDocument = async (document: File) => {
  const formData = new FormData();
  formData.append('document', document);
  
  const response = await axiosInstance.post(`/api/v1/documents/user`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getDocuments = async () => {
  const response = await axiosInstance.get('/api/v1/documents/user');
  return response.data;
};

export const getDocumentContent = async (documentId: string) => {
  const response = await axiosInstance.get(`/api/v1/documents/user/${documentId}`);
  return response.data;
};

export const deleteDocument = async (documentId: string) => {
  const response = await axiosInstance.delete(`/api/v1/documents/user/${documentId}`);
  return response.data;
}; 