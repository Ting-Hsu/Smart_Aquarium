var express = require('express');
var router = express.Router();
const WebSocket = require('ws')
var socket_pi = new WebSocket.Server({ port: 3010 });
var webs = new WebSocket.Server({ port: 3011 });

webs.on("connection", function (server_ws) {
  sockpi(server_ws);
});

function sockpi(server_webs) {
  socket_pi.on("connection", function (server_ws) {
    // server_ws.send(JSON.stringify(msg));
    server_ws.on("message", function (message) { // 接收資料
      // server_ws.send(message);
      try {
        var msg = JSON.parse(message);
        // console.log(msg);// 查看接收到的資料
        switch (msg.type) {
          case "livePiTime":
            server_webs.send(message);
            console.log(msg.text);
            // socket_pi.emit("livePiTime",msg.text)
            break;
          case "livePiTemp":
            server_webs.send(message);
            console.log(msg.text);
            break;
          case "liveTemp":
            server_webs.send(message);
            console.log(msg.text);
            break;
          case "liveCam":
            server_webs.send(message);
            console.log(msg.type);
            break;
          case "liveCamStream":
            server_webs.send(message);
            console.log(msg.type);
            break;
          default:
            console.log(msg.type);
            break;
        }
      } catch (error) {
        console.log(error);
      }
    })
  })
}
/* 主畫面. */
router.get('/', function (req, res, next) {
  // ...
  res.render('index', {
  });
});

module.exports = router;
