// Отправка формы поиска
$(document).on('submit', '.apply-form', function (e) {
    e.preventDefault();
    $('#text-callback').empty();
    $('#text-callback').append('Ваша форма успешно отправлена. Скоро, мы свяжемся с вами!');
    $('html, body').animate({
        scrollTop: $('#form').offset().top
    }, 1000);
});