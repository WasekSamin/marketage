// For buttons
const activeBtn = document.querySelector(".active__btn");
const lateBtn = document.querySelector(".late__btn");
const deliveredBtn = document.querySelector(".delivered__btn");
const completedBtn = document.querySelector(".completed__btn");
const cancelledBtn = document.querySelector(".cancelled__btn");
const reviewBtn = document.querySelector(".review__btn");

// For tables
const activatedTable = document.querySelector('.activated__table');
const lateTable = document.querySelector('.late__table');
const deliveredTable = document.querySelector('.delivered__table');
const completedTable = document.querySelector('.completed__table');
const cancelledTable = document.querySelector('.cancelled__table');
const reviewTable = document.querySelector(".review__table");


let orderedText = document.querySelector(".table__orderText");


activeBtn.addEventListener("click", () => {
    // For button text
    activeBtn.classList.add("active__link");
    lateBtn.classList.remove("active__link");
    deliveredBtn.classList.remove("active__link");
    completedBtn.classList.remove("active__link");
    cancelledBtn.classList.remove("active__link");
    reviewBtn.classList.remove("active__link");
    orderedText.innerHTML = "ACTIVE ORDERS";

    // For table container
    activatedTable.classList.add("show__activeTable");
    lateTable.classList.remove("show__activeTable");
    deliveredTable.classList.remove("show__activeTable");
    completedTable.classList.remove("show__activeTable");
    cancelledTable.classList.remove("show__activeTable");
    reviewTable.classList.remove("show__activeTable");
});

lateBtn.addEventListener("click", () => {
    // For button text
    activeBtn.classList.remove("active__link");
    lateBtn.classList.add("active__link");
    deliveredBtn.classList.remove("active__link");
    completedBtn.classList.remove("active__link");
    cancelledBtn.classList.remove("active__link");
    reviewBtn.classList.remove("active__link");
    orderedText.innerHTML = "LATE ORDERS";

    // For table container
    activatedTable.classList.remove("show__activeTable");
    lateTable.classList.add("show__activeTable");
    deliveredTable.classList.remove("show__activeTable");
    completedTable.classList.remove("show__activeTable");
    cancelledTable.classList.remove("show__activeTable");
    reviewTable.classList.remove("show__activeTable");
});

deliveredBtn.addEventListener("click", () => {
    // For button text
    activeBtn.classList.remove("active__link");
    lateBtn.classList.remove("active__link");
    deliveredBtn.classList.add("active__link");
    completedBtn.classList.remove("active__link");
    cancelledBtn.classList.remove("active__link");
    reviewBtn.classList.remove("active__link");
    orderedText.innerHTML = "DELIVERED ORDERS";

    // For table container
    activatedTable.classList.remove("show__activeTable");
    lateTable.classList.remove("show__activeTable");
    deliveredTable.classList.add("show__activeTable");
    completedTable.classList.remove("show__activeTable");
    cancelledTable.classList.remove("show__activeTable");
    reviewTable.classList.remove("show__activeTable");
});

completedBtn.addEventListener("click", () => {
    // For button text
    activeBtn.classList.remove("active__link");
    lateBtn.classList.remove("active__link");
    deliveredBtn.classList.remove("active__link");
    completedBtn.classList.add("active__link");
    cancelledBtn.classList.remove("active__link");
    reviewBtn.classList.remove("active__link");
    orderedText.innerHTML = "COMPLETED ORDERS";

    // For table container
    activatedTable.classList.remove("show__activeTable");
    lateTable.classList.remove("show__activeTable");
    deliveredTable.classList.remove("show__activeTable");
    completedTable.classList.add("show__activeTable");
    cancelledTable.classList.remove("show__activeTable");
    reviewTable.classList.remove("show__activeTable");
});

cancelledBtn.addEventListener("click", () => {
    // For button text
    activeBtn.classList.remove("active__link");
    lateBtn.classList.remove("active__link");
    deliveredBtn.classList.remove("active__link");
    completedBtn.classList.remove("active__link");
    cancelledBtn.classList.add("active__link");
    reviewBtn.classList.remove("active__link");
    orderedText.innerHTML = "CANCELLED ORDERS";

    // For table container
    activatedTable.classList.remove("show__activeTable");
    lateTable.classList.remove("show__activeTable");
    deliveredTable.classList.remove("show__activeTable");
    completedTable.classList.remove("show__activeTable");
    cancelledTable.classList.add("show__activeTable");
    reviewTable.classList.remove("show__activeTable");
});

reviewBtn.addEventListener("click", () => {
    // For button text
    activeBtn.classList.remove("active__link");
    lateBtn.classList.remove("active__link");
    deliveredBtn.classList.remove("active__link");
    completedBtn.classList.remove("active__link");
    cancelledBtn.classList.remove("active__link");
    reviewBtn.classList.add("active__link");
    orderedText.innerHTML = "CANCELLED ORDERS";

    // For table container
    activatedTable.classList.remove("show__activeTable");
    lateTable.classList.remove("show__activeTable");
    deliveredTable.classList.remove("show__activeTable");
    completedTable.classList.remove("show__activeTable");
    cancelledTable.classList.remove("show__activeTable");
    reviewTable.classList.add("show__activeTable");
});