let {PythonShell} = require('python-shell');

function takePhoto(socket) {
  PythonShell.run('./Camera.py', 'messages', function (err, data) {
      if (err) console.log(err)
      // console.log(data[0] + data[1])
      console.log(data)
      socket.emit('liveCam', 'image.jpg?r=' + Math.floor(Math.random() * 100000));
  })
}
function takeTemper(socket) {
  PythonShell.run('./Temper.py', 'messages', function (err, data) {
      if (err) console.log(err)
      // console.log(data[0] + data[1])
      console.log(data);
      socket.emit('liveTemp', data);
      // socket1.emit('liveTemp', data);

  })
}
function takePiTemper(socket) {
  PythonShell.run('./PiTemper.py', 'messages', function (err, data) {
      if (err) console.log(err)
      // console.log(data[0] + data[1])
      console.log("Pi "+data);
      socket.emit('livePiTemp', data);
      // socket1.emit('liveTemp', data);

  })
}
function takeTime(socket) {
  PythonShell.run('./Time.py', 'messages', function (err, data) {
      if (err) console.log(err)
      // console.log(data[0] + data[1])
      console.log(data);
      socket.emit('liveTime', data);
  })

}
