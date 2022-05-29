// click placed ordered 
const placeOrder = document.querySelector('.place-order');

// click on going project
const ongoingProject = document.querySelector('.ongoing-project');

// place order details
const forPlaceOrder = document.querySelector('.for-placed-order');

// for ongoing project
const ongoingDiv = document.querySelector('.for-ongoing');

// for premium order
const premiumOffer = document.querySelector(".premium-order");
const forPremium = document.querySelector('.for-premium');

// diamone for place order
// const placeArrow = document.querySelector('.diamone-place-order');


// diamond for ongoing project
// const ongoingArrow = document.querySelector('.diamone-ongoing-project');


placeOrder.addEventListener('click', function(){
    forPremium.style.display = 'none';
    forPlaceOrder.style.display = 'block';
    placeOrder.style.color = '#264fc2';
    ongoingDiv.style.display = 'none';
    ongoingProject.style.color = '#000';
    placeOrder.style.borderColor = '#000';
    ongoingProject.style.borderColor = '#f7f7f7';
    premiumOffer.style.borderColor = '#f7f7f7';
    premiumOffer.style.color = '#000';


})

ongoingProject.addEventListener('click', function(){
    forPlaceOrder.style.display = 'none';
    ongoingDiv.style.display = 'block';
    forPremium.style.display = 'none';
    premiumOffer.style.borderColor = '#f7f7f7';
    ongoingProject.style.color = '#264fc2';
    placeOrder.style.color = '#000';
    ongoingProject.style.borderColor = '#000';
    placeOrder.style.borderColor = '#f7f7f7';
    premiumOffer.style.color = '#000';

})
premiumOffer.addEventListener('click', function(){
    forPremium.style.display = 'block';
    forPlaceOrder.style.display = 'none';
    ongoingDiv.style.display = 'none';
    ongoingProject.style.borderColor = '#f7f7f7';
    placeOrder.style.borderColor = '#f7f7f7';
    premiumOffer.style.borderColor = '#000';
    premiumOffer.style.color = '#264fc2';
    ongoingProject.style.color = '#000';
    placeOrder.style.color = '#000';

})