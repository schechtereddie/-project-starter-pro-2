# OpenSpec Library

**Version**: 1.0.0  
**Status**: Active  
**Last Updated**: 2025-10-30  

---

## Overview

The OpenSpec Library provides core utilities and integrations for the OpenSpec system. Currently, it includes the GitHub Integration module for automatic version control of OpenSpec changes.

---

## Modules

### 1. GitHub Integration (`git_integration.py`)

Automatically syncs OpenSpec changes (proposals, applications, archives, updates) to GitHub.

**Features**:
- ✅ Automatic commits with standardized messages
- ✅ Automatic push to GitHub
- ✅ Status tracking and monitoring
- ✅ Enable/disable controls
- ✅ Configurable sync behavior

**Quick Start**:

```python
from openspec.lib.git_integration import get_github_integration

# Get integration instance
github = get_github_integration()

# Check if enabled
if github.is_enabled():
    # Sync changes to GitHub
    github.sync_change(
        change_type="openspec",
        action="proposal",
        change_name="my-feature",
        files=["openspec/changes/my-feature/proposal.md"]
    )
```

**Configuration**: `openspec/.github-config.json`

**Documentation**: `docs/GITHUB_INTEGRATION.md`

---

## Installation

No installation required. The library is part of the OpenSpec system.

**Requirements**:
- Python 3.13.5+
- Git installed and configured
- GitHub repository with remote configured

---

## Usage

### Import the Library

```python
from openspec.lib.git_integration import GitHubIntegration, get_github_integration
```

### Get Integration Instance

```python
# Use the global instance (recommended)
github = get_github_integration()

# Or create a new instance
github = GitHubIntegration()
```

### Check Status

```python
status = github.get_status()

if status["enabled"]:
    print(f"Repository: {status['repository']['url']}")
    print(f"In sync: {status['in_sync']}")
    print(f"Uncommitted files: {status['uncommitted_files']}")
```

### Sync Changes

```python
# Full sync (commit + push)
success = github.sync_change(
    change_type="openspec",
    action="proposal",
    change_name="my-feature",
    files=["openspec/changes/my-feature/proposal.md"]
)

if success:
    print("✅ Synced to GitHub")
```

### Commit Only

```python
# Commit without pushing
commit_hash = github.commit_changes(
    change_type="openspec",
    action="apply",
    change_name="my-feature",
    files=["openspec/specs/features/my-feature.md"]
)

if commit_hash:
    print(f"✅ Committed: {commit_hash[:7]}")
```

### Push Only

```python
# Push existing commits
success = github.push_changes()

if success:
    print("✅ Pushed to GitHub")
```

### Enable/Disable

```python
# Enable integration
github.enable(
    repository_url="https://github.com/user/repo",
    branch="main"
)

# Disable integration
github.disable()

# Check if enabled
if github.is_enabled():
    print("Integration is enabled")
```

---

## Configuration

### Configuration File

**Location**: `openspec/.github-config.json`

**Example**:

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
  "commit_message_template": "openspec: {action} - {change_name}",
  "sync_on_proposal": true,
  "sync_on_apply": true,
  "sync_on_archive": true,
  "sync_on_update": true
}
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enabled` | boolean | false | Enable/disable integration |
| `auto_commit` | boolean | true | Auto-commit changes |
| `auto_push` | boolean | true | Auto-push to GitHub |
| `commit_message_template` | string | See above | Commit message format |
| `sync_on_proposal` | boolean | true | Sync when creating proposals |
| `sync_on_apply` | boolean | true | Sync when applying changes |
| `sync_on_archive` | boolean | true | Sync when archiving |
| `sync_on_update` | boolean | true | Sync when updating specs |

---

## Testing

### Run Tests

```bash
python3 openspec/lib/test_git_integration.py
```

**Expected Output**:

```
============================================================
GitHub Integration Test
============================================================

Test 1: Check if enabled
------------------------------------------------------------
Enabled: True

Test 2: Get status
------------------------------------------------------------
✅ GitHub Integration: ENABLED
   Repository: https://github.com/schechtereddie/-project-starter-pro-2.git
   ...

✅ All tests passed!
```

### Run Examples

```bash
python3 openspec/lib/example_usage.py
```

---

## Integration with OpenSpec Commands

### Proposal Command

```python
from openspec.lib.git_integration import get_github_integration

