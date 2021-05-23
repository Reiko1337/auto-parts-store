selectValue();

$(".brand-select").on("select2:select", function (e) {
    ajaxFunctionSend();
});
$(".model-select").on("select2:select", function (e) {
    ajaxFunctionSend();
});
$(".diameter-select").on("select2:select", function (e) {
    ajaxFunctionSend();
});
$(".material-select").on("select2:select", function (e) {
    ajaxFunctionSend();
});
$(".pcd-select").on("select2:select", function (e) {
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


const urlAjax = '/list/wheel';

function getFilterUrl(){
    let value = getValueSelect();
    let resultUrl = ``

    for (let key in value){
        if (key !== 'brand' && key !== 'model'){
            resultUrl +=`${key}=${value[key]}&`;
        }

    }
    return resultUrl.slice(0, -1).toString();
}


function ajaxRequest(value) {
    const xhr = new XMLHttpRequest();
    const url = `${urlAjax}/filter/?brand=${value.brand}&model=${value.model}&${getFilterUrl()}`;
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

    if (fieldsInput.brand.value === '*') {
        fieldsInput.brand.value = '';
    }
    if (fieldsInput.model.value === '*') {
        fieldsInput.model.value = '';
    }
    if (fieldsInput.diameter.value === '*') {
        fieldsInput.diameter.value = '';
    }
    if (fieldsInput.material.value === '*') {
        fieldsInput.material.value = '';
    }
    if (fieldsInput.pcd.value === '*') {
        fieldsInput.pcd.value = '';
    }
    return {
        'brand': fieldsInput.brand.value,
        'model': fieldsInput.model.value,
        'diameter': fieldsInput.diameter.value,
        'material': fieldsInput.material.value,
        'pcd': fieldsInput.pcd.value,
        'priceFrom': fieldsInput.pricesInput[0].value.toString(),
        'priceTo': fieldsInput.pricesInput[1].value.toString()
    }
}

function selectValue() {
    const pageUrl = new URL(document.location.href);
    let fieldsInput = getInputForm();


    fieldsInput.brand.value = pageUrl.pathname.split('/')[3];
    fieldsInput.model.value = pageUrl.pathname.split('/')[4];

    fieldsInput.diameter.value = pageUrl.searchParams.get('diameter');
    fieldsInput.material.value = pageUrl.searchParams.get('material');
    fieldsInput.pcd.value = pageUrl.searchParams.get('pcd');

    fieldsInput.pricesInput[0].value = pageUrl.searchParams.get('priceFrom')
    fieldsInput.pricesInput[1].value = pageUrl.searchParams.get('priceTo')
}

document.querySelector('.list__filter-button').addEventListener('click', function () {
    let data = getValueSelect()
    let url = `${urlAjax}/`;
    if (data.brand) {
        url = `${urlAjax}/${data.brand}/`
        if (data.model) {
            url = `${urlAjax}/${data.brand}/${data.model}/`
        }
    }
    url += `?${getFilterUrl()}`;
    this.href = url;
})


function getInputForm(){
    let brandSelect = document.querySelector('.brand-select');
    let modelSelect = document.querySelector('.model-select');
    let diameterSelect = document.querySelector('.diameter-select');
    let materialSelect = document.querySelector('.material-select');
    let pcdSelect = document.querySelector('.pcd-select');
    let pricesInput = document.querySelector('.list__filter-input-container_price').children;

    return {
        'brand': brandSelect,
        'model': modelSelect,
        'material': materialSelect,
        'diameter': diameterSelect,
        'pcd': pcdSelect,
        'pricesInput': pricesInput,
    }
}
