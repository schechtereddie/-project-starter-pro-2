#!/usr/bin/env bash
# setup_openspec.sh
# Initializes OpenSpec for "Project Starter Pro 2" with Augment integration

set -e

PROJECT_DIR="/home/eddie/project starter pro 2"
TOOL_NAME="Augment CLI"

echo "=== Initializing OpenSpec in: $PROJECT_DIR ==="

# Ensure directory exists
if [ ! -d "$PROJECT_DIR" ]; then
  echo "Creating project directory..."
  mkdir -p "$PROJECT_DIR"
fi

cd "$PROJECT_DIR"

# Initialize OpenSpec with Augment CLI
echo "Running OpenSpec init..."
yes "" | openspec init <<EOF
$TOOL_NAME
EOF

# Verify structure
echo "Verifying setup..."
openspec list || true

# Create base spec directories if missing
mkdir -p openspec/specs openspec/changes

# Create base project description if not present
if [ ! -f "openspec/project.md" ]; then
  cat > openspec/project.md <<'DOC'
# Project Starter Pro 2
This document defines project-wide standards, conventions, and architecture.

## Overview
Project Starter Pro 2 helps users plan, track, and organize code and business projects
with integrated research, analytics, and AI-driven insights.

## Tech Stack
- Node.js + Python hybrid
- Augment CLI as primary AI assistant
- Local + server hybrid mode

## Conventions
- Use OpenSpec workflow for all changes.
- All specs live in `openspec/specs/`.
- Proposed updates live in `openspec/changes/`.

DOC
fi

# Create AGENTS.md for Augment integration
cat > openspec/AGENTS.md <<'AGENT'
# AGENTS.md
This project follows the OpenSpec workflow.
Primary AI Assistant: Augment CLI

Workflow:
1. /openspec-proposal  - Create change proposals
2. /openspec-apply     - Apply and implement tasks
3. /openspec-archive   - Archive completed changes

Each change lives under openspec/changes/<feature-name>/ with:
- proposal.md
- tasks.md
- specs/<domain>/spec.md

Follow the OpenSpec lifecycle: Draft → Review → Implement → Archive.
AGENT

echo "=== OpenSpec setup complete ==="
echo "Next step: open Augment and run '/openspec-proposal Initialize project context'"
