import React, { useState, useEffect } from 'react';
import { getDocuments, getDocumentContent, deleteDocument } from '../services';
import '../styles/DocumentsPage.css';

interface Document {
  document_id: string;
  filename: string;
  upload_date: string;
  file_size?: number;
  content_preview?: string;
}

const DocumentsPage: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedDocument, setSelectedDocument] = useState<Document | null>(null);
  const [documentContent, setDocumentContent] = useState<string>('');
  const [contentLoading, setContentLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [deleteLoading, setDeleteLoading] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      setLoading(true);
      setError('');
      const response = await getDocuments();
      setDocuments(response.documents || []);
    } catch (err) {
      setError('Failed to fetch documents. Please try again.');
      console.error('Error fetching documents:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDocumentClick = async (document: Document) => {
    try {
      setContentLoading(true);
      setSelectedDocument(document);
      const response = await getDocumentContent(document.document_id);
      setDocumentContent(response.content || '');
    } catch (err) {
      setError('Failed to fetch document content. Please try again.');
      console.error('Error fetching document content:', err);
    } finally {
      setContentLoading(false);
    }
  };

  const handleDeleteDocument = async (documentId: string, event: React.MouseEvent) => {
    event.stopPropagation();
    
    if (!window.confirm('Are you sure you want to delete this document? This action cannot be undone.')) {
      return;
    }

    try {
      setDeleteLoading(documentId);
      await deleteDocument(documentId);
      
      // Remove document from local state
      setDocuments(prev => prev.filter(doc => doc.document_id !== documentId));
      
      // Clear selected document if it was deleted
      if (selectedDocument?.document_id === documentId) {
        setSelectedDocument(null);
        setDocumentContent('');
      }
      
      setError('');
    } catch (err) {
      setError('Failed to delete document. Please try again.');
      console.error('Error deleting document:', err);
    } finally {
      setDeleteLoading(null);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatFileSize = (bytes?: number) => {
    if (!bytes) return 'Unknown size';
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
  };

  const filteredDocuments = documents.filter(doc =>
    doc.filename.toLowerCase().includes(searchTerm.toLowerCase()) ||
    doc.document_id.toLowerCase().includes(searchTerm.toLowerCase())
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
            <div className="view-toggle">
              <button
                className={`view-btn ${viewMode === 'grid' ? 'active' : ''}`}
                onClick={() => setViewMode('grid')}
                title="Grid view"
              >
                ⊞
              </button>
              <button
                className={`view-btn ${viewMode === 'list' ? 'active' : ''}`}
                onClick={() => setViewMode('list')}
                title="List view"
              >
                ☰
              </button>
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
          <div className={`documents-${viewMode}`}>
            {filteredDocuments.map((doc) => (
              <div 
                key={doc.document_id} 
                className={`document-card ${selectedDocument?.document_id === doc.document_id ? 'selected' : ''}`}
                onClick={() => handleDocumentClick(doc)}
              >
                <div className="document-header">
                  <div className="document-info">
                    <h3 className="document-filename" title={doc.filename}>
                      {doc.filename}
                    </h3>
                    <div className="document-meta">
                      <span className="document-date">{formatDate(doc.upload_date)}</span>
                      {doc.file_size && (
                        <span className="document-size">{formatFileSize(doc.file_size)}</span>
                      )}
                    </div>
                  </div>
                  <div className="document-actions">
                    <button
                      className="delete-btn"
                      onClick={(e) => handleDeleteDocument(doc.document_id, e)}
                      disabled={deleteLoading === doc.document_id}
                      title="Delete document"
                    >
                      {deleteLoading === doc.document_id ? '⏳' : '🗑️'}
                    </button>
                  </div>
                </div>
                <div className="document-id">ID: {doc.document_id}</div>
                {doc.content_preview && (
                  <div className="document-preview">
                    {doc.content_preview}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {selectedDocument && (
          <div className="document-content-panel">
            <div className="content-header">
              <div className="content-title">
                <h3>{selectedDocument.filename}</h3>
                <span className="content-meta">
                  Uploaded: {formatDate(selectedDocument.upload_date)}
                </span>
              </div>
              <button 
                className="close-button"
                onClick={() => {
                  setSelectedDocument(null);
                  setDocumentContent('');
                }}
                title="Close"
              >
                ×
              </button>
            </div>
            <div className="content-body">
              {contentLoading ? (
                <div className="loading">
                  <div className="spinner"></div>
                  <p>Loading content...</p>
                </div>
              ) : (
                <div className="document-text">
                  {documentContent || 'No content available'}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DocumentsPage;