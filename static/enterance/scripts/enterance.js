const inputs = document.getElementsByTagName('input')
const login = inputs[0]
const password = inputs[1]

const a = document.getElementsByTagName('a')
const reset = a[0]
const reg = a[1]

const btn = document.getElementsByTagName('button')[0]

const regText = reg.getElementsByTagName('p')[0]
const btnText = btn.getElementsByTagName('h2')[0]

console.log(regText)
let enterKey = true

btn.addEventListener('click', function () {
    console.log(enterKey);
    console.log(login);
    console.log(password);
    if (enterKey){
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
    } else {
        $.get('/reg', {
                    'login'    : $(login).val(),
                    'password' : $(password).val(),
                }, (response) => {
                    if (response === 'true'){
                        window.location.replace("https://t.me/trntrvtr_bot");
                    } else {
                        alert('Логин уже занят')
                    }
                })
    }
});

reg.addEventListener('click', function () {
    if (enterKey){
        btnText.textContent = 'Регестрация'
        regText.textContent = 'Войти'
    } else {
        btnText.textContent = 'Войти'
        regText.textContent = 'Зарегестртроваться'
    }
    enterKey = !enterKey
});

reset.addEventListener('click', function(){
    alert('Ну я хз, начни жизнь с чистого листа!')
});

