const WEEK_DAYS = {'1': 'ПН', '2': 'ВТ', '3': 'СР', '4': 'ЧТ', '5': 'ПТ', '6': 'СБ', '7': 'ВС'}
const table_space = document.getElementById('table')
let dayINweek = {}
const DATE = new Date()
let YEAR = DATE.getFullYear()
let MONTH = DATE.getMonth() + 1
const textarea = document.getElementsByTagName('textarea');
const inputs = document.getElementsByName('val_input');
const checkBoxes = document.getElementsByName('checkBox');
const SET_MONTH = document.getElementsByTagName('li')
const MAIN = document.getElementsByTagName('main')[0]
const SET_MONTH_BTN = MAIN.getElementsByTagName('button')
const SET_YEAR = MAIN.getElementsByTagName('h2')[0]

function push_data(data){
    let block = ''
    for (let week in data){
        block += `<table id="week${week}">
        <thead>
            <td><img src="" alt="love"></td>
            <td><h2>День</h2></td>
            <td><h2>Событие</h2></td>
            <td><h2>Ценность</h2></td>
        </thead>
        <tbody>`
        for (let day in data[week]){
            dayINweek[day] = week
            block += `<tr>
                <td>
                    <label name="checkBox">
                        <input type="radio" name="${week}" ${(data[week][day][3] == 1)?'checked':''} id="chk_${YEAR}_${MONTH}_${day}_${week}">
                        <span></span>
                    </label>
                </td>
                <td><h2>${day} ${WEEK_DAYS[data[week][day][0]]}</h2></td>
                <td><textarea name="" id="txt_${YEAR}_${MONTH}_${day}"> ${data[week][day][1]} </textarea></td>
                <td><input type="text" name="val_input" id="val_${YEAR}_${MONTH}_${day}" list="my_values" placeholder="Выбрать" value="${(data[week][day][2] != null)?data[week][day][2]:''}"></td>
            </tr>`
        }
        block += `</tbody>
        </table>`
    }
    table_space.innerHTML += block
    areaAutoResize()
    // autoFocus()
}

function get_data(){
    $.ajax({
        url: '/memoir',
        type: 'POST',
        data: {
            'Login': localStorage.getItem('login'),
            'Password': localStorage.getItem('password'),
        },
        success: (data) => {
            console.log(data)
            push_data(data)
        },
        error: (response) => {
            alert(response.responseText)
        }
    });
}

function areaAutoResize(){
    for (area of textarea){
        if (area.scrollHeight === 48){
            area.style.height = '24px';
        }
        else{
            area.style.height = `${area.scrollHeight}px`;
        }
        area.addEventListener('input', function () {
            this.style.height = 'auto';
            this.style.height = `${this.scrollHeight - 18}px`;
          });
        area.addEventListener('blur', function () {
            this.style.color = 'red'
            console.log(this.id.slice(4))
            $.ajax({
                url: '/memoir_save',
                type: 'POST',
                data: {
                    'Login': localStorage.getItem('login'),
                    'Password': localStorage.getItem('password'),
                    'Date': this.id.slice(4),
                    'Memoir': this.value,
                },
                success: () => {
                    this.style.color = 'black'
                },
                error: (response) => {
                    console.log(response.responseText)
                }
            });
          });
    }
    for (input of inputs){
        input.addEventListener('blur', function () {
            this.style.color = 'red'
            $.ajax({
                url: '/value_save',
                type: 'POST',
                data: {
                    'Login': localStorage.getItem('login'),
                    'Password': localStorage.getItem('password'),
                    'Date': this.id.slice(4),
                    'Value': this.value,
                },
                success: () => {
                    this.style.color = 'black'
                },
                error: (response) => {
                    console.log(response.responseText)
                }
            });
        });
    }
    for (checkBox of checkBoxes){
        for (input of checkBox.getElementsByTagName('input')){
            input.addEventListener('input', function () {
                $.ajax({
                    url: '/point_save',
                    type: 'POST',
                    data: {
                        'Login': localStorage.getItem('login'),
                        'Password': localStorage.getItem('password'),
                        'Date': this.id.slice(4),
                        'Value': this.value,
                    },
                    success: () => {
                        console.log('success')
                    },
                    error: (response) => {
                        console.log(response.responseText)
                    }
                });
            })
        }
    }
}

function set_nav(){
    for (m of SET_MONTH){
        m.addEventListener('click', function () {
            console.log(this.id)
        })
    }
    for (btn of SET_MONTH_BTN){
        btn.addEventListener('click', function () {
            YEAR = eval(`${YEAR} ${this.name} 1`)
            SET_YEAR.textContent = YEAR
        })
    }
}

function autoFocus(){
    console.log('in development')
    // let now = new Date();
    // window.location.href = `/memoir#week${dayINweek[now.getDate()]}`;
}

window.onload = () => {
    if(localStorage.getItem('login') === null){
        window.location.replace("/")
    } else {
        set_nav()
        get_data()
    }
}