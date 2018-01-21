socket = new WebSocket("ws://" + window.location.host + "/");

socket.onmessage = function(e) {
    data = JSON.parse(e.data);
    console.log(data);

    if (data.type === "data") {
        drawCars(data.cars);
    }
};