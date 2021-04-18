$(document).ready(function () {
    $('.car-brand-select').select2({
        placeholder: "Марка автомобиля",
        maximumSelectionLength: 2,
        language: "ru",
        width: null,
    });
    $('.model-select').select2({
        placeholder: "Модель автомобиля",
        maximumSelectionLength: 2,
        language: "ru",
        width: null
    });
    $('.spare-part-select').select2({
        placeholder: "Название запчасти",
        maximumSelectionLength: 2,
        language: "ru",
        width: null
    });

    const carBrandSelect = $(".car-brand-select");
    const modelSelect = $(".model-select");
    const sparePartSelect = $(".spare-part-select");

    carBrandSelect.on("select2:select", function (e) {
        let dataSelect = getValueSelect();
        ajaxGenerateModelList(dataSelect);

    });
    modelSelect.on("select2:select", function (e) {
        let dataSelect = getValueSelect();
        ajaxRequest(dataSelect);
    });
    sparePartSelect.on("select2:select", function (e) {
        let dataSelect = getValueSelect();
        ajaxRequest(dataSelect);
    });
});

selectValue();

function ajaxRequest(value) {
    const xhr = new XMLHttpRequest();
    const url = `/filter-models/?brand=${value.brand}&model=${value.model}&part=${value.autoPart}`;
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

function ajaxGenerateModelList(value) {
    const xhr = new XMLHttpRequest();
    const url = `/filter-models/?brand=${value.brand}&model=*&part=${value.autoPart}`;
    xhr.open('GET', url);
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            let data = JSON.parse(xhr.response);
            document.querySelector('.filter__btn').innerHTML = `Показать (${data.count})`
            const models = data.models;
            let html = "";
            if (models.length != 0) {
                html += "<option value=\"\"></option>" +
                    "<option value='*'>Все модели автомобилей</option>";
                for (i = 0; i < models.length; i++) {
                    html += `<option value='${models[i].slug}'>${models[i].title}</option>`
                }
            }
            document.querySelector('.model-select').innerHTML = html;
        }
    }
    xhr.send();
}

function getValueSelect() {
    let brand = document.querySelector('.car-brand-select');
    let model = document.querySelector('.model-select');
    let autoPart = document.querySelector('.spare-part-select');
    return {'brand': brand.value, 'model': model.value, 'autoPart': autoPart.value}
}

function selectValue() {
    const pageUrl = new URL(document.location.href);
    let brandSelect = document.querySelector('.car-brand-select');
    let modelSelect = document.querySelector('.model-select');
    let autoPareSelect = document.querySelector('.spare-part-select');
    brandSelect.value = pageUrl.searchParams.get('brand');
    modelSelect.value = pageUrl.searchParams.get('model');
    autoPareSelect.value = pageUrl.searchParams.get('part');
}

document.querySelector('.filter__btn').addEventListener('click', function () {
    let data = getValueSelect()
    this.href = `/auto-parts/?brand=${data.brand}&model=${data.model}&part=${data.autoPart}`;
})
