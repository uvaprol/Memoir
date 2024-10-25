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
    $.get('/enter', {
            'login'    : $(login).val(),
            'password' : $(password).val(),
        }, (response) => {
            if (response === 'true'){
                window.location.replace("/");
            } else {
                alert('Не верный логин или пароль')
            }
        })
});

reg.addEventListener('click', function () {
    window.location.replace("https://t.me/trntrvtr_bot");
});

reset.addEventListener('click', function(){
    alert('Ну я хз, начни жизнь с чистого листа!')
    window.location.replace("https://t.me/trntrvtr_bot");
});

