
$(function() {

    $('#username').keydown(function(event) {
        if (event.which == 13) {
            $('#password').focus().select();
            return false;
        }
        return true;
    });

    $('form').submit(function() {
        if (! $('#username').val()) {
            with ($('#username').get(0)) {
                select();
                focus();
            }
            return false;
        }
        if (! $('#password').val()) {
            with ($('#password').get(0)) {
                select();
                focus();
            }
            return false;
        }
        return true;
    });

    $('#username').focus();

});
