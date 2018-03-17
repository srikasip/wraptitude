var slideIndex = 1; 


function plusSlides(n){
  slideIndex += n;
  showSlides(slideIndex);

}
function currentSlide(n){
  slideIndex = n;
  showSlides(slideIndex);
}

function showSlides(n){
  var i;
  var slides = $(".recSlide");
  var dots = $(".demo");

  if(n>slides.length){slideIndex = 1;}
  else if(n<1) {slideIndex = slides.length - 1;}

  dots.removeClass("active");
  slides.css("display", "none");

  $(".recSlide:eq(" + String(slideIndex-1) + ")").css("display", "block");
  $(".demo:eq(" +String(slideIndex-1)+ ")").addClass("active");
}

function setThumbnails(){
  $(".demo").click(function(){
    currentSlide($(this).attr("data-assoc"));
  });
}

function setSubCarousel(){
  $(".mover").click(function(){
    $showcaser = $(this).parent().parent();
    myID = $showcaser.find("img.showSubImage").attr("id");
    console.log(myID)
    indexParts = myID.split("_");
    $showcaser.find(".showSubImage").removeClass("showSubImage");

    if(parseInt(indexParts[1])>=$showcaser.attr("data-numImages")) {indexParts[1] = "0";}
    newIndex = String(parseInt(indexParts[1])+1);
    newId = "#" + indexParts[0] + "_" + newIndex;
    console.log(newId);
    $(newId).addClass("showSubImage");

  });
}

function SetAddToCart(){
  $("button.addCart").click(function(){
    carouselImgID = $(this).attr('data-carousel');
    console.log(carouselImgID);
  })
}

$(document).ready(function(){
  console.log("firing js");
  setThumbnails();
  setSubCarousel();
  showSlides(slideIndex);
});