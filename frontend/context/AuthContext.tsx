"use client";

import React, { createContext, useState, useContext, useEffect } from "react";

interface AuthContextType {
  token: string | null;
  user: string | null;
  setToken: (token: string | null) => void;
  setUser: (user: string | null) => void;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType>({
  token: null,
  user: null,
  setToken: () => {},
  setUser: () => {},
  logout: () => {},
  isAuthenticated: false,
});

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [token, setTokenState] = useState<string | null>(null);
  const [user, setUserState] = useState<string | null>(null);
  const [isLoaded, setIsLoaded] = useState(false);

  // Load token and user from localStorage on mount
  useEffect(() => {
    try {
      const savedToken = localStorage.getItem('authToken');
      const savedUser = localStorage.getItem('authUser');
      
      if (savedToken) {
        // Check if token is expired
        const payload = JSON.parse(atob(savedToken.split('.')[1]));
        const currentTime = Date.now() / 1000;
        
        if (payload.exp && payload.exp > currentTime) {
          setTokenState(savedToken);
          setUserState(savedUser);
        } else {
          // Token is expired, clear it
          localStorage.removeItem('authToken');
          localStorage.removeItem('authUser');
        }
      }
    } catch (error) {
      console.error('Error loading auth state:', error);
      localStorage.removeItem('authToken');
      localStorage.removeItem('authUser');
    } finally {
      setIsLoaded(true);
    }
  }, []);

  const setToken = (newToken: string | null) => {
    setTokenState(newToken);
    if (newToken) {
      localStorage.setItem('authToken', newToken);
    } else {
      localStorage.removeItem('authToken');
    }
  };

  const setUser = (newUser: string | null) => {
    setUserState(newUser);
    if (newUser) {
      localStorage.setItem('authUser', newUser);
    } else {
      localStorage.removeItem('authUser');
    }
  };

  const logout = () => {
    setTokenState(null);
    setUserState(null);
    localStorage.removeItem('authToken');
    localStorage.removeItem('authUser');
  };

  const isAuthenticated = !!token;

  // Don't render children until we've loaded the auth state
  if (!isLoaded) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white'
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{
            width: '40px',
            height: '40px',
            border: '3px solid rgba(255,255,255,0.3)',
            borderTop: '3px solid white',
            borderRadius: '50%',
            animation: 'spin 1s linear infinite',
            margin: '0 auto 20px'
          }}></div>
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <AuthContext.Provider value={{ 
      token, 
      user, 
      setToken, 
      setUser, 
      logout, 
      isAuthenticated 
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
