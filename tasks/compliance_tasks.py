from crewai import Task
from agents.compliance_agent import create_compliance_agent

agent = create_compliance_agent()

compliance_task = Task(
    description="""Perform comprehensive security and compliance assessment of discovered APIs.
    
    Focus on:
    1. Conducting OWASP API Security Top 10 compliance checks
    2. Identifying security vulnerabilities and misconfigurations
    3. Assessing authentication and authorization mechanisms
    4. Checking regulatory compliance (GDPR, HIPAA, SOX, PCI DSS)
    5. Generating prioritized remediation recommendations
    
    Use the Security Scanner Tool to perform thorough assessments.""",
    agent=agent,
    expected_output="Detailed security assessment report with vulnerability findings, OWASP compliance status, risk levels, and actionable remediation recommendations."
)
