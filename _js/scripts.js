/*-------------------------------------
| Floating Box
-------------------------------------*/
$(function() {

    var $sidebar   = $("#sidebar"), 
        $window    = $(window),
        offset     = $sidebar.offset(),
        topPadding = 15;

    $window.scroll(function() {
        if ($window.scrollTop() > offset.top) {
            $sidebar.stop().animate({
                marginTop: $window.scrollTop() - offset.top + topPadding
            });
        } else {
            $sidebar.stop().animate({
                marginTop: 0
            });
        }
    });
    
});


// <!-- FOR STICKY MENU -->

// $(document).ready(function() {
// var stickyNavTop = $('#mainNav').offset().top;
 
// var stickyNav = function(){
// var scrollTop = $(window).scrollTop();
      
// if (scrollTop > stickyNavTop) { 
//     $('#mainNav').addClass('sticky');
// } else {
//     $('#mainNav').removeClass('sticky'); 
// }
// };
 
// stickyNav();
 
// $(window).scroll(function() {
//   stickyNav();
// });
// });
