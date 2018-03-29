var slideIndex = 1; 

function SetupSignup(){
  
  $('button#signup').click(function(){
    $(".signupOverlay").css("display", "none");
    $(".signupForm").css("display","none");
  });
}

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
    // console.log(myID)
    indexParts = myID.split("_");
    $showcaser.find(".showSubImage").removeClass("showSubImage");

    if(parseInt(indexParts[1])>=$showcaser.attr("data-numImages")) {indexParts[1] = "0";}
    newIndex = String(parseInt(indexParts[1])+1);
    newId = "#" + indexParts[0] + "_" + newIndex;
    // console.log(newId);
    $(newId).addClass("showSubImage");
  });
}

function ManageBasket(){
  $(".basketHead, .giftOverlay").click(function(){
    $(".giftOverlay, .giftBasket").css("display", "none");
  });
  $("#giftbasketLink").click(function(){
    $(".giftOverlay, .giftBasket").css("display", "block");
  });
  $("button.addCart").click(function(){
    carouselID = "#" + $(this).attr("data-carousel");
    imgSrc = $(carouselID).attr("src");
    var name, desc, price;
    gift_id = carouselID.replace("#tn_", "");
    gift_id = "#gift_" + gift_id;
    name = $(gift_id).find(".giftWriteup .rewrapt-title").html();
    desc = $(gift_id).find(".giftWriteup .rewrapt-desc").html();
    price = $(gift_id).find(".closerBlock .pricer").html();

    cartBlock = '<div class="basketGift">\n';
    cartBlock += "<span class='deleter'>&#10005;</span>"
    cartBlock += '<div class="imageBox">\n';
    cartBlock += '<img src="'+imgSrc+'" />\n';
    cartBlock += '<div class="pricer">'+price+'</div>\n';
    cartBlock += '</div>\n';
    cartBlock += '<div class="tinyDesc">\n';
    cartBlock += '<h6>'+name+'</h6>\n';
    cartBlock += '<p>\n';
    cartBlock += desc + "\n";
    cartBlock += '</p>\n';
    cartBlock += '</div>\n';
    cartBlock += '</div>\n';

    $(cartBlock).appendTo("#chosenGifts");

    updateCart();

    $(".deleter").click(function(){
      $(this).parent().remove();
      updateCart();
    });
    $(".giftOverlay, .giftBasket").css("display", "block");
  });
}

function updateCart(){
  subtotal = 0.0;
  $(".basketGift").each(function(){ 
    thisPriceStr = $(this).find(".imageBox .pricer").html();
    subtotal += parseFloat(thisPriceStr.replace("$", ""));
  });
  $(".subtotal").html("$" + String(subtotal.toFixed(2)));

  $("#numItemsInCart").html(String($(".basketGift").length));
}

$(document).ready(function(){
  setThumbnails();
  setSubCarousel();
  ManageBasket();
  SetupSignup();
  showSlides(slideIndex);

  $(".checkoutBtn").click(function(){
    window.location.replace("/checkout");
  });

  $("#dvLoading").css("display", "block");
  setTimeout(function(){
      $("#dvLoading").css("display", "none");
      $(".signupOverlay").css("display", "block");
      $(".signupForm").css("display", "block");
  }, 5000);
});