function checked(id){
    const inputs = document.getElementsByName('myRadio')
    const input = document.getElementById(id)
    for (i of inputs){
        console.log(i, input)
        if (i != input){
            i.checked = false
        }
    }
}