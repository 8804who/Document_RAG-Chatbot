import React, { useState, useEffect } from 'react';
import { getDocuments } from '../services';
import '../styles/DocumentsPage.css';

interface DocumentItem {
  document_name: string;
  document_contents: string;
}

const DocumentsPage: React.FC = () => {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedDocument, setSelectedDocument] = useState<DocumentItem | null>(null);
  const [error, setError] = useState<string>('');
  const [searchTerm, setSearchTerm] = useState<string>('');

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      setLoading(true);
      setError('');
      const response = await getDocuments();
      // Expecting backend to return a list like: [{ document_name, document_contents }]
      const list: DocumentItem[] = Array.isArray(response) ? response : (response?.documents || []);
      setDocuments(list);
      if (list.length > 0) {
        setSelectedDocument(list[0]);
      } else {
        setSelectedDocument(null);
      }
    } catch (err) {
      setError('Failed to fetch documents. Please try again.');
      console.error('Error fetching documents:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDocumentClick = (document: DocumentItem) => {
    setSelectedDocument(document);
  };

  const filteredDocuments = documents.filter(doc =>
    doc.document_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const clearError = () => setError('');

  if (loading) {
    return (
      <div className="documents-container">
        <div className="documents-shell">
          <div className="documents-title">Documents</div>
          <div className="loading">
            <div className="spinner"></div>
            <p>Loading documents...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="documents-container">
      <div className="documents-shell">
        <div className="documents-header">
          <div className="documents-title">Documents</div>
          <div className="documents-controls">
            <div className="search-box">
              <input
                type="text"
                placeholder="Search documents..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="search-input"
              />
            </div>
          </div>
        </div>
        
        {error && (
          <div className="error-message">
            <span>{error}</span>
            <button onClick={clearError} className="error-close">×</button>
          </div>
        )}
        
        {filteredDocuments.length === 0 ? (
          <div className="no-documents">
            {searchTerm ? (
              <div>
                <p>No documents found matching "{searchTerm}"</p>
                <button onClick={() => setSearchTerm('')} className="clear-search">
                  Clear search
                </button>
              </div>
            ) : (
              <div>
                <p>No documents found. Upload some documents to get started!</p>
                <button onClick={fetchDocuments} className="refresh-btn">
                  Refresh
                </button>
              </div>
            )}
          </div>
        ) : (
          <div className="documents-grid">
            {filteredDocuments.map((doc) => (
              <div 
                key={doc.document_name}
                className={`document-card ${selectedDocument?.document_name === doc.document_name ? 'selected' : ''}`}
                onClick={() => handleDocumentClick(doc)}
              >
                <div className="document-header">
                  <div className="document-info">
                    <h3 className="document-filename" title={doc.document_name}>
                      {doc.document_name}
                    </h3>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {selectedDocument && (
          <div className="document-content-panel">
            <div className="content-header">
              <div className="content-title">
                <h3>{selectedDocument.document_name}</h3>
              </div>
              <button 
                className="close-button"
                onClick={() => {
                  setSelectedDocument(null);
                }}
                title="Close"
              >
                ×
              </button>
            </div>
            <div className="content-body">
              <div className="document-text">
                {selectedDocument.document_contents || 'No content available'}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DocumentsPage;