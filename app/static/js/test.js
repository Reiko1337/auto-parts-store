$(document).ready(function () {
    $('#id_car_model').select2({
        width: "260px"
    });
    $('#id_car_model').on("select2:open", function (){
        $('.select2-container').addClass('select2-container--admin-autocomplete');
    });
    $('#id_car_model').next().addClass('select2-container--admin-autocomplete');
});
// select2-container select2-container--default            select2-container--open
// select2-container select2-container--admin-autocomplete select2-container--open