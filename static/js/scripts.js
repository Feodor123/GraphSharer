class Node{
constructor(x,y,num){
this.x = x;
this.y = y;
this.num = num;
}
}

class Link{
constructor(i1,i2,w){
this.i1 = i1;
this.i2 = i2;
this.w = w;
}
}

var links = [];
var nodes = [];
var dpi = window.devicePixelRatio;
var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");
var focus_ind = -1
var radius = 20
var was_dragging = false
var socket

function min_half(){
    return Math.min(canvas.width/2, canvas.height/2);
}

function center_x(){
    return canvas.width/2;
}

function center_y(){
    return canvas.height/2;
}

function screen_x(x){
    return center_x() + x * min_half()
}

function screen_y(y){
    return center_y() + y * min_half()
}

function real_x(x){
    return (x - center_x()) / min_half()
}

function real_y(y){
    return (y - center_y()) / min_half()
}

window.onload = function() {
    fix_dpi();
    fill();
    window.addEventListener('resize', on_reshape, false);
}

window.addEventListener("resize", resize);

function resize(){
    fix_dpi();
    draw();
}

document.addEventListener('DOMContentLoaded', function() {
    socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    socket.on('connect', () => {
        load_graph();
        document.getElementById('build_button').onclick = () => {
            socket.emit('rebuild_graph', {'text': document.getElementById
            ("text_input").value});
        }

        canvas.onmousedown = () => {
            i = closest_node(event.offsetX, event.offsetY, radius);
            if (i != -1){
                focus_ind = i;
                draw();
            }
        }

        canvas.onmousemove = () => {
            if (event.buttons & 1){
                if (focus_ind != -1){
                    move_node(focus_ind, event.movementX, event.movementY);
                    draw();
                }
                was_dragging = true
            }
        }

        canvas.onmouseout = () => {
            draw();
        }

        canvas.onmouseup = () => {
            if (was_dragging){
                if (focus_ind != -1){
                    focus_ind = -1;
                    draw();
                }
            }
            else{
                i = closest_node(event.offsetX, event.offsetY, radius);
                if (i != -1){
                    focus_ind = i;
                    draw();
                }
                else if (focus_ind != -1){
                    teleport_node(focus_ind, event.offsetX, event.offsetY);
                    focus_ind = -1;
                    draw();
                }
            }
            was_dragging = false
        }
    });
    socket.on('rebuild_graph', data => {
        graph_from_data(data);
    });
    socket.on('error', data => {
        alert(data.error)
    });
});

function fill() {
    ctx.fillStyle = 'rgb(245,245,236)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

function load_graph() {
    const request = new XMLHttpRequest();
    request.open('GET', '/load_graph');
    request.onload = () => {
        const data = JSON.parse(request.responseText);
        if (data.success) {
            graph_from_data(data);
        } else {
            alert(data.error);
        }
    }
    request.send();
    return false;
}

function graph_from_data(data) {
    var n = data.n;
    var m = data.m;
    links = [];
    nodes = [];
    for (var i = 0;i < m;i++){
        links.push(new Link(data[`l${i}i1`], data[`l${i}i2`],
        data[`l${i}w`]));
    }
    for (var i = 0;i < n;i++){
        nodes.push(new Node(data[`n${i}x`], data[`n${i}y`],i + 1));
    }
    draw();
}

function draw(){
    fill();
    ctx.strokeStyle = 'rgb(0,20,0)';
    ctx.lineWidth = 1;

    for (var i = 0;i < links.length;i++){
        ctx.beginPath();
        ctx.moveTo(screen_x(nodes[links[i].i1].x),
                   screen_y(nodes[links[i].i1].y));
        ctx.lineTo(screen_x(nodes[links[i].i2].x),
                   screen_y(nodes[links[i].i2].y));
        ctx.closePath();
        ctx.stroke();
    }

    ctx.fillStyle = 'rgb(20,200,20)';
    ctx.strokeStyle = 'rgb(20,200,20)'
    ctx.lineWidth = 4;

    for (var i = 0;i < nodes.length;i++){
        if (i == focus_ind){
            ctx.strokeStyle = 'rgb(0,20,0)'
            ctx.beginPath();
            ctx.arc(screen_x(nodes[i].x),
                    screen_y(nodes[i].y), radius, 0, Math.PI*2);
            ctx.stroke();
            ctx.fill();
            ctx.strokeStyle = 'rgb(20,200,20)'
        }
        ctx.beginPath();
        ctx.arc(screen_x(nodes[i].x),
                screen_y(nodes[i].y), radius, 0, Math.PI*2);
        ctx.fill();
    }
}

function on_reshape(){
    draw();
}

function fix_dpi() {
    let style_height = +getComputedStyle(canvas).getPropertyValue("height").slice(0, -2);
    let style_width = +getComputedStyle(canvas).getPropertyValue("width").slice(0, -2);
    canvas.setAttribute('height', style_height * dpi);
    canvas.setAttribute('width', style_width * dpi);
}

function closest_node(x, y, max){
    min_i = -1;
    min_val = max*max;
    for (var i = 0;i < nodes.length;i++){
        var dist = Math.pow(x - screen_x(nodes[i].x), 2) + Math.pow(y - screen_y(nodes[i].y), 2);
        if (dist < min_val){
            min_i = i;
            min_val = dist;
        }
    }
    return min_i;
}

function teleport_node(i, x, y){
    nodes[i].x = real_x(x);
    nodes[i].y = real_y(y);
    socket.emit('move_node', {'i': i, 'x': nodes[i].x, 'y': nodes[i].y});
}

function move_node(i, x, y){
    teleport_node(i, screen_x(nodes[i].x) + x, screen_y(nodes[i].y) + y);
}