def create_proposal(name: str):
    # ... create proposal files ...
    
    # Sync to GitHub
    github = get_github_integration()
    if github.is_enabled() and github.config.get("sync_on_proposal"):
        files = [
            f"openspec/changes/{change_dir}/proposal.md",
            f"openspec/changes/{change_dir}/tasks.md"
        ]
        github.sync_change("openspec", "proposal", name, files)
```

### Apply Command

```python
def apply_change(name: str):
    # ... apply changes ...
    
    # Sync to GitHub
    github = get_github_integration()
    if github.is_enabled() and github.config.get("sync_on_apply"):
        files = [
            f"openspec/specs/{spec_path}",
            # ... other applied files ...
        ]
        github.sync_change("openspec", "apply", name, files)
```

### Archive Command

```python
def archive_change(name: str):
    # ... archive changes ...
    
    # Sync to GitHub
    github = get_github_integration()
    if github.is_enabled() and github.config.get("sync_on_archive"):
        files = [
            f"openspec/archive/{archive_dir}/",
            # ... cleanup of changes dir ...
        ]
        github.sync_change("openspec", "archive", name, files)
```

---

## API Reference

### `GitHubIntegration` Class

#### Methods

**`__init__(config_path: str = "openspec/.github-config.json")`**
- Initialize the integration with configuration file

**`is_enabled() -> bool`**
- Check if integration is enabled

**`enable(repository_url: str, branch: str = "main")`**
- Enable integration with repository URL

**`disable()`**
- Disable integration

**`commit_changes(change_type: str, action: str, change_name: str, files: List[str]) -> Optional[str]`**
- Commit changes to git
- Returns commit hash if successful

**`push_changes() -> bool`**
- Push commits to GitHub
- Returns True if successful

**`sync_change(change_type: str, action: str, change_name: str, files: List[str]) -> bool`**
- Commit and push changes
- Returns True if successful

**`get_status() -> Dict`**
- Get integration status
- Returns status dictionary

### `get_github_integration()` Function

**Returns**: Global `GitHubIntegration` instance

**Usage**:
```python
github = get_github_integration()
```

---

## Files

| File | Description |
|------|-------------|
| `__init__.py` | Package initialization |
| `git_integration.py` | GitHub integration module |
| `test_git_integration.py` | Test script |
| `example_usage.py` | Usage examples |
| `README.md` | This file |

---

## Troubleshooting

### Issue: Integration Not Working

**Check**:
1. Is integration enabled? `github.is_enabled()`
2. Is git configured? `git config --list`
3. Is remote configured? `git remote -v`

### Issue: Commit Failed

**Check**:
1. Are files modified?
2. Is git user configured?
3. Do you have write permissions?

### Issue: Push Failed

**Check**:
1. Internet connection
2. Git credentials
3. Repository permissions
4. Pull latest changes first

---

## Best Practices

1. **Always check if enabled** before syncing
2. **Handle errors gracefully** - sync failures shouldn't break commands
3. **Use descriptive change names** for clear commit messages
4. **Test locally first** before enabling auto-push
5. **Keep configuration in sync** with repository settings

---

## Security

- **No credentials stored** - Uses existing git credentials
- **Read-only config** - Configuration file doesn't contain secrets
- **Safe operations** - Only commits and pushes, no destructive operations
- **User control** - Can be disabled at any time

---

## Future Enhancements

- [ ] GitHub Issues integration
- [ ] Pull Request creation
- [ ] Webhook notifications
- [ ] Branch strategy support
- [ ] Conflict resolution
- [ ] Multi-repository support

---

## Support

For issues or questions:
1. Check this README
2. Run test script: `python3 openspec/lib/test_git_integration.py`
3. Check documentation: `docs/GITHUB_INTEGRATION.md`
4. Review configuration: `openspec/.github-config.json`

---

## References

- GitHub Integration Docs: `docs/GITHUB_INTEGRATION.md`
- OpenSpec Workflow: `openspec/specs/README.md`
- Git Documentation: https://git-scm.com/doc
- GitHub API: https://docs.github.com/en/rest

---

**The OpenSpec Library is ready to use!** 🚀

