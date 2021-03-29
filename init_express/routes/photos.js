var express = require('express');
var router = express.Router();
var conn = require("../routes/sql/mysqldb"); // mysql config

// 圖片處理
var fs = require('fs')
var multer = require('multer')
let upload = multer({
  storage: multer.memoryStorage(), //若要存入資料庫則啟用
  limit: {
    // 限制上傳檔案的大小為 1MB
    fileSize: 1024 * 1024 * 5,
  },
  // fileFilter: fileFilter
  dest: 'uploads/images', //檔案儲存位置
});

// photos 頁面
router.get('/', function(req, res, next) {
    res.render('photos', { 
        title: 'Photos',
    });
});

// photos 將資料庫圖片傳到client端
router.post('/',function(req,res){
    var date = req.body.date
    console.log(date)
    conn.execute(
        'SELECT * FROM files WHERE createdDate = ?',[date],
        function(err, results, fields) {
            var img_binary64 = []
            for(let i=0;i<results.length;i++){
                var data = {
                    date:results[i]['createdDate'],
                    img_binary:Buffer.from(results[i]['file']).toString("base64"),
                }
                img_binary64.push(data)
            }

            // 可將資料庫圖片存成實體圖片
            // fs.writeFile("test01.png", results[0]['file'], 'binary', (error) => {
            //     if (error) {                    
            //                 console.log('下载失败');
            //     } else {                    
            //                 console.log('下载成功！')
            //     }
            // })
            res.send(img_binary64)
        }
    );
})


// 上傳按鈕觸發 （最多一次上傳10張圖片）
router.post('/upload',upload.array('img',10), async(req, res) =>{
    let FileData = req.files //要注意的是 上傳檔案，檔案不會在req.body(字串資料).
    // console.log(FileData[0].buffer)
    
    try {
        // 存入資料庫
        conn.execute('INSERT INTO files (file, createdDate) VALUES(?,?)',[FileData[0].buffer, "2021-03-08"]);
        
        // 可將上傳的圖片存成實體圖片
        fs.writeFile("insert01.png", FileData[0].buffer, 'binary', (error) => {
            if (error) {                    
                console.log('Download Error');
            } else {                    
                res.send("ok")
                console.log('Download Successfully')
            }
        })
    } catch (e) {
        console.log(e)
    }
})

module.exports = router;