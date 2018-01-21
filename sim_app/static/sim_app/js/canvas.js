var map_container  = document.getElementById("map-container");
var canvas = document.getElementById('map-canvas');

canvas.width = map_container.offsetWidth;
canvas.height = map_container.offsetHeight;

context = canvas.getContext('2d');

// Functions.....................................................

function drawGrid(context, color, stepx, stepy) {
    context.strokeStyle = color;
    context.lineWidth = 0.5;

    for (var i = stepx + 0.5; i < context.canvas.width; i += stepx) {
        context.beginPath();
        context.moveTo(i, 0);
        context.lineTo(i, context.canvas.height);
        context.stroke();
    }

    for (var i = stepy + 0.5; i < context.canvas.height; i += stepy) {
        context.beginPath();
        context.moveTo(0, i);
        context.lineTo(context.canvas.width, i);
        context.stroke();
    }
}

// Initialization................................................

drawGrid(context, 'lightgray', 10, 10);