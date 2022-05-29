const onFileUpload = () => {
    const file = document.querySelector("#profile-pix").value;
    let filename = file.split("\\");
    filename = filename[filename.length - 1];
    document.querySelector(".for-preview").innerText = filename;
    document.querySelector(".for-preview").style.display = "block";
}