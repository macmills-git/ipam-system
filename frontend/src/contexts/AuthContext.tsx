import React, { createContext, useContext, useState, useEffect } from 'react';
import { apiClient } from '../services/api';

interface User {
    id: number;
    username: string;
    email: string;
    role: string;
}

interface AuthContextType {
    user: User | null;
    isAuthenticated: boolean;
    login: (email: string, password: string) => Promise<void>;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        const token = localStorage.getItem('access_token');
        if (token) {
            apiClient.get('/auth/me').then(response => {
                setUser(response.data);
                setIsAuthenticated(true);
            }).catch(() => {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
            });
        }
    }, []);

    const login = async (email: string, password: string) => {
        try {
            const response = await apiClient.post('/auth/login', { email, password });
            localStorage.setItem('access_token', response.data.access_token);
            localStorage.setItem('refresh_token', response.data.refresh_token);

            const userResponse = await apiClient.get('/auth/me');
            setUser(userResponse.data);
            setIsAuthenticated(true);
        } catch (error: any) {
            // Fallback to mock data if backend is not available
            if (error.code === 'ERR_NETWORK' || error.message?.includes('Network Error')) {
                console.warn('Backend not available, using mock data');
                const { mockLogin, mockUser } = await import('../services/mockApi');
                const tokens = mockLogin(email, password);
                localStorage.setItem('access_token', tokens.access_token);
                localStorage.setItem('refresh_token', tokens.refresh_token);
                setUser(mockUser as any);
                setIsAuthenticated(true);
            } else {
                throw error;
            }
        }
    };

    const logout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setUser(null);
        setIsAuthenticated(false);
    };

    return (
        <AuthContext.Provider value={{ user, isAuthenticated, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) throw new Error('useAuth must be used within AuthProvider');
    return context;
};
