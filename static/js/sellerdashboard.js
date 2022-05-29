// banner slider

$('.top-slider').slick({
  dots: true,
  infinite: false,
  speed: 300,
  slidesToShow: 1,
  slidesToScroll: 1,
  autoplay: true,
  arrows: false,
  responsive: [
    {
      breakpoint: 1024,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1,
        infinite: true,
        autoplay: true,
        arrows: false,
        dots: true
      }
    },
    {
      breakpoint: 600,
      settings: {
        slidesToShow: 1,
        autoplay: false,
        arrows: false,
        slidesToScroll: 1
      }
    },
    {
      breakpoint: 480,
      settings: {
        slidesToShow: 1,
        autoplay: true,
        arrows: false,
        slidesToScroll: 1
      }
    }
    // You can unslick at a given breakpoint now by adding:
    // settings: "unslick"
    // instead of a settings object
  ]
});


// active order button
//  complete and cancel button 

const activeText = document.getElementById("active_text")

const upgrade_business = document.getElementById("upgrade_business")


const slider_row = document.getElementById("slider_row")
const upgrade_text = document.getElementById("upgrade_text")

const complete = document.getElementById("complete_order_show")
complete.style.display = "none"

const cancel = document.getElementById("cancel_order")
cancel.style.display= "none"

const active = document.getElementById("activeOrder");
const activeBtn = document.querySelector(".activeBtn");

const activeOrderShow = document.getElementById("active_order_show")
const newActive = document.getElementById("activeOrder")

active.addEventListener("click", (event) =>{
if(active.style.display = "none"){
  active.style.display = "block"
  complete.style.display = "none"
  cancel.style.display = "none"
  upgrade_business.style.display="flex"
  slider_row.style.display="block"
  upgrade_text.style.display="block"
  activeBtn.innerHTML = "Active Orders"
  activeText.innerHTML = "Active Orders"
} else{
  active.style.display = "none"
}
})

activeOrder.addEventListener("click", (event) => {
  if (activeOrderShow.style.display = "none"){
    activeOrderShow.style.display = "block"
    cancel.style.display = "none"
    complete.style.display = "none"
    activeText.innerHTML = "Active Orders"
    activeBtn.innerHTML = "Active Orders"
  } else {
    activeOrderShow.style.display = "none"
  
  }
  })

completed.addEventListener("click", (event) => {
if (complete.style.display = "none"){
  complete.style.display = "block"
  upgrade_business.style.display="none"
  slider_row.style.display="none"
  upgrade_text.style.display="none"
  cancel.style.display = "none"
  activeOrderShow.style.display = "none"
  activeText.innerHTML = "Completed Orders"
  activeBtn.innerHTML = "Completed Orders"
} else {
  complete.style.display = "none"

}
})

canceled.addEventListener("click", (event) => {
if (cancel.style.display = "none"){
  cancel.style.display = "block"
  complete.style.display = "none"
  upgrade_business.style.display="none"
  slider_row.style.display="none"
  upgrade_text.style.display="none"
  complete.style.display = "none"
  activeOrderShow.style.display = "none"
  activeBtn.innerHTML = "Canceled Orders"
  activeText.innerHTML = "Canceled Orders"
} else {
  cancel.style.display = "none"
}
})


// for active name change

