
// // for humburger menu
// let hamburgerMenuArko = document.querySelector(".hamburger_menu");
// let mobileNavLinksArko = document.querySelector(".mobile__navLinks");
// let closeBtnArko = document.querySelector(".nav__close");
// let bodyTagArko = document.querySelector("body");


// let overlay = document.querySelector(".overlay");
// let backGround = document.querySelector(".bg__fixed");

// hamburgerMenuArko.addEventListener('click', () => {
//     mobileNavLinksArko.classList.add("active__navLinks");
//     overlay.style.display = 'block';
//     bodyTagArko.style.overflow = 'hidden';
//     // backGround.style.display = 'block';

// });

// closeBtnArko.addEventListener("click", () => {
//     mobileNavLinksArko.classList.remove("active__navLinks");
//     overlay.style.display = 'none';
//     bodyTagArko.style.overflow = 'visible';
//     // backGround.style.display = 'none';

// });


// //   browse category js
// var coll = document.getElementsByClassName("collapsible");
// var i;

// for (i = 0; i < coll.length; i++) {
//   coll[i].addEventListener("click", function() {
//     this.classList.toggle("new____active____class");
//     var content = this.nextElementSibling;
//     if (content.style.maxHeight){
//       content.style.maxHeight = null;
//     } else {
//       content.style.maxHeight = content.scrollHeight + "100%";
//     }
//   });
// }


// // search input suggetion

// // $("#pageSelectBtn").on('click', function () {
                    
// //     var editing_page = $("#editing_page").val();

// //     if($('#editing_page_list option').filter(function(){
// //         return this.value === editing_page;
// //     }).length) {
// //         //send ajax request
// //         alert(editing_page);
// //     }
// // });


const expendPremiumOffer = (e) => {
    document.querySelector(`.expand__premiumOfferIcon${e}`).classList.toggle(`active__premiumOfferIcon${e}`);
    
    if (document.querySelector(`.active__premiumOfferIcon${e}`)) {
        document.querySelector(`.active__premiumOfferIcon${e}`).querySelector("svg").setAttribute("data-icon", "bx:bx-minus");
        document.querySelector(`.get__expandOffer${e}.hide__expandOffer`).style.visibility = "visible";
        document.querySelector(`.get__expandOffer${e}.hide__expandOffer`).style.opacity = 1;
        document.querySelector(`.get__expandOffer${e}.hide__expandOffer`).style.height = "auto";
    } else {
        document.querySelector(`.expand__premiumOfferIcon${e}`).querySelector("svg").setAttribute("data-icon", "carbon:add");
        document.querySelector(`.get__expandOffer${e}.hide__expandOffer`).style.visibility = "hidden";
        document.querySelector(`.get__expandOffer${e}.hide__expandOffer`).style.opacity = 0;
        document.querySelector(`.get__expandOffer${e}.hide__expandOffer`).style.height = 0;
    }
    
}



// search bar suggestion
var search = document.querySelector('#search');
var results = document.querySelector('#searchresults');
var templateContent = document.querySelector('#resultstemplate').content;
search.addEventListener('keyup', function handler(event) {
    while (results.children.length) results.removeChild(results.firstChild);
    var inputVal = new RegExp(search.value.trim(), 'i');
    var clonedOptions = templateContent.cloneNode(true);
    var set = Array.prototype.reduce.call(clonedOptions.children, function searchFilter(frag, el) {
 if (inputVal.test(el.textContent) && frag.children.length < 10) frag.appendChild(el);
        return frag;
    }, document.createDocumentFragment());
    results.appendChild(set);
});








const CloseButtonForHeader = document.querySelector(".close-button-on-slider-bar");
const sideBarClickButton = document.querySelector(".for-mob-hamburger-menu");

const mainSideBar = document.querySelector(".mobile-version-side-bar")
const overlayBack = document.querySelector(".overlay-background")

document.addEventListener("click", (event) => {
    if (event.target.closest(".for-mob-hamburger-menu")) return;
    if (event.target.closest(".mobile-version-side-bar")) return;
    
    mainSideBar.classList.remove("click-on-menu")
    overlayBack.style.display = 'none';
});


sideBarClickButton.addEventListener("click", function(){
    mainSideBar.classList.add("click-on-menu")
    overlayBack.style.display = 'block';
})
CloseButtonForHeader.addEventListener("click", function(){
    mainSideBar.classList.remove("click-on-menu")
    overlayBack.style.display = 'none';

})

 
//   browse category js

var coll = document.getElementsByClassName("buyer__collapsible");
var i;
for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("buyer___activeNow");
    var content = this.nextElementSibling;
    if (content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "100%";
    }
  });
}



        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
