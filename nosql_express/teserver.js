const WebSocket = require('ws');

const wss = new WebSocket.Server({ port: 3010 });

wss.on('connection', function connection(ws) {
    console.log("server on");
  ws.on('message', function incoming(message) {
    console.log('received: %s', message);
  });

  ws.send('something');
  ws.send('send');
});