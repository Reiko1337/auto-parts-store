$(document).ready(function () {
    $('.country-select').select2({
        placeholder: "Страна",
        maximumSelectionLength: 2,
        minimumResultsForSearch: Infinity,
        language: "ru",
        width: "100%",
    });
      $('.country-phone-select').select2({
        maximumSelectionLength: 2,
        minimumResultsForSearch: Infinity,
        language: "ru",
        width: "100%",
    });
});


let phone = document.querySelector('#phoneMask');


if(phone.value.startsWith('+375')){
     $('.country-phone-select').val('Bel').trigger('change');
}
else if(phone.value.startsWith('+7')){
    $('.country-phone-select').val('ru').trigger('change');
}


jQuery (function ($) {  
    $(function() {
      function maskPhone() {
        var country = $('.country-phone-select').val();
        switch (country) {
          case "ru":
            $("#phoneMask").click(function(){
                $(this).setCursorPosition(3);
            }).mask("+7(999) 999-99-99");
            break;
          case "Bel":
            $("#phoneMask").click(function(){
                $(this).setCursorPosition(5);
            }).mask("+375(99) 999-99-99");
            break;          
        }    
      }
      maskPhone();
      $('.country-phone-select').change(function() {
        maskPhone();
      });
    });
  });


  $.fn.setCursorPosition = function(pos) {
    if ($(this).get(0).setSelectionRange) {
      $(this).get(0).setSelectionRange(pos, pos);
    } else if ($(this).get(0).createTextRange) {
      var range = $(this).get(0).createTextRange();
      range.collapse(true);
      range.moveEnd('character', pos);
      range.moveStart('character', pos);
      range.select();
    }
  };