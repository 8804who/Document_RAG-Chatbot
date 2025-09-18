import React, { useState, useEffect } from 'react';
import { getDocuments, deleteDocument } from '../services';
import '../styles/DocumentsPage.css';

interface DocumentItem {
  document_name: string;
  document_contents: string[][];
  document_id: string;
}

const DocumentsPage: React.FC = () => {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedDocument, setSelectedDocument] = useState<DocumentItem | null>(null);
  const [error, setError] = useState<string>('');
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [selectedChunkIndex, setSelectedChunkIndex] = useState<number>(0);

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      setLoading(true);
      setError('');
      const response = await getDocuments();
      // Expecting backend to return a list like: [{ document_name, document_contents }]
      const rawList: any[] = Array.isArray(response) ? response : (response?.documents || []);
      const list: DocumentItem[] = rawList.map((item: any) => {
        const contents = item?.document_contents ?? [];
        const normalizedContents = Array.isArray(contents) && contents.length > 0 && Array.isArray(contents[0])
          ? contents
          : [Array.isArray(contents) ? contents : []];
        return {
          document_name: item.document_name,
          document_contents: normalizedContents,
          document_id: item.document_id,
        } as DocumentItem;
      });
      setDocuments(list);
      if (list.length > 0) {
        setSelectedDocument(list[0]);
        // reset chunk selection
        setSelectedChunkIndex(0);
      } else {
        setSelectedDocument(null);
        setSelectedChunkIndex(0);
      }
    } catch (err) {
      setError('Failed to fetch documents. Please try again.');
      console.error('Error fetching documents:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (doc: DocumentItem) => {
    try {
      setError('');
      await deleteDocument(doc.document_id);
      if (selectedDocument?.document_id === doc.document_id) {
        setSelectedDocument(null);
      }
      await fetchDocuments();
    } catch (err) {
      setError('Failed to delete document. Please try again.');
      console.error('Error deleting document:', err);
    }
  };

  const handleDocumentClick = (document: DocumentItem) => {
    setSelectedDocument(document);
    // reset chunk selection on new doc
    setSelectedChunkIndex(0);
  };

  const filteredDocuments = documents.filter(doc =>
    doc.document_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const clearError = () => setError('');

  const getSelectedChunkText = () => {
    if (!selectedDocument || !Array.isArray(selectedDocument.document_contents)) return '';
    const flatChunks = selectedDocument.document_contents.flat();
    if (flatChunks.length === 0) return '';
    const safeIndex = Math.min(Math.max(selectedChunkIndex, 0), flatChunks.length - 1);
    return flatChunks[safeIndex] || '';
  };

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
                    <div className="document-meta">
                      <span>{Array.isArray(doc.document_contents) ? doc.document_contents.length : 0} chunks</span>
                    </div>
                  </div>
                  <button
                    className="delete-button"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDelete(doc);
                    }}
                    title="Delete document"
                  >
                    Delete
                  </button>
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
              {Array.isArray(selectedDocument.document_contents) && selectedDocument.document_contents.flat().length > 0 ? (
                <div className="chunks-view">
                  <div className="chunks-sidebar">
                    <div className="chunk-list">
                      {selectedDocument.document_contents.flat().map((_, idx) => {
                        const active = idx === selectedChunkIndex;
                        return (
                          <button
                            key={`chunk-${idx}`}
                            className={`chunk-list-item ${active ? 'active' : ''}`}
                            onClick={() => setSelectedChunkIndex(idx)}
                            title={`Chunk ${idx + 1}`}
                          >
                            Chunk {idx + 1}
                          </button>
                        );
                      })}
                    </div>
                  </div>
                  <div className="chunk-content">
                    <div className="chunk-header">
                      Selected Chunk: {selectedChunkIndex + 1}
                    </div>
                    <div className="chunk-text">
                      {getSelectedChunkText() || 'No content available'}
                    </div>
                  </div>
                </div>
              ) : (
                <div className="document-text">No content available</div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DocumentsPage;