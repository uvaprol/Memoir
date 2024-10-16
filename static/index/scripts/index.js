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