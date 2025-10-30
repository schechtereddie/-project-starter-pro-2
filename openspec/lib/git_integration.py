"""
GitHub Integration for OpenSpec
Handles automatic git operations for OpenSpec changes
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime


class GitHubIntegration:
    """Manages GitHub integration for OpenSpec."""
    
    def __init__(self, config_path: str = "openspec/.github-config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.repo_root = Path(__file__).parent.parent.parent
    
    def _load_config(self) -> Dict:
        """Load GitHub configuration."""
        if self.config_path.exists():
            with open(self.config_path) as f:
                return json.load(f)
        return {"enabled": False}
    
    def _save_config(self):
        """Save GitHub configuration."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def is_enabled(self) -> bool:
        """Check if GitHub integration is enabled."""
        return self.config.get("enabled", False)
    
    def enable(self, repository_url: str, branch: str = "main"):
        """Enable GitHub integration."""
        # Parse repository URL
        if repository_url.endswith('.git'):
            repository_url = repository_url[:-4]
        
        parts = repository_url.replace('https://github.com/', '').split('/')
        owner = parts[0]
        name = parts[1]
        
        self.config = {
            "enabled": True,
            "repository": {
                "url": f"{repository_url}.git",
                "owner": owner,
                "name": name,
                "branch": branch
            },
            "auto_commit": True,
            "auto_push": True,
            "commit_message_template": "openspec: {action} - {change_name}",
            "create_issues": False,
            "create_prs": False,
            "sync_on_proposal": True,
            "sync_on_apply": True,
            "sync_on_archive": True,
            "sync_on_update": True,
            "notifications": {
                "enabled": False,
                "webhook_url": None
            },
            "metadata": {
                "enabled_at": datetime.utcnow().isoformat() + "Z",
                "enabled_by": "system",
                "last_sync": None,
                "total_syncs": 0
            }
        }
        self._save_config()
        
        # Verify git remote
        self._verify_remote()
    
    def disable(self):
        """Disable GitHub integration."""
        self.config["enabled"] = False
        self._save_config()
    
    def _verify_remote(self) -> bool:
        """Verify git remote is configured correctly."""
        try:
            result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                check=True
            )
            current_url = result.stdout.strip()
            expected_url = self.config["repository"]["url"]
            
            if current_url != expected_url:
                print(f"⚠️  Warning: Remote URL mismatch")
                print(f"   Current: {current_url}")
                print(f"   Expected: {expected_url}")
                return False
            
            return True
        except subprocess.CalledProcessError:
            print("❌ Error: Git remote 'origin' not configured")
            return False
    
    def commit_changes(
        self,
        change_type: str,
        action: str,
        change_name: str,
        files: List[str]
    ) -> Optional[str]:
        """
        Commit OpenSpec changes to git.
        
        Args:
            change_type: Type of change (proposal, apply, archive, update)
            action: Action performed (create, update, delete)
            change_name: Name of the change
            files: List of files to commit
        
        Returns:
            Commit hash if successful, None otherwise
        """
        if not self.is_enabled() or not self.config.get("auto_commit"):
            return None
        
        try:
            # Stage files
            subprocess.run(
                ["git", "add"] + files,
                cwd=self.repo_root,
                check=True
            )
            
            # Create commit message
            commit_msg = self.config["commit_message_template"].format(
                action=action,
                change_name=change_name
            )
            
            # Commit
            result = subprocess.run(
                ["git", "commit", "-m", commit_msg],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Get commit hash
            hash_result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                check=True
            )
            commit_hash = hash_result.stdout.strip()
            
            print(f"✅ Committed: {commit_msg}")
            print(f"   Hash: {commit_hash[:7]}")
            
            return commit_hash
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Commit failed: {e}")
            return None
    
    def push_changes(self) -> bool:
        """Push committed changes to GitHub."""
        if not self.is_enabled() or not self.config.get("auto_push"):
            return False
        
        try:
            branch = self.config["repository"]["branch"]
            
            subprocess.run(
                ["git", "push", "origin", branch],
                cwd=self.repo_root,
                check=True,
                capture_output=True
            )
            
            print(f"✅ Pushed to GitHub: {branch}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Push failed: {e}")
            return False
    
    def sync_change(
        self,
        change_type: str,
        action: str,
        change_name: str,
        files: List[str]
    ) -> bool:
        """
        Sync OpenSpec change to GitHub (commit + push).
        
        Args:
            change_type: Type of change (proposal, apply, archive, update)
            action: Action performed (create, update, delete)
            change_name: Name of the change
            files: List of files to commit
        
        Returns:
            True if successful, False otherwise
        """
        if not self.is_enabled():
            return False
        
        # Update metadata
        if "metadata" not in self.config:
            self.config["metadata"] = {}
        
        self.config["metadata"]["last_sync"] = datetime.utcnow().isoformat() + "Z"
        self.config["metadata"]["total_syncs"] = self.config["metadata"].get("total_syncs", 0) + 1
        self._save_config()
        
        # Commit changes
        commit_hash = self.commit_changes(change_type, action, change_name, files)
        if not commit_hash:
            return False
        
        # Push changes
        if self.config.get("auto_push"):
            return self.push_changes()
        
        return True
    
    def get_status(self) -> Dict:
        """Get GitHub integration status."""
        if not self.is_enabled():
            return {
                "enabled": False,
                "message": "GitHub integration is disabled"
            }
        
        try:
            # Check git status
            status_result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                check=True
            )
            
            uncommitted = len(status_result.stdout.strip().split('\n')) if status_result.stdout.strip() else 0
            
            # Check remote status
            subprocess.run(
                ["git", "fetch", "origin"],
                cwd=self.repo_root,
                capture_output=True,
                check=True
            )
            
            branch = self.config["repository"]["branch"]
            
            ahead_result = subprocess.run(
                ["git", "rev-list", "--count", f"origin/{branch}..HEAD"],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                check=True
            )
            commits_ahead = int(ahead_result.stdout.strip())
            
            behind_result = subprocess.run(
                ["git", "rev-list", "--count", f"HEAD..origin/{branch}"],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                check=True
            )
            commits_behind = int(behind_result.stdout.strip())
            
            return {
                "enabled": True,
                "repository": self.config["repository"],
                "uncommitted_files": uncommitted,
                "commits_ahead": commits_ahead,
                "commits_behind": commits_behind,
                "in_sync": uncommitted == 0 and commits_ahead == 0 and commits_behind == 0,
                "metadata": self.config.get("metadata", {})
            }
            
        except subprocess.CalledProcessError as e:
            return {
                "enabled": True,
                "error": str(e),
                "message": "Failed to get git status"
            }


# Global instance
_github_integration = None


def get_github_integration() -> GitHubIntegration:
    """Get global GitHub integration instance."""
    global _github_integration
    if _github_integration is None:
        _github_integration = GitHubIntegration()
    return _github_integration

