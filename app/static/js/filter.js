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
    $('.diameter-select').select2({
        placeholder: "Диаметр",
        maximumSelectionLength: 2,
        language: "ru",
        width: null
    });
    $('.material-select').select2({
        placeholder: "Материал",
        maximumSelectionLength: 2,
        language: "ru",
        width: null
    });
    $('.pcd-select').select2({
        placeholder: "PCD (мм)",
        maximumSelectionLength: 2,
        language: "ru",
        width: null
    });
    $('.transmission-select').select2({
        placeholder: "Коробка передач",
        maximumSelectionLength: 2,
        language: "ru",
        width: null
    });
    $('.bodywork-select').select2({
        placeholder: "Кузов",
        maximumSelectionLength: 2,
        language: "ru",
        width: null
    });
    $('.engine-type-select').select2({
        placeholder: "Тип двигателя",
        maximumSelectionLength: 2,
        language: "ru",
        width: null
    });
    $('.drive-select').select2({
        placeholder: "Привод",
        maximumSelectionLength: 2,
        language: "ru",
        width: null
    });

      $('.checkout-address-select').select2({
        placeholder: "Адрес доставки",
        minimumResultsForSearch: Infinity,
        maximumSelectionLength: 2,
        language: "ru",
        width: '100%'
    });
    $('.checkout-shipping-select').select2({
        placeholder: "Способ получения",
        minimumResultsForSearch: Infinity,
        maximumSelectionLength: 2,
        language: "ru",
        width: '100%'
    });
    $('.checkout-payment-select').select2({
        placeholder: "Способ оплаты",
        minimumResultsForSearch: Infinity,
        maximumSelectionLength: 2,
        language: "ru",
        width: '100%'
    });
});
