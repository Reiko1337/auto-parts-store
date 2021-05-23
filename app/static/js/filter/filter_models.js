const brandSelect = $(".brand-select");

brandSelect.on("select2:select", function (e) {
    const xhr = new XMLHttpRequest();
    const url = `/filter-models/?brand=${this.value}`;
    xhr.open('GET', url);
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            let data = JSON.parse(xhr.response);
            const models = data.models;
            let html = "";
            if (models.length != 0) {
                html += "<option value=\"\"></option>" +
                    "<option value='*'>Модель автомобиля</option>";
                for (i = 0; i < models.length; i++) {
                    html += `<option value='${models[i].slug}'>${models[i].title}</option>`
                }
            }
            document.querySelector('.model-select').innerHTML = html;
        }
    }
    xhr.send();
});
