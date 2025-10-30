# GitHub Integration Specification

**Status**: Active  
**Version**: 1.0.0  
**Last Updated**: 2025-10-30  
**Applied From**: `openspec/changes/github-integration/`  

---

## Overview

The GitHub Integration automatically syncs all OpenSpec changes (proposals, applications, archives, updates) to the GitHub repository. This ensures that all specification changes are version controlled, backed up, and traceable.

---

## Architecture

### Components

1. **GitHubIntegration Class** - Core integration module
2. **Configuration File** - JSON-based configuration
3. **Global Instance** - Singleton pattern for easy access
4. **Auto-Sync Hooks** - Integration points in OpenSpec commands

### File Structure

```
openspec/
├── .github-config.json          # Configuration
└── lib/
    ├── __init__.py              # Package initialization
    ├── git_integration.py       # Core implementation
    ├── test_git_integration.py  # Test suite
    ├── example_usage.py         # Usage examples
    └── README.md                # Library documentation
```

---

## Configuration

### Configuration File

**Location**: `openspec/.github-config.json`

**Schema**:

```json
{
  "enabled": boolean,
  "repository": {
    "url": string,
    "owner": string,
    "name": string,
    "branch": string
  },
  "auto_commit": boolean,
  "auto_push": boolean,
  "commit_message_template": string,
  "create_issues": boolean,
  "create_prs": boolean,
  "sync_on_proposal": boolean,
  "sync_on_apply": boolean,
  "sync_on_archive": boolean,
  "sync_on_update": boolean,
  "notifications": {
    "enabled": boolean,
    "webhook_url": string | null
  },
  "metadata": {
    "enabled_at": string,
    "enabled_by": string,
    "last_sync": string | null,
    "total_syncs": number
  }
}
```

### Default Configuration

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
  "create_issues": false,
  "create_prs": false,
  "sync_on_proposal": true,
  "sync_on_apply": true,
  "sync_on_archive": true,
  "sync_on_update": true,
  "notifications": {
    "enabled": false,
    "webhook_url": null
  }
}
```

---

## API Reference

### GitHubIntegration Class

**Module**: `openspec.lib.git_integration`

#### Constructor

```python
GitHubIntegration(config_path: str = "openspec/.github-config.json")
```

#### Methods

**`is_enabled() -> bool`**
- Check if GitHub integration is enabled
- Returns: `True` if enabled, `False` otherwise

**`enable(repository_url: str, branch: str = "main") -> None`**
- Enable GitHub integration
- Parameters:
  - `repository_url`: GitHub repository URL
  - `branch`: Target branch (default: "main")

**`disable() -> None`**
- Disable GitHub integration

**`commit_changes(change_type: str, action: str, change_name: str, files: List[str]) -> Optional[str]`**
- Commit changes to git
- Parameters:
  - `change_type`: Type of change (e.g., "openspec")
  - `action`: Action performed (e.g., "proposal", "apply")
  - `change_name`: Name of the change
  - `files`: List of file paths to commit
- Returns: Commit hash if successful, `None` otherwise

**`push_changes() -> bool`**
- Push committed changes to GitHub
- Returns: `True` if successful, `False` otherwise

**`sync_change(change_type: str, action: str, change_name: str, files: List[str]) -> bool`**
- Commit and push changes in one operation
- Parameters: Same as `commit_changes()`
- Returns: `True` if successful, `False` otherwise

**`get_status() -> Dict`**
- Get integration status
- Returns: Status dictionary with repository info, sync state, and metadata

### Global Instance Function

```python
get_github_integration() -> GitHubIntegration
```

Returns the global singleton instance of `GitHubIntegration`.

---

## Integration Points

### OpenSpec Commands

The integration should be added to the following OpenSpec commands:

#### 1. Proposal Command (`/openspec-proposal`)

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

#### 2. Apply Command (`/openspec-apply`)

```python
def apply_change(name: str):
    # ... apply changes ...
    
    # Sync to GitHub
    github = get_github_integration()
    if github.is_enabled() and github.config.get("sync_on_apply"):
        files = [
            f"openspec/specs/{spec_path}",
            f"openspec/changes/{change_dir}/APPLIED.md"
        ]
        github.sync_change("openspec", "apply", name, files)
