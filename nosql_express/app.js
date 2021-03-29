var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var session = require('express-session');
var FileStore = require('session-file-store')(session);
var logger = require('morgan');
var signupRouter = require('./routes/signup');
var loginRouter = require('./routes/login');
var indexRouter = require('./routes/index');
var dashboardRouter = require('./routes/dashboard');
var photosRouter = require('./routes/photos');
var settingsRouter = require('./routes/settings');
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
var mysqldb = require('./routes/sql/mysqldb')
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
app.use('/', indexRouter);
app.use('/dashboard', dashboardRouter);
app.use('/photos', photosRouter);
app.use('/settings', settingsRouter);
app.use('/about', aboutRouter);
app.use('/users', usersRouter);


// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
