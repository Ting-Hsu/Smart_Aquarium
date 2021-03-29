$(function () {
    $("#email, #password").change(function () {
        if ($(this).val() != "") {
            $(this).next("div").addClass("labelm_c");
            $(this).next("div").removeClass("labelm");
        } else {
            $(this).next("div").addClass("labelm");
            $(this).next("div").removeClass("labelm_c");
        }
    })
    
    // 檢查帳號密碼使否正確
    $("#login").click(function () {
        $.ajax({
            url : "../login.html", //?
            type: "POST",
            data: {
                email: $("#email").val(),
                password: $("#password").val()
            },
            success: function(data){
                alert(data);
                if ($(this).val() != "") {
                    $("#email").addClass("is-invalid");
                    $("#password").addClass("is-invalid");
                    $(".instruction_p").addClass("invalid-feedback");
                    $(".instruction_p").text("The email or password is incorrect");
                } else {
                    $("#email").removeClass("is-invalid");
                    $("#password").removeClass("is-invalid");
                    $(".instruction_p").removeClass("invalid-feedback");
                    $(".instruction_p").text("");
                }
            },
            error: function(){
                alert('訪問失敗');
            }
        })
    })
});