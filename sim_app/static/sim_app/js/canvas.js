var map_container  = document.getElementById("map-container");
var grid_canvas = document.getElementById('map-canvas-grid');
var map_canvas = document.getElementById('map-canvas');
var car_canvas = document.getElementById('car-canvas');

grid_canvas.width = map_container.offsetWidth;
grid_canvas.height = map_container.offsetHeight;

map_canvas.width = map_container.offsetWidth;
map_canvas.height = map_container.offsetHeight;

car_canvas.width = map_container.offsetWidth;
car_canvas.height = map_container.offsetHeight;


grid_context = grid_canvas.getContext('2d');
map_context = map_canvas.getContext('2d');
car_context = car_canvas.getContext('2d');


// Drawing attributes
var nodeColor = 'black';
var edgeColor = 'green';
var carColor = 'red';
var nodeRadius = 8;
var carRadius = 5;

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

function drawMap(map_state) {
    var context = map_context;

    context.clearRect(0, 0, map_canvas.width, map_canvas.height);
    drawNodes(map_state.nodes, context);
    drawEdges(map_state.edges, context);
}

function drawNodes(nodes, context) {
    var current_node;
    context.strokeStyle = nodeColor;

    for (var i = 0; i < nodes.length; i++) {
        current_node = nodes[i];

        context.beginPath();
        context.arc(current_node.x, current_node.y, nodeRadius, 0, 2*Math.PI);
        context.stroke();
    }
}

function drawEdges(edges, context) {
    var current_edge;
    context.strokeStyle = edgeColor;

    for (var i = 0; i < edges.length; i++) {
        current_edge = edges[i];
        source_node = current_edge.source;
        target_node = current_edge.target;

        context.beginPath();
        context.moveTo(source_node.x, source_node.y);
        context.lineTo(target_node.x, target_node.y);
        context.stroke();
    }
}

function drawCars(cars) {
    var current_car;
    var context = car_context;
    context.fillStyle = carColor;

    context.clearRect(0, 0, car_canvas.width, car_canvas.height);

    for (var i = 0; i < cars.length; i++) {
        current_car = cars[i];

        context.beginPath();
        context.arc(current_car.x, current_car.y, carRadius, 0, 2*Math.PI);
        context.fill();
    }
}

function clearCars() {
    var context = car_context;

    context.clearRect(0, 0, car_canvas.width, car_canvas.height);
}

// Initialization................................................

drawGrid(grid_context, 'lightgray', 10, 10);