
//  for admin panel

$('#searchBar').keyup(function() {
  var search_term = $('#searchBar').val();
  $('.monitor').removeHighlight().highlight(search_term);
});



// for transaction

$('#transaction____search').keyup(function() {
  var search_term = $('#transaction____search').val();
  $('.monitor').removeHighlight().highlight(search_term);
});


// for withdraw

$('#widthraw____search').keyup(function() {
  var search_term = $('#widthraw____search').val();
  $('.monitor').removeHighlight().highlight(search_term);
});




// for all user

$('#user___id').keyup(function() {
  var search_term = $('#user___id').val();
  $('.monitor').removeHighlight().highlight(search_term);
});


// for all order
$('#all____order____search').keyup(function() {
  var search_term = $('#all____order____search').val();
  $('.monitor').removeHighlight().highlight(search_term);
});


// for exam model

$('#exam____search').keyup(function() {
  var search_term = $('#exam____search').val();
  $('.monitor').removeHighlight().highlight(search_term);
});


// for notification

$('#notification____search').keyup(function() {
  var search_term = $('#notification____search').val();
  $('.monitor').removeHighlight().highlight(search_term);
});



// for uploaded offer


$('#uploaded____search').keyup(function() {
  var search_term = $('#uploaded____search').val();
  $('.monitor').removeHighlight().highlight(search_term);
});

// notification details offer description 

function readMore() {
  var dots = document.getElementById("dots");
  var moreText = document.getElementById("more");
  var btnText = document.getElementById("myBtn");

  if (dots.style.display === "none") {
    dots.style.display = "inline";
    btnText.innerHTML = "Read more"; 
    moreText.style.display = "none";
  } else {
    dots.style.display = "none";
    btnText.innerHTML = "Read less"; 
    moreText.style.display = "inline";
  }
}

