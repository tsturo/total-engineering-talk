import http from 'node:http';
import { readFile } from 'node:fs/promises';
import { getReport, applyFilters, renderHtml } from './report.js';

const PORT = process.env.PORT || 3000;

function filtersFrom(url) {
  const filters = {};
  for (const [key, value] of url.searchParams) filters[key] = value;
  return filters;
}

async function handle(req, res) {
  const url = new URL(req.url, `http://localhost:${PORT}`);
  if (url.pathname === '/') {
    res.writeHead(200, { 'content-type': 'text/html' });
    res.end(await readFile(new URL('../public/index.html', import.meta.url)));
    return;
  }
  const match = url.pathname.match(/^\/reports\/([a-z]+)$/);
  if (match) {
    const report = applyFilters(getReport(match[1]), filtersFrom(url));
    res.writeHead(200, { 'content-type': 'text/html' });
    res.end(renderHtml(report));
    return;
  }
  res.writeHead(404);
  res.end('Not found');
}

http.createServer((req, res) => handle(req, res).catch(err => {
  res.writeHead(500);
  res.end(err.message);
})).listen(PORT, () => console.log(`http://localhost:${PORT}`));
