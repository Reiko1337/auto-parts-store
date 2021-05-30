if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
    document.querySelector('body').classList.add('touch');
} else {
    document.querySelector('body').classList.add('mouse');
}
document.querySelector('.navigation__item_spare').addEventListener('click', function () {
    document.querySelector('.sub-navigation__list-container').classList.toggle("sub-navigation__list_active");
});
document.querySelector('.navigation__item_wheel-tires').addEventListener('click', function () {
    this.children[1].classList.toggle("sub-navigation__list_active");
});

document.querySelector('.header__burger').addEventListener('click', function () {
    let navigation = document.querySelectorAll('.navigation');
    for (i = 0; i < 2; i++) {
        navigation[i].classList.toggle("navigation_active");
    }
});