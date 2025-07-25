import React from 'react';
import '../styles/ChatBubble.css';

type Props = {
  sender: 'user' | 'bot';
  text: string;
};

const ChatBubble: React.FC<Props> = ({ sender, text }) => (
  <div className={`chat-bubble ${sender}`}>{text}</div>
);

export default ChatBubble; 