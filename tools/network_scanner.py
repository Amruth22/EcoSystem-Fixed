from crewai.tools import BaseTool
import requests
import socket
import json
from typing import Optional

class NetworkScannerTool(BaseTool):
    name: str = "Network Scanner Tool"
    description: str = "Scan network for API endpoints and active services"

    def _run(self, network_range: str = None) -> str:
        """
        Scan network for API endpoints.
        
        Args:
            network_range: Network range to scan (e.g., '192.168.1.0/24')
                          If None, will scan local network
        """
        try:
            if not network_range:
                local_ip = self._get_local_ip()
                network_range = local_ip.rsplit('.', 1)[0] + '.0/24'
            
            local_ip = self._get_local_ip()
            
            common_ports = [80, 443, 8080, 8000, 3000, 5000, 5001, 9000]
            active_services = []
            
            print(f"Scanning common ports on {local_ip}...")
            
            for port in common_ports:
                if self._is_port_open(local_ip, port):
                    service_info = {
                        'ip': local_ip,
                        'port': port,
                        'status': 'open'
                    }
                    
                    api_info = self._probe_api_endpoints(local_ip, port)
                    if api_info:
                        service_info.update(api_info)
                        service_info['potential_api'] = True
                    
                    active_services.append(service_info)
            
            result = {
                'network_range': network_range,
                'scanned_host': local_ip,
                'scanned_ports': common_ports,
                'active_services': active_services
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Network scan failed: {str(e)}"

    def _get_local_ip(self) -> str:
        """Get the local IP address of the machine."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except Exception:
            return "127.0.0.1"

    def _is_port_open(self, host: str, port: int) -> bool:
        """Check if a port is open on a host."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except Exception:
            return False

    def _probe_api_endpoints(self, host: str, port: int) -> Optional[dict]:
        """Probe common API endpoints to gather more information."""
        try:
            base_url = f"http://{host}:{port}"
            if port == 443:
                base_url = f"https://{host}:{port}"
            
            endpoints = ['/', '/api', '/v1', '/swagger', '/docs']
            found_endpoints = []
            
            for endpoint in endpoints:
                try:
                    url = base_url + endpoint
                    response = requests.get(url, timeout=3)
                    if response.status_code in [200, 401, 403]:
                        found_endpoints.append({
                            'endpoint': endpoint,
                            'status_code': response.status_code,
                            'content_type': response.headers.get('content-type', ''),
                            'has_json': 'application/json' in response.headers.get('content-type', '')
                        })
                except requests.RequestException:
                    continue
            
            return {
                'base_url': base_url,
                'found_endpoints': found_endpoints
            } if found_endpoints else None
            
        except Exception:
            return None
