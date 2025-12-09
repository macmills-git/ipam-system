import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Subnets from './pages/Subnets';
import IPAddresses from './pages/IPAddresses';
import Devices from './pages/Devices';
import VLANs from './pages/VLANs';
import Users from './pages/Users';
import AuditLogs from './pages/AuditLogs';
import Layout from './components/Layout';

const PrivateRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const { isAuthenticated } = useAuth();
    return isAuthenticated ? <>{children}</> : <Navigate to="/login" />;
};

function App() {
    return (
        <AuthProvider>
            <Router>
                <Routes>
                    <Route path="/login" element={<Login />} />
                    <Route path="/" element={<PrivateRoute><Layout /></PrivateRoute>}>
                        <Route index element={<Dashboard />} />
                        <Route path="subnets" element={<Subnets />} />
                        <Route path="ips" element={<IPAddresses />} />
                        <Route path="devices" element={<Devices />} />
                        <Route path="vlans" element={<VLANs />} />
                        <Route path="users" element={<Users />} />
                        <Route path="audit-logs" element={<AuditLogs />} />
                    </Route>
                </Routes>
            </Router>
        </AuthProvider>
    );
}

export default App;
