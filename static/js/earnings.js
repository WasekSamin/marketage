
// document.getElementById("inputnew").addEventListener("change", function() {
//   let inpVal = parseInt(this.value);
// //   console.log(inpVal);
//   if (inpVal < 5) {
//     $('#div1').html('Price cannot be less then 5 USD');
//     $(this).val('');
//   }
//   else
//     {
//         $('#div1').html('');
//     }
// });




// for bkash, paypal and nagad 
const bkash = document.getElementById("bkash____div")
const paypal = document.getElementById("paypal____div")
const nagad = document.getElementById("nagad____div")



bkash.style.display = "none"
paypal.style.display = "none"
nagad.style.display = "none"

function changeFunc(elem) {
    // var selectBox = document.getElementById("selectBox");
    // console.log(elem.value);
    if (elem.value === "paypal") {
        bkash.style.display = "none"
        paypal.style.display = "flex"
        nagad.style.display = "none"
        
    } else if (elem.value === "bkash"){
        bkash.style.display = "flex"
        paypal.style.display = "none"
        nagad.style.display = "none"
        
    } else if (elem.value === "nagad"){
        bkash.style.display = "none"
        paypal.style.display = "none"
        nagad.style.display = "flex"
        
    } else if (elem.value === "withdraw"){
        bkash.style.display = "none"
        paypal.style.display = "none"
        nagad.style.display = "none"
    }
    
    
   }











