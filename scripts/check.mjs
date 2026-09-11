import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
const sceneSrc = readFileSync(new URL('../talk/js/scene.js', import.meta.url), 'utf8');
const parseScene = new Function('window', sceneSrc + '; return parseScene;')({});

const html = readFileSync(new URL('../talk/index.html', import.meta.url), 'utf8');
const objIds = new Set([...html.matchAll(/data-obj="([^"]+)"/g)].map(m => m[1]));
const scenes = [...html.matchAll(/data-scene="([^"]*)"/g)].map(m => m[1]);
const steps = [...html.matchAll(/<div[^>]*class="step[^"]*"[^>]*>/g)].map(m => m[0]);
const stepIds = steps.map(tag => (tag.match(/id="([^"]+)"/) || [])[1]);
const problems = [];

for (const scene of scenes) {
  for (const id of parseScene(scene)) {
    if (!objIds.has(id)) problems.push(`scene references unknown object: ${id}`);
  }
}
for (const [i, tag] of steps.entries()) {
  if (!stepIds[i]) problems.push(`step ${i} has no id`);
  for (const attr of ['data-x', 'data-y', 'data-scale', 'data-scene']) {
    if (!tag.includes(attr + '=')) problems.push(`step ${stepIds[i] || i} lacks ${attr}`);
  }
}
if (new Set(stepIds).size !== stepIds.length) problems.push('duplicate step ids');
if (steps.length === 0) problems.push('no steps');
const notesCount = (html.match(/class="notes"/g) || []).length;
if (notesCount < steps.length) problems.push(`${steps.length - notesCount} steps without notes`);

const rootStart = html.indexOf('<div id="impress"');
let depth = 0;
let rootEnd = -1;
for (const m of html.slice(rootStart).matchAll(/<div\b[^>]*>|<\/div>/g)) {
  depth += m[0].startsWith('<div') ? 1 : -1;
  if (depth === 0) { rootEnd = rootStart + m.index + m[0].length; break; }
}
const stepsInRoot = (html.slice(rootStart, rootEnd).match(/class="step/g) || []).length;
if (stepsInRoot !== steps.length) problems.push(`only ${stepsInRoot} of ${steps.length} steps are inside #impress: a div is unbalanced`);

for (const p of new Set(problems)) console.error(p);
console.log(problems.length ? 'check failed' : `ok: ${steps.length} steps, ${objIds.size} objects, ${scenes.length} scenes`);
process.exit(problems.length ? 1 : 0);
