selectValue();


$(".diameter-select").on("select2:select", function (e) {
    ajaxFunctionSend();
});
$(".manufacturer-select").on("select2:select", function (e) {
    ajaxFunctionSend();
});
$(".season-select").on("select2:select", function (e) {
    ajaxFunctionSend();
});
$(".width-select").on("select2:select", function (e) {
    ajaxFunctionSend();
});
$(".profile-select").on("select2:select", function (e) {
    ajaxFunctionSend();
});


let pricesInput = document.querySelector('.list__filter-input-container_price').children;
pricesInput[0].addEventListener('input', function () {
  ajaxFunctionSend();
});
pricesInput[1].addEventListener('input', function () {
   ajaxFunctionSend();
});

function ajaxFunctionSend(){
     let dataSelect = getValueSelect();
    ajaxRequest(dataSelect);
}


const urlAjax = '/list/tire';

function getFilterUrl(){
    let value = getValueSelect();
    let resultUrl = ``

    for (let key in value){
        resultUrl +=`${key}=${value[key]}&`;
    }
    return resultUrl.slice(0, -1).toString();
}


function ajaxRequest(value) {
    const xhr = new XMLHttpRequest();
    const url = `${urlAjax}/filter/?${getFilterUrl()}`;
    xhr.open('GET', url);
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            let data = JSON.parse(xhr.response);
            document.querySelector('.list__filter-button').innerHTML = `Найдено (${data.count})`
        }
    }
    xhr.send();
}


function getValueSelect() {
    let fieldsInput = getInputForm();

    if (fieldsInput.manufacturer.value === '*') {
        fieldsInput.manufacturer.value = '';
    }
    if (fieldsInput.diameter.value === '*') {
        fieldsInput.diameter.value = '';
    }
    if (fieldsInput.season.value === '*') {
        fieldsInput.season.value = '';
    }
    if (fieldsInput.width.value === '*') {
        fieldsInput.width.value = '';
    }
    if (fieldsInput.profile.value === '*') {
        fieldsInput.profile.value = '';
    }
    return {
        'manufacturer': fieldsInput.manufacturer.value,
        'season': fieldsInput.season.value,
        'diameter': fieldsInput.diameter.value,
        'width': fieldsInput.width.value,
        'profile': fieldsInput.profile.value,
        'priceFrom': fieldsInput.pricesInput[0].value.toString(),
        'priceTo': fieldsInput.pricesInput[1].value.toString()
    }
}

function selectValue() {
    const pageUrl = new URL(document.location.href);
    let fieldsInput = getInputForm();


    fieldsInput.manufacturer.value = pageUrl.searchParams.get('manufacturer');
    fieldsInput.season.value = pageUrl.searchParams.get('season');

    fieldsInput.diameter.value = pageUrl.searchParams.get('diameter');
    fieldsInput.width.value = pageUrl.searchParams.get('width');
    fieldsInput.profile.value = pageUrl.searchParams.get('profile');

    fieldsInput.pricesInput[0].value = pageUrl.searchParams.get('priceFrom')
    fieldsInput.pricesInput[1].value = pageUrl.searchParams.get('priceTo')
}

document.querySelector('.list__filter-button').addEventListener('click', function () {
    let data = getValueSelect()
    let url = `${urlAjax}/`;
    url += `?${getFilterUrl()}`;
    this.href = url;
})


function getInputForm(){
    let manufacturerSelect = document.querySelector('.manufacturer-select');
    let seasonSelect = document.querySelector('.season-select');
    let diameterSelect = document.querySelector('.diameter-select');
    let widthSelect = document.querySelector('.width-select');
    let profileSelect = document.querySelector('.profile-select');
    let pricesInput = document.querySelector('.list__filter-input-container_price').children;

    return {
        'manufacturer': manufacturerSelect,
        'season': seasonSelect,
        'width': widthSelect,
        'diameter': diameterSelect,
        'profile': profileSelect,
        'pricesInput': pricesInput,
    }
}
