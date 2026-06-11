#!/bin/bash
# Check security review results and fail if issues found
set -euo pipefail

if [ ! -f review-report.md ]; then
  echo "❌ No review report generated — treating as failure"
  exit 1
fi

if grep -q "RESULT: FAIL" review-report.md; then
  echo "❌ Security review found critical or warning issues:"
  echo ""
  cat review-report.md
  exit 1
fi

echo "✅ Security review passed — no critical or warning issues found"
