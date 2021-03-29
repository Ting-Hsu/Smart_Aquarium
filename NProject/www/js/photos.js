$(function () {
    $("#datepicker").datepicker({
        dateFormat: "yy-mm-dd",
        minDate: "-30D", 
        maxDate: "+0D",
        prevText: "pre",
        nextText: "next"
    });
    $("#datepicker").datepicker().datepicker("setDate", new Date());
    $("#preday").click(function(){
        var currentDate = $("#datepicker").datepicker("getDate")
        currentDate.setDate(currentDate.getDate() - 1);
        var a = $("#datepicker").datepicker( "setDate", currentDate );
    });
    $("#nextday").click(function(){
        var currentDate = $("#datepicker").datepicker("getDate")
        currentDate.setDate(currentDate.getDate() + 1);
        var a = $("#datepicker").datepicker( "setDate", currentDate );
    })

    //格數
    //setting決定DB保留數，從DB照片張數決定顯示幾張

});