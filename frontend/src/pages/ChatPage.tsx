import React, { useEffect, useRef, useState } from 'react';
import { chat } from '../services';
import '../styles/ChatPage.css';
import '../styles/ChatBubble.css';

interface Message {
  sender: 'user' | 'bot';
  text: string;
}

interface ConversationPreview {
  id: string;
  name: string;
  avatar?: string;
  lastMessage?: string;
}

const ChatPage: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);
  const [conversations] = useState<ConversationPreview[]>([
    { id: '1', name: 'RAG Bot', avatar: '', lastMessage: 'Ask me about your docs' },
    { id: '2', name: 'Support', avatar: '', lastMessage: 'We are here to help' },
    { id: '3', name: 'Updates', avatar: '', lastMessage: 'What is new today' },
  ]);
  const [activeConversationId, setActiveConversationId] = useState<string>('1');

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const activeConversation = conversations.find(c => c.id === activeConversationId) ?? conversations[0];

  const handleSelectConversation = (id: string) => {
    if (id === activeConversationId) return;
    setActiveConversationId(id);
    setMessages([]);
  };

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    const userMsg: Message = { sender: 'user', text: input };
    setMessages(msgs => [...msgs, userMsg]);
    setLoading(true);
    try {
      const data = await chat(input);
      setMessages(msgs => [...msgs, { sender: 'bot', text: data.answer } as Message]);
    } catch {
      setMessages(msgs => [...msgs, { sender: 'bot', text: 'Error: Could not get response.' } as Message]);
    } finally {
      setLoading(false);
      setInput('');
    }
  };

  return (
    <div className="dm-layout">
      <aside className="dm-sidebar">
        <div className="dm-sidebar-header">Messages</div>
        <div className="dm-conversations">
          {conversations.map(c => (
            <button
              key={c.id}
              className={`dm-conversation ${c.id === activeConversationId ? 'active' : ''}`}
              onClick={() => handleSelectConversation(c.id)}
            >
              <div className="dm-avatar" aria-hidden>
                {c.name.charAt(0)}
              </div>
              <div className="dm-conversation-meta">
                <div className="dm-conversation-name">{c.name}</div>
                {c.lastMessage && <div className="dm-conversation-last">{c.lastMessage}</div>}
              </div>
            </button>
          ))}
        </div>
      </aside>

      <section className="dm-chat">
        <div className="dm-chat-header">
          <div className="dm-avatar" aria-hidden>
            {activeConversation?.name.charAt(0)}
          </div>
          <div className="dm-chat-title">{activeConversation?.name}</div>
        </div>

        <div className="chat-history">
          {messages.map((msg, idx) => {
            const prev = messages[idx - 1];
            const isFirstInGroup = !prev || prev.sender !== msg.sender;
            return (
              <div
                key={idx}
                className={`dm-message-row ${msg.sender} ${isFirstInGroup ? 'new-group' : 'grouped'}`}
              >
                {msg.sender === 'bot' && isFirstInGroup && (
                  <div className="dm-avatar" aria-hidden>
                    {activeConversation?.name.charAt(0)}
                  </div>
                )}
                <div className="dm-message">
                  <div className={`chat-bubble ${msg.sender}`}>{msg.text}</div>
                </div>
              </div>
            );
          })}
          <div ref={chatEndRef} />
        </div>

        <form className="chat-input-form" onSubmit={handleSend}>
          <input
            type="text"
            placeholder="Message..."
            value={input}
            onChange={e => setInput(e.target.value)}
            disabled={loading}
          />
          <button type="submit" disabled={loading || !input.trim()}>{loading ? '...' : 'Send'}</button>
        </form>
      </section>
    </div>
  );
};

export default ChatPage; 