#!/usr/bin/env node
const fs = require('node:fs');
const path = require('node:path');

const inputPath = process.argv[2] ?? 'result.json';
const outDir = process.argv[3] ?? path.dirname(inputPath);
const data = JSON.parse(fs.readFileSync(inputPath, 'utf8'));
const results = data.results.results;

fs.mkdirSync(path.join(outDir, 'outputs'), { recursive: true });

const parsed = new Date(data.results.timestamp ?? Date.now());
const runDate = Number.isNaN(parsed.getTime()) ? new Date() : parsed;
const pad = (value) => String(value).padStart(2, '0');
const timestamp = `${runDate.getFullYear()}-${pad(runDate.getMonth() + 1)}-${pad(runDate.getDate())} ${pad(runDate.getHours())}:${pad(runDate.getMinutes())}:${pad(runDate.getSeconds())}`;

const rows = [];
const outputLinks = [];
for (const result of results) {
  const label = result.prompt.label || `prompt-${result.promptIdx}`;
  const slug = label.replace(/[^a-z0-9._-]+/gi, '-').toLowerCase();
  const file = `${slug}.md`;
  fs.writeFileSync(path.join(outDir, 'outputs', file), result.response?.output ?? '');
  outputLinks.push(`- [${file}](outputs/${file})`);

  const checks = result.gradingResult?.componentResults ?? [];
  const passed = checks.filter((check) => check.pass).length;
  const score = (result.score ?? 0).toFixed(2);
  rows.push(`| ${timestamp} | ${label} | ${passed}/${checks.length} | ${score} |`);
}

const resultPath = path.join(outDir, 'result.md');
if (!fs.existsSync(resultPath) || fs.statSync(resultPath).size === 0) {
  fs.writeFileSync(
    resultPath,
    [
      '# RESULTS',
      '',
      '## OUTPUTS',
      '',
      ...outputLinks,
      '',
      '## LOG',
      '',
      '| Time | Column | Assertions | Score |',
      '| --- | --- | --- | --- |',
      '',
    ].join('\n'),
  );
}

if (rows.length > 0) {
  const prefix = fs.readFileSync(resultPath, 'utf8').endsWith('\n') ? '' : '\n';
  fs.appendFileSync(resultPath, `${prefix}${rows.join('\n')}\n`);
}

console.log(`Appended ${rows.length} row(s) to ${resultPath}`);
