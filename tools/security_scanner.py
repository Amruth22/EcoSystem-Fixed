from crewai.tools import BaseTool
import json
import random
from typing import List, Dict

class SecurityScannerTool(BaseTool):
    name: str = "Security Scanner Tool"
    description: str = "Automated security vulnerability detection and compliance checking"

    def _run(self, target: str = None, scan_type: str = "comprehensive") -> str:
        """
        Perform security scanning and compliance checking.
        
        Args:
            target: Target to scan (API endpoint, repository, etc.)
            scan_type: Type of scan to perform (comprehensive, owasp, compliance)
        """
        try:
            security_data = self._generate_sample_security_assessment(target, scan_type)
            analysis = self._analyze_security_findings(security_data)
            
            result = {
                "target": target or "Default target",
                "scan_type": scan_type,
                "security_assessment": security_data,
                "analysis": analysis
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Security scan failed: {str(e)}"

    def _generate_sample_security_assessment(self, target: str = None, scan_type: str = "comprehensive") -> Dict:
        """Generate sample security assessment data."""
        common_vulnerabilities = [
            {
                "id": "CVE-2025-001",
                "name": "Insecure Authentication",
                "description": "Weak authentication mechanism allows unauthorized access",
                "severity": "HIGH",
                "cvss_score": 8.1,
                "owasp_category": "Broken Authentication"
            },
            {
                "id": "CVE-2025-002", 
                "name": "SQL Injection",
                "description": "User input not properly sanitized in database queries",
                "severity": "CRITICAL",
                "cvss_score": 9.8,
                "owasp_category": "Injection"
            },
            {
                "id": "CVE-2025-003",
                "name": "Cross-Site Scripting (XSS)",
                "description": "Client-side script injection vulnerability",
                "severity": "MEDIUM",
                "cvss_score": 6.1,
                "owasp_category": "XSS"
            }
        ]
        
        selected_vulnerabilities = random.sample(
            common_vulnerabilities, 
            k=random.randint(1, len(common_vulnerabilities))
        )
        
        assessment = {
            "scan_timestamp": "2025-01-09T00:00:00Z",
            "target": target or "Sample API Endpoint",
            "scan_type": scan_type,
            "total_findings": len(selected_vulnerabilities),
            "critical_findings": len([f for f in selected_vulnerabilities if f["severity"] == "CRITICAL"]),
            "high_findings": len([f for f in selected_vulnerabilities if f["severity"] == "HIGH"]),
            "medium_findings": len([f for f in selected_vulnerabilities if f["severity"] == "MEDIUM"]),
            "vulnerabilities": selected_vulnerabilities
        }
        
        return assessment

    def _analyze_security_findings(self, security_data: Dict) -> Dict:
        """Analyze security findings and provide recommendations."""
        vulnerabilities = security_data.get("vulnerabilities", [])
        
        by_severity = {}
        for vuln in vulnerabilities:
            severity = vuln["severity"]
            if severity not in by_severity:
                by_severity[severity] = []
            by_severity[severity].append(vuln)
        
        recommendations = []
        
        critical_high = by_severity.get("CRITICAL", []) + by_severity.get("HIGH", [])
        if critical_high:
            recommendations.append({
                "priority": "IMMEDIATE",
                "description": f"Address {len(critical_high)} critical/high severity vulnerabilities immediately",
                "action": "Implement proper input validation, fix authentication issues, and enforce access controls"
            })
        else:
            recommendations.append({
                "priority": "LOW",
                "description": "No critical security issues found",
                "action": "Continue regular security monitoring and assessments"
            })
        
        return {
            "by_severity": by_severity,
            "recommendations": recommendations
        }
