import axios, { AxiosError, AxiosRequestConfig, AxiosResponse, InternalAxiosRequestConfig } from 'axios';
import { getAccessToken, setAccessToken, removeAccessToken } from '../services/token_service';

// axios 인스턴스 생성
const api = axios.create({
  baseURL: 'http://localhost:10004/api/v1',
  timeout: 10000,
  withCredentials: true, // 모든 요청에 쿠키 포함 (refresh token이 쿠키에 있는 경우)
});

// 요청 인터셉터: access_token 자동 삽입
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = getAccessToken();
    if (token && config.headers) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

let isRefreshing = false;
let failedQueue: Array<{
  resolve: (value?: unknown) => void;
  reject: (error: any) => void;
}> = [];

const processQueue = (error: any, token: string | null = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
};

// 응답 인터셉터: 401 발생 시 토큰 갱신 처리
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };
    
    if (error.response?.status === 401 && !originalRequest?._retry) {
      if (isRefreshing) {
        // 토큰 갱신 중이면 큐에 넣고 대기
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then((token) => {
            if (originalRequest?.headers) {
              originalRequest.headers['Authorization'] = `Bearer ${token}`;
            }
            return api(originalRequest);
          })
          .catch((err) => Promise.reject(err));
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        // 토큰 갱신 요청 (refresh token은 백엔드에서 관리)
        const response = await axios.post('http://localhost:10004/api/v1/auth/refresh', {}, {
          withCredentials: true, // 쿠키를 포함하여 요청 (refresh token이 쿠키에 있는 경우)
        });
        
        const newAccessToken = response.data.access_token;
        setAccessToken(newAccessToken);
        
        if (originalRequest?.headers) {
          originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
        }
        
        processQueue(null, newAccessToken);
        return api(originalRequest);
      } catch (err) {
        processQueue(err, null);
        removeAccessToken();
        
        // 브라우저 환경에서만 실행
        if (typeof window !== 'undefined') {
          window.location.href = '/login'; // 로그인 페이지 경로 수정
        }
        
        return Promise.reject(err);
      } finally {
        isRefreshing = false;
      }
    }
    
    return Promise.reject(error);
  }
);

export default api;