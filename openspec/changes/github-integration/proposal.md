# OpenSpec Proposal: GitHub Integration

**Status**: Proposed  
**Created**: 2025-10-30  
**Author**: System  
**Type**: Feature Enhancement  

---

## Summary

Enable GitHub integration for the OpenSpec system to automatically sync specifications, proposals, and archives with the GitHub repository. This integration will streamline the workflow by automating git operations and ensuring all OpenSpec changes are properly version controlled.

---

## Motivation

Currently, OpenSpec changes require manual git operations to commit and push to GitHub. This proposal adds:

1. **Automatic Git Operations** - Auto-commit and push OpenSpec changes
2. **GitHub Metadata Tracking** - Track repository URL, branch, and commit info
3. **Change Notifications** - Optional GitHub issue/PR creation for proposals
4. **Sync Status** - Track sync status of all OpenSpec changes
5. **Rollback Support** - Easy rollback via git history

---

## Proposed Changes

### 1. GitHub Configuration

**File**: `openspec/.github-config.json`

```json
{
  "enabled": true,
  "repository": {
    "url": "https://github.com/schechtereddie/-project-starter-pro-2.git",
    "owner": "schechtereddie",
    "name": "-project-starter-pro-2",
    "branch": "main"
  },
  "auto_commit": true,
  "auto_push": true,
  "commit_message_template": "{type}: {action} - {change_name}",
  "create_issues": false,
  "create_prs": false,
  "sync_on_apply": true,
  "sync_on_archive": true,
  "notifications": {
    "enabled": false,
    "webhook_url": null
  }
}
```

### 2. Git Integration Module

**File**: `openspec/lib/git_integration.py`

```python
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
            "commit_message_template": "{type}: {action} - {change_name}",
            "create_issues": False,
            "create_prs": False,
            "sync_on_apply": True,
            "sync_on_archive": True,
            "notifications": {
                "enabled": False,
                "webhook_url": None
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
                print(f"Warning: Remote URL mismatch")
                print(f"  Current: {current_url}")
                print(f"  Expected: {expected_url}")
                return False
            
            return True
        except subprocess.CalledProcessError:
            print("Error: Git remote 'origin' not configured")
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
                type=change_type,
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
                check=True
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
            
            ahead_result = subprocess.run(
                ["git", "rev-list", "--count", f"origin/{self.config['repository']['branch']}..HEAD"],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                check=True
            )
            commits_ahead = int(ahead_result.stdout.strip())
            
            behind_result = subprocess.run(
                ["git", "rev-list", "--count", f"HEAD..origin/{self.config['repository']['branch']}"],
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
                "in_sync": uncommitted == 0 and commits_ahead == 0 and commits_behind == 0
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
```

### 3. OpenSpec Command Updates

Update OpenSpec commands to use GitHub integration:

**Proposal Command** (`/openspec-proposal`):
```python
def create_proposal(name: str):
    # ... existing code ...
    
    # Sync to GitHub
    github = get_github_integration()
    if github.is_enabled() and github.config.get("sync_on_proposal"):
        files = [
            f"openspec/changes/{change_dir}/proposal.md",
            f"openspec/changes/{change_dir}/tasks.md"
        ]
        github.sync_change("openspec", "proposal", name, files)
```

**Apply Command** (`/openspec-apply`):
```python
def apply_change(name: str):
    # ... existing code ...
    
    # Sync to GitHub
    github = get_github_integration()
    if github.is_enabled() and github.config.get("sync_on_apply"):
        files = [
            f"openspec/specs/{spec_path}",
            # ... other applied files ...
        ]
        github.sync_change("openspec", "apply", name, files)
```

**Archive Command** (`/openspec-archive`):
```python
def archive_change(name: str):
    # ... existing code ...
    
    # Sync to GitHub
    github = get_github_integration()
    if github.is_enabled() and github.config.get("sync_on_archive"):
        files = [
            f"openspec/archive/{archive_dir}/",
            # ... cleanup of changes dir ...
        ]
        github.sync_change("openspec", "archive", name, files)
```

### 4. New Commands

**Enable GitHub Integration**:
```
/openspec-github enable
```

**Disable GitHub Integration**:
```
/openspec-github disable
```

**Check GitHub Status**:
```
/openspec-github status
```

**Manual Sync**:
```
/openspec-github sync
```

---

## Implementation Plan

### Phase 1: Core Integration (Week 1)
- [ ] Create `.github-config.json` configuration file
- [ ] Implement `GitHubIntegration` class
- [ ] Add enable/disable functionality
- [ ] Add status checking

### Phase 2: Auto-Sync (Week 1)
- [ ] Update `/openspec-proposal` command
- [ ] Update `/openspec-apply` command
- [ ] Update `/openspec-archive` command
- [ ] Update `/openspec-update` command
- [ ] Add commit message templates

### Phase 3: Commands (Week 2)
- [ ] Implement `/openspec-github enable`
- [ ] Implement `/openspec-github disable`
- [ ] Implement `/openspec-github status`
- [ ] Implement `/openspec-github sync`

### Phase 4: Testing & Documentation (Week 2)
- [ ] Test all git operations
- [ ] Test error handling
- [ ] Write user documentation
- [ ] Update OpenSpec README

---

## Benefits

1. **Automation** - No manual git operations needed
2. **Consistency** - Standardized commit messages
3. **Traceability** - Every OpenSpec change tracked in git
4. **Collaboration** - Easy sharing via GitHub
5. **Backup** - Automatic backup to GitHub
6. **History** - Complete change history
7. **Rollback** - Easy rollback via git

---

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enabled` | boolean | false | Enable/disable integration |
| `auto_commit` | boolean | true | Auto-commit changes |
| `auto_push` | boolean | true | Auto-push to GitHub |
| `sync_on_apply` | boolean | true | Sync when applying changes |
| `sync_on_archive` | boolean | true | Sync when archiving |
| `commit_message_template` | string | See above | Commit message format |

---

## Security Considerations

1. **Credentials** - Uses existing git credentials (SSH/HTTPS)
2. **No Token Storage** - No GitHub tokens stored in config
3. **Read-Only Operations** - Only commits/pushes, no destructive operations
4. **User Control** - Can be disabled at any time

---

## Future Enhancements

1. **GitHub Issues** - Auto-create issues for proposals
2. **Pull Requests** - Auto-create PRs for major changes
3. **Webhooks** - Notify external systems of changes
4. **Branch Strategy** - Support feature branches
5. **Conflict Resolution** - Handle merge conflicts
6. **Multi-Repo** - Support multiple repositories

---

## Success Criteria

- ✅ GitHub integration can be enabled/disabled
- ✅ All OpenSpec commands auto-sync to GitHub
- ✅ Commit messages follow template
- ✅ Status command shows sync state
- ✅ Manual sync works correctly
- ✅ Error handling is robust

---

## References

- Git Documentation: https://git-scm.com/doc
- GitHub API: https://docs.github.com/en/rest
- Conventional Commits: https://www.conventionalcommits.org/

---

**Status**: Ready for review and implementation

