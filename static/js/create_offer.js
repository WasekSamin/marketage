const proLan = document.querySelector('.pro-lan');
const expertise = document.querySelector('.expertise');

const getSelectedCategory = (elem) => {
    // console.log(elem.value);
    
    if (elem.value === "Programming & Tech") {
        document.querySelector(".num__ofPageRow").style.display = "revert";
        // document.querySelector(".num__ofPageRow").style.display = "table-column";
        document.querySelector(".responsive__designRow").style.display = "revert";
        // document.querySelector(".responsive__designRow").style.display = "table-column";
    } else {
        document.querySelector(".num__ofPageRow").style.display = "none";
        document.querySelector(".responsive__designRow").style.display = "none";
    }
}





//  for loading animation


const postButton = document.getElementById('post-button');

const loaderAnimaiton = document.querySelector('.main-loader-start');

const titleLength = document.querySelector("#for-title");

const SeoTitleLength = document.querySelector("#for-seo-title");

const forCat = document.querySelector ('.for-size');

const inputDetailsForLoader = document.querySelector ('.input-for-details');

const DeliveryDays = document.querySelector ('#delivery-days');

const revisionDays = document.querySelector ('#revision-days');


const ForImageLength = document.querySelector ('.for-img-length')
// main image = uploadedImageName




postButton.addEventListener('click', function(e) {

    console.log(forCat.value);
    console.log(titleLength.value);
    console.log(SeoTitleLength.value);
    
    if(titleLength.value.length > 0 && SeoTitleLength.value.length > 0 && forCat.value.length > 0  &&  inputDetailsForLoader.value.length > 0 && DeliveryDays.value.length > 0 && revisionDays.value.length > 0 &&  ForImageLength.files[0].name.length > 0 ){
            loaderAnimaiton.style.display = 'block';
    }else{
        loaderAnimaiton.style.display = 'none';
    }
    
})






















const getButton = document.getElementById('get');
const multiInput = document.querySelector('multi-input'); 
const values = document.querySelector('#values'); 
const imageFixed = document.querySelector('.showcase-talent');


// for hovering div
const hoverDiv = document.querySelector('.hover-function');
const hiddingDiv = document.querySelector('.defining-gig');

// gigs title
const gigTitle = document.querySelector('.gig-title');
const discribeGig = document.querySelector('.discribe-gig');

// seo title
const seoTitle = document.querySelector('.seo-title');
const seoTitleHover = document.querySelector('.seo-title-hover');

// category
const category = document.querySelector('.category');
const categoryHover = document.querySelector('.category-hover');


// service type
const serviceType = document.querySelector('.service-type');
const serviceTypeHover = document.querySelector('.service-type-hover');

// search tag
const searchTag = document.querySelector('.search-tag');
const searchTagHover = document.querySelector('.search-tag-hover');

// for - description 
const descriptionHover = document.querySelector('.description-hover-div');
const innerDes = document.querySelector('.inner-des');
const desRightDiv = document.querySelector('.right-div-for-description');

// for image section

const galleryImg = document.querySelector('.gallery-img');
const hoverImgDiv = document.querySelector('.inner-img-hover');

// for extra image section
const galleryExtraImg = document.querySelector('.extra-img');
const hoverExtraImgDiv = document.querySelector('.inner-extra-img-hover');


// for video section
const videoHover = document.querySelector('.for-video-hover');
const videosection = document.querySelector('.for-video');

const docHover = document.querySelector('.inner-doc-hover');
const docDiv = document.querySelector('.for-doc');





// doc hover
docDiv.addEventListener('mouseenter', function () {
  docHover.style.display = 'block';
  imageFixed.style.display = 'none';
})
docDiv.addEventListener('mouseleave', function () {
  docHover.style.display = 'none';
  imageFixed.style.display = 'block';
})

// video hover
videosection.addEventListener('mouseenter', function () {
  videoHover.style.display = 'block';
  imageFixed.style.display = 'none';
})
videosection.addEventListener('mouseleave', function () {
  videoHover.style.display = 'none';
  imageFixed.style.display = 'block';
})

// image hover
galleryImg.addEventListener('mouseenter', function () {
  hoverImgDiv.style.display = 'block';
  imageFixed.style.display = 'none';
})
galleryImg.addEventListener('mouseleave', function () {
  hoverImgDiv.style.display = 'none';
  imageFixed.style.display = 'block';
})


