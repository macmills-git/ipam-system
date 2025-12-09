import React, { useEffect, useState } from 'react';
import { apiClient } from '../services/api';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement } from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement);

const Dashboard: React.FC = () => {
    const [stats, setStats] = useState<any>(null);
    const [subnets, setSubnets] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        setLoading(true);
        try {
            const [subnetsRes, ipsRes] = await Promise.all([
                apiClient.get('/subnets'),
                apiClient.get('/ips')
            ]);

            setSubnets(subnetsRes.data);

            const ipStats = ipsRes.data.reduce((acc: any, ip: any) => {
                acc[ip.status] = (acc[ip.status] || 0) + 1;
                return acc;
            }, {});

            setStats(ipStats);
        } catch (error: any) {
            console.error('Failed to load dashboard data', error);
            // Use mock data if backend is not available
            if (error.code === 'ERR_NETWORK' || error.message?.includes('Network Error')) {
                const { mockSubnets, mockIPs } = await import('../services/mockApi');
                setSubnets(mockSubnets);
                const ipStats = mockIPs.reduce((acc: any, ip: any) => {
                    acc[ip.status] = (acc[ip.status] || 0) + 1;
                    return acc;
                }, {});
                setStats(ipStats);
            }
        } finally {
            setLoading(false);
        }
    };

    const barData = stats ? {
        labels: Object.keys(stats).map(key => key.charAt(0).toUpperCase() + key.slice(1)),
        datasets: [{
            label: 'IP Count',
            data: Object.values(stats),
            backgroundColor: [
                '#10b981', // green for free
                '#3b82f6', // blue for assigned
                '#f59e0b', // yellow for reserved
                '#ef4444'  // red for quarantined
            ],
            borderColor: [
                '#059669',
                '#2563eb',
                '#d97706',
                '#dc2626'
            ],
            borderWidth: 1
        }]
    } : null;

    const barOptions = {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: {
                display: false
            },
            title: {
                display: false
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    stepSize: 1
                }
            }
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center py-12">
                <div className="text-center">
                    <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                    <p className="mt-4 text-gray-600">Loading dashboard...</p>
                </div>
            </div>
        );
    }

    return (
        <div>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
                <div className="bg-white p-6 rounded-lg shadow">
                    <h3 className="text-gray-500 text-sm">Total Subnets</h3>
                    <p className="text-3xl font-bold">{subnets.length}</p>
                </div>
                <div className="bg-white p-6 rounded-lg shadow">
                    <h3 className="text-gray-500 text-sm">Free IPs</h3>
                    <p className="text-3xl font-bold text-green-600">{stats?.free || 0}</p>
                </div>
                <div className="bg-white p-6 rounded-lg shadow">
                    <h3 className="text-gray-500 text-sm">Assigned IPs</h3>
                    <p className="text-3xl font-bold text-blue-600">{stats?.assigned || 0}</p>
                </div>
                <div className="bg-white p-6 rounded-lg shadow">
                    <h3 className="text-gray-500 text-sm">Quarantined IPs</h3>
                    <p className="text-3xl font-bold text-red-600">{stats?.quarantined || 0}</p>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div className="bg-white p-6 rounded-lg shadow">
                    <h2 className="text-xl font-bold mb-4">IP Status Distribution</h2>
                    {barData && (
                        <>
                            <Bar data={barData} options={barOptions} />
                            <div className="mt-4 grid grid-cols-2 gap-2">
                                {Object.entries(stats).map(([status, count]: [string, any]) => (
                                    <div key={status} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                                        <span className="text-sm font-medium capitalize">{status}:</span>
                                        <span className="text-sm font-bold">{count}</span>
                                    </div>
                                ))}
                            </div>
                        </>
                    )}
                </div>

                <div className="bg-white p-6 rounded-lg shadow">
                    <h2 className="text-xl font-bold mb-4">Recent Subnets</h2>
                    <div className="space-y-3">
                        {subnets.slice(0, 5).map((subnet: any) => (
                            <div key={subnet.id} className="border-l-4 border-blue-500 pl-3 py-2 bg-gray-50 rounded">
                                <p className="font-semibold font-mono text-blue-600">{subnet.cidr}</p>
                                <p className="text-sm text-gray-600">{subnet.description}</p>
                                {subnet.location && (
                                    <p className="text-xs text-gray-500 mt-1">📍 {subnet.location}</p>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
