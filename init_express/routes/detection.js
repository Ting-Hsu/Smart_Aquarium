var express = require('express');
var router = express.Router();
const axios = require('axios');
var multer = require('multer');
let upload = multer({
  storage: multer.memoryStorage(), //若要存入資料庫則啟用
  limit: {
    // 限制上傳檔案的大小為 1MB
    fileSize: 1024 * 1024 * 5,
  },
  // fileFilter: fileFilter
  dest: 'uploads/images', //檔案儲存位置
});
// settings 頁面
router.get('/', function(req, res, next) {
    res.render('detection', { 
        title: 'Detection',
    });
});

router.post('/',function(req,res){
    res.send("I am is settings.ejs")
})

// POST to Flask-RestFul API
router.post('/inference',upload.array('file',10),async  (req, res) =>{
    // let FileData = req.files //要注意的是 上傳檔案，檔案不會在req.body(字串資料).
    // console.log(FileData)
    // let data=[]
    // for(let i=0;i<FileData.length;i++){
    //   data.push(Buffer.from(FileData[i].buffer).toString('base64')) // base64_string
    // }
    // try {
    //   axios.post('http://localhost:5000/YOLOv5UploadToModelInference1',{ // flask不能return 要改socket
    //     data:data
    //   }).then(response => (
    //     // console.log(JSON.stringify(response.data)),
    //     res.send(response.data)
    //   ))
    // } catch (e) {
    //   console.log("error")
    // }
    res.send("inference_nodejs_route")
})

module.exports = router;