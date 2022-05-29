// sticky navbar

window.addEventListener('scroll', function(){
    var nav = document.querySelector("nav");
    nav.classList.toggle("sticky", window.scrollY > 0);
  });
  
  
const expendPremiumOffer = (e) => {
    document.querySelector(`.expand__premiumOfferIcon${e}`).classList.toggle(`active__premiumOfferIcon${e}`);
    
    if (document.querySelector(`.active__premiumOfferIcon${e}`)) {
        document.querySelector(`.active__premiumOfferIcon${e}`).querySelector("svg").setAttribute("data-icon", "bx:bx-minus");
        document.querySelector(`.get__expandOffer${e}.hide__expandOffer`).style.visibility = "visible";
        document.querySelector(`.get__expandOffer${e}.hide__expandOffer`).style.opacity = 1;
        document.querySelector(`.get__expandOffer${e}.hide__expandOffer`).style.height = "auto";
    } else {
        document.querySelector(`.expand__premiumOfferIcon${e}`).querySelector("svg").setAttribute("data-icon", "carbon:add");
        document.querySelector(`.get__expandOffer${e}.hide__expandOffer`).style.visibility = "hidden";
        document.querySelector(`.get__expandOffer${e}.hide__expandOffer`).style.opacity = 0;
        document.querySelector(`.get__expandOffer${e}.hide__expandOffer`).style.height = 0;
    }
    
}


$('.slider').slick({
    dots: false,
    infinite: true,
    speed: 300,
    slidesToShow: 5,
    slidesToScroll: 3,
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 3,
          slidesToScroll: 3,
          infinite: true,
          dots: true
        }
      },
      {
        breakpoint: 600,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 2
        }
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1
        }
      }
      // You can unslick at a given breakpoint now by adding:
      // settings: "unslick"
      // instead of a settings object
    ]
  });


  $('.imageSlider').slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 2000,
    prevArrow: false,
    nextArrow: false
  });



  $('.secondSlider').slick({
    dots: false,
    infinite: true,
    speed: 300,
    slidesToShow: 4,
    slidesToScroll: 2,
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 2,
          infinite: true,
          dots: true
        }
      },
      {
        breakpoint: 600,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1
        }
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1
        }
      }
      // You can unslick at a given breakpoint now by adding:
      // settings: "unslick"
      // instead of a settings object
    ]
  });


  $('.second__banner__slider').slick({
    autoplay: true,
    arrows: false,
    dots: false,
    infinite: true,
    speed: 300,
    slidesToShow: 1,
    slidesToScroll: 1,
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
          infinite: true,
          dots: false
        }
      },
      {
        breakpoint: 600,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1
        }
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1
        }
      }
      // You can unslick at a given breakpoint now by adding:
      // settings: "unslick"
      // instead of a settings object
    ]
  });
  
  
  
  
  
  
  
  
  
//   become a sller modal js

// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}  
  
  
  
//   browse category js

var coll = document.getElementsByClassName("landing__collapsible");
var i;
for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("activeNow");
    var content = this.nextElementSibling;
    if (content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "100%";
    }
  });
}

  
  
  
  $('.for-card-inner-img-slider').slick({
    dots: false,
    autoplay: false,
    infinite: true,
    slidesToShow: 1,
    slidesToScroll: 1,

    responsive: [
      {
        breakpoint: 992,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
          infinite: false,
          dots: false,

        }
      },
      {
        breakpoint: 600,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
          dots: false,
        }
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
          dots: false,
        }
      }

    ]
  });


  
  
  
//   see more button 

$(document).ready(function() {
    if ($(".premium-see-more").length === 0 ) {
        $(".premium-see-more-button").fadeOut();
    } else {
        $(".premium-see-more").slice(0, 4).show();

        $(".premium-see-more-button").on("click", () => {
            $(".premium-see-more:hidden").slice(0, 4).fadeIn().show();

            if ($(".premium-see-more:hidden").length === 0) {
                $(".premium-see-more-button").fadeOut();
            }
        });
    }
});

  
  
  