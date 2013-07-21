$(document).ready(function() {
    document.session = $('#session').val();
    setTimeout(requestInventory, 100);

    $('#add-button').click(function(event) {
        jQuery.ajax({
            url: '/cart/',
            type: 'POST',
            data: {
                session: document.session,
                action: 'add'
            },
            //dataType: 'json',
            beforeSend: function(xhr, settings) {
                $(event.target).attr('disabled', 'disabled');
            },
            success: function(data, status, xhr) {
                $('#add-to-cart').hide();
                $('#remove-from-cart').show();
                $(event.target).removeAttr('disabled');
            }
        });
    });

    $('#remove-button').click(function(event) {
        jQuery.ajax({
            url: '/cart/',
            type: 'POST',
            data: {
                session: document.session,
                action: 'remove'
            },
            //dataType: 'json',
            beforeSend: function(xhr, settings) {
                $(event.target).attr('disabled', 'disabled');
            },
            success: function(data, status, xhr) {
                $('#remove-from-cart').hide();
                $('#add-to-cart').show();
                $(event.target).removeAttr('disabled');
            }
        });
    });
});

function requestInventory() {
    var endpoint = 'ws://localhost:8000/cart/status/'
    var websocket = new WebSocket(endpoint);

    websocket.onopen = function (evt) {};
    websocket.onmessage = function(evt) {
        $('#count').html($.parseJSON(evt.data)['inventory_count']);
    };
    websocket.onerror = function (evt) {};
}
