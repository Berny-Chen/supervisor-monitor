/**
 * Created by kuga on 15-7-25.
 */

$(function(){
    $(".dropdown").hover(
        function() {
            $('.dropdown-menu', this).stop(true, true).fadeIn("fast");
            $(this).toggleClass('open');
            $('b', this).toggleClass("caret caret-up");
        },
        function() {
            $('.dropdown-menu', this).stop(true, true).fadeOut("fast");
            $(this).toggleClass('open');
            //$('b', this).toggleClass("caret caret-up");
        });
});
