from typing import Dict, List, Any
import json
from datetime import datetime

class ShodanProcessor:
    def __init__(self):
        self.important_fields = [
            'ip_str', 'ports', 'hostnames', 'org', 'os', 'isp',
            'domains', 'vulns', 'tags', 'location'
        ]

    def preprocess_shodan_data(self, shodan_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Preprocess Shodan host data to extract relevant information and format it for better analysis.
        """
        processed_data = {
            'basic_info': {},
            'services': [],
            'vulnerabilities': [],
            'last_update': shodan_data.get('last_update', '')
        }

        # Extract basic information
        for field in self.important_fields:
            if field in shodan_data:
                processed_data['basic_info'][field] = shodan_data[field]

        # Process location data
        if 'location' in shodan_data:
            location = shodan_data['location']
            processed_data['basic_info']['location'] = {
                'country': location.get('country_name', 'Unknown'),
                'city': location.get('city', 'Unknown'),
                'latitude': location.get('latitude', 0),
                'longitude': location.get('longitude', 0)
            }

        # Process services data
        for service in shodan_data.get('data', []):
            service_info = {
                'port': service.get('port', 'Unknown'),
                'transport': service.get('transport', 'Unknown'),
                'product': None,
                'version': None,
                'banner': None
            }

            # Extract product and version information
            if 'http' in service:
                service_info['product'] = 'HTTP'
                service_info['version'] = service.get('version', 'Unknown')
                service_info['banner'] = service['http'].get('server', 'Unknown')
            elif 'ftp' in service:
                service_info['product'] = 'FTP'
                service_info['banner'] = 'FTP Server'
            elif 'ssh' in service:
                service_info['product'] = 'SSH'
                service_info['banner'] = service['ssh'].get('banner', 'Unknown')

            processed_data['services'].append(service_info)

        # Process vulnerabilities
        if 'vulns' in shodan_data:
            # Handle both list and dictionary formats of vulnerabilities
            if isinstance(shodan_data['vulns'], list):
                # If vulns is a list of CVE IDs
                for vuln_id in shodan_data['vulns']:
                    processed_data['vulnerabilities'].append({
                        'id': vuln_id,
                        'details': {}  # No additional details available in list format
                    })
            elif isinstance(shodan_data['vulns'], dict):
                # If vulns is a dictionary with details
                for vuln_id, details in shodan_data['vulns'].items():
                    processed_data['vulnerabilities'].append({
                        'id': vuln_id,
                        'details': details
                    })

        return processed_data

    def create_analysis_prompt(self, processed_data: Dict[str, Any]) -> str:
        """
        Create a well-structured prompt for the language model to analyze Shodan host data.
        """
        basic_info = processed_data['basic_info']
        
        prompt = f"""Analyze the following Shodan host data:

Basic Information:
- IP: {basic_info.get('ip_str', 'Unknown')}
- Organization: {basic_info.get('org', 'Unknown')}
- ISP: {basic_info.get('isp', 'Unknown')}
- Hostnames: {', '.join(basic_info.get('hostnames', ['None']))}
- Domains: {', '.join(basic_info.get('domains', ['None']))}
- Operating System: {basic_info.get('os', 'Unknown')}
- Last Update: {processed_data['last_update']}

Location:
- Country: {basic_info.get('location', {}).get('country', 'Unknown')}
- City: {basic_info.get('location', {}).get('city', 'Unknown')}

Open Ports and Services:
"""

        # Add services information
        for service in processed_data['services']:
            prompt += f"\n- Port {service['port']} ({service['transport']}):"
            prompt += f"\n  * Service: {service['product']}"
            if service['version']:
                prompt += f"\n  * Version: {service['version']}"
            if service['banner']:
                prompt += f"\n  * Banner: {service['banner']}"

        # Add vulnerabilities information
        if processed_data['vulnerabilities']:
            prompt += "\n\nVulnerabilities:"
            for vuln in processed_data['vulnerabilities']:
                prompt += f"\n- {vuln['id']}"
                if vuln['details'] and 'summary' in vuln['details']:
                    prompt += f"\n  * Summary: {vuln['details']['summary']}"
                if vuln['details'] and 'cvss' in vuln['details']:
                    prompt += f"\n  * CVSS Score: {vuln['details']['cvss']}"

        prompt += "\n\nPlease provide a security analysis of this host, including:"
        prompt += "\n1. Potential security risks and vulnerabilities"
        prompt += "\n2. Recommendations for securing this system"
        prompt += "\n3. Notable patterns or trends in the services and configurations"
        prompt += "\n4. Suggestions for improving the security posture"

        return prompt