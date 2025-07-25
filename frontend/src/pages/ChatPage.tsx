import React, { useEffect, useRef, useState } from 'react';
import { chat } from '../services';
import { useNavigate } from 'react-router-dom';
import '../styles/ChatPage.css';

interface Message {
  sender: 'user' | 'bot';
  text: string;
}

const ChatPage: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);

  const navigate = useNavigate();

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    const userMsg: Message = { sender: 'user', text: input };
    setMessages(msgs => [...msgs, userMsg]);
    setLoading(true);
    try {
      const token = localStorage.getItem('access_token') || '';
      const data = await chat(input, token);
      setMessages(msgs => [...msgs, { sender: 'bot', text: data.response } as Message]);
    } catch {
      setMessages(msgs => [...msgs, { sender: 'bot', text: 'Error: Could not get response.' } as Message]);
    } finally {
      setLoading(false);
      setInput('');
    }
  };

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) navigate('/');
  }, []);

  return (
    <div className="chat-container">
      <div className="chat-header">RAG-Chatbot</div>
      <div className="chat-history">
        {messages.map((msg, idx) => (
          <div key={idx} className={`chat-bubble ${msg.sender}`}>{msg.text}</div>
        ))}
        <div ref={chatEndRef} />
      </div>
      <form className="chat-input-form" onSubmit={handleSend}>
        <input
          type="text"
          placeholder="Type your message..."
          value={input}
          onChange={e => setInput(e.target.value)}
          disabled={loading}
        />
        <button type="submit" disabled={loading || !input.trim()}>{loading ? '...' : 'Send'}</button>
      </form>
    </div>
  );
};

export default ChatPage; 