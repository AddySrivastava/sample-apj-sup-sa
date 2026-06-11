#!/bin/bash
# Run Kiro security review scoped to changed files
set -euo pipefail

PROMPT=$(cat .kiro/agents/security-review-prompt.md)
FILES=$(cat changed_files.txt | tr '\n' ', ')
DIFF=$(cat pr_diff.patch)

kiro-cli chat \
    --agent security-reviewer \
    --no-interactive \
    "Review ONLY the following changed files for security issues. Do NOT scan the entire repository.

Changed files: ${FILES}

Here is the diff:
\`\`\`
${DIFF}
\`\`\`

${PROMPT}"
