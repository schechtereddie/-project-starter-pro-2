# GitHub Integration for OpenSpec

**Status**: Active  
**Version**: 1.0.0  
**Last Updated**: 2025-10-30  

---

## Overview

GitHub Integration automatically syncs all OpenSpec changes (proposals, applications, archives, updates) to your GitHub repository. This ensures that all specification changes are version controlled and backed up.

---

## Features

✅ **Automatic Commits** - Auto-commit OpenSpec changes  
✅ **Automatic Push** - Auto-push to GitHub  
✅ **Standardized Messages** - Consistent commit messages  
✅ **Status Tracking** - Monitor sync status  
✅ **Manual Sync** - Force sync when needed  
✅ **Enable/Disable** - Full control over integration  

---

## Quick Start

### 1. Enable Integration

The integration is **already enabled** for this repository!

**Configuration**: `openspec/.github-config.json`

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
  "auto_push": true
}
```

### 2. Verify Status

Check integration status:
```bash
/openspec-github status
```

Expected output:
```
✅ GitHub Integration: ENABLED
Repository: https://github.com/schechtereddie/-project-starter-pro-2
Branch: main
Status: In sync
Uncommitted files: 0
Commits ahead: 0
Commits behind: 0
```

### 3. Use OpenSpec Commands

All OpenSpec commands now automatically sync to GitHub:

```bash
# Create proposal (auto-syncs)
/openspec-proposal Add new feature

# Apply changes (auto-syncs)
/openspec-apply Add new feature

# Archive changes (auto-syncs)
/openspec-archive Add new feature

# Update specs (auto-syncs)
/openspec-update Update API specification
```

---

## How It Works

### Automatic Sync Workflow

1. **You run an OpenSpec command** (proposal, apply, archive, update)
2. **OpenSpec performs the operation** (creates/modifies files)
3. **GitHub Integration detects the change**
4. **Files are staged** (`git add`)
5. **Changes are committed** with standardized message
6. **Changes are pushed** to GitHub
7. **Success confirmation** is displayed

### Commit Message Format

```
openspec: {action} - {change_name}
```

**Examples**:
- `openspec: proposal - Add new feature`
- `openspec: apply - Add new feature`
- `openspec: archive - Add new feature`
- `openspec: update - Update API specification`

---

## Configuration

### Configuration File

**Location**: `openspec/.github-config.json`

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enabled` | boolean | true | Enable/disable integration |
| `repository.url` | string | - | GitHub repository URL |
| `repository.owner` | string | - | Repository owner |
| `repository.name` | string | - | Repository name |
| `repository.branch` | string | main | Target branch |
| `auto_commit` | boolean | true | Auto-commit changes |
| `auto_push` | boolean | true | Auto-push to GitHub |
| `commit_message_template` | string | See above | Commit message format |
| `sync_on_proposal` | boolean | true | Sync when creating proposals |
| `sync_on_apply` | boolean | true | Sync when applying changes |
| `sync_on_archive` | boolean | true | Sync when archiving |
| `sync_on_update` | boolean | true | Sync when updating specs |

### Customizing Commit Messages

Edit `openspec/.github-config.json`:

```json
{
  "commit_message_template": "docs(openspec): {action} {change_name}"
}
```

**Available Variables**:
- `{action}` - Action performed (proposal, apply, archive, update)
- `{change_name}` - Name of the change

---

## Commands

### Check Status

```bash
/openspec-github status
```

Shows:
- Integration enabled/disabled
- Repository information
- Sync status
- Uncommitted files
- Commits ahead/behind

### Manual Sync

```bash
/openspec-github sync
```

Manually sync all uncommitted OpenSpec changes to GitHub.

### Enable Integration

```bash
/openspec-github enable
```

Enable GitHub integration (if disabled).

### Disable Integration

```bash
/openspec-github disable
```

Temporarily disable GitHub integration. Changes will not be auto-synced.

---

## Workflow Examples

### Example 1: Create and Apply Proposal

```bash
# 1. Create proposal
/openspec-proposal Implement user authentication

# Output:
# ✅ Proposal created: openspec/changes/user-authentication/
# ✅ Committed: openspec: proposal - Implement user authentication
# ✅ Pushed to GitHub: main

# 2. Edit proposal files
# ... make changes ...

# 3. Apply proposal
/openspec-apply Implement user authentication

# Output:
# ✅ Applied to: openspec/specs/auth/user-authentication.md
# ✅ Committed: openspec: apply - Implement user authentication
# ✅ Pushed to GitHub: main

# 4. Archive proposal
/openspec-archive Implement user authentication

# Output:
# ✅ Archived to: openspec/archive/2025-10-30-user-authentication/
# ✅ Committed: openspec: archive - Implement user authentication
# ✅ Pushed to GitHub: main
```

