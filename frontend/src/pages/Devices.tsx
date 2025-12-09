import React, { useEffect, useState } from 'react';
import { apiClient } from '../services/api';

const Devices: React.FC = () => {
    const [devices, setDevices] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        setLoading(true);
        apiClient.get('/devices')
            .then(res => setDevices(res.data))
            .catch(async (error: any) => {
                console.error('Failed to load devices', error);
                if (error.code === 'ERR_NETWORK' || error.message?.includes('Network Error')) {
                    const { mockDevices } = await import('../services/mockApi');
                    setDevices(mockDevices);
                }
            })
            .finally(() => setLoading(false));
    }, []);

    if (loading) {
        return (
            <div className="flex items-center justify-center py-12">
                <div className="text-center">
                    <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                    <p className="mt-4 text-gray-600">Loading devices...</p>
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
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Hostname</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Owner</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                        {devices.map((device) => (
                            <tr key={device.id}>
                                <td className="px-6 py-4">{device.hostname}</td>
                                <td className="px-6 py-4">{device.device_type}</td>
                                <td className="px-6 py-4">{device.owner}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default Devices;
