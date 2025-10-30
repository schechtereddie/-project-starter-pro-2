#!/usr/bin/env bash
# openspec_manual_init.sh
set -e

PROJECT_DIR="/home/eddie/project starter pro 2"

echo "=== Setting up OpenSpec (Augment CLI) non-interactive ==="

mkdir -p "$PROJECT_DIR/openspec/specs" "$PROJECT_DIR/openspec/changes"
cd "$PROJECT_DIR"

# Create AGENTS.md
cat > openspec/AGENTS.md <<'AGENTS'
# AGENTS.md
Primary AI Assistant: Augment CLI

Follow the OpenSpec workflow:
/openspec-proposal  – create a new proposal
/openspec-apply     – apply and implement
/openspec-archive   – archive completed change

Specs:   openspec/specs/
Changes: openspec/changes/
AGENTS

# Create project.md
cat > openspec/project.md <<'DOC'
# Project Starter Pro 2

Purpose: unified workspace for planning, tracking, and analyzing software or business projects.

Tech Stack
- Node.js + Python hybrid
- Augment CLI for OpenSpec workflow
- Local & cloud synchronization

Conventions
- Every feature uses the OpenSpec proposal → apply → archive cycle.
- Deltas are stored under openspec/changes/.
- Approved specs live under openspec/specs/.
DOC

# Create internal metadata to mark initialized
cat > openspec/.init.json <<'JSON'
{
  "initialized": true,
  "assistant": "Augment CLI",
  "version": "1.0.0"
}
JSON

echo "✅ OpenSpec manually initialized in:"
echo "   $PROJECT_DIR/openspec"
echo
echo "Next:"
echo "1. Open Augment."
echo "2. Run: /openspec-proposal Initialize project context"
