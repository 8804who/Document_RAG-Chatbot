import React, { useState } from 'react';
import { uploadDocument } from '../services';
import { useNavigate } from 'react-router-dom';
import '../styles/DocumentUploadPage.css';

const DocumentUploadPage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState('');
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFile(e.target.files?.[0] || null);
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    setStatus('');
    try {
      const token = localStorage.getItem('access_token') || '';
      const data = await uploadDocument(file, token);
      setStatus('Upload successful!');
    } catch {
      setStatus('Upload failed.');
    } finally {
      setLoading(false);
      setFile(null);
    }
  };

  React.useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) navigate('/');
  }, []);

  return (
    <div className="upload-container">
      <form className="upload-form" onSubmit={handleUpload}>
        <h2>Upload Document</h2>
        <input type="file" accept=".pdf,.doc,.docx,.txt" onChange={handleFileChange} />
        <button type="submit" disabled={loading || !file}>{loading ? 'Uploading...' : 'Upload'}</button>
        {status && <div className="upload-status">{status}</div>}
      </form>
    </div>
  );
};

export default DocumentUploadPage; 