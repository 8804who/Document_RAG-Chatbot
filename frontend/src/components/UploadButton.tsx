import React from 'react';
import '../styles/UploadButton.css';

type Props = {
  loading: boolean;
  disabled: boolean;
  onClick: () => void;
  children: React.ReactNode;
};

const UploadButton: React.FC<Props> = ({ loading, disabled, onClick, children }) => (
  <button className="upload-btn" onClick={onClick} disabled={disabled || loading} type="button">
    {loading ? 'Uploading...' : children}
  </button>
);

export default UploadButton; 