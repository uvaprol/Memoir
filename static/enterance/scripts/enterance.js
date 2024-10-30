const inputs = document.getElementsByTagName('input')
const login = inputs[0]
const password = inputs[1]

const a = document.getElementsByTagName('a')
const reset = a[0]
const reg = a[1]

const btn = document.getElementsByTagName('button')[0]

const regText = reg.getElementsByTagName('p')[0]
const btnText = btn.getElementsByTagName('h2')[0]

btn.addEventListener('click', function () {
    $.ajax({
        url: '/enter', // URL вашего API
        type: 'POST',
        data: {
            'login': $(login).val(),
            'password': $(password).val()
        },
        success: function(response) {
             window.location.replace("/memoir");
        },
        error: function(xhr, status, error) {
            alert('Не верный логин или пароль')
            console.error("Ошибка: ", error);
        }
    });
});

reg.addEventListener('click', function () {
    window.location.replace("https://t.me/trntrvtr_bot");
});

reset.addEventListener('click', function(){
    alert('Ну я хз, начни жизнь с чистого листа!')
    window.location.replace("https://t.me/trntrvtr_bot");
});

