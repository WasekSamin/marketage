const selectPayment = document.getElementById('selectPaymentMethod');
const paypal = document.querySelector('.paypal');
const aamarpay = document.querySelector('.ammrpay');
// const sslcommerz = document.querySelector('.sslcommerz');
const razorpay = document.querySelector('.razorpay');
const body = document.querySelector('.for-add-class');
const add = document.querySelector('.ordering');
const manualPayment = document.querySelector(".manualPayment");

const paypalButton = document.querySelector('#paypal-button-container');


selectPayment.addEventListener('click', function(){
    if (selectPayment.value === "paypal") {
        paypal.style.display = 'none';   
        aamarpay.style.display = 'none';
        // sslcommerz.style.display = 'none';
        razorpay.style.display = 'none';
        paypalButton.style.display = 'block'; 
        manualPayment.style.display = 'none';
    } else if (selectPayment.value === "AAMMR PAY") {
        aamarpay.style.display = 'block';
        paypal.style.display = 'none';
        // sslcommerz.style.display = 'none';
        razorpay.style.display = 'none';
        paypalButton.style.display = 'none';
        manualPayment.style.display = 'none';
    } else if(selectPayment.value === 'sslcommerz'){
        aamarpay.style.display = 'none';
        paypal.style.display = 'none';
        razorpay.style.display = 'none';
        // sslcommerz.style.display = 'block';
        paypalButton.style.display = 'none';
        manualPayment.style.display = 'none';

    } else if(selectPayment.value === 'razorpay' ){
        aamarpay.style.display = 'none';
        paypal.style.display = 'none';
        razorpay.style.display = 'block';
        // sslcommerz.style.display = 'none';
        paypalButton.style.display = 'none';
        manualPayment.style.display = 'none';

    } else if(selectPayment.value === 'manual_payment' ){
        aamarpay.style.display = 'none';
        paypal.style.display = 'none';
        razorpay.style.display = 'none';
        // sslcommerz.style.display = 'none';
        paypalButton.style.display = 'none'; 
        manualPayment.style.display = 'block';

    }
})