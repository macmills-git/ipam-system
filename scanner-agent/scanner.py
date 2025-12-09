#!/usr/bin/env python3
"""
IPAM Scanner Agent - Discovers and monitors IP addresses
Can run on-premises with network access for real scanning
"""
import os
import time
import subprocess
import socket
import requests
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

API_URL = os.getenv('API_URL', 'http://localhost:8000/api/v1')
API_KEY = os.getenv('API_KEY', 'scanner-service-key')
SCAN_INTERVAL = int(os.getenv('SCAN_INTERVAL', '300'))
MOCK_MODE = os.getenv('MOCK_MODE', 'true').lower() == 'true'

class IPScanner:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'Bearer {API_KEY}'})
    
    def get_ips_to_scan(self):
        """Fetch IPs that need scanning from API"""
        try:
            response = self.session.get(f'{API_URL}/ips?status=assigned')
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch IPs: {e}")
            return []
    
    def ping_ip(self, ip_address):
        """Ping an IP address (real implementation)"""
        if MOCK_MODE:
            # Mock mode - simulate ping
            return True, "Mock scan successful"
        
        try:
            # Real ping implementation
            param = '-n' if os.name == 'nt' else '-c'
            command = ['ping', param, '1', '-W', '2', ip_address]
            result = subprocess.run(command, capture_output=True, timeout=3)
            return result.returncode == 0, "Reachable" if result.returncode == 0 else "Unreachable"
        except Exception as e:
            return False, str(e)
    
    def scan_port(self, ip_address, port=80, timeout=2):
        """Check if a port is open"""
        if MOCK_MODE:
            return True
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip_address, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def update_ip_status(self, ip_id, last_seen, status):
        """Update IP status in IPAM"""
        try:
            data = {
                'last_seen': last_seen,
                'metadata': {'scan_status': status}
            }
            response = self.session.put(f'{API_URL}/ips/{ip_id}', json=data)
            response.raise_for_status()
            logger.info(f"Updated IP {ip_id}: {status}")
        except Exception as e:
            logger.error(f"Failed to update IP {ip_id}: {e}")
    
    def scan_all(self):
        """Scan all assigned IPs"""
        logger.info("Starting IP scan...")
        ips = self.get_ips_to_scan()
        logger.info(f"Found {len(ips)} IPs to scan")
        
        for ip in ips:
            ip_address = ip['address']
            ip_id = ip['id']
            
            logger.info(f"Scanning {ip_address}...")
            reachable, status = self.ping_ip(ip_address)
            
            if reachable:
                # Check common ports
                port_80 = self.scan_port(ip_address, 80)
                port_443 = self.scan_port(ip_address, 443)
                status += f" | HTTP: {port_80} | HTTPS: {port_443}"
            
            self.update_ip_status(ip_id, datetime.utcnow().isoformat(), status)
            time.sleep(0.1)  # Rate limiting
        
        logger.info("Scan complete")
    
    def run(self):
        """Main scanner loop"""
        logger.info(f"Scanner started (Mock mode: {MOCK_MODE})")
        logger.info(f"API URL: {API_URL}")
        logger.info(f"Scan interval: {SCAN_INTERVAL} seconds")
        
        while True:
            try:
                self.scan_all()
            except Exception as e:
                logger.error(f"Scan error: {e}")
            
            logger.info(f"Waiting {SCAN_INTERVAL} seconds until next scan...")
            time.sleep(SCAN_INTERVAL)

if __name__ == '__main__':
    scanner = IPScanner()
    scanner.run()
