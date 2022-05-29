//  for loading animation


const submitButton = document.getElementById('submit-button');

const submitloaderAnimaiton = document.querySelector('.main-loader-start');

const fileVal = document.querySelector("#formUpload");
// main image = uploadedImageName




submitButton.addEventListener('click', function(e) {
    let fileUpload = fileVal.files[0].name;
    
    if(fileUpload.length > 0){
            submitloaderAnimaiton.style.display = 'block';
    }else{
        submitloaderAnimaiton.style.display = 'none';
    }
    
})



const postButton = document.getElementById('post-button');

const loaderAnimaiton = document.querySelector('.main-loader-start');

postButton.addEventListener('click', function(e) {
    // e.preventDefault();
    loaderAnimaiton.style.display = 'block';
})



const forfile = () => {

    const FileName = document.querySelector("#formFileLg").value;

  let docFileMain = FileName.split("\\");
  docFileMain = docFileMain[docFileMain.length - 1];
  document.querySelector("#for-doc-file-name").innerText = docFileMain;
}

function forupload(e) {
    let fileVal = e.files[0].name;
    
  document.querySelector("#for-upload-name").innerText = fileVal;
  document.querySelector("#for-upload-name").style.display = 'block';
  document.querySelector("#for-upload-name").style.background  = '#f5f5f5';
}
