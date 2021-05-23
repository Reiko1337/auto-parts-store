document.addEventListener("DOMContentLoaded", function (event) {
    window.onresize = function () {
        showItems();
    };
});


let start = 0;

showItems();



document.querySelector('.pagination__previous').addEventListener('click', function () {

    let itemWidth = document.querySelector('.product__similar-item').clientWidth;
    let containerWidth = document.querySelector('.container').offsetWidth;

    let numItems = 3;
    
    if(containerWidth <= 1430 && containerWidth > 760){
        numItems = 3;
    }
    else if(containerWidth <= 760 && containerWidth > 500){
        numItems = 2;
    }
    else if(containerWidth <= 500){
        numItems = 1;
    }

    start -= numItems;
    showItems();
})

document.querySelector('.pagination__next').addEventListener('click', function () {
    let itemWidth = document.querySelector('.product__similar-item').clientWidth;
    let containerWidth = document.querySelector('.container').offsetWidth;

    let numItems = 3;

    if(containerWidth <= 1430 && containerWidth > 760){
        numItems = 3;
    }
    else if(containerWidth <= 760 && containerWidth > 500){
        numItems = 2;
    }
    else if(containerWidth <= 500){
        numItems = 1;
    }

    start += numItems;
    showItems();
});

function showItems() {
    let similarItems = document.querySelector('.product__similar-items').children;
    let itemWidth = document.querySelector('.product__similar-item').clientWidth;
    let containerWidth = document.querySelector('.container').offsetWidth;  

    let numItems = 2;
    if(containerWidth <= 1430 && containerWidth > 760){
        numItems = 2;
    }
    else if(containerWidth <= 760 && containerWidth > 500){
        numItems = 1;
    }
    else if(containerWidth <= 500){
        numItems = 0;
    }

    let last = numItems + start;

     if (similarItems.length > 3){
        if (start <= 0) {
            document.querySelector('.pagination__previous').classList.add('pagination_active');
        }
        else {
            document.querySelector('.pagination__previous').classList.remove('pagination_active');
        }

        if (last >= similarItems.length || last == similarItems.length - 1) {
            document.querySelector('.pagination__next').classList.add('pagination_active');
        }
        else {
            document.querySelector('.pagination__next').classList.remove('pagination_active');
        }
    }
    else{
       document.querySelector('.product__similar-pagination').style.display = 'none';
    }

    if (last >= similarItems.length) {
        last = similarItems.length;
        numItems = 3;
        if(containerWidth <= 1430 && containerWidth > 760){
            numItems = 3;
        }
        else if(containerWidth <= 760 && containerWidth > 500){
            numItems = 2;
        }
        else if(containerWidth <= 500){
            numItems = 1;
        }

        start = last - numItems;
    }
    if (start <= 0) {
        start = 0;
        numItems = 2;
        if(containerWidth <= 1430 && containerWidth > 760){
            numItems = 2;
        }
        else if(containerWidth <= 760 && containerWidth > 500){
            numItems = 1;
        }
        else if(containerWidth <= 500){
            numItems = 0;
        }
        last = numItems;

    }

    for (let i = 0; i < similarItems.length; i++) {
        if (i >= start && i <= last) {
            similarItems[i].style.display = 'block';
        }
        else {
            similarItems[i].style.display = 'none';
        }
    }
}
