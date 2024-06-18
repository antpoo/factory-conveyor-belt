// making the socket 
var socket = io();

// connecting
socket.on("connect", function() {
    console.log("connected");
});

// when conveyor status is received
socket.on("conveyor", function(msg) {
    var s = msg.status;

    console.log(s);

    document.getElementById("conveyor").innerHTML = s;
});
// when measuring status is received
socket.on("measuring", function(msg) {
    var s = msg.status;

    console.log(s);

    document.getElementById("measuring").innerHTML = s;
});
// when conveyor status is received
socket.on("mixing", function(msg) {
    var s = msg.status;

    console.log(s);

    document.getElementById("mixing").innerHTML = s;
});
// when conveyor status is received
socket.on("baking", function(msg) {
    var s = msg.status;

    console.log(s);

    document.getElementById("baking").innerHTML = s;
});
// when conveyor status is received
socket.on("topping", function(msg) {
    var s = msg.status;

    console.log(s);

    document.getElementById("topping").innerHTML = s;
});
// when conveyor status is received
socket.on("packaging", function(msg) {
    var s = msg.status;

    console.log(s);

    document.getElementById("packaging").innerHTML = s;
});
// when conveyor status is received
socket.on("cleaning", function(msg) {
    var s = msg.status;

    console.log(s);

    document.getElementById("cleaning").innerHTML = s;
});