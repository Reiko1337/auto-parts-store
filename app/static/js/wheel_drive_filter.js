selectValue();

$(".car-brand-select").on("select2:select", function (e) {
    let dataSelect = getValueSelect();
    ajaxRequest(dataSelect);
});
$(".model-select").on("select2:select", function (e) {
    let dataSelect = getValueSelect();
    ajaxRequest(dataSelect);
});
$(".diameter-select").on("select2:select", function (e) {
    let dataSelect = getValueSelect();
    ajaxRequest(dataSelect);
});
$(".material-select").on("select2:select", function (e) {
    let dataSelect = getValueSelect();
    ajaxRequest(dataSelect);
});
$(".pcd-select").on("select2:select", function (e) {
    let dataSelect = getValueSelect();
    ajaxRequest(dataSelect);
});


function ajaxRequest(value) {
    const xhr = new XMLHttpRequest();
    const url = `/wheels-drive/filter/?brand=${value.brand}&model=${value.model}&diameter=${value.diameter}&material=${value.material}&pcd=${value.pcd}`;
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
    let diameter = document.querySelector('.diameter-select');
    let material = document.querySelector('.material-select');
    let pcd = document.querySelector('.pcd-select');
    if (brand.value === '*') {
        brand.value = '';
    }
    if (model.value === '*') {
        model.value = '';
    }
    if (diameter.value === '*') {
        diameter.value = '';
    }
    if (material.value === '*') {
        material.value = '';
    }
    if (pcd.value === '*') {
        pcd.value = '';
    }
    return {
        'brand': brand.value,
        'model': model.value,
        'diameter': diameter.value,
        'material': material.value,
        'pcd': pcd.value
    }
}

function selectValue() {
    const pageUrl = new URL(document.location.href);
    let brandSelect = document.querySelector('.car-brand-select');
    let modelSelect = document.querySelector('.model-select');
    let diameterSelect = document.querySelector('.diameter-select');
    let materialSelect = document.querySelector('.material-select');
    let pcdSelect = document.querySelector('.pcd-select');
    brandSelect.value = pageUrl.pathname.split('/')[2];
    modelSelect.value = pageUrl.pathname.split('/')[3];

    diameterSelect.value = pageUrl.searchParams.get('diameter');
    materialSelect.value = pageUrl.searchParams.get('material');
    pcdSelect.value = pageUrl.searchParams.get('pcd');
}

document.querySelector('.filter__btn').addEventListener('click', function () {
    let data = getValueSelect()
    let url = "/wheels-drive/";
    if (data.brand) {
        url = `/wheels-drive/${data.brand}/`
        if (data.model) {
            url = `/wheels-drive/${data.brand}/${data.model}/`
        }
    }
    url += `?&diameter=${data.diameter}&material=${data.material}&pcd=${data.pcd}`;
    this.href = url;
})
