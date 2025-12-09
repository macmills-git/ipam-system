import React, { useEffect, useState } from 'react';
import { apiClient } from '../services/api';

const VLANs: React.FC = () => {
    const [vlans, setVlans] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        setLoading(true);
        apiClient.get('/vlans')
            .then(res => setVlans(res.data))
            .catch(async (error: any) => {
                console.error('Failed to load VLANs', error);
                if (error.code === 'ERR_NETWORK' || error.message?.includes('Network Error')) {
                    const { mockVLANs } = await import('../services/mockApi');
                    setVlans(mockVLANs);
                }
            })
            .finally(() => setLoading(false));
    }, []);

    if (loading) {
        return (
            <div className="flex items-center justify-center py-12">
                <div className="text-center">
                    <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                    <p className="mt-4 text-gray-600">Loading VLANs...</p>
                </div>
            </div>
        );
    }

    return (
        <div>
            <div className="bg-white rounded-lg shadow overflow-hidden">
                <table className="min-w-full">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Number</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Description</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                        {vlans.map((vlan) => (
                            <tr key={vlan.id}>
                                <td className="px-6 py-4">{vlan.number}</td>
                                <td className="px-6 py-4">{vlan.name}</td>
                                <td className="px-6 py-4">{vlan.description}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default VLANs;
