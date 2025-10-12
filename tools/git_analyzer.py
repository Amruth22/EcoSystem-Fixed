from crewai.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field
import git
import os
import tempfile
import json
import logging

logger = logging.getLogger(__name__)

class GitRepositoryAnalyzerInput(BaseModel):
    """Input schema for Git Repository Analyzer Tool."""
    repo_path: Optional[str] = Field(
        default=None,
        description="Local path to git repository. If not provided, uses current directory."
    )
    repo_url: Optional[str] = Field(
        default=None,
        description="Remote git repository URL to clone and analyze."
    )

class GitRepositoryAnalyzerTool(BaseTool):
    name: str = "Git Repository Analyzer Tool"
    description: str = """Parse repositories for API definitions and related files.

    Parameters:
    - repo_path (optional): Local path to git repository. If not provided, analyzes current directory.
    - repo_url (optional): Remote git repository URL to clone and analyze.

    Returns: JSON string with repository information including API files, Python files, config files, and recent commits.

    Example usage:
    - {} - analyze current directory
    - {"repo_path": "."} - analyze current directory explicitly
    - {"repo_url": "https://github.com/user/repo.git"} - clone and analyze remote repo
    """
    args_schema: Type[BaseModel] = GitRepositoryAnalyzerInput

    def _run(
        self,
        repo_path: Optional[str] = None,
        repo_url: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Analyze a git repository for API-related files and metadata.

        Args:
            repo_path: Local path to analyze (default: current directory)
            repo_url: Remote repository URL to clone
            **kwargs: Additional arguments (ignored for compatibility)

        Returns:
            JSON string with repository analysis results
        """
        temp_dir = None

        # Log what we received for debugging
        logger.info(f"Git Analyzer Tool called with: repo_path={repo_path}, repo_url={repo_url}, kwargs={kwargs}")

        try:
            # Handle remote repository cloning
            if repo_url is not None and repo_url != "":
                # Validate URL format
                if not isinstance(repo_url, str):
                    return json.dumps({"error": "Repository URL must be a string"})

                repo_url = repo_url.strip()
                if len(repo_url) == 0:
                    return json.dumps({"error": "Repository URL cannot be empty"})
                logger.info(f"Cloning repository from: {repo_url}")

                temp_dir = tempfile.mkdtemp()
                try:
                    git.Repo.clone_from(repo_url, temp_dir, depth=1)  # Shallow clone for speed
                    repo_path = temp_dir
                    logger.info(f"Successfully cloned to: {temp_dir}")
                except git.exc.GitCommandError as e:
                    return json.dumps({"error": f"Failed to clone repository: {str(e)}"})
                except Exception as e:
                    return json.dumps({"error": f"Unexpected error cloning repository: {str(e)}"})

            # Set default path
            if not repo_path:
                repo_path = "."

            # Validate repository path
            if not os.path.exists(repo_path):
                return json.dumps({"error": f"Repository path does not exist: {repo_path}"})

            # Check if it's a git repository
            if not os.path.exists(os.path.join(repo_path, '.git')):
                return json.dumps({"error": f"Path is not a git repository: {repo_path}"})

            # Open repository
            try:
                repo = git.Repo(repo_path)
            except git.exc.InvalidGitRepositoryError:
                return json.dumps({"error": f"Invalid git repository at: {repo_path}"})
            except Exception as e:
                return json.dumps({"error": f"Failed to open repository: {str(e)}"})

            # Get repository info safely
            repo_info = {
                "repository": repo_url or os.path.abspath(repo_path),
                "active_branch": self._get_active_branch(repo),
                "commit_count": self._get_commit_count(repo),
                "file_count": 0
            }

            api_files = []
            python_files = []
            config_files = []
            file_count = 0

            # Traverse repository tree safely
            try:
                for item in repo.tree().traverse():
                    if item.type == 'blob':
                        file_count += 1
                        filename = item.name.lower()

                        # Categorize files
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
            except Exception as e:
                logger.warning(f"Error traversing repository tree: {e}")

            repo_info["file_count"] = file_count
            repo_info["potential_api_files"] = api_files
            repo_info["python_files"] = python_files[:50]  # Limit to first 50
            repo_info["config_files"] = config_files[:50]  # Limit to first 50

            # Get recent commits safely
            repo_info["recent_commits"] = self._get_recent_commits(repo)

            return json.dumps(repo_info, indent=2)

        except Exception as e:
            import traceback
            error_traceback = traceback.format_exc()
            logger.error(f"Unexpected error analyzing repository: {e}\n{error_traceback}")
            return json.dumps({
                "error": f"Failed to analyze repository: {str(e)}",
                "error_type": type(e).__name__,
                "traceback": error_traceback
            })

        finally:
            # Clean up temporary directory
            if temp_dir and os.path.exists(temp_dir):
                try:
                    import shutil
                    shutil.rmtree(temp_dir)
                    logger.info(f"Cleaned up temporary directory: {temp_dir}")
                except Exception as e:
                    logger.warning(f"Failed to clean up temporary directory: {e}")

    def _get_active_branch(self, repo: git.Repo) -> str:
        """Safely get the active branch name."""
        try:
            return str(repo.active_branch.name)
        except TypeError:
            # Detached HEAD state
            try:
                return f"detached at {repo.head.commit.hexsha[:8]}"
            except Exception:
                return "unknown"
        except Exception as e:
            logger.warning(f"Could not determine active branch: {e}")
            return "unknown"

    def _get_commit_count(self, repo: git.Repo, max_count: int = 1000) -> int:
        """Safely get commit count with a reasonable limit."""
        try:
            # Limit to max_count to avoid performance issues
            commits = list(repo.iter_commits(max_count=max_count))
            return len(commits)
        except Exception as e:
            logger.warning(f"Could not count commits: {e}")
            return 0

    def _get_recent_commits(self, repo: git.Repo, count: int = 5) -> list:
        """Safely get recent commits."""
        recent_commits = []
        try:
            for commit in list(repo.iter_commits(max_count=count)):
                try:
                    recent_commits.append({
                        "sha": commit.hexsha[:8],
                        "message": commit.message.strip()[:100],  # Limit message length
                        "author": str(commit.author),
                        "date": commit.committed_datetime.isoformat()
                    })
                except Exception as e:
                    logger.warning(f"Error processing commit: {e}")
                    continue
        except Exception as e:
            logger.warning(f"Could not retrieve recent commits: {e}")

        return recent_commits
