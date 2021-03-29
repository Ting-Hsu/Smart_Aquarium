$(function () {
    $(".tips").tooltip();
    // $('.tooltip-show').tooltip('show');

    function ShowTime() {
        setInterval(function () {
            var NowDate = new Date();
            var h = (NowDate.getHours() < 10 ? "0" + NowDate.getHours() : NowDate.getHours());
            var m = (NowDate.getMinutes() < 10 ? "0" + NowDate.getMinutes() : NowDate.getMinutes());
            var s = (NowDate.getSeconds() < 10 ? "0" + NowDate.getSeconds() : NowDate.getSeconds());
            $("#live_time").text(h + ':' + m + ':' + s);
        }, 100);
    }

    $("#liveb").click(function () {
        ShowTime();
    });
});