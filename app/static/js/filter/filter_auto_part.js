selectValue();

$(".brand-select").on("select2:select", function (e) {
    let dataSelect = getValueSelect();
    ajaxRequest(dataSelect);
});
$(".model-select").on("select2:select", function (e) {
    let dataSelect = getValueSelect();
    ajaxRequest(dataSelect);
});
$(".spare-part-select").on("select2:select", function (e) {
    let dataSelect = getValueSelect();
    ajaxRequest(dataSelect);
});

let pricesInput = document.querySelector('.list__filter-input-container_price').children;
pricesInput[0].addEventListener('input', function () {
    let dataSelect = getValueSelect();
    ajaxRequest(dataSelect);
});
pricesInput[1].addEventListener('input', function () {
    let dataSelect = getValueSelect();
    ajaxRequest(dataSelect);
});


function ajaxRequest(value) {
    const xhr = new XMLHttpRequest();
    const url = `/list/spare-part/${value.chapter}/filter/?brand=${value.brand}&model=${value.model}&part=${value.autoPart}&priceFrom=${value.priceFrom}&priceTo=${value.priceTo}`;
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
    const pageUrl = new URL(document.location.href);
    let chapter = pageUrl.pathname.split('/')[3]

    let brand = document.querySelector('.brand-select');
    let model = document.querySelector('.model-select');
    let autoPart = document.querySelector('.spare-part-select');

    let pricesInput = document.querySelector('.list__filter-input-container_price').children;

    if (brand.value === '*') {
        brand.value = '';
    }
    if (model.value === '*') {
        model.value = '';
    }
    if (autoPart.value === '*') {
        autoPart.value = '';
    }
    return {
        'brand': brand.value,
        'model': model.value,
        'autoPart': autoPart.value,
        'priceFrom': pricesInput[0].value.toString(),
        'priceTo': pricesInput[1].value.toString(),
        'chapter': chapter,
    }
}


function selectValue() {
    const pageUrl = new URL(document.location.href);
    let brandSelect = document.querySelector('.brand-select');
    let modelSelect = document.querySelector('.model-select');
    let autoPareSelect = document.querySelector('.spare-part-select');
    let pricesInput = document.querySelector('.list__filter-input-container_price').children;

    brandSelect.value = pageUrl.pathname.split('/')[4];
    modelSelect.value = pageUrl.pathname.split('/')[5];

    if (autoPareSelect) {
        autoPareSelect.value = pageUrl.searchParams.get('part');
    }
    pricesInput[0].value = pageUrl.searchParams.get('priceFrom')
    pricesInput[1].value = pageUrl.searchParams.get('priceTo')

}

document.querySelector('.list__filter-button').addEventListener('click', function () {
    let data = getValueSelect()
    let url = `/list/spare-part/${data.chapter}/`;
    if (data.brand) {
        url = `/list/spare-part/${data.chapter}/${data.brand}/`
        if (data.model) {
            url = `/list/spare-part/${data.chapter}/${data.brand}/${data.model}/`
        }
    }
    url += `?part=${data.autoPart}&priceFrom=${data.priceFrom}&priceTo=${data.priceTo}`;
    this.href = url;
})
