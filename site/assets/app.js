(() => {
  const root = document.documentElement;
  const toggle = document.querySelector('[data-theme-toggle]');
  const media = window.matchMedia('(prefers-color-scheme: dark)');
  let explicitlyChosen = false;
  try { explicitlyChosen = ['light', 'dark'].includes(localStorage.getItem('bioinformatics-theme')); } catch (_) {}
  function updateToggle() {
    const dark = root.dataset.theme === 'dark';
    toggle.setAttribute('aria-label', `Switch to ${dark ? 'light' : 'dark'} mode`);
    toggle.setAttribute('aria-pressed', String(dark));
    toggle.querySelector('[data-theme-label]').textContent = dark ? 'Light mode' : 'Dark mode';
  }
  updateToggle();
  toggle.addEventListener('click', () => {
    root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    explicitlyChosen = true;
    try { localStorage.setItem('bioinformatics-theme', root.dataset.theme); } catch (_) {}
    updateToggle();
  });
  media.addEventListener('change', event => {
    if (!explicitlyChosen) {
      root.dataset.theme = event.matches ? 'dark' : 'light';
      updateToggle();
    }
  });

  const menu = document.querySelector('[data-menu-toggle]');
  const sidebar = document.querySelector('.sidebar');
  const backdrop = document.querySelector('[data-backdrop]');
  function setMenu(open) {
    root.classList.toggle('menu-open', open);
    menu.setAttribute('aria-expanded', String(open));
    menu.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
    const mobile = window.matchMedia('(max-width: 900px)').matches;
    sidebar.inert = mobile && !open;
    backdrop.hidden = !open;
  }
  setMenu(false);
  menu.addEventListener('click', () => setMenu(!root.classList.contains('menu-open')));
  backdrop.addEventListener('click', () => { setMenu(false); menu.focus(); });
  document.addEventListener('keydown', event => {
    if (!root.classList.contains('menu-open')) return;
    if (event.key === 'Escape') { setMenu(false); menu.focus(); }
    if (event.key === 'Tab') {
      const items = [menu, ...sidebar.querySelectorAll('a[href], button')];
      const current = items.indexOf(document.activeElement);
      const direction = event.shiftKey ? -1 : 1;
      const next = current < 0 ? 0 : (current + direction + items.length) % items.length;
      event.preventDefault();
      items[next].focus();
    }
  });
  sidebar.querySelectorAll('a').forEach(link => link.addEventListener('click', () => setMenu(false)));
  window.matchMedia('(max-width: 900px)').addEventListener('change', () => setMenu(false));

  const form = document.querySelector('[data-resource-filters]');
  if (!form) return;
  const search = form.querySelector('[name=q]');
  const track = form.querySelector('[name=track]');
  const level = form.querySelector('[name=level]');
  const cards = [...document.querySelectorAll('[data-resource]')];
  const count = document.querySelector('[data-result-count]');
  const empty = document.querySelector('[data-empty]');
  const params = new URLSearchParams(location.search);
  for (const field of [search, track, level]) {
    const value = params.get(field.name);
    if (value !== null && (field === search || [...field.options].some(option => option.value === value))) field.value = value;
  }
  function filter(updateURL = true) {
    const words = search.value.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
    let visible = 0;
    for (const card of cards) {
      const matches = words.every(word => card.dataset.search.includes(word)) && (!track.value || card.dataset.tracks.split(' ').includes(track.value)) && (!level.value || card.dataset.level === level.value);
      card.hidden = !matches;
      if (matches) visible++;
    }
    count.textContent = `${visible} ${visible === 1 ? 'resource' : 'resources'}`;
    empty.hidden = visible !== 0;
    if (updateURL) {
      const next = new URLSearchParams();
      for (const field of [search, track, level]) if (field.value.trim()) next.set(field.name, field.value.trim());
      history.replaceState(null, '', `${location.pathname}${next.size ? '?' + next.toString() : ''}${location.hash}`);
    }
  }
  form.addEventListener('submit', event => event.preventDefault());
  search.addEventListener('input', () => filter());
  track.addEventListener('change', () => filter());
  level.addEventListener('change', () => filter());
  document.querySelector('[data-clear-filters]').addEventListener('click', () => {
    search.value = ''; track.value = ''; level.value = ''; filter(); search.focus();
  });
  filter(false);
})();
