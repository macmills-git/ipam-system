import React, { useState } from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Layout: React.FC = () => {
    const { user, logout } = useAuth();
    const location = useLocation();
    const [sidebarOpen, setSidebarOpen] = useState(true);

    const isActive = (path: string) => {
        return location.pathname === path;
    };

    const navItems = [
        { path: '/', label: 'Dashboard', icon: '📊' },
        { path: '/subnets', label: 'Subnets', icon: '🌐' },
        { path: '/ips', label: 'IP Addresses', icon: '🔢' },
        { path: '/devices', label: 'Devices', icon: '💻' },
        { path: '/vlans', label: 'VLANs', icon: '🔀' },
    ];

    if (user?.role === 'admin' || user?.role === 'auditor') {
        navItems.push({ path: '/audit-logs', label: 'Audit Logs', icon: '📋' });
    }

    if (user?.role === 'admin') {
        navItems.push({ path: '/users', label: 'Users', icon: '👥' });
    }

    return (
        <div className="flex h-screen bg-gray-100">
            {/* Sidebar - Light Theme */}
            <aside
                className={`${sidebarOpen ? 'w-64' : 'w-20'
                    } bg-white border-r border-gray-200 shadow-lg transition-all duration-300 flex flex-col`}
            >
                {/* Logo/Header */}
                <div className="p-4 border-b border-gray-200">
                    <div className="flex items-center justify-between">
                        {sidebarOpen ? (
                            <h1 className="text-2xl font-bold text-blue-600">IPAM System</h1>
                        ) : (
                            <h1 className="text-2xl font-bold text-blue-600">IP</h1>
                        )}
                        <button
                            onClick={() => setSidebarOpen(!sidebarOpen)}
                            className="text-gray-500 hover:text-gray-700 focus:outline-none"
                        >
                            {sidebarOpen ? '◀' : '▶'}
                        </button>
                    </div>
                </div>

                {/* Navigation */}
                <nav className="flex-1 overflow-y-auto py-4">
                    {navItems.map((item) => (
                        <Link
                            key={item.path}
                            to={item.path}
                            className={`flex items-center px-4 py-3 transition-colors ${isActive(item.path)
                                    ? 'bg-blue-50 text-blue-600 border-l-4 border-blue-600 font-semibold'
                                    : 'text-gray-700 hover:bg-gray-50 hover:text-blue-600'
                                }`}
                        >
                            <span className="text-2xl">{item.icon}</span>
                            {sidebarOpen && <span className="ml-3">{item.label}</span>}
                        </Link>
                    ))}
                </nav>

                {/* User Info */}
                <div className="border-t border-gray-200 p-4 bg-gray-50">
                    {sidebarOpen ? (
                        <div>
                            <div className="flex items-center mb-3">
                                <div className="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold">
                                    {user?.username?.charAt(0).toUpperCase()}
                                </div>
                                <div className="ml-3">
                                    <p className="text-sm font-medium text-gray-900">{user?.username}</p>
                                    <p className="text-xs text-gray-500 capitalize">{user?.role?.replace('_', ' ')}</p>
                                </div>
                            </div>
                            <button
                                onClick={logout}
                                className="w-full bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded transition-colors"
                            >
                                Logout
                            </button>
                        </div>
                    ) : (
                        <button
                            onClick={logout}
                            className="w-full text-red-600 hover:text-red-700 text-2xl"
                            title="Logout"
                        >
                            🚪
                        </button>
                    )}
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 overflow-y-auto">
                {/* Top Bar */}
                <div className="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
                    <div className="flex items-center justify-between">
                        <h2 className="text-2xl font-semibold text-gray-800">
                            {navItems.find(item => item.path === location.pathname)?.label || 'Dashboard'}
                        </h2>
                        <div className="flex items-center space-x-4">
                            <span className="text-sm text-gray-600">
                                Welcome, <span className="font-semibold">{user?.username}</span>
                            </span>
                        </div>
                    </div>
                </div>

                {/* Page Content */}
                <div className="p-6">
                    <Outlet />
                </div>
            </main>
        </div>
    );
};

export default Layout;
