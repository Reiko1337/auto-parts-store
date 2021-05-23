let buttonsClose = document.querySelectorAll('.message__close');


for (let i = 0; i < buttonsClose.length; i++){
    buttonsClose[i].addEventListener('click', function(){
        buttonsClose[i].parentElement.classList.add('message__content_remove');
        checkCountMessage();
    });
}

function checkCountMessage(){
    let messageList = document.querySelector('.message__list');
    let messageClose = document.querySelectorAll('.message__content_remove');

    if(messageList.children.length == messageClose.length){
        messageList.style.margin = '0';
    }
}
