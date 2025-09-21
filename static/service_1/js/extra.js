// Отправка формы поиска
$(document).on('submit', '.apply-form', function (e) {
    e.preventDefault();
    $('#text-form').empty();
    $('#text-form').css("color", "#fff");
    $('#text-form').append('Ваша форма успешно отправлена. Скоро, мы свяжемся с вами!');

});