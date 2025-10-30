# GitHub Setup Guide

Complete guide to setting up GitHub for Project Starter Pro 2.

## Current Status

✅ **Git Repository**: Initialized locally  
✅ **Git Configuration**: User configured as `schechtereddie <schechtereddie@users.gmail.com>`  
✅ **Initial Commit**: Created with 59 files  
✅ **Files Added**: `.gitignore`, `README.md`, `LICENSE`  
⏳ **GitHub Remote**: Not yet configured  

## Quick Setup (Recommended)

### Option 1: Using GitHub Web Interface

1. **Create Repository on GitHub**
   - Go to: https://github.com/new
   - Repository name: `project-starter-pro-2`
   - Description: `AI-Powered Project Management and Research Platform with integrated AI agents`
   - Visibility: **Public** (or Private if preferred)
   - **DO NOT** check "Initialize this repository with:"
     - ❌ Add a README file
     - ❌ Add .gitignore
     - ❌ Choose a license
   - Click **"Create repository"**

2. **Connect Local Repository**
   ```bash
   cd "/home/eddie/project starter pro 2"
   
   # Add remote
   git remote add origin https://github.com/schechtereddie/project-starter-pro-2.git
   
   # Ensure main branch
   git branch -M main
   
   # Push to GitHub
   git push -u origin main
   ```

3. **Verify**
   - Visit: https://github.com/schechtereddie/project-starter-pro-2
   - You should see all your files!

### Option 2: Using GitHub CLI (if installed)

```bash
# Install GitHub CLI (if not installed)
# Ubuntu/Debian:
sudo apt install gh

# Authenticate
gh auth login

# Create repository and push
gh repo create project-starter-pro-2 \
  --public \
  --source=. \
  --remote=origin \
  --description="AI-Powered Project Management and Research Platform"

# Push code
git push -u origin main
```

### Option 3: Using Setup Script

```bash
# Run the automated setup script
./scripts/setup-github.sh
```

## Detailed Steps

### 1. Verify Git Configuration

```bash
# Check current configuration
git config --global user.name
git config --global user.email

# Should show:
# schechtereddie
# schechtereddie@users.gmail.com
```

### 2. Check Repository Status

```bash
cd "/home/eddie/project starter pro 2"

# View current status
git status

# View commit history
git log --oneline

# Should show:
# 8eded54 Add .gitignore, README, and LICENSE
# ae0cb87 Initial OpenSpec and project setup
```

### 3. Create GitHub Repository

**Via Web Interface**:
1. Navigate to https://github.com/new
2. Fill in repository details:
   - **Owner**: schechtereddie
   - **Repository name**: project-starter-pro-2
   - **Description**: AI-Powered Project Management and Research Platform with integrated AI agents for research, documentation, analytics, and intelligent project insights
   - **Visibility**: Public
   - **Initialize**: Leave all unchecked
3. Click "Create repository"

### 4. Add Remote and Push

```bash
# Add GitHub as remote
git remote add origin https://github.com/schechtereddie/project-starter-pro-2.git

# Verify remote
git remote -v
# Should show:
# origin  https://github.com/schechtereddie/project-starter-pro-2.git (fetch)
# origin  https://github.com/schechtereddie/project-starter-pro-2.git (push)

# Ensure on main branch
git branch -M main

# Push to GitHub
git push -u origin main
```

### 5. Verify on GitHub

Visit: https://github.com/schechtereddie/project-starter-pro-2

You should see:
- ✅ README.md displayed
- ✅ All project files
- ✅ 2 commits
- ✅ MIT License

## Post-Setup Configuration

### 1. Add Repository Topics

On GitHub repository page:
1. Click "⚙️ Settings" (or the gear icon near "About")
2. Add topics:
   - `ai`
   - `project-management`
   - `fastapi`
   - `react`
   - `crewai`
   - `langgraph`
   - `langchain`
   - `python`
   - `typescript`
   - `ai-agents`

### 2. Configure Repository Settings

**General Settings**:
- ✅ Issues enabled
- ✅ Projects enabled
- ✅ Wiki enabled
- ✅ Discussions (optional)

**Branch Protection** (optional but recommended):
1. Go to Settings → Branches
2. Add rule for `main` branch:
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging

### 3. Add Collaborators (if needed)

1. Go to Settings → Collaborators
2. Click "Add people"
3. Enter GitHub username or email

### 4. Set Up GitHub Actions (optional)

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.13'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest tests/ -v
```

## Common Issues and Solutions

### Issue: Permission Denied (publickey)

**Solution**: Use HTTPS instead of SSH, or set up SSH keys:

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "schechtereddie@users.gmail.com"

# Add to ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub:
# 1. Go to https://github.com/settings/keys
# 2. Click "New SSH key"
# 3. Paste the public key
```

### Issue: Remote Already Exists

**Solution**: Update the remote URL:

```bash
# Remove existing remote
git remote remove origin

# Add new remote
git remote add origin https://github.com/schechtereddie/project-starter-pro-2.git
```

### Issue: Branch Name Mismatch

**Solution**: Rename branch to main:

```bash
git branch -M main
git push -u origin main
```

## Daily Git Workflow

### Making Changes

```bash
# 1. Check status
git status

# 2. Add files
git add .

# 3. Commit with message
git commit -m "feat: add new feature"

# 4. Push to GitHub
git push
```

### Commit Message Conventions

Use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

**Examples**:
```bash
git commit -m "feat: implement Documentation Agent scraper"
git commit -m "fix: resolve WebSocket connection issue"
git commit -m "docs: update API documentation"
git commit -m "refactor: improve blocker detection logic"
```

### Creating Branches

```bash
# Create and switch to new branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "feat: implement new feature"

# Push branch to GitHub
git push -u origin feature/new-feature

# Create Pull Request on GitHub
```

### Pulling Latest Changes

```bash
# Pull latest from main
git pull origin main

# Or fetch and merge
git fetch origin
git merge origin/main
```

## Repository Structure on GitHub

```
project-starter-pro-2/
├── .github/              # GitHub-specific files
│   └── workflows/       # GitHub Actions
├── docs/                # Documentation
├── openspec/            # Specifications
├── src/                 # Source code
├── scripts/             # Utility scripts
├── tests/               # Tests
├── .gitignore          # Git ignore rules
├── LICENSE             # MIT License
├── README.md           # Project overview
└── requirements.txt    # Python dependencies
```

## Next Steps

After GitHub setup:

1. ✅ **Clone on other machines**:
   ```bash
   git clone https://github.com/schechtereddie/project-starter-pro-2.git
   ```

2. ✅ **Set up CI/CD** with GitHub Actions

3. ✅ **Enable Dependabot** for security updates

4. ✅ **Add project board** for task tracking

5. ✅ **Create issues** for planned features

6. ✅ **Write contributing guidelines**

## Resources

- **GitHub Docs**: https://docs.github.com/
- **Git Docs**: https://git-scm.com/doc
- **GitHub CLI**: https://cli.github.com/
- **Conventional Commits**: https://www.conventionalcommits.org/

## Support

If you encounter issues:
1. Check this guide
2. Review GitHub documentation
3. Open an issue on the repository
4. Contact: schechtereddie@users.gmail.com

---

**Ready to push to GitHub!** 🚀

