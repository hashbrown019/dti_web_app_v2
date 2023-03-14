// var slideIndex = 0;
// showDivs(slideIndex);
var hidden_talent = document.getElementById("hidden_talent")
var show_talent = document.getElementsByClassName("show_talent")
var hidden_talent_div = hidden_talent
hidden_talent.remove()

for (var i = 0; i < show_talent.length; i++) {
	show_talent[i].innerHTML = hidden_talent.innerHTML
}


function plusDivs(n) {
	showDivs(slideIndex += n);
}

function showDivs(n) {
	var i;
	var x = document.getElementsByClassName("mySlides");
	if (n > x.length) {slideIndex = 1}    
	if (n < 1) {slideIndex = x.length} ;
	for (i = 0; i < x.length; i++) {
		 x[i].style.display = "none";  
	}
	x[slideIndex-1].style.display = "block";  
}


// $onload(mini_carousel(0))
var rapid = ["R","A","P","I","D"]
function mini_carousel(ind){
	var x = document.getElementsByClassName("mySlides");
	for (var i = 0; i < x.length; i++) {
		x[i].style.display = "none";
	}
	x[ind].style.display = "block";


	var car_btn = document.getElementsByClassName("car_btn__");
	for (var i = 0; i < car_btn.length; i++) {
		car_btn[i].style.textDecoration = "none"	
	}
	car_btn[ind].style.textDecoration = "underline"	
	// car_btn[ind].style.textDecoration = "underline"	
	println(car_btn[ind].style.textDecoration)
	// car_btn[ind].innerText ="<u>"+ rapid[i] + "</u>"
	// println(car_btn[ind].innerText)
	// showDivs(slideIndex += ind);
}



// Navbar Dropdown

$(document).ready(function(){
  $('ul.dropdown-menu [data-toggle=dropdown]').on('click', function(event) {
    event.preventDefault(); 
    event.stopPropagation(); 
    $(this).parent().siblings().removeClass('open');
    $(this).parent().toggleClass('open');
  });
});


// Scrollspy

$('.navbar-nav>li>a').on('click', function(){
    $('.navbar-collapse').collapse('hide');
});


