console.log("socket_recv_client...on ! ")

var {socket_client}= require('./socket_config')
var conn = require('../sql/mysqldb') 
var moment = require('moment') // 時間處理模組

function socket_add_listener(client_ws) {

    // 接收訊息
    client_ws.on("message", function(message) {
        console.log("server_text收到訊息："+message); 
        var data = {}
        let time_now = moment().format("YYYY-MM-DD HH:mm:ss")
        let temp = Math.floor(Math.random() * Math.floor(30))
        client_ws.send(JSON.stringify({
            time_now:time_now,
            temp:temp,
        })); 
        // if(message =='temp'){
        //     console.log("是溫度")
        //     // SQL 以下傳出 (長時間讀取最新一筆 資料寫死就好，短時間讀取資料用ajax)
        //     conn.Temp.findOne({
        //         limit: 1,where: {},order:[[ 'createdAt','DESC']]
        //     }).then((temp)=>{
        //         data['temp_time'] = format_moment(temp.createdAt)
        //         data['temp'] = temp.temp
        //         console.log()
        //         client_ws.send(JSON.stringify(data)); 
        //     })
        // }
        // //圖片改用讀取base64存在圖檔去覆蓋，前端讀path
        // if(message == 'img'){
        //     console.log("是圖片")
        //     conn.File.findOne({
        //         limit: 1,where: {},order:[[ 'createdAt','DESC']]
        //     }).then((files)=>{
        //         let a = JSON.stringify(files)
        //         client_ws.send(files); 
        //     })
        // }

    });

    // socket連線被關閉時觸發
    client_ws.on('close',function(){
        console.log("close")
    })

    // socket異常時觸發
    client_ws.on("error", function(err) {
        console.log("client error", err);
    });

    // 開啟連線時觸發
    client_ws.send("start_cl") 
}


/******************************************/
const socket_client_recv = function(){
    this.connection = function(){
        socket_client.on("connection", function(client_ws){
            console.log("client comming");
            socket_add_listener(client_ws);
        })
    },
    this.error = function(){
        socket_client.on("error", function(err){
            console.log(err)
        });
    },
    this.header = function(){
        socket_client.on("headers", function(header){
            console.log(header);
        });
    }
}

/******************************************/

var con = new socket_client_recv().connection()
var err = new socket_client_recv().error()
var header = new socket_client_recv().header()

module.exports = {socket_client_recv}


