#!/bin/bash
# Get list of files changed in PR or push
set -euo pipefail

EVENT_NAME="$1"
BASE_REF="$2"

if [ "$EVENT_NAME" = "pull_request" ]; then
  git diff --name-only --diff-filter=ACMR "origin/${BASE_REF}...HEAD" > changed_files.txt
else
  git diff --name-only --diff-filter=ACMR HEAD~1 HEAD > changed_files.txt
fi

echo "Changed files:"
cat changed_files.txt
