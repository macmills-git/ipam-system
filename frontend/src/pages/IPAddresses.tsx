import React, { useEffect, useState } from 'react';
import { apiClient } from '../services/api';

const IPAddresses: React.FC = () => {
    const [ips, setIps] = useState<any[]>([]);
    const [subnets, setSubnets] = useState<any[]>([]);
    const [filter, setFilter] = useState({ subnet_id: '', status: '', hostname: '' });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        setLoading(true);
        try {
            const [ipsRes, subnetsRes] = await Promise.all([
                apiClient.get('/ips'),
                apiClient.get('/subnets')
            ]);
            setIps(ipsRes.data);
            setSubnets(subnetsRes.data);
        } catch (error: any) {
            console.error('Failed to load data', error);
            // Use mock data if backend is not available
            if (error.code === 'ERR_NETWORK' || error.message?.includes('Network Error')) {
                const { mockIPs, mockSubnets } = await import('../services/mockApi');
                setIps(mockIPs);
                setSubnets(mockSubnets);
            }
        } finally {
            setLoading(false);
        }
    };

    const allocateIP = async () => {
        const subnetId = prompt('Enter Subnet ID:');
        if (subnetId) {
            try {
                await apiClient.post('/ips/allocate', { subnet_id: parseInt(subnetId), count: 1 });
                loadData();
            } catch (error: any) {
                alert(error.response?.data?.detail || 'Failed to allocate IP');
            }
        }
    };

    const filteredIps = ips.filter(ip => {
        if (filter.subnet_id && ip.subnet_id !== parseInt(filter.subnet_id)) return false;
        if (filter.status && ip.status !== filter.status) return false;
        if (filter.hostname && !ip.hostname?.toLowerCase().includes(filter.hostname.toLowerCase())) return false;
        return true;
    });

    if (loading) {
        return (
            <div className="flex items-center justify-center py-12">
                <div className="text-center">
                    <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                    <p className="mt-4 text-gray-600">Loading IP addresses...</p>
                </div>
            </div>
        );
    }

    return (
        <div>
            <div className="flex justify-end items-center mb-6">
                <button onClick={allocateIP} className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
                    Allocate IP
                </button>
            </div>

            <div className="bg-white p-4 rounded-lg shadow mb-6">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <select
                        value={filter.subnet_id}
                        onChange={(e) => setFilter({ ...filter, subnet_id: e.target.value })}
                        className="border px-3 py-2 rounded"
                    >
                        <option value="">All Subnets</option>
                        {subnets.map(s => <option key={s.id} value={s.id}>{s.cidr}</option>)}
                    </select>
                    <select
                        value={filter.status}
                        onChange={(e) => setFilter({ ...filter, status: e.target.value })}
                        className="border px-3 py-2 rounded"
                    >
                        <option value="">All Status</option>
                        <option value="free">Free</option>
                        <option value="assigned">Assigned</option>
                        <option value="reserved">Reserved</option>
                        <option value="quarantined">Quarantined</option>
                    </select>
                    <input
                        type="text"
                        placeholder="Search hostname..."
                        value={filter.hostname}
                        onChange={(e) => setFilter({ ...filter, hostname: e.target.value })}
                        className="border px-3 py-2 rounded"
                    />
                </div>
            </div>

            <div className="bg-white rounded-lg shadow overflow-hidden">
                <table className="min-w-full">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Address</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Hostname</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Subnet</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                        {filteredIps.map((ip) => (
                            <tr key={ip.id}>
                                <td className="px-6 py-4 whitespace-nowrap font-mono">{ip.address}</td>
                                <td className="px-6 py-4">
                                    <span className={`px-2 py-1 rounded text-xs ${ip.status === 'free' ? 'bg-green-100 text-green-800' :
                                        ip.status === 'assigned' ? 'bg-blue-100 text-blue-800' :
                                            ip.status === 'reserved' ? 'bg-yellow-100 text-yellow-800' :
                                                'bg-red-100 text-red-800'
                                        }`}>
                                        {ip.status}
                                    </span>
                                </td>
                                <td className="px-6 py-4">{ip.hostname || '-'}</td>
                                <td className="px-6 py-4">{ip.subnet_id}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default IPAddresses;
