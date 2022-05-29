// click placed ordered 
const placeOrder = document.querySelector('.place-order');

// click on going project
const ongoingProject = document.querySelector('.ongoing-project');

// place order details
const forPlaceOrder = document.querySelector('.for-placed-order');

// for ongoing project
const ongoingDiv = document.querySelector('.for-ongoing');

// diamone for place order
// const placeArrow = document.querySelector('.diamone-place-order');


// diamond for ongoing project
// const ongoingArrow = document.querySelector('.diamone-ongoing-project');


placeOrder.addEventListener('click', function(){
    forPlaceOrder.style.display = 'block';
    placeOrder.style.color = '#264fc2';
    ongoingDiv.style.display = 'none';
    ongoingProject.style.color = '#000';
    placeOrder.style.borderColor = '#000';
    ongoingProject.style.borderColor = '#f7f7f7';
})

ongoingProject.addEventListener('click', function(){
    forPlaceOrder.style.display = 'none';
    ongoingDiv.style.display = 'block';
    ongoingProject.style.color = '#264fc2';
    placeOrder.style.color = '#000';
    ongoingProject.style.borderColor = '#000';
    placeOrder.style.borderColor = '#f7f7f7';
})