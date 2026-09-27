document.addEventListener('DOMContentLoaded', function () {
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.getElementById('site-nav');

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      const open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(open));
    });
  }

  document.querySelectorAll('.alert-close').forEach(function (button) {
    button.addEventListener('click', function () {
      button.closest('.alert').remove();
    });
  });
});
