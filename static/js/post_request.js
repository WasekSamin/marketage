const onFileUpload = () => {
    const file = document.querySelector(".file__uploaded").value;
    let filename = file.split("\\");
    filename = filename[filename.length - 1];
    document.querySelector("#file_val").innerText = filename;
    document.querySelector("#file_val").style.display = "block";
}


// submit button
const clickForSubmit = document.querySelector("#button-for-submit");



const descriptionVal = document.querySelector("#description-value");
const deliveryTime = document.querySelector("#delivery-time");
const CatVal = document.querySelector("#category-selection");
const PriceSelect = document.querySelector("#price-for-the-post");
const OnTitle = document.querySelector('#for-title-value');
// const ForImg = document.querySelector('#file-upload')


clickForSubmit.addEventListener('click', function(e){
    // e.preventDefault();

    
    if(deliveryTime.value.length > 0 && descriptionVal.value.length > 0 && PriceSelect.value.length > 0 && CatVal.value.length > 0 && OnTitle.value.length > 0){
        document.querySelector('.main-loader-start').style.display = 'block'
    }else{
        document.querySelector('.main-loader-start').style.display = 'none'
    }
    
})