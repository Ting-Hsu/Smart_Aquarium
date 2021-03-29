var express = require('express');
var router = express.Router();

// settings 頁面
router.get('/', function(req, res, next) {
    res.render('settings', { 
        title: 'Express',
    });
});


router.post('/',function(req,res,next){
    
    res.send("I am is settings.ejs")
})

module.exports = router;