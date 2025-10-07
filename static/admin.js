// СЕТИМ --scrollbar-width В CSS ПЕРЕМЕННУЮ

function set_scrollbar_width() {
    document.documentElement.style.setProperty('--scrollbar-width', (window.innerWidth - document.documentElement.clientWidth) + "px");
}

window.addEventListener('load', () => {
    set_scrollbar_width();
});

window.addEventListener('resize', () => {
    set_scrollbar_width();
});


// ИСПРАВЛЯЕМ БАГ С collapse

for (const fieldset of document.querySelectorAll('.collapse.open')) {
    fieldset.querySelector('details').setAttribute('open', true);
}


// ЛЕВАЯ ПАНЕЛЬ В ШАПКЕ

document.querySelector('#Bars').addEventListener('click', function(e) {
    e.currentTarget.classList.toggle('_Opened');
    document.body.classList.toggle('NavSidebarOpened');
});


// CSRF

// https://docs.djangoproject.com/en/5.2/howto/csrf/#using-csrf-protection-with-ajax
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const originalFetch = window.fetch;
window.fetch = function(url, params) {
    if (!params) params = {};
    if (!params.headers) params.headers = new Headers();
    const csrftoken = getCookie('csrftoken');
    if (params.headers instanceof Headers) {
        params.headers.append('X-CSRFToken', csrftoken);
    } else if (Array.isArray(params.headers)) {
        params.headers.push(['X-CSRFToken', csrftoken]);
    } else {
        params.headers['X-CSRFToken'] = csrftoken;
    }
    return originalFetch(url, params)
};