$(document).ready(function(){
  SmoothScrollLinks();
  occassionRedirect();
});


function occassionRedirect(){
  $(".occasionsBox .occasion div").click(function(){
    url = "/quiz/"+$(this).parent().attr('data-question')+"/" + $(this).parent().attr('id');
    window.location.replace(url);
  });
}

function SmoothScrollLinks()
{
  $('a[href^="#"]').on('click', function(event) {
    var target = $(this.getAttribute('href'));
    var windowHeight = $(window).outerHeight();
    if(target.length) {
      event.preventDefault();
        $('html, body').stop().animate({
            scrollTop: target.offset().top
        }, 1000);
    }
  });
}