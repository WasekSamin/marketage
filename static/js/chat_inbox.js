// azim message eror showing for mail and phone
function ValidateEmail(inputText)
{
    console.log(inputText.value);
    // inputText.value.includes(".com") || inputText.value.includes(".net") || inputText.value.includes(".io") || inputText.value.includes(".org") || inputText.value.includes(".xyz") || inputText.value.includes(".in") || inputText.value.includes(".pk") || inputText.value.includes(".kl") || inputText.value.includes(".uk") || inputText.value.includes(".au") || inputText.value.includes(".uae")
    if ((inputText.value.includes("@") && inputText.value.length > 1) || inputText.value.includes("zero") || inputText.value.includes("one") || inputText.value.includes("two") || inputText.value.includes("three") || inputText.value.includes("four") || inputText.value.includes("five") || inputText.value.includes("six") || inputText.value.includes("seven") || inputText.value.includes("eight") || inputText.value.includes("nine") || inputText.value.includes("ten")) {
        alert("Hey Wait! Do not try to communicate using Mail or phone! Thank you!");
        inputText.value = "";
        return;
    }
    try {
        const get_num = parseInt(inputText.value);
        
        if (Number.isInteger(get_num) && inputText.value.length >= 7) {
            alert("Hey Wait! Do not try to communicate using phone! Thank you!");
            inputText.value = "";
            return;
        }
        
    } catch(err) {
        return;
    }
}

