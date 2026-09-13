import { REPORTS } from './data.js';

export function getReport(id) {
  const report = REPORTS[id];
  if (!report) throw new Error(`Unknown report: ${id}`);
  return report;
}

export function applyFilters(report, filters = {}) {
  const rows = report.rows.filter(row =>
    Object.entries(filters).every(([column, value]) => {
      const index = report.columns.indexOf(column);
      return index === -1 || String(row[index]) === String(value);
    }),
  );
  return { ...report, rows };
}

export function renderHtml(report) {
  const head = report.columns.map(c => `<th>${c}</th>`).join('');
  const body = report.rows
    .map(row => `<tr>${row.map(cell => `<td>${cell}</td>`).join('')}</tr>`)
    .join('\n');
  return `<h1>${report.title}</h1>\n<table>\n<thead><tr>${head}</tr></thead>\n<tbody>\n${body}\n</tbody>\n</table>`;
}
