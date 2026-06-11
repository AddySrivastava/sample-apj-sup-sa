# QuickSight Visualization Setup

## Architecture

```
GitHub Actions → Kiro CLI → findings.json → S3 (partitioned) → Athena → QuickSight
```

## Prerequisites

1. **S3 Bucket** for storing findings (e.g., `my-org-security-findings`)
2. **IAM Role** with OIDC trust for GitHub Actions (to push to S3)
3. **Athena** database and workgroup
4. **QuickSight** with Athena as a data source

## Step 1: Create S3 Bucket

```bash
aws s3 mb s3://my-org-security-findings --region us-east-1
```

## Step 2: Create IAM Role for GitHub Actions

Create an OIDC identity provider for GitHub Actions, then a role with this trust policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:AddySrivastava/*:*"
        }
      }
    }
  ]
}
```

Attach a policy allowing `s3:PutObject` on the bucket:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:PutObject"],
      "Resource": "arn:aws:s3:::my-org-security-findings/security-findings/*"
    }
  ]
}
```

## Step 3: Add GitHub Secrets

| Secret | Value |
|--------|-------|
| `AWS_ROLE_ARN` | `arn:aws:iam::ACCOUNT_ID:role/github-actions-security-findings` |
| `AWS_REGION` | `us-east-1` |
| `SECURITY_FINDINGS_BUCKET` | `my-org-security-findings` |

## Step 4: Create Athena Table

Run `athena-table.sql` in the Athena query editor (replace `YOUR_BUCKET_NAME`).

Then load partitions:

```sql
MSCK REPAIR TABLE kiro_security_findings;
```

## Step 5: Connect QuickSight

1. In QuickSight, create a new **Athena** data source
2. Select the `kiro_security_findings` table
3. Create an analysis with suggested visualizations:

### Recommended Dashboards

| Visual | Type | Fields |
|--------|------|--------|
| Issues over time | Line chart | scan_date (X), count (Y), severity (color) |
| Issues by author | Bar chart | author (X), count (Y), severity (color) |
| Issues by type | Pie chart | issue_type (segment), count (size) |
| Issues by repo | Stacked bar | repository (X), count (Y), issue_type (color) |
| Trend by branch | Line chart | scan_date (X), count (Y), branch (color) |
| Top risky files | Table | file, count, severity |
| Critical issues detail | Table | scan_date, author, repository, file, summary, pr_url |

## Data Schema

Each record in S3 is a newline-delimited JSON object with these fields:

| Field | Type | Description |
|-------|------|-------------|
| severity | string | critical, warning, info |
| issue_type | string | Category (hardcoded_secret, sql_injection, etc.) |
| file | string | File path in the repo |
| line_start | int | Starting line number |
| line_end | int | Ending line number |
| summary | string | One-line issue description |
| remediation | string | Fix suggestion |
| commit_id | string | Full SHA |
| short_commit | string | Short SHA (7 chars) |
| branch | string | Branch name |
| repository | string | org/repo |
| author | string | GitHub actor who triggered the workflow |
| scan_date | string | ISO 8601 timestamp |
| pull_request_number | string | PR number (if applicable) |
| pull_request_url | string | PR URL (if applicable) |
| run_id | string | GitHub Actions run ID |
| run_url | string | Link to the workflow run |
