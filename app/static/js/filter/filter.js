$(document).ready(function () {
    // $('.brand-select').select2({
    //     placeholder: "Марка автомобиля",
    //     maximumSelectionLength: 2,
    //     language: "ru",
    //     width: "100%",
    // });
    // $('.model-select').select2({
    //     placeholder: "Модель автомобиля",
    //     maximumSelectionLength: 2,
    //     language: "ru",
    //     width: "100%",
    // });
    // $('.spare-part-select').select2({
    //     placeholder: "Запчасти",
    //     maximumSelectionLength: 2,
    //     language: "ru",
    //     width: "100%",
    // });
    //
    // $('.transmission-select').select2({
    //     placeholder: "Коробка передач",
    //     maximumSelectionLength: 2,
    //     language: "ru",
    //     width: "100%",
    // });
    // $('.bodywork-select').select2({
    //     placeholder: "Кузов",
    //     maximumSelectionLength: 2,
    //     language: "ru",
    //     width: "100%",
    // });
    // $('.engine-type-select').select2({
    //     placeholder: "Тип двигателя",
    //     maximumSelectionLength: 2,
    //     language: "ru",
    //     width: "100%",
    // });
    // $('.drive-select').select2({
    //     placeholder: "Привод",
    //     maximumSelectionLength: 2,
    //     language: "ru",
    //     width: "100%",
    // });
    //
    // $('.year-from-select').select2({
    //     placeholder: "Год от",
    //     maximumSelectionLength: 2,
    //     language: "ru",
    //     width: "100px",
    // });
    // $('.year-to-select').select2({
    //     placeholder: "До",
    //     maximumSelectionLength: 2,
    //     language: "ru",
    //     width: "100px",
    // });
    //
    // $('.engine-capacity-from-select').select2({
    //     placeholder: "Объем от",
    //     maximumSelectionLength: 2,
    //     language: "ru",
    //     width: "100px",
    // });
    // $('.engine-capacity-to-select').select2({
    //     placeholder: "До",
    //     maximumSelectionLength: 2,
    //     language: "ru",
    //     width: "100px",
    // });
    //
    // $('.material-select').select2({
    //     placeholder: "Материал",
    //     maximumSelectionLength: 2,
    //     language: "ru",
    //     width: "100%",
    // });
    //
    // $('.diameter-select').select2({
    //     placeholder: "Диаметр",
    //     maximumSelectionLength: 2,
    //     language: "ru",
    //     width: "100%",
    // });
    // $('.pcd-select').select2({
    //     placeholder: "PCD",
    //     maximumSelectionLength: 2,
    //     language: "ru",
    //     width: "100%",
    // });
    //
    //
    // $('.manufacturer-select').select2({
    //     placeholder: "Производитель",
    //     maximumSelectionLength: 2,
    //     language: "ru",
    //     width: "100%",
    // });
    // $('.season-select').select2({
    //     placeholder: "Сезон",
    //     maximumSelectionLength: 2,
    //     language: "ru",
    //     width: "100%",
    // });
    // $('.width-select').select2({
    //     placeholder: "Ширина",
    //     maximumSelectionLength: 2,
    //     language: "ru",
    //     width: "100%",
    // });
    // $('.profile-select').select2({
    //     placeholder: "Профиль",
    //     maximumSelectionLength: 2,
    //     language: "ru",
    //     width: "100%",
    // });
    $('.select2-filter').select2({

        maximumSelectionLength: 2,
        language: "ru",
        width: "100%",
    });

});

$(".year-from-select").on("select2:select", function (e) {
    let year_from = document.querySelector('.year-from-select');
    let value = year_from.value

    let items = document.querySelector('.year-to-select').children

    for (i = 2; i < items.length; i++) {
        if (parseInt(value) > parseInt(items[i].value)) {
            items[i].disabled = true;
        } else {
            items[i].disabled = false;
        }
    }
});

$(".year-to-select").on("select2:select", function (e) {
    let year_to = document.querySelector('.year-to-select');
    let value = year_to.value

    let items = document.querySelector('.year-from-select').children

    for (i = 2; i < items.length; i++) {
        if (parseInt(value) < parseInt(items[i].value)) {
            items[i].disabled = true;
        } else {
            items[i].disabled = false;
        }
    }
});


$(".engine-capacity-from-select").on("select2:select", function (e) {
    let year_from = document.querySelector('.engine-capacity-from-select');
    let value = year_from.value

    let items = document.querySelector('.engine-capacity-to-select').children

    for (i = 2; i < items.length; i++) {
        if (parseFloat(value) > parseFloat(items[i].value)) {
            items[i].disabled = true;
        } else {
            items[i].disabled = false;
        }
    }
});

$(".engine-capacity-to-select").on("select2:select", function (e) {
    let year_to = document.querySelector('.engine-capacity-to-select');
    let value = year_to.value

    let items = document.querySelector('.engine-capacity-from-select').children

    for (i = 2; i < items.length; i++) {
        if (parseFloat(value) < parseFloat(items[i].value)) {
            items[i].disabled = true;
        } else {
            items[i].disabled = false;
        }
    }
});


document.querySelector('.filter__burger').addEventListener('click', function () {
    let listFilter = document.querySelector('.list__filter-items');
    listFilter.classList.toggle("filter_active");
});

const maskPrice = document.querySelectorAll('.mask__price');


for (i = 0; i < maskPrice.length; i++) {
    maskPrice[i].addEventListener('input', function (e) {
        let value = this.value;
        let valueValid = value.replace(/[^0-9.]/g, '');

        if (valueValid.split('.')[1]) {
            if (valueValid.split('.')[1].length > 2) {
                valueValid = valueValid.slice(0, -1)
            }
        }
        this.value = valueValid;
    });
}

const maskMileage = document.querySelectorAll('.mask__mileage');


for (i = 0; i < maskMileage.length; i++) {
    maskMileage[i].addEventListener('input', function (e) {
        let value = this.value;
        let valueValid = value.replace(/[^0-9]/g, '');
        this.value = valueValid;
    });
}
