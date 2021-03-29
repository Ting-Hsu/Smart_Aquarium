var express = require('express');
var router = express.Router();

// login 頁面
router.get('/', function(req, res, next) {
     // ...
    res.render('login', { 
        
    });
});

router.post('/',function(req,res,next){
    let email = req.body.email
    let password = req.body.password
    let session = req.session;
    console.log(session)
    if(email=="aiot08@gmail.com" & password=="123456"){
        req.session.loginUser = email;
        res.redirect('/')
    }else{
        res.redirect('/login')
    }
})



module.exports = router;
