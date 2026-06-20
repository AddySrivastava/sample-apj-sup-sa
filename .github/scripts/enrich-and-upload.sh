#!/bin/bash
# Enrich findings with git metadata and upload to S3
set -euo pipefail

COMMIT_ID="$GITHUB_SHA"
SHORT_COMMIT="${COMMIT_ID:0:7}"
BRANCH="$GITHUB_REF_NAME"
REPO="$GITHUB_REPOSITORY"
AUTHOR="$GITHUB_ACTOR"
DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
PR_NUMBER="${PR_NUMBER:-}"
PR_URL="${PR_URL:-}"
RUN_ID="$GITHUB_RUN_ID"
RUN_URL="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/actions/runs/${GITHUB_RUN_ID}"

# If findings.json doesn't exist, create empty array
if [ ! -f findings.json ]; then
  echo "[]" > findings.json
fi

# Enrich each finding with git metadata using jq
jq --arg commit_id "$COMMIT_ID" \
   --arg short_commit "$SHORT_COMMIT" \
   --arg branch "$BRANCH" \
   --arg repo "$REPO" \
   --arg author "$AUTHOR" \
   --arg date "$DATE" \
   --arg pr_number "$PR_NUMBER" \
   --arg pr_url "$PR_URL" \
   --arg run_id "$RUN_ID" \
   --arg run_url "$RUN_URL" \
   '[.[] | . + {
     commit_id: $commit_id,
     short_commit: $short_commit,
     branch: $branch,
     repository: $repo,
     author: $author,
     scan_date: $date,
     pull_request_number: $pr_number,
     pull_request_url: $pr_url,
     run_id: $run_id,
     run_url: $run_url
   }]' findings.json > enriched-findings.json

# Determine S3 path: partition by date for efficient QuickSight queries
YEAR=$(date -u +"%Y")
MONTH=$(date -u +"%m")
DAY=$(date -u +"%d")
S3_KEY="security-findings/year=${YEAR}/month=${MONTH}/day=${DAY}/${REPO//\//-}_${SHORT_COMMIT}_${RUN_ID}.json"

# Upload to S3 as newline-delimited JSON (for Athena/QuickSight compatibility)
jq -c '.[]' enriched-findings.json > findings-ndjson.json

if [ -s findings-ndjson.json ]; then
  aws s3 cp findings-ndjson.json "s3://${S3_BUCKET}/${S3_KEY}" \
    --content-type "application/json"
  echo "✅ Uploaded $(wc -l < findings-ndjson.json) findings to s3://${S3_BUCKET}/${S3_KEY}"
else
  echo "ℹ️ No findings to upload"
fi
