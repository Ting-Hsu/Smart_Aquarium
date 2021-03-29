// var moment = require('moment')
// var insqlarr = new Array(5);
// insqlarr[0] = 12333;
// insqlarr[1] = 1232;
// insqlarr[1] = 41232;
// insqlarr[3] = 123;
// insqlarr[4] = "123";

// // insqlarr.forEach(function (item, index, array) {
// //     console.log(item, index)
// //     if (item==null) return false;
// // });

// for (i = 0; i < 5; i++) {
//     if (insqlarr[i] == null) break;
//     console.log(insqlarr[i]+" index:"+i);
//     if (i == 4) console.log("done");
// }
// let time_now = moment().format("YYYY-MM-DD");
// console.log(time_now);


const fs = require('fs')

// const request = require('request')
// const x = request('http://192.168.43.118:8080/?action=snapshot')

// request(url).pipe(fs.createWriteStream(buffer));
// var x=fs.ReadStream( request.get('http://192.168.43.118:8080/?action=snapshot'));
// request('http://192.168.43.118:8080/?action=snapshot').pipe(fs.ReadStream(x));
// console.log(typeof(x));
// request('http://fromrussiawithlove.com/baby.mp3').pipe(fs.readStream('song.mp3'))
// const download = (url, path, callback) => {
//   request.head(url, (err, res, body) => {
//     request(url)
//       .pipe(fs.createWriteStream(path))
//       .on('close', callback)
//   })
// }

const url = 'http://192.168.43.118:8080/?action=snapshot';
const path = './images/image.png';
const { createCanvas, loadImage } = require('canvas')
const canvas = createCanvas(640, 480)
const ctx = canvas.getContext('2d')

// Draw cat with lime helmet
loadImage(url).then((image) => {
  ctx.drawImage(image, 0, 0);

  var url = canvas.toDataURL("image/png");

  var dataURL = url.replace(/^data:image\/(png|jpg);base64,/, "");
  // const out = fs.createWriteStream("./images/imagew.png");
  // const stream = canvas.createPNGStream()
  // stream.pipe(out)

  fs.writeFile('./images/imagew1.png', dataURL, { encoding: 'base64' }, function (err) {
    console.log('File created');
  });
})
// function getBase64Image(img) {
//     // Create an empty canvas element
//     var canvas = createCanvas(img.width,img.height);

//     // Copy the image contents to the canvas
//     var ctx = canvas.getContext("2d");
//     ctx.drawImage(img, 0, 0);

//     // Get the data-URL formatted image
//     // Firefox supports PNG and JPEG. You could check img.src to
//     // guess the original format, but be aware the using "image/jpg"
//     // will re-encode the image.
//     var dataURL = canvas.toDataURL("image/png");

//     return dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
// }