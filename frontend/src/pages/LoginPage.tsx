import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { setAccessToken } from '../services/token_service';
import { useAuth } from '../contexts/AuthContext';

interface OAuthMessageData {
  access_token: string;
  id_token: string;
  userinfo: any;
  verified: boolean;
}

const LoginPage: React.FC = () => {
  const { isAuthenticated, setIsAuthenticated } = useAuth();
  const navigate = useNavigate();

  // OAuth 메시지 수신
  useEffect(() => {
    const handleMessage = (event: MessageEvent) => {
      if (event.origin !== 'http://localhost:10004') return;

      try {
        const data: OAuthMessageData = JSON.parse(event.data);
        if (data.verified) {
          setAccessToken(data.access_token);
          setIsAuthenticated(true);
        } else {
          alert('인증에 실패했습니다. 다시 시도해주세요.');
        }
      } catch (error) {
        console.error('메시지 파싱 실패:', error);
      }
    };

    window.addEventListener('message', handleMessage);
    return () => window.removeEventListener('message', handleMessage);
  }, [setIsAuthenticated]);

  // 로그인 상태 변화 감지 후 이동
  useEffect(() => {
    if (isAuthenticated) {
      alert('로그인 성공!');
      navigate('/chat');
    }
  }, [isAuthenticated, navigate]);

  const loginOauth = () => {
    const authUrlProvider = 'http://localhost:10004/api/v1/auth/login';
    window.open(authUrlProvider, 'Google Login - PANGCORN', 'width=600,height=600');
  };

  return (
    <div>
      <button onClick={loginOauth}>구글 로그인</button>
    </div>
  );
};

export default LoginPage;