// image extra hover
galleryExtraImg.addEventListener('mouseenter', function () {
  hoverExtraImgDiv.style.display = 'block';
  imageFixed.style.display = 'none';
})
galleryExtraImg.addEventListener('mouseleave', function () {
  hoverExtraImgDiv.style.display = 'none';
  imageFixed.style.display = 'block';
})







hoverDiv.addEventListener('mouseenter', function () {
    hiddingDiv.style.display = 'none';
})

hoverDiv.addEventListener('mouseleave', function () {
    hiddingDiv.style.display = 'block';
})

// gigs title
gigTitle.addEventListener('mouseenter', function() {
    discribeGig.style.display = 'block';
})

gigTitle.addEventListener('mouseleave', function() {
    discribeGig.style.display = 'none';
})

// seo title
seoTitle.addEventListener('mouseenter', function () {
  seoTitleHover.style.display = 'block';
})
seoTitle.addEventListener('mouseleave', function () {
  seoTitleHover.style.display = 'none';
})

// category
category.addEventListener('mouseenter', function () {
  categoryHover.style.display = 'block';
})
category.addEventListener('mouseleave', function () {
  categoryHover.style.display = 'none';
})

// service type
// searchTag.addEventListener('mouseenter', function () {
//   searchTagHover.style.display = 'block';
// })
// searchTag.addEventListener('mouseleave', function () {
//   searchTagHover.style.display = 'none';
// })
// search tag
serviceType.addEventListener('mouseenter', function () {
  serviceTypeHover.style.display = 'block';
})
serviceType.addEventListener('mouseleave', function () {
  serviceTypeHover.style.display = 'none';
})
// search tag
innerDes.addEventListener('mouseenter', function () {
  descriptionHover.style.display = 'block';
  desRightDiv.style.display = 'none';
})
innerDes.addEventListener('mouseleave', function () {
  descriptionHover.style.display = 'none';
  desRightDiv.style.display = 'block';
})

function checkResponsive1() {
  let res1 = document.getElementById("res1");

  if (res1.value === "off")
      res1.value = "on"
  else
      res1.value = "off"

  // console.log(res1.value);
}

function checkResponsive2() {
  let res2 = document.getElementById("res2");

  if (res2.value === "off")
      res2.value = "on"
  else
      res2.value = "off"

  // console.log(res2.value);
}

function checkResponsive3() {
  let res3 = document.getElementById("res3");

  if (res3.value === "off")
      res3.value = "on"
  else
      res3.value = "off"

  // console.log(res3.value);
}

function cancel_offer() {
  window.location.href = "/manage-offers/";
}



// azim input limit work
// for offer title textarea

function count_up(obj) {
  document.getElementById('counter').innerHTML = obj.value.length;
}

function count_down(obj) {
   
  element.innerHTML = 80 - obj.value.length;   
}


// for seo title
function countUp(obj) {
  document.getElementById('counter-seo').innerHTML = obj.value.length;
}

function count_down(obj) {
   
  element.innerHTML = 60 - obj.value.length;   
}




// arko uploaded file name showing 

const onMainImageUpload = () => {
    const uploadedImageName = document.querySelector("#main-image");
    document.querySelector("#uploaded-image-name").innerText = uploadedImageName.files[0].name;
    document.querySelector("#uploaded-image-name").style.display = 'block';
}

const onExtraImagesUpload = () => {
    const extraImages = document.querySelector("#extraImages");
    const uploadImage1 = document.querySelector("#uploaded-images-name1");
    const uploadImage2 = document.querySelector("#uploaded-images-name2");
    const uploadImage3 = document.querySelector("#uploaded-images-name3");
    
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


const forVideo = () => {
  const videoFile = document.querySelector("#video-upload").value;

  let videoFileMain = videoFile.split("\\");
  videoFileMain = videoFileMain[videoFileMain.length - 1];
  
  document.querySelector("#video-name").innerText = videoFileMain;
  document.querySelector("#video-name").style.display = 'block';
}


const forDoc = () => {
const docFile = document.querySelector("#document-upload").value;

  let docFileMain = docFile.split("\\");
  docFileMain = docFileMain[docFileMain.length - 1];
  document.querySelector("#for-doc-file-name").innerText = docFileMain;
  document.querySelector("#for-doc-file-name").style.display = 'block';
}




// azim price set js


document.getElementById("inputnew").addEventListener("change", function() {
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


document.getElementById("inputForStand").addEventListener("change", function() {
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

document.getElementById("inputForPrem").addEventListener("change", function() {
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




