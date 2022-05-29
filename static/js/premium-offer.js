const premiumSelect = document.getElementById('premium-select');
const paypal = document.querySelector('.paypal');
const stripe = document.querySelector('.stripe');
const sslcommerz = document.querySelector('.sslcommerz');
const razorpay = document.querySelector('.razorpay');
const body = document.querySelector('.for-add-class');
const add = document.querySelector('.ordering');



const paypalButton = document.querySelector('#paypal-button-container');


premiumSelect.addEventListener('click', function(){
    if (premiumSelect.value === "paypal") {
        paypal.style.display = 'none';   
        sslcommerz.style.display = 'none';
        razorpay.style.display = 'none';
        paypalButton.style.display = 'block'; 
        stripe.style.display= 'none'; 

    } else if(premiumSelect.value === 'sslcommerz'){
        
        paypal.style.display = 'none';
        razorpay.style.display = 'none';
        sslcommerz.style.display = 'block';
        paypalButton.style.display = 'none'; 
        stripe.style.display= 'none'; 


    } else if (premiumSelect.value === "stripe") {
        paypal.style.display = 'none';
        razorpay.style.display = 'none';
        sslcommerz.style.display = 'none';
        paypalButton.style.display = 'none';
        stripe.style.display= 'block'; 
    } 
     else if(premiumSelect.value === 'razorpay' ){
        
        paypal.style.display = 'none';
        razorpay.style.display = 'block';
        sslcommerz.style.display = 'none';
        paypalButton.style.display = 'none';

    }
})