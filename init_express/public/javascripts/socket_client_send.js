// /******************************************/
// function on_listener(sid,timer){
//     this.ws = new WebSocket("ws://localhost:3000");//和server要最新資料
//     this.timer = timer
//     this.sid = sid
//     // 接收訊息
//     this.ws.onmessage = function(message) {
//         let data = JSON.parse(message.data)
//         // 在這裡加入死資料
//         if(sid=='temp'){
//             $("#picture_time").text("Last: "+data.time_now);
//             $("#feeding").text(data.time_now);
//             $("#temperature").text(data.temp);
//         }
//         if(sid=='img'){
//             // $("#picture").attr('src',"data:image/jpeg;base64,"+data['img'])
//             $("#picture").attr('src','/img/new_img.jpg');
//             $("#picture_time").text("Last:  "+ data['time'])
//         }
//     };
//     // 開啟頁面自動執行
//     this.ws.onopen = function(){    //連接成功觸發
//         timer = setInterval(function(){
//             this.ws.send(sid)
//         },timer);
//     };
//     // 連線關閉時觸發
//     this.ws.onclose = function(){//關閉連接觸發
//         clearInterval(timer);
//         console.log("close: "+sid)
//     };
//     // 異常關閉時觸發
//     this.ws.onerror = function(){//連接失敗觸發
//         alert("error: "+sid);
//     };
// }
// // 啟動socket
// on_listener("temp",800) //auto
// // on_listener("img",1000) //auto



// /******************* Select_Button ***********************/
// //樹莓派端 socket server ip << 如果沒開啟client會出現error
// var ws_btn = new WebSocket("ws://localhost:8765/");

// // 接收訊息
// ws_btn.onmessage = function(mes){
//     console.log(mes)
// }
// // 開啟連線並送出資料
// ws_btn.onopen = function(){ 
//     $("#selectID").on('change',function(){
//         let abc = $("#selectID").find("option:selected").text()
//         ws_btn.send("送出資料: "+abc)
//     })
// }

// $("#selectID").on('change',function(){
//     ws_btn.send("test")
// })


// // /******************************************/
// // ws_btn.onclose = function(){//關閉連接觸發
// //     console.log("close: "+1)
// // };
// // /******************************************/
// // ws_btn.onerror = function(){//連接失敗觸發
// //     alert("error: "+1);
// // };



// var socket5 = io("ws://localhost:3000");
// socket5.on('liveTemp', function (url) {
//     //$('#sp1id').text("Out temperature:" + url);
//     console.log(url)
// });

