// Сетим --scrollbar-width в CSS Переменную
document.documentElement.style.setProperty('--scrollbar-width', (window.innerWidth - document.documentElement.clientWidth) + "px");

// Исправляем баг с collapse
for (const fieldset of document.querySelectorAll('.collapse.open')) {
    fieldset.querySelector('details').setAttribute('open', true);
}

// Левая панель в Шапке
document.querySelector('#Bars').addEventListener('click', function(e) {
    e.currentTarget.classList.toggle('Opened');
    document.body.classList.toggle('NavSidebarOpened');
});