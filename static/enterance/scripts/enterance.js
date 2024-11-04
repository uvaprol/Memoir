const inputs = document.getElementsByTagName('input')
const login = inputs[0]
const password = inputs[1]
const mode = inputs[2]
const email = inputs[3]

const btn = document.getElementsByTagName('button')[0]

function make_relocation(){
    localStorage.setItem('login', $(login).val());
    localStorage.setItem('password', $(password).val());
    window.location.replace('/memoir')
}

btn.addEventListener('click', function () {
    $.ajax({
        url: '/',
        type: 'POST',
        data: {
            'Mode': mode.checked,
            'Login': $(login).val(),
            'Password': $(password).val(),
            'Email': $(email).val()
        },
        success: () => {
            make_relocation()
        },
        error: (response) => {
            alert(response.responseText)
        }
    });
});

