function box_checked(id){
    const input = document.getElementById(id)
    const inputs = document.getElementsByName('myRadio')
    const spans = document.getElementsByTagName('span')
    const span = document.getElementById('s_'+id)
    event.preventDefault()
    if (input.checked == false){       
        for (let i = 0; i < inputs.length; i++){
            inputs[i].checked = false
            spans[i].style.width = '0px'
            spans[i].style.height = '0px'
        }
        input.checked = true
        span.style.width = '12px'
        span.style.height = '12px'
    }
    
}

function areaAutoResize(){
    const textarea = document.getElementsByTagName('textarea');
    for (area of textarea){
        area.style.height = area.scrollHeight - 22 + 'px';
        area.addEventListener('input', function () {
            this.style.height = 'auto';
            this.style.height = `${this.scrollHeight - 18}px`;
          });
    }
}


window.onload = () => {
    if(localStorage.getItem('user') != null){
        areaAutoResize()
    }else{
        window.location.replace("https://t.me/trntrvtr_bot");
    }    
}

