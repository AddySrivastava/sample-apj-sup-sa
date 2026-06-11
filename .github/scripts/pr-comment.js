// Post summary comment on PR with security findings
const fs = require('fs');

module.exports = async ({ github, context }) => {
  let reportBody = '## 🔒 Kiro Security Review\n\n';

  // Read the markdown report if it exists
  if (fs.existsSync('review-report.md')) {
    const report = fs.readFileSync('review-report.md', 'utf8');
    reportBody += report;
  } else {
    reportBody += '⚠️ Security review did not produce a report.\n';
  }

  // Add findings summary from JSON if available
  if (fs.existsSync('findings.json')) {
    try {
      const findings = JSON.parse(fs.readFileSync('findings.json', 'utf8'));
      const critical = findings.filter(f => f.severity === 'critical').length;
      const warning = findings.filter(f => f.severity === 'warning').length;
      const info = findings.filter(f => f.severity === 'info').length;

      reportBody += '\n\n---\n';
      reportBody += `### Summary: ${findings.length} findings\n`;
      reportBody += `| Severity | Count |\n|----------|-------|\n`;
      reportBody += `| 🔴 Critical | ${critical} |\n`;
      reportBody += `| 🟡 Warning | ${warning} |\n`;
      reportBody += `| 🔵 Info | ${info} |\n`;

      if (critical > 0 || warning > 0) {
        reportBody += '\n❌ **This PR has security issues that must be resolved before merging.**\n';
      } else {
        reportBody += '\n✅ **No critical or warning security issues found.**\n';
      }
    } catch (e) {
      reportBody += '\n\n_Could not parse findings.json_\n';
    }
  }

  reportBody += `\n\n_Run: [${context.runId}](${context.serverUrl}/${context.repo.owner}/${context.repo.repo}/actions/runs/${context.runId})_`;

  // Find and update existing comment or create new one
  const { data: comments } = await github.rest.issues.listComments({
    owner: context.repo.owner,
    repo: context.repo.repo,
    issue_number: context.issue.number,
  });

  const botComment = comments.find(c => c.body.includes('## 🔒 Kiro Security Review'));

  if (botComment) {
    await github.rest.issues.updateComment({
      owner: context.repo.owner,
      repo: context.repo.repo,
      comment_id: botComment.id,
      body: reportBody,
    });
  } else {
    await github.rest.issues.createComment({
      owner: context.repo.owner,
      repo: context.repo.repo,
      issue_number: context.issue.number,
      body: reportBody,
    });
  }
};
