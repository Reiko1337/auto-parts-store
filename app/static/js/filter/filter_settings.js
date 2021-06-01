$(document).ready(function () {
    $('.select2-filter').select2({
        maximumSelectionLength: 2,
        language: "ru",
        width: "100%",
    });
    $('.select2-filter-between').select2({
        maximumSelectionLength: 2,
        language: "ru",
        width: "100px",
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



