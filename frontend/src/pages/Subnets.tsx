import React, { useEffect, useState } from 'react';
import { apiClient } from '../services/api';

const Subnets: React.FC = () => {
    const [subnets, setSubnets] = useState<any[]>([]);
    const [showForm, setShowForm] = useState(false);
    const [formData, setFormData] = useState({ cidr: '', description: '', location: '' });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadSubnets();
    }, []);

    const loadSubnets = async () => {
        setLoading(true);
        try {
            const response = await apiClient.get('/subnets');
            setSubnets(response.data);
        } catch (error: any) {
            console.error('Failed to load subnets', error);
            // Use mock data if backend is not available
            if (error.code === 'ERR_NETWORK' || error.message?.includes('Network Error')) {
                const { mockSubnets } = await import('../services/mockApi');
                setSubnets(mockSubnets);
            }
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await apiClient.post('/subnets', formData);
            setShowForm(false);
            setFormData({ cidr: '', description: '', location: '' });
            loadSubnets();
        } catch (error: any) {
            alert(error.response?.data?.detail || 'Failed to create subnet');
        }
    };

    const handleDelete = async (id: number) => {
        if (window.confirm('Delete this subnet?')) {
            try {
                await apiClient.delete(`/subnets/${id}`);
                loadSubnets();
            } catch (error: any) {
                alert(error.response?.data?.detail || 'Failed to delete subnet');
            }
        }
    };

    return (
        <div>
            <div className="flex justify-end items-center mb-6">
                <button onClick={() => setShowForm(!showForm)} className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
                    {showForm ? 'Cancel' : 'Add Subnet'}
                </button>
            </div>

            {showForm && (
                <div className="bg-white p-6 rounded-lg shadow mb-6">
                    <form onSubmit={handleSubmit}>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            <input
                                type="text"
                                placeholder="CIDR (e.g., 10.0.0.0/24)"
                                value={formData.cidr}
                                onChange={(e) => setFormData({ ...formData, cidr: e.target.value })}
                                className="border px-3 py-2 rounded"
                                required
                            />
                            <input
                                type="text"
                                placeholder="Description"
                                value={formData.description}
                                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                                className="border px-3 py-2 rounded"
                            />
                            <input
                                type="text"
                                placeholder="Location"
                                value={formData.location}
                                onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                                className="border px-3 py-2 rounded"
                            />
                        </div>
                        <button type="submit" className="mt-4 bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">
                            Create Subnet
                        </button>
                    </form>
                </div>
            )}

            {loading ? (
                <div className="flex items-center justify-center py-12 bg-white rounded-lg shadow">
                    <div className="text-center">
                        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                        <p className="mt-4 text-gray-600">Loading subnets...</p>
                    </div>
                </div>
            ) : (
                <div className="bg-white rounded-lg shadow overflow-hidden">
                    <table className="min-w-full">
                        <thead className="bg-gray-50">
                            <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">CIDR</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Description</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Location</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-200">
                            {subnets.map((subnet) => (
                                <tr key={subnet.id}>
                                    <td className="px-6 py-4 whitespace-nowrap font-mono">{subnet.cidr}</td>
                                    <td className="px-6 py-4">{subnet.description}</td>
                                    <td className="px-6 py-4">{subnet.location}</td>
                                    <td className="px-6 py-4">
                                        <button onClick={() => handleDelete(subnet.id)} className="text-red-600 hover:text-red-800">
                                            Delete
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};

export default Subnets;
