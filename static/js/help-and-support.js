

const ForFileName = function(){
    const mainfile = document.querySelector("#file-up").value;
    let NameOfFile = mainfile.split("\\")
    NameOfFile = NameOfFile[NameOfFile.length - 1];
    document.querySelector("#file-name-showing").innerText = NameOfFile;
    document.querySelector('#file-name-showing').style.display = "block"
    
}

const ForImageUp = function(){
    const imageFile = document.querySelector("#img-upload").files[0].name;
    console.log(imageFile);
    document.querySelector("#image-name-showing").innerText = imageFile;
    document.querySelector('#image-name-showing').style.display = "block"
    // let MainImageName = imageFile.split("//");
    // MainImageName = MainImageName[MainImageName.length - 1];
    
}


// for loader 

const ClickOnButton = document.querySelector(".send-msg");
const forMail = document.querySelector("#enter-mail");
const forDes = document.querySelector("#description");

ClickOnButton.addEventListener('click', function(e){
    // e.preventDefault();
    
    const expression = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;

    if(forMail.value.match(expression)  && forDes.value.length > 0){
        document.querySelector(".main-loader-start").style.display = 'block';
    }
    else{
        document.querySelector(".main-loader-start").style.display = 'none';
    }
})
