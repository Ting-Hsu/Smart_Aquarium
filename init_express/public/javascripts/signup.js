$(function () {
    $("#tankname, #email, #password").change(function () {
        if ($(this).val() != "") {
            $(this).next("div").addClass("labelm_c");
            $(this).next("div").removeClass("labelm");
        } else {
            $(this).next("div").addClass("labelm");
            $(this).next("div").removeClass("labelm_c");
        }
    });
    
    // check input
    $("#tankname").blur(function () {
        if ($(this).val() == "") {
            $(this).addClass("is-invalid");
            $(".instruction_t").addClass("invalid-feedback");
            $(".instruction_t").text("Must input!");
        } else{
            console.log($(this).val());
            let valid= /[0-9a-zA-Z_]/;
            let flag = false;
            for (let i = 0; i < $(this).val().length; i++) {
                let ch = $(this).val().charAt(i);
                if(valid.test(ch)){
                    console.log(ch);
                    continue;
                }else{
                    flag = true;
                }
                if (flag) 
                break;
            }
            if (flag) {
                $(this).addClass("is-invalid");
                    $(".instruction_t").addClass("invalid-feedback");
                    $(".instruction_t").text("Only can use letters, numbers & underscore");
            }else{
                $(this).removeClass("is-invalid");
                $(".instruction_t").removeClass("invalid-feedback");
                $(".instruction_t").text("You can use letters, numbers & underscore");
            } 
        }
    });
    $("#email").blur(function () {
        if ($(this).val() == "") {
            $(this).addClass("is-invalid");
            $(".instruction_e").addClass("invalid-feedback");
            $(".instruction_e").text("Must input!");
        } else {
            $(this).removeClass("is-invalid");
            $(".instruction_e").removeClass("invalid-feedback");
            $(".instruction_e").text("Use a valid email");
        }
    });
    $("#password").blur(function () {
        if ($(this).val() == "") {
            $(this).addClass("is-invalid");
            $(".instruction_p").addClass("invalid-feedback");
            $(".instruction_p").text("Must input!");
        } else if ($(this).val().length<8){
            $(this).addClass("is-invalid");
            $(".instruction_p").addClass("invalid-feedback");
            $(".instruction_p").text("Must have 8 characters!");
        }else {
            $(this).removeClass("is-invalid");
            $(".instruction_p").removeClass("invalid-feedback");
            $(".instruction_p").text("Use 8 or more characters with a mix of letters, numbers & symbols");
        }
    });









    
    //檢查格式

    //檢查email是否重複
});