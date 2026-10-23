// Aplica modo e idioma antes del primer render para evitar parpadeo:
// el elegido por la persona o, si no hay, el del sistema.
(function () {
  var t = null;
  try { t = localStorage.getItem('portfolio-theme'); } catch (e) {}
  if (t !== 'musgo' && t !== 'arcilla') {
    t = matchMedia('(prefers-color-scheme: dark)').matches ? 'musgo' : 'arcilla';
  }
  document.documentElement.dataset.theme = t;

  var l = null;
  try { l = localStorage.getItem('portfolio-lang'); } catch (e) {}
  if (l !== 'es' && l !== 'en') {
    l = (navigator.language || '').toLowerCase().indexOf('es') === 0 ? 'es' : 'en';
  }
  document.documentElement.lang = l;
})();
