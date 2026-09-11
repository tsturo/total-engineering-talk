import { parseScene, applyScene } from './scene.js';

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
  if (beat) beat.textContent = (el && el.dataset.beat) || '';
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
