 // logostyle


 $('.logoStyle').slick({
  dots: false,
  infinite: false,
  arrows: false,
  autoplaySpeed: 1500,
  Speed:150,
  slidesToShow: 6,
  slidesToScroll: 1,
  autoplay: true,
  responsive: [
    {
      breakpoint: 1024,
      settings: {
        slidesToShow: 3,
        slidesToScroll: 3,
        infinite: false,
        arrows: false,
        dots: false,
        
      }
    },
    {
      breakpoint: 600,
      settings: {
        slidesToShow: 2,
        arrows: false,
        slidesToScroll: 2
      }
    },
    {
      breakpoint: 480,
      settings: {
        slidesToShow: 1,
        arrows: false,
        slidesToScroll: 1
      }
    }
    // You can unslick at a given breakpoint now by adding:
    // settings: "unslick"
    // instead of a settings object
  ]
});



$('.for-card-inner-img-slider').slick({
  dots: true,
  autoplay: false,
  autoplaySpeed:1500,
  dots: false,
  slidesToShow: 1,
  slidesToScroll: 1,
  arrows: true,
  centerMode: false,
});





// for see more button on sub category page

$(document).ready(function() {
    if ($(".for-category-see-more").length === 0 ) {
        $(".category-see-more-button").fadeOut();
    } else {
        $(".for-category-see-more").slice(0, 20).show();

        $(".category-see-more-button").on("click", () => {
            $(".for-category-see-more:hidden").slice(0, 20).fadeIn().show();

            if ($(".for-category-see-more:hidden").length === 0) {
                $(".category-see-more-button").fadeOut();
            }
        });
    }
});




// for see more button category_wise_page

$(document).ready(function() {
    if ($(".category-wise-page-card").length === 0 ) {
        $(".category-wise-see-more-button").fadeOut();
    } else {
        $(".category-wise-page-card").slice(0, 20).show();

        $(".category-wise-see-more-button").on("click", () => {
            $(".for-category-see-more:hidden").slice(0, 20).fadeIn().show();

            if ($(".category-wise-page-card:hidden").length === 0) {
                $(".category-wise-see-more-button").fadeOut();
            }
        });
    }
});


// for see more button service wise page

$(document).ready(function() {
    if ($(".for-service-see-more").length === 0 ) {
        $(".service-see-more-button").fadeOut();
    } else {
        $(".for-service-see-more").slice(0, 20).show();

        $(".service-see-more-button").on("click", () => {
            $(".for-category-see-more:hidden").slice(0, 20).fadeIn().show();

            if ($(".for-service-see-more:hidden").length === 0) {
                $(".service-see-more-button").fadeOut();
            }
        });
    }
});


















