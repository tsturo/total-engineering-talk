const poster = document.getElementById('poster');
const NAV_KEYS = new Set(['PageDown', 'PageUp', 'ArrowLeft', 'ArrowRight', ' ', 'ArrowUp', 'ArrowDown']);
const SUPPRESSED_KEYS = new Set(['F5', 'Escape']);

function sceneOf(el) {
  return parseScene(el.getAttribute('data-scene'));
}

function currentScene(step) {
  const visible = step.querySelectorAll('.substep-visible');
  return visible.length ? sceneOf(visible[visible.length - 1]) : sceneOf(step);
}

function transitionDuration() {
  const root = document.getElementById('impress');
  const value = Number(root.getAttribute('data-transition-duration'));
  return Number.isFinite(value) ? value : 1000;
}

function lastSceneOf(step) {
  const substeps = step.querySelectorAll('.substep');
  return substeps.length ? sceneOf(substeps[substeps.length - 1]) : sceneOf(step);
}

function revealAllSubsteps(step) {
  const count = step.querySelectorAll('.substep').length;
  for (let i = 0; i < count; i++) document.dispatchEvent(new CustomEvent('impress:substep:show'));
}

function installSceneWiring() {
  let goingBack = false;
  window.impress.addPreStepLeavePlugin(e => {
    goingBack = e.detail.reason === 'prev';
  }, 0);
  document.addEventListener('impress:stepleave', e => {
    if (!e.detail || !e.detail.next) return;
    applyScene(poster, goingBack ? lastSceneOf(e.detail.next) : sceneOf(e.detail.next));
  });
  document.addEventListener('impress:stepenter', e => {
    clearStagger();
    applyBeat(null);
    if (goingBack) {
      revealAllSubsteps(e.target);
      applyScene(poster, currentScene(e.target));
    } else {
      applyScene(poster, sceneOf(e.target));
    }
  });
  document.addEventListener('impress:substep:enter', e => enterSubstep(e.detail.substep));
  document.addEventListener('impress:substep:leave', e => { clearStagger(); const v = e.target.querySelectorAll('.substep-visible'); applyBeat(v[v.length - 1]); applyScene(poster, currentScene(e.target)); });
}

let staggerTimers = [];

function clearStagger() {
  for (const t of staggerTimers) clearTimeout(t);
  staggerTimers = [];
}

function applyBeat(el) {
  const beat = document.querySelector('#pitch .beat');
  if (!beat) return;
  const text = beat.querySelector('.beat-text');
  const paper = beat.querySelector('.paper');
  const pin = beat.querySelector('.pin');
  const pointer = beat.querySelector('.pointer');
  const label = (el && el.dataset.beat) || '';
  text.textContent = label;
  if (!el || !el.dataset.beatX) return;
  const ax = Number(el.dataset.beatX), ay = Number(el.dataset.beatY);
  const side = el.dataset.beatSide || 'above';
  const pad = 40, h = 120;
  text.setAttribute('x', 0); text.setAttribute('y', 0);
  const w = text.getBBox().width + pad * 2;
  const offsets = { above: [-w / 2, -h - 260], below: [-w / 2, 260], left: [-w - 200, -h / 2], right: [200, -h / 2] };
  const [dx, dy] = offsets[side] || offsets.above;
  const x = ax + dx, y = ay + dy;
  paper.setAttribute('x', x); paper.setAttribute('y', y); paper.setAttribute('width', w); paper.setAttribute('height', h); paper.setAttribute('rx', 6);
  text.setAttribute('x', x + pad); text.setAttribute('y', y + h * 0.68);
  pin.setAttribute('cx', x + w / 2); pin.setAttribute('cy', y);
  const anchors = { above: [x + w / 2, y + h], below: [x + w / 2, y], left: [x + w, y + h / 2], right: [x, y + h / 2] };
  const [px, py] = anchors[side] || anchors.above;
  pointer.setAttribute('d', `M${px} ${py} L${ax} ${ay}`);
}

function enterSubstep(sub) {
  clearStagger();
  applyBeat(sub);
  const groups = sub.dataset.stagger;
  if (!groups) { applyScene(poster, sceneOf(sub)); return; }
  const shows = groups.split('|').map(g => g.trim().split(/\s+/));
  const hides = (sub.dataset.staggerHide || '').split('|').map(g => g.trim().split(/\s+/).filter(Boolean));
  const gap = Number(sub.dataset.staggerMs) || 1000;
  const full = sceneOf(sub);
  const current = new Set(full);
  for (const g of shows) for (const id of g) current.delete(id);
  for (const g of hides) for (const id of g) current.add(id);
  applyScene(poster, current);
  shows.forEach((g, i) => {
    staggerTimers.push(setTimeout(() => {
      for (const id of g) current.add(id);
      for (const id of (hides[i] || [])) current.delete(id);
      applyScene(poster, current);
    }, gap * (i + 1)));
  });
}

function installClickerSafety() {
  let busy = false;
  window.addEventListener('keydown', e => {
    if (SUPPRESSED_KEYS.has(e.key)) {
      e.preventDefault();
      e.stopImmediatePropagation();
      return;
    }
    if (!NAV_KEYS.has(e.key)) return;
    if (busy) {
      e.preventDefault();
      e.stopImmediatePropagation();
      return;
    }
    busy = true;
    setTimeout(() => { busy = false; }, transitionDuration() + 50);
  }, true);
}

function applyUrlModes() {
  const params = new URLSearchParams(location.search);
  const root = document.getElementById('impress');
  if (params.has('print') || params.has('nomotion') || matchMedia('(prefers-reduced-motion: reduce)').matches) {
    root.setAttribute('data-transition-duration', '0');
    document.documentElement.classList.add('no-motion');
  }
}

function prefixTargetTimes() {
  for (const step of document.querySelectorAll('.step[data-target]')) {
    const notes = step.querySelector('.notes');
    if (notes) notes.insertAdjacentHTML('afterbegin', `<p><b>Target ${step.dataset.target}</b></p>`);
  }
}

applyUrlModes();
prefixTargetTimes();
installSceneWiring();
installClickerSafety();
window.impress().init();
