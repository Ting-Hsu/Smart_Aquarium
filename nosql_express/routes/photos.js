var express = require('express');
var router = express.Router();

// photos 頁面
router.get('/', function(req, res, next) {
    res.render('photos', { 
        title: 'Express',
    });
});

router.post('/',function(req,res,next){
    
    res.send("I am is photos.ejs")
})


module.exports = router;