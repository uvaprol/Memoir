const WEEK_DAYS = {'1': 'ПН', '2': 'ВТ', '3': 'СР', '4': 'ЧТ', '5': 'ПТ', '6': 'СБ', '7': 'ВС'}
const table_space = document.getElementById('table')

function push_data(data){
    let block = ''
    for (let week in data){
        block += `<table>
        <thead>
            <td><img src="" alt="love"></td>
            <td><h2>День</h2></td>
            <td><h2>Событие</h2></td>
            <td><h2>Ценность</h2></td>
        </thead>
        <tbody>`
        for (let day in data[week]){
            block += `<tr>
                <td>
                    <label>
                        <input type="radio" name="${week}">
                        <span></span>
                    </label>
                </td>
                <td><h2>${day} ${WEEK_DAYS[data[week][day][0]]}</h2></th>
                <td><textarea name="" id=""> ${data[week][day][1]} </textarea></td>
                <td><input type="text" name="values" list="my_values" placeholder="Выбрать"></td>
            </tr>`
        }
        block += `</tbody>
        </table>`
    }
    table_space.innerHTML += block
    areaAutoResize()
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
    const textarea = document.getElementsByTagName('textarea');
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
    }
}


window.onload = () => {
    if(localStorage.getItem('login') === null){
        window.location.replace("/")
    } else {
        get_data()
    }
}

