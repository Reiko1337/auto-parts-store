selectValue();

$(".car-brand-select").on("select2:select", function (e) {
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

function ajaxRequest(value) {
    const xhr = new XMLHttpRequest();
    const url = `/auto-parts/filter/?brand=${value.brand}&model=${value.model}&part=${value.autoPart}`;
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
    let autoPart = document.querySelector('.spare-part-select');
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
    }
}

function selectValue() {
    const pageUrl = new URL(document.location.href);
    let brandSelect = document.querySelector('.car-brand-select');
    let modelSelect = document.querySelector('.model-select');
    let autoPareSelect = document.querySelector('.spare-part-select');
    brandSelect.value = pageUrl.pathname.split('/')[2];
    modelSelect.value = pageUrl.pathname.split('/')[3];
    if (autoPareSelect) {
        autoPareSelect.value = pageUrl.searchParams.get('part');
    }
}

document.querySelector('.filter__btn').addEventListener('click', function () {
    let data = getValueSelect()
    let url = "/auto-parts/";
    if (data.brand) {
        url = `/auto-parts/${data.brand}/`
        if (data.model) {
            url = `/auto-parts/${data.brand}/${data.model}/`
        }
    }
    url += `?part=${data.autoPart}`;
    this.href = url;
})
