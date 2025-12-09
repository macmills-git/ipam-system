// Mock API for testing without backend
export const mockLogin = (email: string, password: string) => {
    if (email === 'admin@ipam.local' && password === 'Admin123!') {
        return {
            access_token: 'mock-access-token',
            refresh_token: 'mock-refresh-token',
            token_type: 'bearer'
        };
    }
    throw new Error('Invalid credentials');
};

export const mockUser = {
    id: 1,
    username: 'admin',
    email: 'admin@ipam.local',
    role: 'admin',
    active: true,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
};

export const mockSubnets = [
    { id: 1, cidr: '10.0.0.0/24', description: 'Management Network', location: 'Datacenter A', created_at: new Date().toISOString() },
    { id: 2, cidr: '10.0.1.0/24', description: 'Server Network', location: 'Datacenter A', created_at: new Date().toISOString() },
    { id: 3, cidr: '10.0.2.0/24', description: 'Workstation Network', location: 'Office Building', created_at: new Date().toISOString() },
    { id: 4, cidr: '2001:db8::/64', description: 'IPv6 Test Network', location: 'Datacenter A', created_at: new Date().toISOString() }
];

export const mockIPs = [
    { id: 1, address: '10.0.0.1', subnet_id: 1, status: 'reserved', hostname: 'gateway' },
    { id: 2, address: '10.0.0.11', subnet_id: 1, status: 'assigned', hostname: 'router-01' },
    { id: 3, address: '10.0.0.12', subnet_id: 1, status: 'assigned', hostname: 'switch-01' },
    { id: 4, address: '10.0.1.20', subnet_id: 2, status: 'assigned', hostname: 'server-01' },
    { id: 5, address: '10.0.1.21', subnet_id: 2, status: 'assigned', hostname: 'server-02' },
    { id: 6, address: '10.0.2.100', subnet_id: 3, status: 'assigned', hostname: 'workstation-01' },
    { id: 7, address: '10.0.2.101', subnet_id: 3, status: 'free', hostname: null },
    { id: 8, address: '2001:db8::1', subnet_id: 4, status: 'reserved', hostname: 'ipv6-gateway' }
];

export const mockDevices = [
    { id: 1, hostname: 'router-01', device_type: 'Router', owner: 'Network Team' },
    { id: 2, hostname: 'switch-01', device_type: 'Switch', owner: 'Network Team' },
    { id: 3, hostname: 'server-01', device_type: 'Server', owner: 'IT Team' },
    { id: 4, hostname: 'server-02', device_type: 'Server', owner: 'IT Team' },
    { id: 5, hostname: 'workstation-01', device_type: 'Workstation', owner: 'John Doe' }
];

export const mockVLANs = [
    { id: 1, name: 'Management', number: 10, description: 'Management VLAN' },
    { id: 2, name: 'Servers', number: 20, description: 'Server VLAN' },
    { id: 3, name: 'Workstations', number: 30, description: 'Workstation VLAN' }
];
