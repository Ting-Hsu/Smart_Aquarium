var express = require('express');
var router = express.Router();

// dashboard 頁面
router.get('/', function(req, res, next) {
    res.render('dashboard', { 
        title: 'Dashboard',
    });
});


router.post('/',function(req,res,next){
    
    res.send("I am is dashboard.ejs")
})


module.exports = router;