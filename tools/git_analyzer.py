from crewai.tools import BaseTool
import git
import os
import tempfile
import json

class GitRepositoryAnalyzerTool(BaseTool):
    name: str = "Git Repository Analyzer Tool"
    description: str = "Parse repositories for API definitions and related files"

    def _run(self, repo_path: str = None, repo_url: str = None) -> str:
        if repo_url:
            temp_dir = tempfile.mkdtemp()
            try:
                git.Repo.clone_from(repo_url, temp_dir)
                repo_path = temp_dir
            except Exception as e:
                return f"Failed to clone repository: {str(e)}"
        
        if not repo_path:
            repo_path = "."
            
        try:
            repo = git.Repo(repo_path)
            
            repo_info = {
                "repository": repo_url or repo_path,
                "active_branch": str(repo.active_branch),
                "commit_count": len(list(repo.iter_commits())),
                "file_count": len([item for item in repo.tree().traverse() if item.type == 'blob'])
            }
            
            api_files = []
            python_files = []
            config_files = []
            
            for item in repo.tree().traverse():
                if item.type == 'blob':
                    filename = item.name.lower()
                    if any(pattern in filename for pattern in [
                        'openapi', 'swagger', 'api', 'routes', 'endpoints'
                    ]):
                        api_files.append({
                            "name": item.name,
                            "path": item.path,
                            "type": "api_definition"
                        })
                    elif filename.endswith(('.json', '.yaml', '.yml')):
                        api_files.append({
                            "name": item.name,
                            "path": item.path,
                            "type": "config_or_spec"
                        })
                    elif filename.endswith('.py'):
                        python_files.append({
                            "name": item.name,
                            "path": item.path
                        })
                    elif any(pattern in filename for pattern in [
                        'config', 'settings', 'env', '.env', '.ini', '.cfg'
                    ]):
                        config_files.append({
                            "name": item.name,
                            "path": item.path
                        })
            
            repo_info["potential_api_files"] = api_files
            repo_info["python_files"] = python_files
            repo_info["config_files"] = config_files
            
            recent_commits = []
            for commit in list(repo.iter_commits())[:5]:
                recent_commits.append({
                    "sha": commit.hexsha[:8],
                    "message": commit.message.strip(),
                    "author": str(commit.author),
                    "date": commit.committed_datetime.isoformat()
                })
            
            repo_info["recent_commits"] = recent_commits
            
            return json.dumps(repo_info, indent=2)
            
        except Exception as e:
            return f"Failed to analyze repository: {str(e)}"
