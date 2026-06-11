-- Athena table definition for Kiro security findings
-- This enables QuickSight to query findings stored in S3

CREATE EXTERNAL TABLE IF NOT EXISTS kiro_security_findings (
    severity        STRING,
    issue_type      STRING,
    file            STRING,
    line_start      INT,
    line_end        INT,
    summary         STRING,
    remediation     STRING,
    commit_id       STRING,
    short_commit    STRING,
    branch          STRING,
    repository      STRING,
    author          STRING,
    scan_date       STRING,
    pull_request_number STRING,
    pull_request_url    STRING,
    run_id          STRING,
    run_url         STRING
)
PARTITIONED BY (
    year STRING,
    month STRING,
    day STRING
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://kiro-security-findings-us-east-1-798836978083/security-findings/'
TBLPROPERTIES ('has_encrypted_data'='false');

-- After creating the table, load partitions:
-- MSCK REPAIR TABLE kiro_security_findings;