function matchName(inputVal) {
    var input, ul, li, a, i, txtValue, p;
    input = document.getElementById("myInput");
    ul = document.querySelector(".user__chatList");
    li = ul.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("a")[0];
        p = a.getElementsByClassName("getChat__username")[0];
        // console.log(p.innerText);
        txtValue = p.textContent || p.innerText;
        if (txtValue.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}

$(document).ready(function () {
  const userAllChats = document.querySelector(".user__allChats");
  userAllChats.scrollTop = userAllChats.scrollHeight;
  const chatReload = document.querySelector(".alert__chatReload");
  const checkedUser = document.querySelector("#checked__user");
  const leftTopSection = document.querySelector(".left__topSection");
  
  if (checkedUser) {
      if (window.innerWidth <= 991)
            leftTopSection.style.display = "none";
     window.addEventListener("resize", () => {
         if (window.innerWidth <= 991)
            leftTopSection.style.display = "none";
        else
            leftTopSection.style.display = "flex";
     });
  }
  
  let audioClasses = document.getElementsByClassName("play__audio");
  let soundCount = 0;
  
  const playAudioFunc = (audioClasses) => {
      for (let i=0; i<audioClasses.length; i++) {
          if (audioClasses[i].value === "False") {
              if (soundCount === 0) {
                  document.getElementById("notify__audio").play();
                  soundCount++;
              }
          }
      }
  }
  
  playAudioFunc(audioClasses);


document.getElementById("tap__reload").addEventListener("click", () => {
    window.location.reload();
})

function addChatClass() {
    chatReload.classList.add("active__reloadChat");
}

setTimeout(function() {
    addChatClass();
}, 1000);


  goBack = document.querySelector(".go__back");

  goBack.addEventListener("click", () => {
      if (checkedUser.value === "true")
        window.location.href = "/buyer_chat";
      else
        window.location.href = "/inbox";
  });

  const chatForm = $("#chat__form");

  chatForm.submit(function (event) {
    event.preventDefault();

    const actionEndPoint = chatForm.attr("action");

    const method = chatForm.attr("method");

    let data = chatForm.serialize();

    $.ajax({
      url: actionEndPoint,

      method: method,

      data: data,

      success: function (data) {
        if (data.message_info) {
          // alert(data.message_info);
            // console.log(data);
          appendToMessage(data.message_info);

          $("#chat__form")[0].reset();
        }
      },

      error: function (errorData) {
        alert("Message not sent!");
      },
    });
  });
});



const profilePic = $(".chat__profileImage");
// console.log(profilePic.val());

function appendToMessage(message) {
  // console.log(message.username);
  
//   console.log(message);
console.log(message.message.includes("https://"));
    
    if (message.message && (message.message.includes("https://") || message.message.includes("http://"))) {
  $(".user__allChats").append(`

  <div style="word-break: break-all;" class="user__me w-100  d-flex justify-content-end pe-2" id="message_${message.id}">

  <div class="opposite__userImg">
            
    <img

      src="${profilePic.val()}"

      alt=""

    />
    
    <input type="hidden" value="${profilePic.val()}" class="chat__profileImage" />

  </div>

  <div class="chat__msg">

    <div class="chat__timestamp">

      <span class="fw-bold">${message.username}</span>

      <small class="text-muted">${message.send_at}</small>

    </div>
    
    <p>
        <a href="${message.message}">${message.message}</a>
    </p>
  </div>

</div>

  `);
    }
    
    else if (message.message) {
  $(".user__allChats").append(`

  <div style="word-break: break-all;" class="user__me w-100  d-flex justify-content-end pe-2" id="message_${message.id}">

  <div class="opposite__userImg">
            
    <img

      src="${profilePic.val()}"

      alt=""

    />
    
    <input type="hidden" value="${profilePic.val()}" class="chat__profileImage" />

  </div>

  <div class="chat__msg">

    <div class="chat__timestamp">

      <span class="fw-bold">${message.username}</span>

      <small class="text-muted">${message.send_at}</small>

    </div>
    
    <p>${message.message}</p>

  </div>

</div>

  `);
    }

  userAllChats = document.querySelector(".user__allChats");

  userAllChats.scrollTop = userAllChats.scrollHeight;
}

// Window width

// const windowWidth = window.innerWidth;

const searchIcon = document.querySelector(".searchbar");

const seachBoxInput = document.querySelector(".seach__boxInput");

const userDropDown = document.querySelector(".user__dropdown");

const leftSearchBar = document.querySelector(".left__searchBar");

const closeSearchBar = document.querySelector(".close__searchBar");

const userChatGroup = document.querySelector(".user__chatGroup");

// const userList = document.querySelector(".user__chatList");

const rightTopDots = document.querySelector(".right__topDots");

const rightAlternateOptions = document.querySelector(
  ".right__alternateOptions"
);

const closeAlternateOptions = document.querySelector(".close__alternateOption");

// const rightMainContent = document.querySelector(".right__mainContent");

// const leftSide = document.querySelector(".left__side");

// const userChatInfo = document.getElementsByClassName("user__chatInfo");

// const middleSide = document.querySelector(".middle__side");

// const goBack = document.querySelector(".go__back");

// // Search bar input show/hide section starts

searchIcon.addEventListener("click", () => {
  userChatGroup.style.marginTop = "0.6rem";

  // userList.style.display = "none";

  userDropDown.style.display = "none";

  leftSearchBar.style.display = "none";

  seachBoxInput.style.display = "flex";

  seachBoxInput.style.justifyContent = "space-between";

  seachBoxInput.style.alignItems = "center";
});

closeSearchBar.addEventListener("click", () => {
  // userList.style.display = "inherit";

  userChatGroup.style.display = "inherit";

  userDropDown.style.display = "inherit";

  leftSearchBar.style.display = "inherit";

  seachBoxInput.style.display = "none";

  userChatGroup.style.marginTop = "1.45rem";
});

// // Search bar input show/hide section ends

// // Right side top section alternate options show/hide section starts

// rightTopDots.addEventListener("click", () => {

//   rightTopDots.style.display = "none";

//   rightAlternateOptions.style.display = "flex";

//   rightAlternateOptions.style.justifyContent = "space-between";

// });

// closeAlternateOptions.addEventListener("click", () => {

//   rightMainContent.style.marginTop = "1.5rem";

//   rightTopDots.style.display = "flex";

//   rightAlternateOptions.style.display = "none";

// });

// // Right side top section alternate options show/hide section ends

// // Open chat section starts

// if (windowWidth <= 991) {

//   for (let i = 0; i < userChatInfo.length; i++) {

//     if (

//       userChatInfo[i].addEventListener("click", () => {

//         leftSide.style.display = "none";

//         middleSide.style.display = "inherit";

//       })

//     );

//   }

// }

// // Open chat section ends

// // Go back to user all chat section starts

// goBack.addEventListener("click", () => {

//   middleSide.style.display = "none";

//   leftSide.style.display = "inherit";

// });

// Go back to user all chat section ends
const link = document.querySelector(".createOffer");

const showForHover = document.querySelector(".for-hover-actived");

link.addEventListener("mouseenter", function () {
  showForHover.style.display = "block";
});

link.addEventListener("mouseleave", function () {
  showForHover.style.display = "none";
});


// for modal

const clickForModal = document.querySelector('.attachment__icon');
const closeForModal = document.querySelector('.close-button');
const forModal = document.querySelector('.for-modal');

clickForModal.addEventListener('click', function(){
    console.log('click')
    document.querySelector('.overlay').style.display = 'block';
    forModal.classList.add('coming');
})
closeForModal.addEventListener('click', function(){
    document.querySelector('.overlay').style.display = 'none';
    forModal.classList.remove('coming');
   
})


const forprofile = () => {
    const proPix = document.querySelector("#main-image");

    // let fileName = proPix.split("\\");
    // fileName = fileName[fileName.length - 1];
    const fileName = proPix.files[0].name;
  
  document.querySelector("#uploaded-image-name").innerText = fileName;

}

// for loader 

const SubmitButton = document.querySelector('#modal-submit-button');
const pixName = document.querySelector('#main-image');

SubmitButton.addEventListener('click', function(){
    if(pixName.files[0].name.length > 0){
        document.querySelector('.main-loader-start').style.display = 'block'
    }else{
        document.querySelector('.main-loader-start').style.display = 'none'
    }
})








