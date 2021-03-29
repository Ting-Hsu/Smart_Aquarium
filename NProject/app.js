var express = require('express');
var io = require('socket.io')(app);
var app = express();
let { PythonShell } = require('python-shell');
var fs = require("fs");
app.use(express.static("www"));
var server = app.listen(5438, function () {
    console.log('伺服器在5438埠口開工了。');
});
var sio = io.listen(server);
var wsflag = false;
const WebSocket = require('ws');
var ws;
serverconn();
function serverconn() {
    try {
        //接到網頁server
        ws = new WebSocket('ws://192.168.43.164:3010');
        ws.onmessage = function (e) {
            console.log(e.data);
        }
        wsflag = true;
    } catch (error) {
        console.log("ws error" + error)
    }
}
sio.on('connection', function (socket) {
    socket.on('disconnect', function () {
        socket.emit('stop');
    });
    socket.on('startsenser', function () {
        if (wsflag == false) serverconn(socket);
        else {
            takePhoto(socket);
            takeTime(socket);
            takeTemper(socket);
            takePiTemper(socket);
        }
    });
    socket.on('stopsenser', function () {
        wsflag = false;
    })
});
function takePhoto(socket) {
    // use python to catch pitcher
    // PythonShell.run('./python/Camera.py', 'messages', function (err, data) {
    //     if (err) console.log(err)
    //     // console.log(data[0] + data[1])
    //     console.log(data)
    //     randnu = 'image.jpg?r=' + Math.floor(Math.random() * 100000);
    //     socket.emit('liveCam', randnu);
    //     fs.readFile('./www/images/image.jpg', function (err, data) {
    //         if (err) throw err;
    //         outputstream = Buffer.from(data).toString('base64');
    //         // console.log(outputstream);
    //         serverSocket("liveCam", outputstream);
    //     });
    // })
    var snapshot = "http://192.168.43.118:8080/?action=snapshot";
    var stream = "http://192.168.43.118:8080/?action=stream";
    socket.emit('liveCam', snapshot);
    // socket.emit('liveCamStream', stream);
    serverSocket("liveCam", snapshot);
    serverSocket("liveCamStream", stream);
}
function takeTemper(socket) {
    PythonShell.run('./python/Temper.py', 'messages', function (err, data) {
        if (err) console.log(err)
        // console.log(data[0] + data[1])
        socket.emit('liveTemp', data);
        serverSocket("liveTemp", data);

    })
}
function takePiTemper(socket) {
    PythonShell.run('./python/PiTemper.py', 'messages', function (err, data) {
        if (err) console.log(err)
        socket.emit('livePiTemp', data);
        serverSocket("livePiTemp", data);
    })
}
function takeTime(socket) {
    PythonShell.run('./python/Time.py', 'messages', function (err, data) {
        if (err) console.log(err)
        socket.emit('livePiTime', data);
        serverSocket("livePiTime", data);
    })
}
function serverSocket(type, data) {
    try {
        var msg = {
            type: type.toString(),
            text: data.toString()
        }
        ws.send(JSON.stringify(msg));
        console.log("ws send:" + msg.type + " " + msg.text);
    } catch (error) {
        console.log(error);
    }
}