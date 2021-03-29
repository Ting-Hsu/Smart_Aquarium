var express = require('express');
var router = express.Router();
var conn = require("../routes/sql/mysqldb");
// login 頁面
router.get('/', function (req, res, next) {
    // ...
    res.render('login', {
        title: "Login"
    });
});

router.post('/', function (req, res) {

    let userEmail = req.body.email;
    let password = req.body.password;
    //...這邊要寫一個資料庫查詢帳密再加上Hash密碼加密和解密，再進入以下帳號判斷
    if (userEmail == "" || password == "") {
        return res.redirect('/login');
    }
    conn.execute(
        'SELECT * FROM members WHERE email = ? AND password = ?',
        [userEmail, password],
        function (err, results, fields) {
            if (results == "") { // 如果sql找不到資料就傳回login頁面
                res.redirect('/login');
            } else if (results[0]['email'] == userEmail && results[0]['password'] == password) {
                res.locals.useremail = userEmail;
                req.session.tankname = results[0]['username']
                //設定session
                req.session.useremail = res.locals.useremail;

                //req.session.time++; // 相同帳號連線就+1
                res.redirect('/');    // 導入主頁面
            } else { // 如果帳密輸入錯誤就再次導入login頁面
                res.redirect('/login')
            }
        }
    );
})

router.post('/logout', function (req, res) {
    req.session.destroy()
    res.redirect('/login')
})

module.exports = router;