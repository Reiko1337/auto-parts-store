let addresses = document.querySelectorAll('input[type=radio][name=address]');

for (let i = 0; i < addresses.length; i++) {
    addresses[i].addEventListener('change', function () {
        const xhr = new XMLHttpRequest();
        const url = `/accounts/chekout/address/${this.value}/`;
        xhr.open('GET', url);
        xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                let data = JSON.parse(xhr.response);
                valueSetInput(data['address']);
            }
        }
        xhr.send();
    });
}


function valueSetInput(data) {
    document.querySelector('input[name=last_name]').value = data['last_name'];
    document.querySelector('input[name=first_name]').value = data['first_name'];
    document.querySelector('input[name=patronymic]').value = data['patronymic'];
    $('.country-select').val(data['country']).trigger('change');

    document.querySelector('input[name=region]').value = data['region'];
    document.querySelector('input[name=city]').value = data['city'];
    document.querySelector('input[type=text][name=address]').value = data['address'];

    if (data['phone_number'].startsWith('+375')) {
        $('.country-phone-select').val('Bel').trigger('change');
    } else if (data['phone_number'].startsWith('+7')) {
        $('.country-phone-select').val('ru').trigger('change');
    }

    document.querySelector('input[name=phone_number]').value = data['phone_number'];
}



