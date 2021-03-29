var express = require('express');
var router = express.Router();
var moment = require('moment')

var sqlconn = require('../routes/sql/mysqldb');
var sqlinsert = "insert into pitank (tankid ,date,time,temper,pitemper,image) values(?,?,?,?,?,?);";
// insert into pitank (tankid ,date,time,temper,pitemper) values('no1','2021-03-01','13-24-56',30,40);

const { createCanvas, loadImage } = require('canvas')
const canvas = createCanvas(640, 480)
const ctx = canvas.getContext('2d')

var insqlarr = new Array(6);
insqlarr[0] = 1;
function insql(type, data) {
  switch (type) {
    case "livePiTime":
      let time_now = moment().format("YYYY-MM-DD");
      insqlarr[1] = time_now;
      insqlarr[2] = data;
      console.log(type+"  "+data);
      break;
    case "livePiTemp":
      insqlarr[4] = data;
      console.log(type+"  "+data);
      break;
    case "liveTemp":
      insqlarr[3] = data;
      console.log(type+"  "+data);
      break;
    case "liveCam":
      console.log(type+"  "+data);
      try {
        loadImage(data).then((image) => {
          ctx.drawImage(image, 0, 0);
          var urlx = canvas.toDataURL("image/png");
          var dataURL = urlx.replace(/^data:image\/(png|jpg);base64,/, "");
          insqlarr[5] = dataURL;
        })
      } catch (error) {
        console.log(error);
      }
      break;
    default:
      break;
  }
  for (i = 0; i < 6; i++) {
    if (insqlarr[i] == null) break;
    console.log("index" + i);
    if (i == 5) {
      try {
          sqlconn.execute(sqlinsert,insqlarr);
        } catch (error) {
          console.log(error);
        }
      console.log("done");
      insqlarr = new Array(6);
      insqlarr[0] = 1;
    }
  }
}
// try {
//   sqlconn.execute(sqlinsert,["no3" ,"2021-03-12","15-19-59","23.5","image"]);
// } catch (error) {
//   console.log(error);
// }


const WebSocket = require('ws')
var socket_pi = new WebSocket.Server({ port: 3010 });
var webs = new WebSocket.Server({ port: 3011 });
var sqlflag = false;
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
            // console.log(msg.text);
            insql(msg.type, msg.text);
            // socket_pi.emit("livePiTime",msg.text)
            break;
          case "livePiTemp":
            server_webs.send(message);
            // console.log(msg.text);
            insql(msg.type, msg.text);
            break;
          case "liveTemp":
            server_webs.send(message);
            // console.log(msg.text);
            insql(msg.type, msg.text);
            break;
          case "liveCam":
            server_webs.send(message);
            // console.log(msg.type);
            insql(msg.type, msg.text);
            break;
          case "liveCamStream":
            server_webs.send(message);
            // console.log(msg.type);
            break;
          default:
            // console.log(msg.type);
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
