import { useCallback } from 'react';

export function useAuth() {
  const token = localStorage.getItem('access_token');
  const isAuthenticated = !!token;

  const logout = useCallback(() => {
    localStorage.removeItem('access_token');
    window.location.href = '/';
  }, []);

  return { token, isAuthenticated, logout };
} 