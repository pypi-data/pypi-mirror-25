PCART.success_notification = function(value) {
    $('.cart_popup').delay(300).slideDown(300).html(value);
    $('.cart_popup').delay(2000).slideUp(400);
}

PCART.error_notification = function(value) {
    $('.cart_popup').delay(300).slideDown(300).html(value);
    $('.cart_popup').delay(2000).slideUp(400);
}
