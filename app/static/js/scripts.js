const spoiler = document.querySelectorAll('.footer__item-title')

for (let i = 0; i < spoiler.length; i++) {
    spoiler[i].addEventListener("click", function () {
        this.nextElementSibling.classList.toggle('spoiler-active')
    });
}

lightbox.option({
    'disableScrolling': true,
    'albumLabel': "Картинка %1 из %2"
})

function menuActive() {
    const a = document.querySelectorAll('.navigation [href]');
    for (i = 0; i < a.length; i++) {
        let url = new URL(a[i].href);
        if (url.pathname === document.location.pathname) {
            a[i].classList.add("active");
            break;
        }
    }
}
menuActive();