```

#### 3. Archive Command (`/openspec-archive`)

```python
def archive_change(name: str):
    # ... archive changes ...
    
    # Sync to GitHub
    github = get_github_integration()
    if github.is_enabled() and github.config.get("sync_on_archive"):
        files = [
            f"openspec/archive/{archive_dir}/",
        ]
        github.sync_change("openspec", "archive", name, files)
```

#### 4. Update Command (`/openspec-update`)

```python
def update_spec(name: str):
    # ... update spec ...
    
    # Sync to GitHub
    github = get_github_integration()
    if github.is_enabled() and github.config.get("sync_on_update"):
        files = [f"openspec/specs/{spec_path}"]
        github.sync_change("openspec", "update", name, files)
```

---

## Commit Message Format

### Template

```
openspec: {action} - {change_name}
```

### Variables

- `{action}`: Action performed (proposal, apply, archive, update)
- `{change_name}`: Name of the change

### Examples

- `openspec: proposal - Add new feature`
- `openspec: apply - Add new feature`
- `openspec: archive - Add new feature`
- `openspec: update - Update API specification`

---

## Workflow

### Automatic Sync Workflow

1. User runs OpenSpec command (e.g., `/openspec-proposal`)
2. OpenSpec performs the operation (creates/modifies files)
3. GitHub Integration detects the change
4. Files are staged (`git add`)
5. Changes are committed with standardized message
6. Changes are pushed to GitHub (if `auto_push` is enabled)
7. Success confirmation is displayed
8. Metadata is updated (last_sync, total_syncs)

### Manual Sync Workflow

1. User runs `/openspec-github sync`
2. Integration detects all uncommitted OpenSpec files
3. Files are staged and committed
4. Changes are pushed to GitHub
5. Success confirmation is displayed

---

## Security

### Credentials

- **No credentials stored** in configuration file
- Uses existing git credentials (SSH keys or HTTPS tokens)
- Relies on system git configuration

### Permissions Required

- Read access to repository
- Write access to repository (for push)

### Safe Operations

- Only performs `git add`, `git commit`, and `git push`
- No destructive operations (no `git reset`, `git rebase`, etc.)
- User can disable integration at any time

---

## Error Handling

### Commit Failures

- Check if files were modified
- Verify git user is configured
- Check file permissions
- Display clear error message

### Push Failures

- Check internet connection
- Verify git credentials
- Check repository permissions
- Suggest pulling latest changes
- Display clear error message

### Configuration Errors

- Validate configuration file format
- Check required fields
- Verify repository URL format
- Display clear error message

---

## Testing

### Test Suite

**Location**: `openspec/lib/test_git_integration.py`

**Tests**:
1. Check if integration is enabled
2. Get integration status
3. Verify git remote configuration
4. Check configuration options

**Run Tests**:
```bash
python3 openspec/lib/test_git_integration.py
```

### Expected Output

```
✅ All tests passed!
GitHub integration is ready to use.
```

---

## Usage Examples

### Basic Usage

```python
from openspec.lib.git_integration import get_github_integration

# Get integration instance
github = get_github_integration()

# Sync changes
if github.is_enabled():
    github.sync_change(
        change_type="openspec",
        action="proposal",
        change_name="my-feature",
        files=["openspec/changes/my-feature/proposal.md"]
    )
```

### Check Status

```python
status = github.get_status()

if status["enabled"]:
    print(f"Repository: {status['repository']['url']}")
    print(f"In sync: {status['in_sync']}")
```

### Enable/Disable

```python
# Enable
github.enable("https://github.com/user/repo", "main")

# Disable
github.disable()
```

---

## Future Enhancements

### Planned Features

- [ ] GitHub Issues integration
- [ ] Pull Request creation
- [ ] Webhook notifications
- [ ] Branch strategy support
- [ ] Conflict resolution
- [ ] Multi-repository support

---

## References

- **Implementation**: `openspec/lib/git_integration.py`
- **Configuration**: `openspec/.github-config.json`
- **User Guide**: `docs/GITHUB_INTEGRATION.md`
- **Library Docs**: `openspec/lib/README.md`
- **Proposal**: `openspec/changes/github-integration/proposal.md`

---

## Changelog

### Version 1.0.0 (2025-10-30)

**Initial Release**:
- ✅ Core GitHubIntegration class
- ✅ Configuration file support
- ✅ Auto-commit and auto-push
- ✅ Status tracking
- ✅ Enable/disable controls
- ✅ Test suite
- ✅ Documentation

---

**Status**: Active and ready for use in OpenSpec commands

