const forPdf = () => {
const docFile = document.querySelector("#uploadAnswer").value;

  let docFileMain = docFile.split("\\");
  docFileMain = docFileMain[docFileMain.length - 1];
  document.querySelector("#forPdfFileName").innerText = docFileMain;
  document.querySelector("#forPdfFileName").style.display = 'block';
  document.querySelector("#forPdfFileName").style.background  = '#f5f5f5';
}
