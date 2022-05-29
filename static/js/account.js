const nav_header = document.querySelector(".nav__header");

nav_header.classList.add("account__header");

const changeButton = document.getElementById("changingEffect");
changeButton.style.display = "none"

function myFunction() {
    const desig = document.getElementById("designation");
        if (desig.style.display === "none") {
          desig.style.display = "block"
          
      } else {
        desig.style.display = "none"
        changeButton.style.display = "block"
      }
    }  


    const update = document.getElementById("updateButton")
    const desig = document.getElementById("designation")

    function newFun(){
        const input = document.getElementById("userInput").value
        desig.innerText = input
        if (changeButton.style.display === "none"){
            changeButton.style.display = "block"
        } else{
            changeButton.style.display = "none"
            desig.style.display = "block"
        }
    }

    const cancel = document.getElementById("cancelButton")

    function mySecondFunction(){
        desig.style.display = "block"
        if (changeButton.style.display === "block"){
            changeButton.style.display = "none"
        }else {
            changeButton.style.display = "block"
        }
    }
    
    
    
    // arko part
    const forprofile = () => {
    const proPix = document.querySelector("#main-image").value;

    let fileName = proPix.split("\\");
    fileName = fileName[fileName.length - 1];
  
  document.querySelector("#uploaded-image-name").innerText = fileName;
//   document.querySelector("#video-name").style.display = 'block';
}


const clickForModal = document.querySelector('.for-profile-pix');
const closeForModal = document.querySelector('.close-button');
const forModal = document.querySelector('.for-modal');

clickForModal.addEventListener('click', function(){
    document.querySelector('.overlay').style.display = 'block';
    forModal.classList.add('coming');
})
closeForModal.addEventListener('click', function(){
    document.querySelector('.overlay').style.display = 'none';
    forModal.classList.remove('coming');
   
})
   
   
   
   
    
    
    
    
    
    
    
    
    
    
    
    