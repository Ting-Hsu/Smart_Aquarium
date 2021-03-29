var express = require('express');
var router = express.Router();

// signup 頁面
router.get('/', function(req, res, next) {
    // ...
    res.render('signup', { 
        title: 'Express',
    });
});

router.post('/',function(req,res,next){

    res.send("I am is signup.ejs")
})

module.exports = router;