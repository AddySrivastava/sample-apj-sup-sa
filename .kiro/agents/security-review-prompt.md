# Security Review Prompt

Perform a security review of ONLY the changed files provided below. Do NOT scan other files in the repository. Focus exclusively on the diff content and the files listed.

Scan for the following specific vulnerability categories:

## Critical Issues (🔴 must block PR)

### Hardcoded Secrets
- AWS access keys, secret keys, session tokens
- API keys, Bearer tokens, OAuth secrets
- Database connection strings with credentials
- Private keys (RSA, SSH, PGP)
- Passwords or passphrases in plaintext
- .env files committed with real values

### Injection Vulnerabilities
- **SQL injection**: string concatenation or f-strings in SQL queries, missing parameterized statements, raw SQL with user input
- **Command injection**: user input passed to `os.system()`, `subprocess.run(shell=True)`, `exec()`, `eval()`, backtick execution
- **LDAP injection**: unsanitized input in LDAP queries
- **Template injection**: user input in server-side template rendering

### Path Traversal
- User-controlled input used in `open()`, `os.path.join()`, `send_file()`, `readFile()`
- Missing path canonicalization or allowlist validation
- Directory listing exposure

### Insecure Deserialization
- `pickle.loads()` or `yaml.load()` on untrusted input
- `JSON.parse()` with `eval` or `Function` constructors
- Java `ObjectInputStream` on network data

### Authentication & Authorization Bypass
- Endpoints missing auth middleware/decorators
- Broken access control (horizontal/vertical privilege escalation)
- JWT validation disabled or using `none` algorithm
- Hardcoded admin backdoors

## Warning Issues (🟡 should fix before merge)

### Missing Input Validation
- No size limits on file uploads
- Missing type/format checks on API inputs
- No rate limiting on sensitive endpoints
- Regex DoS (ReDoS) patterns

### Overly Permissive Configurations
- IAM policies with `"Resource": "*"` or `"Action": "*"`
- Security groups with `0.0.0.0/0` ingress on non-standard ports
- CORS with `Access-Control-Allow-Origin: *` on authenticated endpoints
- File permissions broader than 644/755
- S3 buckets with public access

### Dependency Issues
- Dependencies without pinned versions (e.g., `flask` instead of `flask==3.0.2`)
- Known vulnerable dependency versions
- Dependencies from untrusted registries

### Insecure Communication
- Disabled TLS/SSL verification (`verify=False`, `rejectUnauthorized: false`)
- HTTP endpoints for sensitive data
- Missing HSTS headers

## Info Issues (🔵 best practice suggestions)

### Logging & Monitoring
- Sensitive data logged (tokens, passwords, PII, credit cards)
- Missing audit logging on auth events
- Verbose error messages exposing internals to users

### Code Quality Security
- Empty catch blocks swallowing security exceptions
- TODO/FIXME comments indicating incomplete security work
- Debug mode enabled in production configs

## Output Requirements

1. Write findings to `review-report.md` with severity categories
2. Write structured findings to `findings.json` as an array of objects with fields:
   - severity: "critical", "warning", or "info"
   - issue_type: category (e.g., "hardcoded_secret", "sql_injection", "command_injection", "path_traversal", "insecure_deserialization", "missing_auth", "overly_permissive", "insecure_protocol", "unpinned_dependency", "sensitive_logging")
   - file: relative file path
   - line_start: starting line number
   - line_end: ending line number
   - summary: one-line description
   - remediation: specific fix suggestion

3. At the end of review-report.md include exactly:
   - `RESULT: FAIL` if ANY critical or warning issues found
   - `RESULT: PASS` if only info issues or no issues found
