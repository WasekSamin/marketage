$('.responsive').slick({
    dots: true,
    autoplay: true,
    autoplaySpeed: 2000,
    speed: 300,
    dots: false,
    slidesToShow: 2,
    slidesToScroll: 2,
    arrows: false,
    responsive: [
      {
        breakpoint: 992,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
          infinite: true,
          dots: false,
          autoplay: true,
        }
      },
      {
        breakpoint: 600,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
        }
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1
        }
      }

    ]
  });




  $('.inner-service-card').slick({
    dots: false,
    autoplay: false,
    infinite: false,
    slidesToShow: 4,
    slidesToScroll: 1,

    responsive: [
      {
        breakpoint: 992,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 2,
          infinite: false,
          dots: false,

        }
      },
      {
        breakpoint: 600,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 2,
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



  $('.slidermoron').slick({
    dots: true,
    autoplay: false,
    speed: 300,
    infinite: true,
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: false,

  });

  $('.for-card-inner-img-slider').slick({
    dots: true,
    autoplay: false,
    speed: 300,
    dots: false,
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: true,
    centerMode: false,
  });



// ========================================================================
                            // For Mobile view (600 px screen)
// ========================================================================


$('.main-top').slick({
  dots: true,
  autoplay: false,
  autoplaySpeed: 2000,
  speed: 300,
  dots: false,
  slidesToShow: 2,
  slidesToScroll: 2,
  arrows: false,
  centerMode: false,
  responsive: [
    {
      breakpoint: 992,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1,
        infinite: true,
        dots: false,
        autoplay: true,
      }
    },
    {
      breakpoint: 600,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1,
      }
    },
    {
      breakpoint: 480,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1
      }
    }

  ]
});

// const clickSeeMore = document.querySelector('.click-see-more-to-show');
// const SeeMoreButton = document.querySelector('.see-more-button');

// SeeMoreButton.addEventListener("click", () => {
//     clickSeeMore.style.display = "block"
// });



// popular offer
$(document).ready(function() {
    if ($(".for-see-more").length === 0 ) {
        $(".see-more-button").fadeOut();
    } else {
        $(".for-see-more").slice(0, 20).show();

        $(".see-more-button").on("click", () => {
            $(".for-see-more:hidden").slice(0, 20).fadeIn().show();

            if ($(".for-see-more:hidden").length === 0) {
                $(".see-more-button").fadeOut();
            }
        });
    }
});



// premium offer

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




// verified service
$(document).ready(function() {
    if ($(".verified-service-see-more").length === 0 ) {
        $(".verified-service-see-more-button").fadeOut();
    } else {
        $(".verified-service-see-more").slice(0, 12).show();

        $(".verified-service-see-more-button").on("click", () => {
            $(".verified-service-see-more:hidden").slice(0, 12).fadeIn().show();

            if ($(".verified-service-see-more:hidden").length === 0) {
                $(".verified-service-see-more-button").fadeOut();
            }
        });
    }
});




// new Typed('#typed',{
//     strings : ['TO SHOW...',],
//     typeSpeed : 90,
//     delaySpeed : 90,
//     loop : true
//   });



