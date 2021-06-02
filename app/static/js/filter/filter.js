$(".brand-select").change(function () {
    let brandSlug = $(this).val();
    const pageUrl = new URL(document.location.href);
    let chapter = pageUrl.pathname.split('/')[3]
    $.ajax({
        url: '/ajax/filter-models/',
        data: {
            'brand': brandSlug,
            'chapter': chapter
        },
        success: function (data) {
            $(".model-select").html(data);
        }
    });
});
$(document).ready(function () {
    $(".select2-filter").change(function () {
        $.ajaxRequest();
    });
    $(".list__filter-input-container").on('input', function () {
        $.ajaxRequest();
    });

    $.getValueForm = function () {
        let dataValue = {}
        let selectForm = $(".select2-filter");
        let inputForm = $(".list__filter-input-container").children().not('span');
        $.each(selectForm, function (index, value) {
            let selectValue = $(value).val();
            if (selectValue === '*') {
                selectValue = '';
            }
            dataValue[$(value).attr('name')] = selectValue;
        })
        $.each(inputForm, function (index, value) {
            dataValue[$(value).attr('name')] = $(value).val().replace(',', '.');
        })
        return dataValue;
    };


    $.getUrlFilter = function () {
        return $('input[name=ajaxURL]').val();
    };


    $.ajaxRequest = function () {
        let dataValue = $.getValueForm();
        const pageUrl = new URL(document.location.href);
        let chapter = pageUrl.pathname.split('/')[3];
        dataValue['chapter'] = chapter;
        $.ajax({
            url: $.getUrlFilter() + 'filter/',
            data: dataValue,
            success: function (data) {
                $('.list__filter-button').text(`Найдено (${data.count})`);
            }
        });
    };
});

$.getSearchParams = function () {
    let dataValue = $.getValueForm();
    let searchParams = '';
    for (let key in dataValue) {
        if (key !== 'brand' && key !== 'model') {
            searchParams += `${key}=${dataValue[key]}&`;
        }
    }
    return searchParams.slice(0, -1).toString();
};


$('.list__filter-button').click(function () {
    let dataValue = $.getValueForm();
    let url = $.getUrlFilter();
    if (dataValue.brand) {
        url += `${dataValue.brand}/`
        if (dataValue.model) {
            url += `${dataValue.model}/`
        }
    }
    url += `?${$.getSearchParams()}`;
    $(this).attr("href", url);
});
