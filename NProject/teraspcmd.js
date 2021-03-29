var exec = require('child_process').exec;
//./mjpg-streamer-experimental/mjpg_streamer -o "
//./mjpg-streamer-experimental/output_http.so -w 
//./mjpg-streamer-experimental/www" -i "
//./mjpg-streamer-experimental/input_raspicam.so"
var cmd = './mjpg-streamer-experimental/mjpg_streamer -o "./mjpg-streamer-experimental/output_http.so -w ./mjpg-streamer-experimental/www" -i "./mjpg-streamer-experimental/input_raspicam.so"';
exec(cmd, function (error, stdout, stderr) {
    if (error != null) {
        console.log("error" + error);
        throw error;
    } else {
        console.log(stdout);
        console.log('http://192.168.43.118:8080/?');
    }
});