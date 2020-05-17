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
var width = canvas.width;
var height = canvas.height;

window.onload = function() {
    fix_dpi();
    fill();
}

document.addEventListener('DOMContentLoaded', function() {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    socket.on('connect', () => {
        load_graph();
        document.addEventListener('DOMContentLoaded', () => {
            document.getElementById('build_button').onsubmit = () => {
                socket.emit('rebuild_graph', {'text': document.getElementById
                ("text_input").text});
            }
        })
    });
    socket.on('rebuild_graph', data => {
        graph_from_data(data);
    });
});

function fill() {
    var width = canvas.width,
        height = canvas.height;
    ctx.fillStyle = 'rgb(245,245,236)';
    ctx.fillRect(0, 0, width, height);
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
    for (var i = 0;i < m;i++){
        links.push(Link(data['l${i}i1'], data['l${i}i2'],
        data['l${i}w']));
    }
    for (var i = 0;i < n;i++){
        nodes.push(new Node(data[`n${i}x`], data[`n${i}y`],i + 1));
    }
    draw();
}

function draw(){
    fill();
    ctx.fillStyle = 'rgb(20,200,20)';

    for (var i = 0;i < nodes.length;i++){
        ctx.beginPath();
        ctx.arc(nodes[i].x, nodes[i].y, 20, 0, Math.PI*2);
        ctx.fill();
    }
}

function fix_dpi() {
    let style_height = +getComputedStyle(canvas).getPropertyValue("height").slice(0, -2);
    let style_width = +getComputedStyle(canvas).getPropertyValue("width").slice(0, -2);
    canvas.setAttribute('height', style_height * dpi);
    canvas.setAttribute('width', style_width * dpi);
}
