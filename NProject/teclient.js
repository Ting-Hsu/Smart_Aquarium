const WebSocket = require('ws');
const ws = new WebSocket('ws://192.168.43.164:3010');

ws.on('open', function open() {
  ws.send('something123');
});

ws.on('message', function incoming(data) {
  console.log(data);
});