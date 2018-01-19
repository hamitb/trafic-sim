$('#settings-container').find('form').on('submit', function (e) {
    e.preventDefault();
    var form = this;
    var form_action = $(form).attr('action');
    var form_data = $(form).serialize();

    startWait();
    $.ajax({
        type: "POST",
        url: form_action,
        data: form_data,
        success: function (data) {
            stopWait(data.notification, data.result);
        }
    });
});

function startWait() {
    info = $('#info');
    info.removeClass('alert-success alert-danger').addClass('alert-warning');
    info.text("Wait...").fadeTo(600, 1).delay(600);
}

function stopWait(notification, result) {
    info = $('#info');

    info.fadeTo(600, 0, function() {
        info.text(notification).removeClass('alert-warning').addClass('alert-'+result);
    }).fadeTo(600, 1).delay(600).fadeTo(1200, 0);
}
