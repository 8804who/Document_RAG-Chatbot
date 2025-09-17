import React, { useState, useEffect } from 'react';
import { getDocuments } from '../services';
import '../styles/DocumentsPage.css';

interface DocumentItem {
  document_name: string;
  document_contents: string[][];
}

const DocumentsPage: React.FC = () => {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedDocument, setSelectedDocument] = useState<DocumentItem | null>(null);
  const [error, setError] = useState<string>('');
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [selectedChunkGroupIndex, setSelectedChunkGroupIndex] = useState<number>(0);
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
      const list: DocumentItem[] = Array.isArray(response) ? response : (response?.documents || []);
      setDocuments(list);
      if (list.length > 0) {
        setSelectedDocument(list[0]);
        // reset chunk selection
        const first = list[0];
        const hasGroups = Array.isArray(first.document_contents) && first.document_contents.length > 0;
        const firstGroupLen = hasGroups && Array.isArray(first.document_contents[0]) ? first.document_contents[0].length : 0;
        setSelectedChunkGroupIndex(0);
        setSelectedChunkIndex(0);
        if (!firstGroupLen) {
          setSelectedChunkIndex(0);
        }
      } else {
        setSelectedDocument(null);
        setSelectedChunkGroupIndex(0);
        setSelectedChunkIndex(0);
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
    // reset chunk selection on new doc
    setSelectedChunkGroupIndex(0);
    setSelectedChunkIndex(0);
  };

  const filteredDocuments = documents.filter(doc =>
    doc.document_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const clearError = () => setError('');

  const getSelectedChunkText = () => {
    if (!selectedDocument || !Array.isArray(selectedDocument.document_contents)) return '';
    const groups = selectedDocument.document_contents;
    if (groups.length === 0) return '';
    const safeGroupIndex = Math.min(Math.max(selectedChunkGroupIndex, 0), groups.length - 1);
    const group = groups[safeGroupIndex] || [];
    const safeChunkIndex = Math.min(Math.max(selectedChunkIndex, 0), Math.max(group.length - 1, 0));
    const text = group[safeChunkIndex] || '';
    return text;
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
              {Array.isArray(selectedDocument.document_contents) && selectedDocument.document_contents.length > 0 ? (
                <div className="chunks-view">
                  <div className="chunks-sidebar">
                    {selectedDocument.document_contents.map((chunkGroup, groupIndex) => (
                      <div className="chunk-group" key={`chunk-group-${groupIndex}`}>
                        <div className="chunk-group-title">Group {groupIndex + 1}</div>
                        <div className="chunk-list">
                          {Array.isArray(chunkGroup) && chunkGroup.map((_, chunkIndex) => {
                            const active = groupIndex === selectedChunkGroupIndex && chunkIndex === selectedChunkIndex;
                            return (
                              <button
                                key={`chunk-${groupIndex}-${chunkIndex}`}
                                className={`chunk-list-item ${active ? 'active' : ''}`}
                                onClick={() => {
                                  setSelectedChunkGroupIndex(groupIndex);
                                  setSelectedChunkIndex(chunkIndex);
                                }}
                                title={`Chunk ${groupIndex + 1}${chunkGroup.length > 1 ? `.${chunkIndex + 1}` : ''}`}
                              >
                                Chunk {groupIndex + 1}{chunkGroup.length > 1 ? `.${chunkIndex + 1}` : ''}
                              </button>
                            );
                          })}
                        </div>
                      </div>
                    ))}
                  </div>
                  <div className="chunk-content">
                    <div className="chunk-header">
                      Selected Chunk: {selectedChunkGroupIndex + 1}{(selectedDocument.document_contents[selectedChunkGroupIndex]?.length || 0) > 1 ? `.${selectedChunkIndex + 1}` : ''}
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