# Tools Quick Reference Guide

## Quick Tool Lookup

| # | Tool Name | Purpose | Input | Output | Status |
|---|-----------|---------|-------|--------|--------|
| 1 | **Git Repository Analyzer** | Analyze git repos for APIs | `repo_path`, `repo_url` | Repository analysis | ✅ **FIXED** |
| 2 | **Network Scanner** | Scan network for APIs | `network_range` | Active services | ⚠️ Works |
| 3 | **Security Scanner** | Vulnerability scanning | `target`, `scan_type` | Security report | ⚠️ Works |
| 4 | **Contract Validator** | Validate API contracts | `contract_data` | Validation status | ⚠️ Works |
| 5 | **SDK Generator** | Generate client SDKs | `api_endpoints`, `languages` | SDKs in multiple languages | ⚠️ Works |
| 6 | **Test Generator** | Generate API tests | `api_spec` | Test suites | ⚠️ Works |
| 7 | **Documentation Builder** | Generate API docs | `api_data` | OpenAPI docs | ⚠️ Works |
| 8 | **Performance Metrics** | Collect metrics | `api_endpoint` | Performance data | ⚠️ Works |

---

## One-Liner Usage

### 1. Git Repository Analyzer ✅
```python
# Analyze current directory
result = git_tool._run()

# Analyze specific path
result = git_tool._run(repo_path="/path/to/repo")

# Clone and analyze remote repo
result = git_tool._run(repo_url="https://github.com/user/repo.git")
```

### 2. Network Scanner
```python
# Scan local network
result = network_tool._run()

# Scan specific range
result = network_tool._run(network_range="192.168.1.0/24")
```

### 3. Security Scanner
```python
# Comprehensive scan
result = security_tool._run(target="http://localhost:8000", scan_type="comprehensive")

# OWASP scan
result = security_tool._run(target="http://api.example.com", scan_type="owasp")
```

### 4. Contract Validator
```python
result = validator_tool._run(contract_data='{"openapi": "3.0.0", ...}')
```

### 5. SDK Generator
```python
result = sdk_tool._run(
    api_endpoints="/users,/posts",
    languages="python,javascript"
)
```

### 6. Test Generator
```python
result = test_tool._run(api_spec='{"paths": {...}}')
```

### 7. Documentation Builder
```python
result = doc_tool._run(api_data='{"endpoints": [...]}')
```

### 8. Performance Metrics
```python
result = metrics_tool._run(api_endpoint="http://localhost:8000/api/users")
```

---

## Common Workflows

### Workflow 1: Complete API Discovery
```python
# Step 1: Discover
git_result = git_analyzer._run()
network_result = network_scanner._run()

# Step 2: Secure
security_result = security_scanner._run(target="http://localhost:8000")

# Step 3: Document
doc_result = doc_builder._run(api_data=git_result)

# Step 4: Generate SDKs
sdk_result = sdk_generator._run(languages="python,javascript")
```

### Workflow 2: Security-First
```python
# Discover
apis = discover_apis()

# Scan
security = security_scanner._run(target=apis)

# Validate
contracts = contract_validator._run(contract_data=apis)

# Test
tests = test_generator._run(api_spec=apis)
```

---


## Error Codes Quick Reference

### Git Repository Analyzer ✅
- `Repository path does not exist` - Invalid path provided
- `Path is not a git repository` - Non-git directory
- `Repository URL cannot be empty` - Empty URL string
- `Failed to clone repository` - Network/auth issues

### Other Tools ⚠️
- Generic string errors (not structured JSON)
- Need to be updated to match Git Analyzer pattern

---

## Agent Usage in CrewAI

### Correct Usage
```python
from crewai import Agent
from tools.git_analyzer import GitRepositoryAnalyzerTool

agent = Agent(
    role="API Discovery Specialist",
    goal="Discover APIs",
    tools=[GitRepositoryAnalyzerTool()],
    verbose=True
)
```

### Tool Call Format (from Agent)
```
Action: Git Repository Analyzer Tool
Action Input: {}
```
or
```
Action: Git Repository Analyzer Tool
Action Input: {"repo_path": "."}
```

---
