import { useCallback, useState } from 'react';

export function useAuth() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const logout = useCallback(() => {
    localStorage.removeItem('access_token');
    window.location.href = '/';
  }, []);

  return { isAuthenticated, setIsAuthenticated, logout };
} 