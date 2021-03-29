var express = require('express');
var router = express.Router();
var conn = require("../routes/sql/mysqldb");
// signup 頁面
router.get('/', function (req, res) {
    // ...
    res.render('signup', {
        title: 'Signup',
    });
});

router.post('/', function (req, res) {
    var tankname = req.body.tankname;
    var userEmail = req.body.email;
    var password = req.body.password;
    console.log(tankname)
    console.log(userEmail)
    console.log(password)
    if (userEmail && password) { // 輸入資料
        conn.execute( //判斷是否有這組帳號
            'SELECT * FROM members WHERE email = ? AND username = ?',
            [userEmail, tankname], function (err, results, fields) {
                if (results == "") { //沒有這組帳號就可以新增。
                    // 新增帳號
                    conn.execute('INSERT INTO members (username, password, email) VALUES(?,?,?)', [tankname, password, userEmail]);
                    res.redirect('/login');
                } else { // 有這組帳號就返回signup 重新註冊一組
                    res.redirect('/signup');
                }
            })
    } else { // 如果輸入匡空白就再次導入signup
        res.redirect("/signup")
    }

})

module.exports = router;