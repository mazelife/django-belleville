/* Window Resizing */
var min_width = 1422;
var currently_positioned = null;
$(window).resize(set_body_class);
$(document).ready(function() { currently_positioned = set_body_class(); });
function set_body_class() {
    var page_width = $(window).width()
    var is_positioned = page_width  < min_width
    if (is_positioned && !currently_positioned) { 
        $("body").addClass('background_positioned');
        currently_positioned = true;
    }
    if (!is_positioned && currently_positioned) {
        $("body").removeClass('background_positioned');
        currently_positioned = false;
    }
    return is_positioned
}
/* Search Box */
$(document).ready(function () {$("#search-box").click(clear_search_box);})
function clear_search_box() {
    box = $(this);
    if (box.attr("value") == "search") box.attr("value", "");
}