var express = require('express');
var router = express.Router();

// 使用者頁面 (未設置)
router.get('/', function(req, res, next) {
  res.send('respond with a resource');
});


router.post('/',function(req,res,next){
  res.send("I am is users.ejs")
})

module.exports = router;
