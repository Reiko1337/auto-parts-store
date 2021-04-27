selectValue();

$(".car-brand-select").on("select2:select", function (e) {
    let dataSelect = getValueSelect();
    ajaxRequest(dataSelect);
});
$(".model-select").on("select2:select", function (e) {
    let dataSelect = getValueSelect();
    ajaxRequest(dataSelect);
});
$(".transmission-select").on("select2:select", function (e) {
    let dataSelect = getValueSelect();
    ajaxRequest(dataSelect);
});
$(".bodywork-select").on("select2:select", function (e) {
    let dataSelect = getValueSelect();
    ajaxRequest(dataSelect);
});
$(".engine-type-select").on("select2:select", function (e) {
    let dataSelect = getValueSelect();
    ajaxRequest(dataSelect);
});
$(".drive-select").on("select2:select", function (e) {
    let dataSelect = getValueSelect();
    ajaxRequest(dataSelect);
});


function ajaxRequest(value) {
    const xhr = new XMLHttpRequest();
    const url = `/kits-car/filter/?brand=${value.brand}&model=${value.model}&transmission=${value.transmission}&bodywork=${value.bodywork}&engineType=${value.engineType}&drive=${value.drive}`;
    xhr.open('GET', url);
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            let data = JSON.parse(xhr.response);
            document.querySelector('.filter__btn').innerHTML = `Показать (${data.count})`
        }
    }
    xhr.send();
}


function getValueSelect() {
    let brand = document.querySelector('.car-brand-select');
    let model = document.querySelector('.model-select');
    let transmission = document.querySelector('.transmission-select');
    let bodywork = document.querySelector('.bodywork-select');
    let engineType = document.querySelector('.engine-type-select');
    let drive = document.querySelector('.drive-select');
    if (brand.value === '*') {
        brand.value = '';
    }
    if (model.value === '*') {
        model.value = '';
    }
    if (transmission.value === '*') {
        transmission.value = '';
    }
    if (bodywork.value === '*') {
        bodywork.value = '';
    }
    if (engineType.value === '*') {
        engineType.value = '';
    }
    if (drive.value === '*') {
        drive.value = '';
    }
    return {
        'brand': brand.value,
        'model': model.value,
        'transmission': transmission.value,
        'bodywork': bodywork.value,
        'engineType': engineType.value,
        'drive': drive.value
    }
}

function selectValue() {
    const pageUrl = new URL(document.location.href);
    let brandSelect = document.querySelector('.car-brand-select');
    let modelSelect = document.querySelector('.model-select');
    let transmissionSelect = document.querySelector('.transmission-select');
    let bodyworkSelect = document.querySelector('.bodywork-select');
    let engineTypeSelect = document.querySelector('.engine-type-select');
    let driveSelect = document.querySelector('.drive-select');

    brandSelect.value = pageUrl.pathname.split('/')[2];
    modelSelect.value = pageUrl.pathname.split('/')[3];

    transmissionSelect.value = pageUrl.searchParams.get('transmission');
    bodyworkSelect.value = pageUrl.searchParams.get('bodywork');
    engineTypeSelect.value = pageUrl.searchParams.get('engineType');
    driveSelect.value = pageUrl.searchParams.get('drive');
}

document.querySelector('.filter__btn').addEventListener('click', function () {
    let data = getValueSelect()
    let url = "/kits-car/";
    if (data.brand) {
        url = `/kits-car/${data.brand}/`
        if (data.model) {
            url = `/kits-car/${data.brand}/${data.model}/`
        }
    }
    url += `?transmission=${data.transmission}&bodywork=${data.bodywork}&engineType=${data.engineType}&drive=${data.drive}`;
    this.href = url;
})
