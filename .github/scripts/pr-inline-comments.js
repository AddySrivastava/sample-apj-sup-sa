// Post inline review comments on PR for each security finding
const fs = require('fs');

module.exports = async ({ github, context }) => {
  if (!fs.existsSync('findings.json')) {
    console.log('No findings.json — skipping inline comments');
    return;
  }

  let findings;
  try {
    findings = JSON.parse(fs.readFileSync('findings.json', 'utf8'));
  } catch (e) {
    console.log('Could not parse findings.json:', e.message);
    return;
  }

  if (findings.length === 0) {
    console.log('No findings to comment on');
    return;
  }

  // Get the list of files changed in this PR
  const { data: prFiles } = await github.rest.pulls.listFiles({
    owner: context.repo.owner,
    repo: context.repo.repo,
    pull_number: context.issue.number,
    per_page: 100,
  });
  const changedFiles = new Set(prFiles.map(f => f.filename));

  // Build review comments only for files in the PR diff
  const comments = [];
  const severityEmoji = { critical: '🔴', warning: '🟡', info: '🔵' };

  for (const finding of findings) {
    if (!changedFiles.has(finding.file)) continue;

    const emoji = severityEmoji[finding.severity] || '⚪';
    const body = [
      `${emoji} **${finding.severity.toUpperCase()}**: ${finding.issue_type.replace(/_/g, ' ')}`,
      '',
      finding.summary,
      '',
      `**Remediation:** ${finding.remediation}`,
    ].join('\n');

    comments.push({
      path: finding.file,
      line: finding.line_end || finding.line_start,
      body: body,
    });
  }

  if (comments.length === 0) {
    console.log('No findings match files in this PR');
    return;
  }

  // Submit as a PR review with inline comments
  const reviewEvent = comments.some(c => c.body.includes('CRITICAL'))
    ? 'REQUEST_CHANGES'
    : 'COMMENT';

  try {
    await github.rest.pulls.createReview({
      owner: context.repo.owner,
      repo: context.repo.repo,
      pull_number: context.issue.number,
      commit_id: context.sha,
      event: reviewEvent,
      body: `🔒 **Kiro Security Review** found ${comments.length} issue(s) in changed files.`,
      comments: comments,
    });
    console.log(`Posted ${comments.length} inline comments`);
  } catch (e) {
    console.log('Review submission failed, posting individual comments:', e.message);
    for (const comment of comments) {
      try {
        await github.rest.pulls.createReviewComment({
          owner: context.repo.owner,
          repo: context.repo.repo,
          pull_number: context.issue.number,
          commit_id: context.sha,
          path: comment.path,
          line: comment.line,
          body: comment.body,
        });
      } catch (innerErr) {
        console.log(`Could not comment on ${comment.path}:${comment.line} — ${innerErr.message}`);
      }
    }
  }
};