### Example 2: Update Existing Spec

```bash
# Update specification
/openspec-update Update API endpoints

# Output:
# ✅ Updated: openspec/specs/api/spec.md
# ✅ Committed: openspec: update - Update API endpoints
# ✅ Pushed to GitHub: main
```

### Example 3: Manual Sync

```bash
# Check status
/openspec-github status

# Output:
# ✅ GitHub Integration: ENABLED
# Uncommitted files: 3
# Commits ahead: 0

# Sync manually
/openspec-github sync

# Output:
# ✅ Committed: openspec: manual sync
# ✅ Pushed to GitHub: main
```

---

## Troubleshooting

### Issue: Push Failed

**Symptom**: `❌ Push failed: ...`

**Solutions**:
1. Check internet connection
2. Verify git credentials
3. Check repository permissions
4. Pull latest changes: `git pull origin main`

### Issue: Commit Failed

**Symptom**: `❌ Commit failed: ...`

**Solutions**:
1. Check if files were modified
2. Verify git is configured
3. Check file permissions

### Issue: Integration Not Working

**Symptom**: Changes not syncing to GitHub

**Solutions**:
1. Check if enabled: `/openspec-github status`
2. Verify configuration: `cat openspec/.github-config.json`
3. Check git remote: `git remote -v`
4. Enable integration: `/openspec-github enable`

### Issue: Merge Conflicts

**Symptom**: Git reports conflicts

**Solutions**:
1. Pull latest changes: `git pull origin main`
2. Resolve conflicts manually
3. Commit resolved changes
4. Re-run OpenSpec command

---

## Best Practices

1. **Always check status** before major operations
2. **Pull before pushing** if working in a team
3. **Use descriptive change names** for clear commit messages
4. **Review commits** on GitHub periodically
5. **Keep integration enabled** for automatic backup

---

## Security

### Credentials

GitHub Integration uses your existing git credentials:
- **SSH**: Uses `~/.ssh/` keys
- **HTTPS**: Uses credential helper or token

**No credentials are stored** in the configuration file.

### Permissions

Integration requires:
- ✅ Read access to repository
- ✅ Write access to repository (for push)

### What's Synced

Only OpenSpec files are synced:
- `openspec/changes/`
- `openspec/specs/`
- `openspec/archive/`
- `openspec/.github-config.json`

---

## Advanced Usage

### Disable Auto-Push

Keep auto-commit but disable auto-push:

```json
{
  "auto_commit": true,
  "auto_push": false
}
```

Then manually push when ready:
```bash
git push origin main
```

### Disable Specific Syncs

Disable sync for specific operations:

```json
{
  "sync_on_proposal": true,
  "sync_on_apply": true,
  "sync_on_archive": false,
  "sync_on_update": true
}
```

### Custom Branch

Use a different branch:

```json
{
  "repository": {
    "branch": "openspec-changes"
  }
}
```

---

## FAQ

**Q: Can I disable GitHub integration?**  
A: Yes, run `/openspec-github disable` or set `"enabled": false` in config.

**Q: Will it push every time I run a command?**  
A: Only if changes are made and `auto_push` is enabled.

**Q: Can I use a different branch?**  
A: Yes, change `repository.branch` in the configuration.

**Q: What if I'm offline?**  
A: Commits will succeed, but push will fail. Sync when back online.

**Q: Can I customize commit messages?**  
A: Yes, edit `commit_message_template` in the configuration.

**Q: Is this required?**  
A: No, it's optional. You can disable it and use git manually.

---

## Support

For issues or questions:
1. Check this documentation
2. Run `/openspec-github status`
3. Check git status: `git status`
4. Review configuration: `cat openspec/.github-config.json`
5. Open an issue on GitHub

---

## References

- Git Documentation: https://git-scm.com/doc
- GitHub Docs: https://docs.github.com/
- OpenSpec Workflow: `openspec/specs/README.md`

---

**GitHub Integration is now active!** All OpenSpec changes will be automatically synced to your repository. 🚀

