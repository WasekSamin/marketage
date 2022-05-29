



// arko part for loading



const editpostButton = document.getElementById('edit-post-button');

const editloaderAnimaiton = document.querySelector('.main-loader-start');

const editTitleLength = document.querySelector("#for-title");

const editSeoTitleLength = document.querySelector("#for-seo-title");

const editforCat = document.querySelector ('.for-size');

const editinputDetailsForLoader = document.querySelector ('.input-for-details');

const editDeliveryDays = document.querySelector ('#delivery-days');

const editrevisionDays = document.querySelector ('#revision-days');


const editForImageLength = document.querySelector ('#main-image1');
const anotherImage = document.querySelector ("#for-img-length");
const offerImageVal = document.querySelector(".offer_image_val");

// main image = uploadedImageName




editpostButton.addEventListener('click', function(e) {
    if(editTitleLength.value.length > 0 && editSeoTitleLength.value.length > 0 && editforCat.value.length > 0  &&  editinputDetailsForLoader.value.length > 0 && editDeliveryDays.value.length > 0 && editrevisionDays.value.length > 0){
            
            if (offerImageVal) {
                if (offerImageVal.src)
                    editloaderAnimaiton.style.display = 'block';
            }
            else if (editForImageLength.files[0].name.length > 0){
                editloaderAnimaiton.style.display = 'block';
            } else if(anotherImage.files[0].name.length > 0){
                editloaderAnimaiton.style.display = 'block';
            }
    }else{
        editloaderAnimaiton.style.display = 'none';
    }

})
















// after upload new image preview
const forSomething = () => {
const docFile = document.querySelector("#main-image1").value;

  let docFileMain = docFile.split("\\");
  docFileMain = docFileMain[docFileMain.length - 1];
  document.querySelector("#newID").innerText = docFileMain;
  document.querySelector("#newID").style.display = 'block';
  document.querySelector("#newID").style.background  = '#f5f5f5';
}



// for 3 images

const onExtra = () => {
    const extraImages = document.querySelector("#extra-images1");
    const uploadImage1 = document.querySelector("#change-images-name1");
    const uploadImage2 = document.querySelector("#change-images-name2");
    const uploadImage3 = document.querySelector("#change-images-name3");
    uploadImage1.style.background = "#f5f5f5"
    uploadImage2.style.background = "#f5f5f5"
    uploadImage3.style.background = "#f5f5f5"
    
    
    for (let i = 0; i<extraImages.files.length; i++) {
        if (i == 0) {
            uploadImage1.innerText = extraImages.files[i].name;
            uploadImage1.style.display = 'block';
        }
        else if (i == 1) {
            uploadImage2.innerText = extraImages.files[i].name;
            uploadImage2.style.display = 'block';
        }
        else if (i == 2) {
            uploadImage3.innerText = extraImages.files[i].name;
            uploadImage3.style.display = 'block';
        }
    }
}


// for video preview
const forVideo1 = () => {
  const videoFile = document.querySelector("#videoFile1").value;

  let videoFileMain = videoFile.split("\\");
  videoFileMain = videoFileMain[videoFileMain.length - 1];
  
  document.querySelector("#video-name1").innerText = videoFileMain;
  document.querySelector("#video-name1").style.display = 'block';
   document.querySelector("#video-name1").style.background  = '#f5f5f5';
}


// for pdf preview

const pdfNew = () => {
  const videoFile = document.querySelector("#pdfFile1").value;

  let videoFileMain = videoFile.split("\\");
  videoFileMain = videoFileMain[videoFileMain.length - 1];
  
  document.querySelector("#pdf-new").innerText = videoFileMain;
  document.querySelector("#pdf-new").style.display = 'block';
   document.querySelector("#pdf-new").style.background  = '#f5f5f5';
}








// azim price set js

const selectedCategory = document.querySelector(".selected__categoryTitle");

const editSelectedCategory = (elem) => {
  if (elem.value === "Programming & Tech") {
    document.querySelector(".edit__pageRow").style.display = "revert";
    document.querySelector(".edit__responsiveDesign").style.display = "revert";
  } else {
    document.querySelector(".edit__pageRow").style.display = "none";
    document.querySelector(".edit__responsiveDesign").style.display = "none";
  }
}

const admineditSelectedCategory = (elem) => {
  if (elem.value === "Programming & Tech") {
    document.querySelector(".edit__pageRow").style.display = "revert";
    document.querySelector(".edit__responsiveDesign").style.display = "revert";
  } else {
    document.querySelector(".edit__pageRow").style.display = "none";
    document.querySelector(".edit__responsiveDesign").style.display = "none";
  }
}


document.getElementById("editOffer").addEventListener("change", function() {
  let inpVal = parseInt(this.value);
//   console.log(inpVal);
  if (inpVal < 5) {
    $('#div1').html('Price cannot be less then 5 USD');
    $(this).val('');
  }
  else
    {
        $('#div1').html('');
    }
});


document.getElementById("editOfferStand").addEventListener("change", function() {
  let inpVal = parseInt(this.value);
  if (inpVal < 5) {
    $('#div1').html('Price cannot be less then 5 USD');
    $(this).val('');
  }
  else
    {
        $('#div1').html('');
    }
});

document.getElementById("editOfferPrem").addEventListener("change", function() {
  let inpVal = parseInt(this.value);
  if (inpVal < 5) {
    $('#div1').html('Price cannot be less then 5 USD');
    $(this).val('');
  }
  else
    {
        $('#div1').html('');
    }
});



const offer_extra_image_button1 = document.querySelector(".offer_extra_image_button1");
const offer_extra_image_button2 = document.querySelector(".offer_extra_image_button2");
const offer_extra_image_button3 = document.querySelector(".offer_extra_image_button3");

offer_extra_image_button1.addEventListener("click", () => {
    document.querySelector(".extra_image_id1").value = 1;
});

offer_extra_image_button2.addEventListener("click", () => {
    document.querySelector(".extra_image_id2").value = 2;
});

offer_extra_image_button3.addEventListener("click", () => {
    document.querySelector(".extra_image_id3").value = 3;
});

function mainImageDelete(offer_id) {
    document.querySelector(".main_image_id").value = offer_id;
}

function offerVideoDelete(video_id) {
    document.querySelector(".offer_video_id").value = video_id;
}

function offerDocumentDelete(doc_id) {
    document.querySelector(".offer_document_id").value = doc_id;
}













