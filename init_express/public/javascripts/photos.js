
$(function () {
    $("#datepicker").datepicker({
        dateFormat: "yy-mm-dd",
        minDate: "-30D", 
        maxDate: "+0D",
        prevText: "pre",
        nextText: "next"
    });
    $("#datepicker").datepicker().datepicker("setDate", new Date());

    var img_col = document.getElementById("img_columns")

    $("#datepicker").on('change',function(){
        var date = this.value
        $.ajax({
            url:'/photos',
            type:'post',
            data: {"date":date},
            success: function(data){
                console.log(data)
                if(data.length==0){
                    img_col.innerHTML=""
                    alert("沒有資料")
                }else{
                    img_col.innerHTML=""
                    // $('#picture1').attr("src","data:image/jpeg;base64,"+data+"")
                    // $('#picture1').css("width","150px")
                    for(let i=0;i<data.length;i++){
                        img_col.innerHTML+='<div class="col-12 col-md-3 picture">\
                        <div class="" style="text-align:center">'+moment(data[i]['date']).format("HH:mm:ss")+'</div>\
                        <div class="wrapper_i">\
                            <img src="data:image/jpeg;base64,'+data[i]['img_binary']+'" id="picture1" style="width:150px;">\
                        </div>\
                        </div>'
                    }
                }
            }
        })
    })

    $("#preday").click(function(){
        var currentDate = $("#datepicker").datepicker("getDate")
        currentDate.setDate(currentDate.getDate() - 1);
        var a = $("#datepicker").datepicker( "setDate", currentDate );
        var date = moment(currentDate).format("YYYY-MM-DD")
        $.ajax({
            url:'/photos',
            type:'post',
            data: {"date":date},
            success: function(data){
                if(data.length==0){
                    img_col.innerHTML=""
                    alert("沒有資料")
                }else{
                    // $('#picture1').attr("src","data:image/jpeg;base64,"+data+"")
                    // $('#picture1').css("width","150px")
                    console.log(data.length)
                    for(let i=0;i<data.length;i++){
                        img_col.innerHTML+='<div class="col-12 col-md-3 picture">\
                        <div class="" style="text-align:center">'+moment(data[i]['date']).format("HH:mm:ss")+'</div>\
                        <div class="wrapper_i">\
                            <img src="data:image/jpeg;base64,'+data[i]['img_binary']+'" id="picture1" style="width:150px;">\
                        </div>\
                        </div>'
                    }
                }
            }

        })
    });

    $("#nextday").click(function(){
        var currentDate = $("#datepicker").datepicker("getDate")
        currentDate.setDate(currentDate.getDate() + 1);
        var a = $("#datepicker").datepicker( "setDate", currentDate );
        var date = moment(currentDate).format("YYYY-MM-DD")
        $.ajax({
            url:'/photos',
            type:'post',
            data: {"date":date},
            success: function(data){
                img_col.innerHTML=""
                if(data.length==0){
                    img_col.innerHTML=""
                    alert("沒有資料")
                }else{
                    img_col.innerHTML=""
                    console.log(data)
                    for(let i=0;i<data.length;i++){
                        img_col.innerHTML+='<div class="col-12 col-md-3 picture" style="">\
                        <div class="" style="text-align:center">'+moment(data[i]['date']).format("HH:mm:ss")+'</div>\
                        <div class="wrapper_i">\
                            <img src="data:image/jpeg;base64,'+data[i]['img_binary']+'" id="picture1" style="width:150px;">\
                        </div>\
                        </div>'
                    }
                }
            }

        })
    })

    //格數
    //setting決定DB保留數，從DB照片張數決定顯示幾張

    $('#img_send_server').on('click',function(){
        var form_data = new FormData();  // 建立一個裝載檔案的箱子
        var file_data = $('#file').prop('files'); //取得檔案資料
        for(let i=0; i<file_data.length;i++){    // 迴圈是要把多個檔案裝到箱子裡
            form_data.append('img', file_data[i]) //把多個檔案放到form_data箱子裡，blockimg對應後端upload.array('img',10)
        }
        $.ajax({
            url: '/photos/upload',
            type: 'post',
            data: form_data,     // 要傳送的檔案   
            contentType: false,  //務必false (是網頁要送到Server的資料型態)
            processData: false, //必須false ，否則出現 jquery35.min.js:2 Uncaught TypeError: Illegal invocation
            // cache: false,
            // async:false,        
            // dataType: 'json', 
            enctype: 'multipart/form-data',
            success: function(data){
                console.log(data)
            }
        })
    
    })
});