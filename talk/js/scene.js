export function parseScene(text) {
  const ids = new Set();
  for (const token of (text || '').trim().split(/\s+/)) {
    if (!token) continue;
    if (token.startsWith('-')) ids.delete(token.slice(1));
    else ids.add(token.replace(/^\+/, ''));
  }
  return ids;
}

export function applyScene(root, ids) {
  for (const el of root.querySelectorAll('[data-obj]')) {
    el.classList.toggle('on', ids.has(el.dataset.obj));
  }
  mirrorStates(root);
}

function mirrorStates(root) {
  for (const el of root.querySelectorAll('[data-obj][data-mirror]')) {
    const target = document.getElementById(el.dataset.mirror);
    if (target) target.classList.toggle('on-' + el.dataset.obj, el.classList.contains('on'));
  }
}
