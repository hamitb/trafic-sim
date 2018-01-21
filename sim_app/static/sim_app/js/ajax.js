// Settings AJAX
fadeSpeed = 400;

$('#settings-container, #sim-container').find('form').on('submit', function (e) {
    e.preventDefault();
    var form = this;
    var form_action = $(form).attr('action');
    var form_data = $(form).serialize();

    form_data += ("&" + document.activeElement.name + '=');

    startWait();
    $.ajax({
        type: "POST",
        url: form_action,
        data: form_data,
        success: function (data) {
            console.log(data.map_state);
            stopWait(data.notification, data.result);
        }
    });
});


function startWait() {
    info = $('#info');
    info.removeClass('alert-success alert-danger').addClass('alert-warning');
    info.text("Wait...").fadeTo(fadeSpeed, 1).delay(fadeSpeed);
}

function stopWait(notification, result) {
    info = $('#info');

    info.fadeTo(fadeSpeed, 0, function() {
        info.text(notification).removeClass('alert-warning').addClass('alert-'+result);
    }).fadeTo(fadeSpeed, 1).delay(fadeSpeed).fadeTo(fadeSpeed, 0);
}
