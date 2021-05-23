document.querySelector('.footer__list-item_spare').addEventListener('click', function () {
    this.firstElementChild.classList.toggle("footer__list-item_spare-spoiler");
    document.querySelector('.footer__list-sub').classList.toggle("footer__list-sub_active");
});


const spoiler = document.querySelectorAll('.footer__info-title')

for (let i = 0; i < spoiler.length; i++) {
    spoiler[i].addEventListener("click", function () {
        this.classList.toggle('footer__info-title_spoiler');
        this.nextElementSibling.classList.toggle('spoiler-active');
    });
}