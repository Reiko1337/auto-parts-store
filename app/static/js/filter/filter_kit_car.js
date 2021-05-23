selectValue();

$(".brand-select").on("select2:select", function (e) {
   ajaxFunctionSend();
});
$(".model-select").on("select2:select", function (e) {
    ajaxFunctionSend();
});
$(".transmission-select").on("select2:select", function (e) {
   ajaxFunctionSend();
});
$(".bodywork-select").on("select2:select", function (e) {
   ajaxFunctionSend();
});
$(".engine-type-select").on("select2:select", function (e) {
  ajaxFunctionSend();
});
$(".drive-select").on("select2:select", function (e) {
   ajaxFunctionSend();
});

$(".year-from-select").on("select2:select", function (e) {
   ajaxFunctionSend();
});
$(".year-to-select").on("select2:select", function (e) {
   ajaxFunctionSend();
});

$(".engine-capacity-from-select").on("select2:select", function (e) {
   ajaxFunctionSend();
});
$(".engine-capacity-to-select").on("select2:select", function (e) {
  ajaxFunctionSend();
});

let mileageInput = document.querySelector('.list__filter-input-container_mileage').children;
mileageInput[0].addEventListener('input', function () {
  ajaxFunctionSend();
});
mileageInput[1].addEventListener('input', function () {
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


const urlAjax = '/list/kit-car';

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
    if (fieldsInput.brand.value === '*') {fieldsInput.brand.value = '';}
    if (fieldsInput.model.value === '*') {fieldsInput.model.value = '';}
    if (fieldsInput.transmission.value === '*') {fieldsInput.transmission.value = '';}
    if (fieldsInput.bodywork.value === '*') {fieldsInput.bodywork.value = '';}
    if (fieldsInput.engineType.value === '*') {fieldsInput.engineType.value = '';}
    if (fieldsInput.drive.value === '*') {fieldsInput.drive.value = '';}
    if (fieldsInput.yearFrom.value === '*') {fieldsInput.yearFrom.value = '';}
    if (fieldsInput.yearTo.value === '*') {fieldsInput.yearTo.value = '';}
    if (fieldsInput.engineCapacityFrom.value === '*') {fieldsInput.engineCapacityFrom.value = '';}
    if (fieldsInput.engineCapacityTo.value === '*') {fieldsInput.engineCapacityTo.value = '';}

    return {
        'brand': fieldsInput.brand.value,
        'model': fieldsInput.model.value,
        'transmission': fieldsInput.transmission.value,
        'bodywork': fieldsInput.bodywork.value,
        'engineType': fieldsInput.engineType.value,
        'drive': fieldsInput.drive.value,
        'yearFrom': fieldsInput.yearFrom.value,
        'yearTo': fieldsInput.yearTo.value,
        'engineCapacityFrom': fieldsInput.engineCapacityFrom.value,
        'engineCapacityTo': fieldsInput.engineCapacityTo.value,
        'mileageFrom': fieldsInput.mileageInput[0].value.toString(),
        'mileageTo': fieldsInput.mileageInput[1].value.toString(),
        'priceFrom': fieldsInput.pricesInput[0].value.toString(),
        'priceTo': fieldsInput.pricesInput[1].value.toString()
    }
}

function selectValue() {
    const pageUrl = new URL(document.location.href);
    let fieldsInput = getInputForm();

    fieldsInput.brand.value = pageUrl.pathname.split('/')[3];
    fieldsInput.model.value = pageUrl.pathname.split('/')[4];

    fieldsInput.transmission.value = pageUrl.searchParams.get('transmission');
    fieldsInput.bodywork.value = pageUrl.searchParams.get('bodywork');
    fieldsInput.engineType.value = pageUrl.searchParams.get('engineType');
    fieldsInput.drive.value = pageUrl.searchParams.get('drive');

    fieldsInput.yearFrom.value = pageUrl.searchParams.get('yearFrom');
    fieldsInput.yearTo.value = pageUrl.searchParams.get('yearTo');

    setValueRangeInput(fieldsInput.yearFrom, fieldsInput.yearTo);

    fieldsInput.engineCapacityFrom.value = pageUrl.searchParams.get('engineCapacityFrom');
    fieldsInput.engineCapacityTo.value = pageUrl.searchParams.get('engineCapacityTo');

    setValueRangeInput(fieldsInput.engineCapacityFrom, fieldsInput.engineCapacityTo);

    fieldsInput.mileageInput[0].value = pageUrl.searchParams.get('mileageFrom')
    fieldsInput.mileageInput[1].value = pageUrl.searchParams.get('mileageTo')

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


function setValueRangeInput(from, to) {
    let from_select = from;
    let from_value = from_select.value;

    let to_select = to;
    let to_value = to_select.value;

    for (i = 2; i < to_select.length; i++) {
        if (parseFloat(from_value) > parseFloat(to_select[i].value)) {
            to_select[i].disabled = true;
        } else {
            to_select[i].disabled = false;
        }
    }

    for (i = 2; i < from_select.length; i++) {
        if (parseFloat(to_value) < parseFloat(from_select[i].value)) {
            from_select[i].disabled = true;
        } else {
            from_select[i].disabled = false;
        }
    }
}



function getInputForm(){
    let brandSelect = document.querySelector('.brand-select');
    let modelSelect = document.querySelector('.model-select');
    let transmissionSelect = document.querySelector('.transmission-select');
    let bodyworkSelect = document.querySelector('.bodywork-select');
    let engineTypeSelect = document.querySelector('.engine-type-select');
    let driveSelect = document.querySelector('.drive-select');
    let yearFrom = document.querySelector('.year-from-select');
    let yearTo = document.querySelector('.year-to-select');
    let pricesInput = document.querySelector('.list__filter-input-container_price').children;
    let mileageInput = document.querySelector('.list__filter-input-container_mileage').children;
    let engineCapacityFrom = document.querySelector('.engine-capacity-from-select');
    let engineCapacityTo = document.querySelector('.engine-capacity-to-select');

    return {
        'brand': brandSelect,
        'model': modelSelect,
        'transmission': transmissionSelect,
        'bodywork': bodyworkSelect,
        'engineType': engineTypeSelect,
        'drive': driveSelect,
        'yearFrom': yearFrom,
        'yearTo': yearTo,
        'pricesInput': pricesInput,
        'mileageInput': mileageInput,
        'engineCapacityFrom': engineCapacityFrom,
        'engineCapacityTo': engineCapacityTo,
    }
}