var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var session = require('express-session');
var FileStore = require('session-file-store')(session);
var logger = require('morgan');
var axios = require("axios")

var signupRouter = require('./routes/signup');
var loginRouter = require('./routes/login');
var indexRouter = require('./routes/index');
var dashboardRouter = require('./routes/dashboard');
var photosRouter = require('./routes/photos');
var detectionRouter = require('./routes/detection');
var aboutRouter = require('./routes/about');
var usersRouter = require('./routes/users');

var app = express();

app.set('trust proxy', 1)
app.use(session({
  name: 'skey',
  secret: 'chyingp', // 用來對session id相關的cookie進行簽名
  // store: new FileStore(), // 本地儲存session（文字檔案，也可以選擇其他store，比如redis的）
  saveUninitialized: true, // 是否自動儲存未初始化的會話，建議false
  resave: false, // 是否每次都重新儲存會話，建議false
  cookie: {
    maxAge: 3600 * 1000 // 有效期，單位是毫秒（10秒）
  }
}))

// SQL setup
var mongodb = require('./routes/sql/mongodb')
var conn = require('./routes/sql/mysqldb')
var sequlize_mysql = require('./routes/sql/sequlize_mysql')

// socket setup
var socket_recv_pi = require('./routes/socket/socket_recv_pi');
var socket_recv_client = require('./routes/socket/socket_recv_client');

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/signup', signupRouter);
app.use('/login', loginRouter);

// 登入驗證
app.use(function (req, res, next) {
  console.log("------驗證階段------")
  // console.log(res.locals.test)
  // console.log(req.session.useremail) // aiot08@gmail.com
  res.locals.useremail = req.session.useremail;
  res.locals.tankname = req.session.tankname;
  if (res.locals.useremail) {
    console.log(res.locals.tankname)
    next(); // 驗證成功，進入 app.use('/', indexRouter);
  } else {
    res.redirect('/login') // 驗證失敗，回到 login
  }
});

app.use('/', indexRouter);
app.use('/dashboard', dashboardRouter);
app.use('/photos', photosRouter);
app.use('/detection', detectionRouter);
app.use('/about', aboutRouter);
app.use('/users', usersRouter);

// catch 404 and forward to error handler
app.use(function (req, res, next) {
  next(createError(404));
});

// error handler
app.use(function (err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});


//----------------------------------------------------------
// 下載url圖檔
// const url = 'http://192.168.43.181:8080/?action=snapshot'
// var req_img = require('request').defaults({ encoding: null });
// req_img.get(url, function (err, res, body) {
//       mysqldb.execute('INSERT INTO files (file, createdDate) VALUES(?,?)',[body, "2021-03-08"]);
//       console.log(body)
// });
// read serialport
// 1To5iblL4d5NBVWWzinA7QQwbbR1yE8yPN8HuCeugSg
//-F 'imageFile=@01.jpg'
/*
curl -X POST -H 'Authorization: Bearer 1To5iblL4d5NBVWWzinA7QQwbbR1yE8yPN8HuCeugSg' -F 'message=foobar' -F 'imageFile=/Users/yuhsien/Pictures/images.png' \
https://notify-api.line.me/api/notify
//line傳圖片
curl -X POST https://notify-api.line.me/api/notify \
     -H 'Authorization: Bearer 1To5iblL4d5NBVWWzinA7QQwbbR1yE8yPN8HuCeugSg' \
     -F 'message=test' -F 'imageFile=@/Users/yuhsien/Pictures/images.png'
//
curl -X POST https://notify-api.line.me/api/notify \
     -H 'Authorization: Bearer 1To5iblL4d5NBVWWzinA7QQwbbR1yE8yPN8HuCeugSg' \
     -F 'message=test' -F 'imageFile=@/Users/yuhsien/Pictures/images.png'
//https://notify-bot.line.me/doc/en/
*/
// const moment = require('moment')
// let date = moment().format("YYYY-MM-DD HH:mm:ss")
// axios.post("https://notify-api.line.me/api/notify", "message="+date+"", {
//   headers: {
//     "Content-Type": "application/x-www-form-urlencoded",
//     Authorization: "Bearer 1To5iblL4d5NBVWWzinA7QQwbbR1yE8yPN8HuCeugSg"
//   },
// })
// .then(response => {
//   // console.log(response);
// });
// const moment = require('moment')
// let date = moment().format("YYYY-MM-DD HH:mm:ss")
// axios.post("https://notify-api.line.me/api/notify", 'imageFile=@/Users/yuhsien/Pictures/yolov5_improve.jpg', {
//   headers: {
//     "Content-Type": "application/x-www-form-urlencoded",
//     Authorization: "Bearer 1To5iblL4d5NBVWWzinA7QQwbbR1yE8yPN8HuCeugSg",
//     // 'Access-Control-Allow-Origin': '*'
//   },
// })
// .then(response => {
//   // console.log(response);
// });

module.exports = app;
