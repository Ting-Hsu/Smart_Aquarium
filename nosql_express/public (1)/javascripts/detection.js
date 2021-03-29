

function financial(x) {
    return Number.parseFloat(x).toFixed(1);
}
function financial_3(x) {
    return Number.parseFloat(x).toFixed(3);
}
function BoundingBox(x){
    data = []
    for(let i=0; i<x.length;i++){
        data.push(financial_3(x[i]*1000))
    }
    return data
}

$(document).ready(function () {

//yolov4
$('#blockimg').on('change',function(){
    var form_data = new FormData();  // 建立一個裝載檔案的箱子
    var file_data = $('#blockimg').prop('files'); //取得檔案資料
    for(let i=0; i<file_data.length;i++){    // 迴圈是要把多個檔案裝到箱子裡
        form_data.append('file', file_data[i]);
        // form_data.append('img', file_data[i]) //把多個檔案放到form_data箱子裡，blockimg對應後端upload.array('img',10)
    }
    // yolov4
    $.ajax({
        url: 'http://172.20.10.6:5000/YOLOv4UploadToModelInference',
        type: 'post',
        data: form_data,     // 要傳送的檔案   
        contentType: false,  //務必false (是網頁要送到Server的資料型態)
        processData: false, //必須false ，否則出現 jquery35.min.js:2 Uncaught TypeError: Illegal invocation
        // cache: false,
        // async:false,        // 待查
        // dataType: 'json', 
        enctype: 'multipart/form-data',
        success: function(data){
            document.getElementById('div_img').innerHTML="";
            var div = document.getElementById('div_img')
            for(let i=0;i<data.length;i++){ // 幾張圖
                data[i].index=i;
                div.innerHTML+=
                    '<div class="col-12 col-xl-6"><div class="wrapper"><img src=data:image/png;base64,'+data[i][1]['base64']+' style="width:100%; height:360px"></div></div>    \
                    <div class="col-12 col-xl-6"><div class="wrapper"><table id="example'+i+'" class="table table-striped" style="height:360px; table-layout:fixed"> \
                    <thead  class="">\
                            <tr>\
                                <th class="t_calss">Class</th>\
                                <th class="t_accuracy">Acc (%)</th>\
                                <th class="t_boundingbox">BoundingBox (x,y,w,h)</th>\
                            </tr>\
                    </thead>\
                    <tbody id="inference_data'+i+'"></tbody></table></div></div>'
                // 放入每張圖的 每個物件的 資訊（class_name, acc, bbox... ）
                var inference_data = document.getElementById("inference_data"+i+"")
                for(let a=0;a<data[0][0].length;a++){ //有幾個物件
                    console.log(data[i][a]) 
                    for(let g=0; g<data[i][a].length;g++){
                        var content = 
                        '<tr>\
                                <td>'+data[i][a][g]['label']+'</td>\
                                <td>'+financial(data[i][a][g]['confidences']*100)+'</td>\
                                <td>'+data[i][a][g]['bbox']+'</td>\
                        </tr>'
                        inference_data.innerHTML+=content
                    }
                }
            }
        }
    })
})

//yolov5
$('#btn_yolov5').on('change',function(){
    var form_data = new FormData();  // 建立一個裝載檔案的箱子
    var file_data = $('#btn_yolov5').prop('files'); //取得檔案資料
    for(let i=0; i<file_data.length;i++){    // 迴圈是要把多個檔案裝到箱子裡
        form_data.append('file', file_data[i]);
        // form_data.append('img', file_data[i]) //把多個檔案放到form_data箱子裡，blockimg對應後端upload.array('img',10)
    }
    $.ajax({
        url: 'http://127.0.0.1:5000/z',
        type: 'post',
        data: form_data,     // 要傳送的檔案   
        contentType: false,  //務必false (是網頁要送到Server的資料型態)
        processData: false, //必須false ，否則出現 jquery35.min.js:2 Uncaught TypeError: Illegal invocation
        // cache: false,
        // async:false,        // 待查
        // dataType: 'json', 
        enctype: 'multipart/form-data',
        success: function(data){
            console.log(data)
            document.getElementById('div_img').innerHTML="";
            var div = document.getElementById('div_img')
            for(let i=0;i<data.length;i++){ // 幾張圖
                data[i].index=i;
                div.innerHTML+=
                    '<div class="col-6 col_width"><img src=data:image/png;base64,'+data[i][1]['base64']+' style="width:100%; height:360px"></div>    \
                    <div class="col-6 col_width" style="width:100%"><table id="example'+i+'" class="table table-striped" style="height:360px; table-layout:fixed"> \
                    <thead  class="">\
                            <tr>\
                                <th>Class</th>\
                                <th>Accuracy %</th>\
                                <th style="width:40%">BoundingBox (x,y,w,h)</th>\
                            </tr>\
                    </thead>\
                    <tbody id="inference_data'+i+'"></tbody></table></div>'

                // 放入每張圖的 每個物件的 資訊（class_name, acc, bbox... ）
                var inference_data = document.getElementById("inference_data"+i+"")
                for(let a=0;a<data[i][0].length;a++){
                    var content = 
                    '<tr>\
                            <td>'+data[i][0][a]['class_name']+'</td>\
                            <td>'+financial(data[i][0][a]['confidence']*100)+'</td>\
                            <td>'+BoundingBox(data[i][0][a]['normalized_box'])+'</td>\
                    </tr>'
                    inference_data.innerHTML+=content
                }
            }
        }
    })
})

});