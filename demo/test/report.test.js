import { test } from 'node:test';
import assert from 'node:assert/strict';
import { getReport, applyFilters, renderHtml } from '../src/report.js';

test('unknown report throws', () => {
  assert.throws(() => getReport('nope'), /Unknown report/);
});

test('filters keep matching rows only', () => {
  const report = applyFilters(getReport('sales'), { Quarter: 'Q1' });
  assert.equal(report.rows.length, 3);
  assert.ok(report.rows.every(row => row[1] === 'Q1'));
});

test('renders a table with one row per record', () => {
  const html = renderHtml(getReport('headcount'));
  assert.equal((html.match(/<tr>/g) || []).length, 5);
});
