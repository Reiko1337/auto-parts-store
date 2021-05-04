function menuActive() {
    const a = document.querySelectorAll('.profile__navigation [href]');
    for (i = 0; i < a.length; i++) {
        let url = new URL(a[i].href);
        if (url.pathname === document.location.pathname) {
            a[i].parentElement.classList.add("profile__navigation-link-active");
            break;
        }
    }
}
menuActive();
