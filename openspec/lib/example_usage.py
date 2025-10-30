#!/usr/bin/env python3
"""
Example usage of GitHub Integration
This demonstrates how to use the integration in OpenSpec commands
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from openspec.lib.git_integration import get_github_integration


def example_proposal_workflow():
    """Example: Creating a proposal with auto-sync."""
    
    print("=" * 60)
    print("Example: Proposal Workflow with GitHub Integration")
    print("=" * 60)
    print()
    
    # Get GitHub integration instance
    github = get_github_integration()
    
    # Check if enabled
    if not github.is_enabled():
        print("❌ GitHub integration is not enabled")
        return
    
    # Simulate creating a proposal
    change_name = "example-feature"
    files = [
        "openspec/changes/example-feature/proposal.md",
        "openspec/changes/example-feature/tasks.md"
    ]
    
    print(f"Creating proposal: {change_name}")
    print(f"Files to sync: {len(files)}")
    print()
    
    # Sync to GitHub (this would be called after creating the proposal files)
    if github.config.get("sync_on_proposal"):
        print("Syncing to GitHub...")
        success = github.sync_change(
            change_type="openspec",
            action="proposal",
            change_name=change_name,
            files=files
        )
        
        if success:
            print()
            print("✅ Proposal synced to GitHub successfully!")
        else:
            print()
            print("❌ Failed to sync proposal to GitHub")
    else:
        print("⚠️  Auto-sync on proposal is disabled")
    
    print()


def example_apply_workflow():
    """Example: Applying changes with auto-sync."""
    
    print("=" * 60)
    print("Example: Apply Workflow with GitHub Integration")
    print("=" * 60)
    print()
    
    # Get GitHub integration instance
    github = get_github_integration()
    
    # Check if enabled
    if not github.is_enabled():
        print("❌ GitHub integration is not enabled")
        return
    
    # Simulate applying changes
    change_name = "example-feature"
    files = [
        "openspec/specs/features/example-feature.md",
        "openspec/changes/example-feature/APPLIED.md"
    ]
    
    print(f"Applying changes: {change_name}")
    print(f"Files to sync: {len(files)}")
    print()
    
    # Sync to GitHub (this would be called after applying the changes)
    if github.config.get("sync_on_apply"):
        print("Syncing to GitHub...")
        success = github.sync_change(
            change_type="openspec",
            action="apply",
            change_name=change_name,
            files=files
        )
        
        if success:
            print()
            print("✅ Changes synced to GitHub successfully!")
        else:
            print()
            print("❌ Failed to sync changes to GitHub")
    else:
        print("⚠️  Auto-sync on apply is disabled")
    
    print()


def example_status_check():
    """Example: Checking GitHub integration status."""
    
    print("=" * 60)
    print("Example: Status Check")
    print("=" * 60)
    print()
    
    # Get GitHub integration instance
    github = get_github_integration()
    
    # Get status
    status = github.get_status()
    
    if not status.get("enabled"):
        print("❌ GitHub integration is disabled")
        print(f"   {status.get('message', 'No message')}")
        return
    
    if "error" in status:
        print(f"❌ Error: {status['message']}")
        print(f"   Details: {status['error']}")
        return
    
    # Display status
    print("✅ GitHub Integration Status")
    print()
    print(f"Repository: {status['repository']['url']}")
    print(f"Branch: {status['repository']['branch']}")
    print()
    print(f"Uncommitted files: {status['uncommitted_files']}")
    print(f"Commits ahead: {status['commits_ahead']}")
    print(f"Commits behind: {status['commits_behind']}")
    print(f"In sync: {'✅ Yes' if status['in_sync'] else '❌ No'}")
    print()
    
    if status.get('metadata'):
        print("Metadata:")
        print(f"  Last sync: {status['metadata'].get('last_sync', 'Never')}")
        print(f"  Total syncs: {status['metadata'].get('total_syncs', 0)}")
    
    print()


def example_manual_commit():
    """Example: Manual commit without push."""
    
    print("=" * 60)
    print("Example: Manual Commit (No Push)")
    print("=" * 60)
    print()
    
    # Get GitHub integration instance
    github = get_github_integration()
    
    # Check if enabled
    if not github.is_enabled():
        print("❌ GitHub integration is not enabled")
        return
    
    # Simulate manual commit
    change_name = "manual-update"
    files = ["openspec/specs/README.md"]
    
    print(f"Committing changes: {change_name}")
    print(f"Files: {files}")
    print()
    
    # Commit only (no push)
    commit_hash = github.commit_changes(
        change_type="openspec",
        action="update",
        change_name=change_name,
        files=files
    )
    
    if commit_hash:
        print()
        print(f"✅ Committed successfully!")
        print(f"   Commit hash: {commit_hash[:7]}")
        print()
        print("Note: Changes are committed but not pushed.")
        print("Run 'git push origin main' to push manually.")
    else:
        print()
        print("❌ Commit failed")
    
    print()


def main():
    """Run all examples."""
    
    print()
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "GitHub Integration - Usage Examples" + " " * 13 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    # Example 1: Status check
    example_status_check()
    
    print("\n" + "-" * 60 + "\n")
    
    # Example 2: Proposal workflow
    print("NOTE: The following examples show the workflow,")
    print("      but won't actually create files or commit.")
    print()
    
    # Uncomment to run actual examples:
    # example_proposal_workflow()
    # print("\n" + "-" * 60 + "\n")
    # example_apply_workflow()
    # print("\n" + "-" * 60 + "\n")
    # example_manual_commit()
    
    print()
    print("=" * 60)
    print("Integration Guide")
    print("=" * 60)
    print()
    print("To use GitHub integration in your OpenSpec commands:")
    print()
    print("1. Import the integration:")
    print("   from openspec.lib.git_integration import get_github_integration")
    print()
    print("2. Get the instance:")
    print("   github = get_github_integration()")
    print()
    print("3. Check if enabled:")
    print("   if github.is_enabled() and github.config.get('sync_on_proposal'):")
    print()
    print("4. Sync changes:")
    print("   github.sync_change('openspec', 'proposal', 'feature-name', files)")
    print()
    print("5. Or commit only:")
    print("   github.commit_changes('openspec', 'apply', 'feature-name', files)")
    print()
    print("6. Or push only:")
    print("   github.push_changes()")
    print()
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()

