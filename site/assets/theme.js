/* Apply before paint. A stored choice wins; otherwise follow the device. */
(() => {
  let preference = null;
  try { preference = localStorage.getItem('bioinformatics-theme'); } catch (_) {}
  const chosen = preference === 'light' || preference === 'dark';
  const dark = chosen ? preference === 'dark' : window.matchMedia('(prefers-color-scheme: dark)').matches;
  document.documentElement.dataset.theme = dark ? 'dark' : 'light';
})();
