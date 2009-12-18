/* Window Resizing */
var min_width = 1280;
var background_repositioned = null;
$(window).resize(set_body_class);
$(document).ready(function() { background_repositioned = set_body_class(); });
function set_body_class() {
    var page_width = $(window).width()
    var is_positioned = page_width  < min_width
    if (is_positioned && !background_repositioned) { 
        $("body").addClass('background_repositioned');
        background_repositioned = true;
    }
    if (!is_positioned && background_repositioned) {
        $("body").removeClass('background_repositioned');
        background_repositioned = false;
    }
    return is_positioned
}

/* Search Box */
$(document).ready(function () {$("#search-box").click(clear_search_box);})
function clear_search_box() {
    box = $(this);
    if (box.attr("value") == "search") box.attr("value", "");
}

/* Comment Notifiction */
$(document).ready(function () {
    if (window.location.search === "") return;
    var comment = window.location.search.match(/c=(\d+)/);
    if (comment) comment = comment[1];
    else return; 
    var mssg = $("<div id=\"comment-thanks-flash\">Thanks for leaving a <a href=\"#comment-" + comment + "\">comment</a>!</div>");
    $(document.body).append(mssg);    
    window.setTimeout('$("#comment-thanks-flash").fadeOut(600)', 4 * 1000);
});