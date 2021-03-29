var express = require('express');
var router = express.Router();

// about 頁面
router.get('/', function(req, res, next) {
    res.render('about', { 
        title: 'About',
    });
});

module.exports = router;