#!/usr/bin/env bash
set -euo pipefail

# GitHub Setup Script for Project Starter Pro 2
# This script helps set up the GitHub repository

echo "=========================================="
echo "GitHub Setup for Project Starter Pro 2"
echo "=========================================="
echo ""

# Check if git is configured
echo "Checking Git configuration..."
GIT_USER=$(git config --global user.name || echo "")
GIT_EMAIL=$(git config --global user.email || echo "")

if [ -z "$GIT_USER" ] || [ -z "$GIT_EMAIL" ]; then
    echo "❌ Git is not configured!"
    echo ""
    echo "Please configure Git with:"
    echo "  git config --global user.name \"Your Name\""
    echo "  git config --global user.email \"your.email@example.com\""
    exit 1
fi

echo "✅ Git configured as: $GIT_USER <$GIT_EMAIL>"
echo ""

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Not in a git repository!"
    echo "Run: git init"
    exit 1
fi

echo "✅ Git repository initialized"
echo ""

# Check current status
echo "Current Git Status:"
echo "-------------------"
git status --short
echo ""

# Check if there are uncommitted changes
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    echo "⚠️  You have uncommitted changes!"
    echo ""
    read -p "Do you want to commit all changes? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add .
        read -p "Enter commit message: " COMMIT_MSG
        git commit -m "$COMMIT_MSG"
        echo "✅ Changes committed"
    fi
    echo ""
fi

# Check if remote already exists
if git remote get-url origin > /dev/null 2>&1; then
    CURRENT_REMOTE=$(git remote get-url origin)
    echo "✅ Remote 'origin' already configured: $CURRENT_REMOTE"
    echo ""
    read -p "Do you want to push to this remote? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Pushing to remote..."
        git push -u origin main || git push -u origin master
        echo "✅ Pushed to remote!"
    fi
else
    echo "ℹ️  No remote configured yet"
    echo ""
    echo "To create a GitHub repository and connect it:"
    echo ""
    echo "Option 1: Using GitHub CLI (gh)"
    echo "  1. Install GitHub CLI: https://cli.github.com/"
    echo "  2. Authenticate: gh auth login"
    echo "  3. Create repo: gh repo create project-starter-pro-2 --public --source=. --remote=origin"
    echo "  4. Push: git push -u origin main"
    echo ""
    echo "Option 2: Using GitHub Web Interface"
    echo "  1. Go to: https://github.com/new"
    echo "  2. Repository name: project-starter-pro-2"
    echo "  3. Description: AI-Powered Project Management and Research Platform"
    echo "  4. Choose: Public"
    echo "  5. DO NOT initialize with README, .gitignore, or license"
    echo "  6. Click 'Create repository'"
    echo "  7. Run these commands:"
    echo ""
    echo "     git remote add origin https://github.com/schechtereddie/project-starter-pro-2.git"
    echo "     git branch -M main"
    echo "     git push -u origin main"
    echo ""
    
    read -p "Have you created the GitHub repository? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter the repository URL (e.g., https://github.com/schechtereddie/project-starter-pro-2.git): " REPO_URL
        
        if [ -n "$REPO_URL" ]; then
            git remote add origin "$REPO_URL"
            echo "✅ Remote added: $REPO_URL"
            
            # Ensure we're on main branch
            CURRENT_BRANCH=$(git branch --show-current)
            if [ "$CURRENT_BRANCH" != "main" ]; then
                git branch -M main
                echo "✅ Renamed branch to 'main'"
            fi
            
            echo ""
            echo "Pushing to GitHub..."
            git push -u origin main
            echo ""
            echo "✅ Successfully pushed to GitHub!"
            echo ""
            echo "Your repository is now available at:"
            echo "${REPO_URL%.git}"
        fi
    fi
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Visit your repository on GitHub"
echo "  2. Add repository topics: ai, project-management, fastapi, react, crewai"
echo "  3. Enable GitHub Actions (if needed)"
echo "  4. Set up branch protection rules (optional)"
echo "  5. Add collaborators (optional)"
echo ""
echo "Repository URL: https://github.com/schechtereddie/project-starter-pro-2"
echo ""

