let hamburgerMenu = document.querySelector(".hamburger__menu");
let mobileNavLinks = document.querySelector(".mobile__navLinks"); 
let closeBtn = document.querySelector(".nav__close");
let bodyTag = document.querySelector("body");
let bgFixed = document.querySelector(".bg__fixed");

const playAudio = document.querySelector("#get__notified");

const getNotified = () => {
    if (playAudio) {
        if (playAudio.value) {
            if (playAudio.value === "False") {
                document.getElementById("get__notificationAudio").muted = false;
               document.getElementById("get__notificationAudio").play();
            }
        }
    }
}

getNotified();

document.addEventListener("click", (event) => {
    if (event.target.closest(".hamburger__menu")) return;
    if (event.target.closest(".mobile__navLinks")) return;
    
    mobileNavLinks.classList.remove("active__navLinks");
    bgFixed.style.display = "none";
    bodyTag.style.overflow = "visible";
})

hamburgerMenu.addEventListener('click', () => {
    mobileNavLinks.classList.add("active__navLinks");
    bgFixed.style.display = "block";
    bodyTag.style.overflow = "hidden";
});

closeBtn.addEventListener("click", () => {
    mobileNavLinks.classList.remove("active__navLinks");
    bgFixed.style.display = "none";
    bodyTag.style.overflow = "visible";
});

//   browse category js
var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("new____active____class");
    var content = this.nextElementSibling;
    if (content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "100%";
    } 
  });
}



//   more category js
var coll = document.getElementsByClassName("collapsibleMore");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("new____active____class");
    var content = this.nextElementSibling;
    if (content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "100%";
    } 
  });
}