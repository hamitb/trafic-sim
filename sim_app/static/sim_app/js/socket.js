socket = new WebSocket("ws://" + window.location.host + "/");

socket.onmessage = function(e) {
    console.log("Socket message from server: " + e.data);
};