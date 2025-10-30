#!/usr/bin/env python3
"""
Test script for GitHub Integration
Run this to verify the integration is working correctly
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from openspec.lib.git_integration import get_github_integration


def test_integration():
    """Test GitHub integration functionality."""
    
    print("=" * 60)
    print("GitHub Integration Test")
    print("=" * 60)
    print()
    
    # Get integration instance
    github = get_github_integration()
    
    # Test 1: Check if enabled
    print("Test 1: Check if enabled")
    print("-" * 60)
    is_enabled = github.is_enabled()
    print(f"Enabled: {is_enabled}")
    print()
    
    if not is_enabled:
        print("❌ GitHub integration is not enabled!")
        print("   Enable it by setting 'enabled': true in openspec/.github-config.json")
        return False
    
    # Test 2: Get status
    print("Test 2: Get status")
    print("-" * 60)
    status = github.get_status()
    
    if "error" in status:
        print(f"❌ Error: {status['message']}")
        print(f"   Details: {status['error']}")
        return False
    
    print(f"✅ GitHub Integration: ENABLED")
    print(f"   Repository: {status['repository']['url']}")
    print(f"   Owner: {status['repository']['owner']}")
    print(f"   Name: {status['repository']['name']}")
    print(f"   Branch: {status['repository']['branch']}")
    print()
    print(f"   Uncommitted files: {status['uncommitted_files']}")
    print(f"   Commits ahead: {status['commits_ahead']}")
    print(f"   Commits behind: {status['commits_behind']}")
    print(f"   In sync: {status['in_sync']}")
    print()
    
    if status.get('metadata'):
        print(f"   Metadata:")
        print(f"     Enabled at: {status['metadata'].get('enabled_at', 'N/A')}")
        print(f"     Last sync: {status['metadata'].get('last_sync', 'Never')}")
        print(f"     Total syncs: {status['metadata'].get('total_syncs', 0)}")
    print()
    
    # Test 3: Verify remote
    print("Test 3: Verify git remote")
    print("-" * 60)
    remote_ok = github._verify_remote()
    if remote_ok:
        print("✅ Git remote is correctly configured")
    else:
        print("⚠️  Git remote configuration issue (see warnings above)")
    print()
    
    # Test 4: Check configuration
    print("Test 4: Check configuration")
    print("-" * 60)
    print(f"Auto-commit: {github.config.get('auto_commit', False)}")
    print(f"Auto-push: {github.config.get('auto_push', False)}")
    print(f"Sync on proposal: {github.config.get('sync_on_proposal', False)}")
    print(f"Sync on apply: {github.config.get('sync_on_apply', False)}")
    print(f"Sync on archive: {github.config.get('sync_on_archive', False)}")
    print(f"Sync on update: {github.config.get('sync_on_update', False)}")
    print(f"Commit message template: {github.config.get('commit_message_template', 'N/A')}")
    print()
    
    # Summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    print()
    
    if is_enabled and not status.get('error') and remote_ok:
        print("✅ All tests passed!")
        print()
        print("GitHub integration is ready to use.")
        print("All OpenSpec commands will now auto-commit and push to GitHub.")
        return True
    else:
        print("⚠️  Some tests failed or have warnings.")
        print()
        print("Please review the output above and fix any issues.")
        return False


if __name__ == "__main__":
    success = test_integration()
    sys.exit(0 if success else 1)

