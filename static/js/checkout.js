const confirmButton = document.getElementById("confirm_button")

confirmButton.style.display = "none"

const fname = document.getElementById ("f_name")
const lname = document.getElementById ("l_name")

fname.addEventListener ("keyup", function(){
    if (fname.value.length >  0){
        confirmButton.style.display = "block"
    }else{
        confirmButton.style.display = "none"
    }
})
lname.addEventListener ("keyup", function(){
    if (lname.value.length >  0){
        confirmButton.style.display = "block"
    }else{
        confirmButton.style.display = "none"
    }
})