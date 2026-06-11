#!/bin/bash
# Generate diff for security review
set -euo pipefail

EVENT_NAME="$1"
BASE_REF="$2"

if [ "$EVENT_NAME" = "pull_request" ]; then
  git diff "origin/${BASE_REF}...HEAD" -- $(cat changed_files.txt) > pr_diff.patch
else
  git diff HEAD~1 HEAD -- $(cat changed_files.txt) > pr_diff.patch
fi
