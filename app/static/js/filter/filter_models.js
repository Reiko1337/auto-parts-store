$(".brand-select").change(function () {
    let brandSlug = $(this).val();
    const pageUrl = new URL(document.location.href);
    let chapter = pageUrl.pathname.split('/')[3]
    $.ajax({
        url: '/filter-models/',
        data: {
            'brand': brandSlug,
            'chapter': chapter
        },
        success: function (data) {
            $(".model-select").html(data);
        }
    });
});